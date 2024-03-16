import logging
import math
import os
from typing import Optional

import ffmpeg

from .analyse import analyse_file
from .eprofile import Profile
from .rendition import OutputRendition

logger = logging.getLogger(__name__)


class FfmpegEncoder:
    def __init__(
        self,
        profile: Profile,
        output_folder: str,
        skip_transformations: bool = False,
        debug: bool = False,
    ) -> None:
        self.profile = profile
        self.output_folder: str = output_folder
        self.skip_transformations = skip_transformations
        self.debug = debug

    def _validate_input(self, input: dict) -> None:
        pass

    def encode(self, input: dict, duration_overwrite: Optional[int] = None) -> list:
        if duration_overwrite:
            # We need to ensure that the info in the profile is not used
            self.profile.overwrite_duration(duration_overwrite)

        renditions = []

        video_input = input["video"]
        video_spec = analyse_file(video_input)

        # Determine input type
        if video_spec["format"]["format_name"] in ["image2", "png_pipe"]:
            input_type = "image"
            # For images-to-video, the duration is defined
            # by the filters.trim.duration in the profile.yaml file
            duration = duration_overwrite
        elif (
            len(video_spec["streams"]) == 1
            and video_spec["streams"][0]["codec_type"] == "audio"
        ):
            input_type = "audio"
            duration = float(video_spec["format"]["duration"])
        else:
            input_type = "video"
            duration = float(video_spec["format"]["duration"])

        # Video
        for spec in self.profile.video_renditions():
            video_input = input["video"]
            spec_name = "{}_{}p_{}k".format(
                spec["codec"],
                spec["height"],
                int(spec["bitrate"]) // 1000,
            )
            rung_name = "{}_{}".format(input["asset_id"], spec_name)

            logger.info("Transcoding video: %s", rung_name)
            output_filename = f"{rung_name}.mp4"
            output_path = os.path.join(self.output_folder, output_filename)

            rendition = OutputRendition(rung_name, "video", spec_name)
            rendition.mp4 = output_path
            renditions.append(rendition)

            input_stream = self._make_input_stream(
                input_type,
                input=video_input,
                duration=duration,
                fps=spec["fps"],
                metadata=input["metadata"],
                with_filters=not self.skip_transformations,
            )

            # Final scale
            input_stream = ffmpeg.filter(
                input_stream, "scale", spec["width"], spec["height"]
            )

            gop_size = int(float(spec["gop"]) * float(spec["fps"]))
            x264opts = [f"keyint={gop_size}", f"keyint_min={gop_size}", "no-scenecut"]

            output_params = {
                "c:v": spec["ffmpeg_codec"],
                "b:v": spec["bitrate"],
                "profile:v": spec["profile"],
                "level:v": spec["level"],
                "r": spec["fps"],
                "g": gop_size,
                "keyint_min": gop_size,
                "sc_threshold": "0",
                "preset": self.profile.preset(),
                "pix_fmt": "yuv420p",
                "x264opts": f"keyint={gop_size}:keyint_min={gop_size}:no-scenecut",
            }

            if spec["cbr"]:
                x264opts.append("nal-hrd=cbr")
                output_params["minrate"] = spec["bitrate"]
                output_params["maxrate"] = spec["bitrate"]
                output_params["bufsize"] = spec["bitrate"]

            if x264opts:
                output_params["x264opts"] = ":".join(x264opts)

            self._encode_output(input_stream, output_params, output_path)

        # Audio
        for spec in self.profile.audio_renditions():
            for lang, audio_input in input["audio"].items():
                # path only - extract first audio track
                if isinstance(audio_input, str):
                    audio_input = [audio_input, 0]

                spec_name = "{}_{}_{}k".format(
                    lang,
                    spec["codec"],
                    int(spec["bitrate"]) // 1000,
                )
                rung_name = "{}_{}".format(input["asset_id"], spec_name)
                logger.info("Transcoding audio: %s", rung_name)

                output_filename = f"{rung_name}.mp4"
                output_path = os.path.join(self.output_folder, output_filename)

                rendition = OutputRendition(rung_name, "audio", spec_name)
                rendition.mp4 = output_path
                rendition.lang = lang
                renditions.append(rendition)

                input_stream = self._make_input_stream(
                    "audio",
                    input=audio_input[0] if audio_input else None,
                    track_index=audio_input[1] if audio_input else 0,
                    duration=duration,
                    fps=None,
                    with_filters=not self.skip_transformations,
                )

                output_params = {
                    "c:a": spec["ffmpeg_codec"],
                    "b:a": spec["bitrate"],
                    "ac": spec["channels"],
                    "metadata:s:a:0": f"language={lang}",
                }

                self._encode_output(input_stream, output_params, output_path)

        return renditions

    def _make_input_stream(
        self,
        type_,
        input,
        duration,
        fps,
        track_index=0,
        metadata=[],
        with_filters: bool = True,
    ):
        flags = {}

        # DEPRECATED in favour of trim/atrim filters
        # if with_filters:
        #     if repeat := self.profile.filter_repeat():
        #         flags["stream_loop"] = repeat - 1
        #         duration = repeat * duration

        #     if trim := self.profile.filter_trim():
        #         flags["ss"] = trim["start"]
        #         flags["t"] = trim["duration"]
        #         duration = trim["duration"]

        if type_ == "image":
            flags["loop"] = 1
            input_stream = ffmpeg.input(input, **flags)

        if type_ == "video":
            input_stream = ffmpeg.input(input, **flags)
            input_stream = input_stream.video
        if type_ == "audio":
            if input:
                if input.startswith("pulse"):
                    pulse_file = make_pulse(duration=duration, level=int(input[5:]))
                    input_stream = ffmpeg.input(pulse_file, **flags)
                else:
                    # must be a file
                    input_stream = ffmpeg.input(input, **flags)
                    input_stream = input_stream[f"a:{track_index}"]
            else:
                input_stream = ffmpeg.input("anullsrc=r=48000:cl=stereo", f="lavfi")

        if with_filters:
            # Loop
            if repeat := self.profile.filter_repeat():
                duration = repeat * duration
                input_streams = [input_stream] * repeat
                if type_ == "video":
                    input_stream = ffmpeg.concat(*input_streams, n=repeat, a=0, v=1)
                if type_ == "audio":
                    input_stream = ffmpeg.concat(*input_streams, n=repeat, a=1, v=0)

            # Trim
            if trim := self.profile.filter_trim():
                if trim["duration"]:
                    duration = trim["duration"]
                else:
                    duration = duration - trim["start"]

                if type_ == "audio":
                    trim_filter_name = "atrim"
                    setpts_filter_name = "asetpts"
                else:
                    trim_filter_name = "trim"
                    setpts_filter_name = "setpts"

                input_stream = ffmpeg.filter(
                    input_stream,
                    trim_filter_name,
                    start=trim["start"],
                    duration=duration,
                )

                input_stream = ffmpeg.filter(
                    input_stream, setpts_filter_name, "PTS-STARTPTS"
                )

            # Video-only filters
            if type_ in ["video", "image"]:
                # Resize
                if resize := self.profile.filter_resize():
                    if resize["crop"] and resize["crop"]["aspect_width"]:
                        input_stream = ffmpeg.filter(
                            input_stream,
                            "crop",
                            w=f'in_h*{resize["crop"]["aspect_width"]}/{resize["crop"]["aspect_height"]}',
                            h="in_h",
                        )

                    if resize["size"]:
                        input_stream = ffmpeg.filter(
                            input_stream,
                            "scale",
                            width=resize["size"]["width"],
                            height=resize["size"]["height"],
                            force_original_aspect_ratio="decrease",
                        )

                    if resize["pad"]:
                        input_stream = ffmpeg.filter(
                            input_stream,
                            "pad",
                            width=resize["pad"]["width"],
                            height=resize["pad"]["height"],
                            x=resize["pad"]["x"],
                            y=resize["pad"]["y"],
                            color=resize["pad"]["color"],
                        )

                # Overlays
                for overlay in self.profile.filter_overlay():
                    overlay_input_stream = ffmpeg.input(overlay["path"], loop=1)

                    if overlay["width"] or overlay["height"]:
                        overlay_input_stream = ffmpeg.filter(
                            overlay_input_stream,
                            "scale",
                            width=overlay["width"],
                            height=overlay["height"],
                        )

                    if overlay["fade_in"] and overlay["fade_in"]["duration"] > 0:
                        overlay_input_stream = apply_fade(
                            "in",
                            overlay_input_stream,
                            video_duration=duration,
                            start=overlay["fade_in"]["start"],
                            duration=overlay["fade_in"]["duration"],
                        )

                    if overlay["fade_out"] and overlay["fade_out"]["duration"] > 0:
                        overlay_input_stream = apply_fade(
                            "out",
                            overlay_input_stream,
                            video_duration=duration,
                            start=overlay["fade_out"]["start"],
                            duration=overlay["fade_out"]["duration"],
                        )

                    input_stream = ffmpeg.overlay(
                        input_stream,
                        overlay_input_stream,
                        shortest=1,
                        x=overlay["x"],
                        y=overlay["y"],
                    )

                # Progress bar Overlays
                if progressbar := self.profile.filter_progressbar():
                    input_stream = apply_progressbar(
                        input_stream, duration, progressbar
                    )

                # Text Overlays
                for text in self.profile.filter_text(duration=duration):
                    text["text"] = text["text"].replace("$$TOTDUR$$", str(duration))
                    text["text"] = text["text"].replace("$$FRAMEDUR$$", str(1 / fps))
                    text["text"] = text["text"].replace(
                        "$$METADATA1$$", str(metadata[0] if len(metadata) > 0 else "")
                    )

                    rotation = 0
                    if "rotate" in text:
                        rotation = text.pop("rotate")

                    input_stream = ffmpeg.drawtext(
                        input_stream, escape_text=False, **text
                    )
                    # .filter("rotate", angle=rotation, c="none")

                    # TODO: if we want to rotate the text,
                    #   we need to add the rotation to the drawtext filter, not the whole input stream,
                    #   and then concatenate it
                    # if rotation != 0:
                    #     input_stream = ffmpeg.filter(
                    #         input_stream,
                    #         "rotate",
                    #         angle=math.radians(rotation),
                    #         c="none",
                    #     )

            # Concatenate other videos
            for outro in self.profile.filter_intro():
                outro_input_stream = ffmpeg.input(
                    outro["path"], ss=outro["start"], t=outro["duration"]
                )
                input_stream = ffmpeg.concat(
                    outro_input_stream,
                    input_stream,
                    v=1 if type_ == "video" else 0,
                    a=1 if type_ == "audio" else 0,
                )

            for outro in self.profile.filter_outro():
                outro_input_stream = ffmpeg.input(
                    outro["path"], ss=outro["start"], t=outro["duration"]
                )
                input_stream = ffmpeg.concat(
                    input_stream,
                    outro_input_stream,
                    v=1 if type_ == "video" else 0,
                    a=1 if type_ == "audio" else 0,
                )

        return input_stream

    def _encode_output(self, input_stream, output_params, output_path):
        output_params["metadata"] = "comment=opinionated-media-processor"
        output = ffmpeg.output(input_stream, output_path, **output_params).global_args(
            "-hide_banner"
        )

        logger.debug("FFMPEG command: " + " ".join(output.compile()))
        if self.debug:
            ffmpeg.view(
                input_stream,
                filename=f"{output_path}.filtergraph.dot",
                detail=True,
            )

        output.run(overwrite_output=True)


def apply_fade(type_, input_stream, video_duration, start, duration):
    if start < 0:
        start = video_duration + start
    return ffmpeg.filter(
        input_stream,
        "fade",
        t=type_,
        st=start,
        d=duration,
        alpha=1,
    )


def apply_progressbar(input_stream, duration, spec):
    # Create the progress bar's background and foreground
    pbbg = ffmpeg.input(
        f"color={spec['backcolor']}:size={spec['width']}x{spec['height']}",
        f="lavfi",
    ).filter(
        "loop",
        loop=1,
    )

    pbfg = ffmpeg.input(
        f"color={spec['frontcolor']}:size={spec['width']}x{spec['height']}", f="lavfi"
    ).filter(
        "loop",
        loop=1,
    )

    # Overlay the progress bar's foreground on its background
    # TODO - adjust to take into account frame rate, so that start of last frame is actually at end of the progressbar
    if spec["orientation"] == "vertical":
        pb = ffmpeg.filter(
            [pbbg, pbfg],
            "overlay",
            x="(W-w)/2",
            y="t/{}*h-h".format(math.floor(duration)),
        )
    else:
        pb = ffmpeg.filter(
            [pbbg, pbfg],
            "overlay",
            x="t/{}*w-w".format(math.floor(duration)),
            y="(H-h)/2",
        )

    # Add a border around the progress bar using the drawbox filter
    bordered_pb = (
        pb.drawbox(
            x=0,
            y=0,
            width="iw",
            height="ih",
            color=spec["bordercolor"],
            t=spec["border"],
        )
        .filter("format", "rgba")  # ensure the stream has an alpha channel
        .filter("colorchannelmixer", aa=spec["opacity"])  # set the alpha channel
    )

    # Overlay the progress bar on the main background and add text
    return ffmpeg.filter(
        [input_stream, bordered_pb], "overlay", x=spec["x"], y=spec["y"], shortest=1
    )


def make_pulse(duration: float = 1, level: int = 0):
    duration = math.floor(duration)
    base_frequency = 440
    freq = base_frequency * (2 ** (level / 12))  # semitones

    # beep
    (
        ffmpeg.input(
            f"sine=frequency={freq}:duration=0.1",
            f="lavfi",
        )
        .output(f"beep_{freq}.wav", **{"c:a": "pcm_s16le"})
        .overwrite_output()
        .run()
    )

    # silence
    (
        ffmpeg.input("anullsrc=r=44100:cl=stereo", f="lavfi")
        .output(
            "silent.wav",
            t=0.9,
        )
        .overwrite_output()
        .run()
    )

    # concatenate
    input1 = ffmpeg.input(f"beep_{freq}.wav")
    input2 = ffmpeg.input("silent.wav")
    (
        ffmpeg.concat(input1, input2, n=2, v=0, a=1)
        .output(f"beep_{freq}-silent.wav")
        .overwrite_output()
        .run()
    )

    # loop
    # Generate a list of the same file repeated 'times' times
    inputs = [ffmpeg.input(f"beep_{freq}-silent.wav") for _ in range(duration)]

    # Concatenate the inputs
    joined = (
        ffmpeg.concat(*inputs, v=0, a=1).output("pulse_track.wav").overwrite_output()
    )

    # Run the FFmpeg process
    joined.run()

    return "pulse_track.wav"
