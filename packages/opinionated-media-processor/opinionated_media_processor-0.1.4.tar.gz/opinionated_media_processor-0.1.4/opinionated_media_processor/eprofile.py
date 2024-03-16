from copy import deepcopy

import yaml

from .utils import check_framerate_multiples, seconds_to_timecode


class Profile:
    def __init__(self, config: dict):
        self.profile = {}
        if config:
            self.profile = config
            self.validate()

    def __repr__(self):
        return str(self)

    @staticmethod
    def from_yaml(path: str) -> "Profile":
        with open(path, "r") as f:
            return Profile(config=yaml.safe_load(f))

    def video_renditions(self) -> list:
        default = dict(
            codec="h264",
            bitrate=1_000_000,
            height=-2,
            width=-2,
            fps=25,
            gop=2,
            profile="high",
            level="4.1",
            cbr=False,
        )

        renditions = []

        for v in self.profile.get("video", []):
            r = deep_merge(default, v)
            r["ffmpeg_codec"] = r["codec"]
            if r["codec"] == "h264":
                r["ffmpeg_codec"] = "libx264"
            renditions.append(r)

        return renditions

    def audio_renditions(self) -> list:
        default = dict(
            codec="aac",
            bitrate=128_000,
            channels=2,
            sample_rate=48_000,
        )

        renditions = []

        for v in self.profile["audio"]:
            r = deep_merge(default, v)
            r["ffmpeg_codec"] = r["codec"]
            renditions.append(r)

        return renditions

    def overwrite_duration(self, duration: int):
        if duration and isinstance(duration, int):
            filters = self.profile.get("filters", {})
            trim_filter = filters.get("trim", {})
            trim_filter["duration"] = duration
            filters["trim"] = trim_filter
            self.profile["filters"] = filters

    def preset(self) -> str:
        return self.profile.get("preset", "medium")

    def filter_repeat(self) -> None | dict:
        if self.profile.get("filters") and "repeat" in self.profile["filters"]:
            return self.profile["filters"]["repeat"]
        else:
            return None

    def filter_resize(self) -> None | dict:
        default = dict(
            crop=dict(aspect_width=None, aspect_height=None),
            size=dict(width="in_w", height="in_h"),
            pad=dict(
                width="in_w",
                height="in_h",
                x="(ow-iw)/2",
                y="(oh-ih)/2",
                color="black",
            ),
        )

        if self.profile["filters"] and "resize" in self.profile["filters"]:
            return deep_merge(default, self.profile["filters"]["resize"])

    def filter_trim(self) -> None | dict:
        default = dict(start=0, duration=None)

        if self.profile.get("filters") and "trim" in self.profile["filters"]:
            return deep_merge(default, self.profile["filters"]["trim"])

    def filter_overlay(self) -> list:
        padding = 20
        x_macros = dict(
            LEFT=padding,
            MIDDLE="(main_w-overlay_w)/2",
            RIGHT=f"main_w-overlay_w-{padding}",
        )

        y_macros = dict(
            TOP=padding,
            MIDDLE="(main_h-overlay_h)/2",
            BOTTOM=f"main_h-overlay_h-{padding}",
        )

        default = dict(
            path="",
            x=0,
            y=0,
            width=-1,
            height=-1,
            fade_in=dict(start=0, duration=0),
            fade_out=dict(start=None, duration=0),
        )

        arr = []
        if self.profile["filters"] and "overlay" in self.profile["filters"]:
            for f in self.profile["filters"]["overlay"]:
                ox = deep_merge(default, f)
                for label, value in x_macros.items():
                    ox["x"] = str(ox["x"]).replace(label, str(value))
                for label, value in y_macros.items():
                    ox["y"] = str(ox["y"]).replace(label, str(value))
                arr.append(ox)

        return arr

    def filter_text(self, duration=0) -> list:
        padding = 20
        x_macros = dict(
            LEFT=padding,
            MIDDLE="(w-text_w)/2",
            RIGHT=f"w-text_w-{padding}",
        )

        y_macros = dict(
            TOP=padding,
            MIDDLE="(h-text_h)/2",
            BOTTOM=f"h-text_h-{padding}",
        )

        text_macros = dict(
            PTS="%{pts}",
            TIME="%{pts:hms}",
            # COUNTDOWN="%{eif:trunc(max($$TOTDUR$$-$$FRAMEDUR$$-t,0))/3600:d:2}:%{eif:trunc(max(mod($$TOTDUR$$-$$FRAMEDUR$$-t,3600),0)/60):d:2}:%{eif:max(mod($$TOTDUR$$-$$FRAMEDUR$$-t,60),0):d:2}",
            # COUNTDOWN_MS="%{eif:trunc(max($$TOTDUR$$-$$FRAMEDUR$$-t, 0)/3600):d:2}:%{eif:trunc(max(mod($$TOTDUR$$-$$FRAMEDUR$$-t,3600),0)/60):d:2}:%{eif:max(mod($$TOTDUR$$-$$FRAMEDUR$$-t,60),0):d:2}.%{eif:trunc(max(mod($$TOTDUR$$-$$FRAMEDUR$$-t,1),0)*1000):d:3}",
            COUNTDOWN="%{eif:trunc($$TOTDUR$$-t)/3600:d:2}:%{eif:trunc(mod($$TOTDUR$$-t,3600)/60):d:2}:%{eif:mod($$TOTDUR$$-t,60):d:2}",
            COUNTDOWN_MS="%{eif:trunc(mod($$TOTDUR$$-t,3600)/60):d:2}:%{eif:trunc(mod($$TOTDUR$$-t,60)):d:2}.%{eif:trunc(mod($$TOTDUR$$-t,1)*1000):d:3}",
            DURATION=seconds_to_timecode(
                duration, include_milliseconds=False, force_hours=False
            ),
            DURATION_MS=seconds_to_timecode(
                duration, include_milliseconds=True, force_hours=False
            ),
            DURATION_IN_S=duration,
        )

        if duration < 3600:
            text_macros["COUNTDOWN"] = (
                "%{eif:trunc(mod($$TOTDUR$$-t,3600)/60):d:2}:%{eif:mod($$TOTDUR$$-t,60):d:2}"
            )

        default = dict(text="", x=padding, y=padding, fontsize=48, rotate=0)

        # To add fade-in/out for text, add this to the filter:
        # if(lt(t,10),0,if(lt(t,40),(t-10)/30,if(lt(t,70),1,if(lt(t,110),(40-(t-70))/40,0))))
        # with 10 = start of fade, 20 = duration of fade in, 30 = start of fade out, 40 = duration of fade out

        arr = []
        if self.profile["filters"] and "text" in self.profile["filters"]:
            for t in self.profile["filters"]["text"]:
                tx = deep_merge(default, t)
                for label, value in x_macros.items():
                    tx["x"] = str(tx["x"]).replace(label, str(value))
                for label, value in y_macros.items():
                    tx["y"] = str(tx["y"]).replace(label, str(value))

                # replace all occurrences of the text_macros in the string. text_macros are surrounded by $$
                for k, v in text_macros.items():
                    tx["text"] = tx["text"].replace(f"$${k}$$", str(v))

                arr.append(tx)

        return arr

    def filter_intro(self) -> list:
        return self._filter_intro_outro("intro")

    def filter_outro(self) -> list:
        return self._filter_intro_outro("outro")

    def _filter_intro_outro(self, type_) -> list:
        default = dict(path="", start=0, duration=None)
        arr = []

        if self.profile.get("filters") and type_ in self.profile["filters"]:
            for f in self.profile["filters"][type_]:
                arr.append(deep_merge(default, f))

        return arr

    def filter_progressbar(self) -> dict:
        default = dict(
            orientation="horizontal",
            x="0",
            y="H-h",
            width="W",
            height="32",
            backcolor="white",
            frontcolor="green",
            border="2",
            bordercolor="black",
            opacity=1,
        )

        if self.profile["filters"] and "progressbar" in self.profile["filters"]:
            return deep_merge(default, self.profile["filters"]["progressbar"])

    def hls_spec(self):
        default = {"segment_size": 4, "iframes": False}

        if "hls" in self.profile:
            return deep_merge(default, self.profile["hls"])

    def dash_spec(self):
        default = {"segment_size": 4}

        if "dash" in self.profile:
            return deep_merge(default, self.profile["dash"])

    def mp4_spec(self):
        default = {"multiplex": "none"}

        if "mp4" in self.profile:
            return deep_merge(default, self.profile["mp4"])

    def validate(self):
        if "video" in self.profile:
            # STEP 0 - Validate and clean the input data
            lowest_fps = check_framerate_multiples(
                [v["fps"] for v in self.profile["video"]]
            )
            assert (
                lowest_fps
            ), "All framerates must be equivalent or multiple of the smallest one"

            min_gop_size = min([float(v["gop"]) for v in self.profile["video"]])

            if "hls" in self.profile:
                assert (
                    self.profile["hls"]["segment_size"] % min_gop_size == 0
                ), "HLS segment size must be a multiple of the GOP size"


def deep_merge(a: dict, b: dict) -> dict:
    result = deepcopy(a)
    for bk, bv in b.items():
        av = result.get(bk)
        if isinstance(av, dict) and isinstance(bv, dict):
            result[bk] = deep_merge(av, bv)
        else:
            result[bk] = deepcopy(bv)
    return result
