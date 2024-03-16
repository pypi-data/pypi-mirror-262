import argparse
import json

from .__version__ import __version__
from .tool import OpinionatedMediaProcessingTool


def main():
    args = parse_args()

    app = OpinionatedMediaProcessingTool(debug=args.debug)
    app.build_input_payload(
        input_path=args.input,
        asset_id=args.asset,
        language=args.language,
        audio=args.audio,
        suffix=args.suffix,
        metadata=args.metadata,
    )

    outputs = app.run(
        profile_path=args.profile,
        destination=args.output,
        duration=args.duration,
        no_transformation=args.no_transformation,
    )

    print("OUTPUTS")
    print(json.dumps(outputs, indent=2))


def parse_args():
    def check_lang_code(value):
        if len(value) != 3:
            raise argparse.ArgumentTypeError(
                f"Language codes should be a 3-letter string. '{value}' does not meet that constraint"
            )
        return value

    parser = argparse.ArgumentParser(
        description=f"Opinionated Media Processor - version {__version__}",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Opinionated Media Processor, version {__version__}",
        help="Print the version number and exit",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input file or YAML file",
        default="input.yaml",
    )
    parser.add_argument(
        "-a",
        "--asset",
        type=str,
        help="Asset Identifier (used as output prefix)",
        default=None,
    )
    parser.add_argument(
        "-s",
        "--suffix",
        type=str,
        help="Suffix for the output files. Use 'RANDOM' for a random string",
        default=None,
    )
    parser.add_argument(
        "-l",
        "--language",
        type=check_lang_code,
        help="Language for the audio track (if not using an input YAML file)",
        default="eng",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output folder",
        default="outputs",
    )
    parser.add_argument(
        "-p",
        "--profile",
        type=str,
        default="profile.yaml",
        help="YAML file containing the definition of the encoding / packaging profiles",
    )
    parser.add_argument(
        "-nt",
        "--no-transformation",
        action="store_true",
        default=False,
        help="Disable transformations of the input file (other than final scaling), use source as is",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug mode",
    )
    parser.add_argument(
        "-m",
        "--metadata",
        action="append",
        default=[],
        help="Additional metadata",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        required=False,
        help="Duration (overwrite)",
    )
    parser.add_argument(
        "--audio",
        type=str,
        required=False,
        help="Audio track, as a path to a file, or an expression",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
