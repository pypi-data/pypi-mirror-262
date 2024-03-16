import logging
import os
import random
import shutil
import string
import time
from typing import Optional

import requests
import yaml
from .analyse import extract_audio_tracks
from .encode import FfmpegEncoder
from .eprofile import Profile
from .multiplexer import FfmpegMultiplexer
from .package import ShakaPackager
from .transfer import download_file_from_s3, upload_to_s3, write_flag_to_s3

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)7s] (%(filename)s:%(lineno)s)  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


class OpinionatedMediaProcessingTool:
    def __init__(self, debug=False) -> None:
        self.input: dict
        self.debug = debug

    def build_input_payload(
        self,
        input_path,
        asset_id: Optional[str] = None,
        language: str = "und",
        audio: Optional[str] = None,
        suffix: Optional[str] = None,
        metadata: list = [],
    ):
        """Reads a YAML input payload, or generate it for a single media file as input"""
        if input_path.endswith(".yaml"):
            self.input = yaml.safe_load(open(input_path, "r"))

        else:
            asset_id = asset_id or os.path.basename(input_path).split(".")[0]
            if suffix == "RANDOM":
                asset_id += "_" + _id_generator(6)
            elif suffix:
                asset_id += "_" + suffix

            folder = os.path.dirname(input_path)
            self.input = dict(
                asset_id=asset_id,
                folder=folder,
                video=input_path,
                metadata=metadata,
            )

            # Special treatment for image-to-video
            if input_path.endswith(".jpg") or input_path.endswith(".png"):
                if audio:
                    self.input["audio"] = {language: audio}
                else:
                    self.input["audio"] = {language: None}
            else:
                audio_tracks = extract_audio_tracks(input_path)
                self.input["audio"] = {
                    language: [input_path, pos]
                    for language, pos in audio_tracks.items()
                }

        return self.input

    def load_profile_yaml(self, profile_path: str):
        if profile_path.startswith(("http://", "https://")):
            logger.info(f"Downloading profile from {profile_path}")
            response = requests.get(profile_path)
            if response.status_code == 200:
                profile_path = "/tmp/profile.yaml"
                with open(profile_path, "w") as f:
                    f.write(response.text)

        if profile_path.startswith("s3://"):
            logger.info(f"Downloading profile from {profile_path}")
            dest_file = "/tmp/profile.yaml"
            download_file_from_s3(profile_path, dest_file)
            profile_path = dest_file

        profile_yaml = Profile.from_yaml(profile_path)
        return profile_yaml

    def run(
        self,
        profile_path: str,
        destination: str,
        no_transformation: bool = False,
        skip_if_output_exists: bool = False,
        duration: int = None,
    ):
        if destination.startswith("s3://"):
            # make a temporary directory locally
            output_folder = "/tmp/opinionated-media-prep/"
            logger.debug(f"Outputs to be stored in temporary folder: {output_folder}")
        else:
            output_folder = destination

        # Get the profile
        profile = self.load_profile_yaml(profile_path)

        # Prepare output folder
        output_folder = os.path.join(output_folder, self.input["asset_id"])
        if skip_if_output_exists and os.path.exists(output_folder):
            logger.info(
                f"Skipping processing: an output already exists in this location: {output_folder}"
            )
            return (None, output_folder)
        else:
            _create_output_folder(output_folder)

            _set_flag("start", output_folder)

            if destination.startswith("s3://"):
                # suffix asset name
                destination = os.path.join(destination, self.input["asset_id"])
                write_flag_to_s3("start", destination)

            # Encode
            encoder = FfmpegEncoder(
                profile=profile,
                output_folder=output_folder,
                skip_transformations=no_transformation,
                debug=self.debug,
            )
            renditions = encoder.encode(input=self.input, duration_overwrite=duration)

            manifests = {}

            # Multiplex
            multiplexer = FfmpegMultiplexer(
                profile=profile,
                output_folder=output_folder,
                debug=self.debug,
            )
            multiplexed_renditions = multiplexer.mux(renditions=renditions)
            manifests["muxed"] = multiplexed_renditions

            # Package
            packager = ShakaPackager(
                profile=profile,
                output_folder=output_folder,
                debug=self.debug,
            )
            manifests.update(packager.package(renditions=renditions))

            _set_flag("ready", output_folder)

            # Optionally transfer to S3
            if destination.startswith("s3://"):
                # Transfer
                logger.info(f"Uploading outputs to {destination}")
                upload_to_s3(destination, output_folder)
                write_flag_to_s3("ready", destination)

                # Cleanup
                logger.debug("Clearing temporary outputs")
                shutil.rmtree(output_folder)

            return (manifests, destination)


def _create_output_folder(output_folder) -> None:
    os.makedirs(output_folder, exist_ok=True)


def _id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def _set_flag(name, output_folder) -> None:
    # remove all other flag files
    for f in os.listdir(output_folder):
        if f.startswith("flag."):
            os.remove(os.path.join(output_folder, f))

    with open(os.path.join(output_folder, f"flag.{name}"), "w") as f:
        # Write the current date time as ISO in the file
        f.write(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
