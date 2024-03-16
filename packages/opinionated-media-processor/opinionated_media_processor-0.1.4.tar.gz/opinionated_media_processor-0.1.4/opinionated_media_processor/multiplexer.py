import os
from typing import List

import ffmpeg

from .eprofile import Profile
from .rendition import OutputRendition


class FfmpegMultiplexer:
    def __init__(
        self, profile: Profile, output_folder: str, debug: bool = False
    ) -> None:
        self.profile: Profile = profile
        self.output_folder: str = output_folder
        self.debug = debug

    def mux(self, renditions: List[OutputRendition]):
        muxed_mp4s = []
        if spec := self.profile.mp4_spec():
            if spec["multiplex"] == "all":
                for vr in [r for r in renditions if r.type == "video"]:
                    for ar in [r for r in renditions if r.type == "audio"]:
                        input_files = [vr.mp4, ar.mp4]
                        output_name = f"{vr.name}_{ar.spec}.mp4"

                        muxed_mp4s.append(
                            self.mux_streams(
                                input_files=input_files,
                                output_path=os.path.join(
                                    self.output_folder, output_name
                                ),
                            )
                        )

            if spec["multiplex"] == "first":
                vr = next(r for r in renditions if r.type == "video")
                ar = next(r for r in renditions if r.type == "audio")
                
                combined_mp4 = self.mux_streams(
                    input_files=[vr.mp4, ar.mp4],
                    output_path=os.path.join(
                        self.output_folder, f"{vr.name}_muxed_audio.mp4"
                    ),
                )
                muxed_mp4s.append(combined_mp4)

        return muxed_mp4s

    def mux_streams(self, input_files: list, output_path):
        inputs = []
        for i in input_files:
            inputs.append(ffmpeg.input(i))

        ffmpeg.output(*inputs, output_path, acodec="copy", vcodec="copy").run(
            overwrite_output=True
        )

        return output_path
