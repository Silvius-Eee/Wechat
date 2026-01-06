from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Optional

from .dedup import dedup_file
from .render import render_file


def _path(value: str) -> Path:
    return Path(value).expanduser()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WeChat text exporter utilities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    dedup_parser = subparsers.add_parser("dedup", help="Deduplicate raw_dump.txt by screen.")
    dedup_parser.add_argument("--in", dest="input_path", required=True, type=_path, help="Path to raw_dump.txt")
    dedup_parser.add_argument("--out", dest="output_path", required=True, type=_path, help="Path to write deduplicated text")

    render_parser = subparsers.add_parser("render", help="Render deduplicated text to txt or markdown.")
    render_parser.add_argument("--in", dest="input_path", required=True, type=_path, help="Path to deduplicated text")
    render_parser.add_argument("--out", dest="output_path", required=True, type=_path, help="Path to write rendered output")
    render_parser.add_argument("--format", dest="format", required=True, choices=["txt", "md"], help="Output format")

    return parser


def main(argv: Optional[Iterable[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "dedup":
        dedup_file(args.input_path, args.output_path)
    elif args.command == "render":
        render_file(args.input_path, args.output_path, args.format)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
