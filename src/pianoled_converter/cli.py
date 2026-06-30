"""Command-line interface for pianoled-converter."""

import argparse
from collections.abc import Sequence
from pathlib import Path
import sys

from .converter import convert


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pianoled-converter",
        description="Convert a piano MusicXML file to a three-track MIDI file.",
    )
    parser.add_argument("input_path", type=Path, help="input MusicXML file")
    parser.add_argument("output_path", type=Path, help="output MIDI file")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        convert(args.input_path, args.output_path)
    except Exception as error:
        print(f"pianoled-converter: error: {error}", file=sys.stderr)
        return 1

    print(f"Created MIDI file: {args.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
