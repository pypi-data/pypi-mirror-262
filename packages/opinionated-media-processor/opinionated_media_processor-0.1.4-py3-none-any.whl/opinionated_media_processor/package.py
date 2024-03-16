import logging
import os
from typing import List

from .eprofile import Profile
from .executor import execute
from .rendition import OutputRendition

USE_DOCKER = False

logger = logging.getLogger(__name__)


class ShakaPackager:
    def __init__(
        self, profile: Profile, output_folder: str, debug: bool = False
    ) -> None:
        self.profile: Profile = profile
        self.output_folder: str = output_folder
        self.debug = debug

        self.command = ["packager"]
        if USE_DOCKER:
            self.command = [
                ["docker", "run", "--rm", "-it"],
                ["-v", f"{self.output_folder}:/media"],
                "google/shaka-packager",
                "packager",
            ]

    def package(self, renditions: List[OutputRendition]):
        outputs = {}

        if spec := self.profile.hls_spec():
            logger.info("Packaging HLS/ts")
            outputs["hls"] = self.package_hls_ts(renditions, spec)

        if spec := self.profile.dash_spec():
            logger.info("Packaging DASH/isoff-live")
            outputs["dash"] = self.package_dash_isofflive(renditions, spec)

        return outputs

    def package_hls_ts(self, renditions: List[OutputRendition], spec: dict):
        # Package into HLS/ts
        subfolder = "hls"
        main_playlist = "stream.m3u8"
        os.makedirs(os.path.join(self.output_folder, subfolder), exist_ok=True)

        default_lang = next((r.lang for r in renditions if r.type == "audio"), "eng")

        command = self.command
        folder = "/media" if USE_DOCKER else self.output_folder

        for rung in renditions:
            playlist_name = f"{rung.name}.m3u8"

            params = {
                "in": f"{folder}/{rung.name}.mp4",
                "stream": rung.type,
                "segment_template": f"{folder}/{subfolder}/{rung.name}/{rung.name}_$Number$.ts",
                "playlist_name": f"{folder}/{subfolder}/{playlist_name}",
            }

            if rung.type == "video" and spec["iframes"] is True:
                params["iframe_playlist_name"] = (
                    f"{folder}/{subfolder}/iframe_{playlist_name}"
                )

            command.append(",".join(f"{k}={v}" for k, v in params.items()))

        command.append(["--segment_duration", spec["segment_size"]])
        command.append(
            ["--hls_master_playlist_output", f"{folder}/{subfolder}/{main_playlist}"]
        )
        command.append(["--default_language", default_lang])

        execute(command)
        return os.path.join(self.output_folder, subfolder, main_playlist)

    def package_dash_isofflive(self, renditions: List[OutputRendition], spec: dict):
        # Package into DASH/isoff-live
        subfolder = "dash"
        main_playlist = "stream.mpd"
        os.makedirs(os.path.join(self.output_folder, subfolder), exist_ok=True)

        command = self.command
        folder = "/media" if USE_DOCKER else self.output_folder

        for rung in renditions:
            params = [
                f"in={folder}/{rung.name}.mp4",
                f"stream={rung.type}",
                f"init_segment={folder}/{subfolder}/{rung.name}/init.m4s",
                f"segment_template={folder}/{subfolder}/{rung.name}/{rung.name}_$Number$.m4s",
            ]

            command.append(",".join(params))

        command.append(["--segment_duration", spec["segment_size"]])
        command.append(["--generate_static_live_mpd"])
        command.append(["--mpd_output", f"{folder}/{subfolder}/{main_playlist}"])

        execute(command)
        return os.path.join(self.output_folder, subfolder, main_playlist)
