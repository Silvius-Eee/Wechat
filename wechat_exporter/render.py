from __future__ import annotations

from pathlib import Path
from typing import Literal

OutputFormat = Literal["txt", "md"]


def render_text(text: str, fmt: OutputFormat) -> str:
    content = text.rstrip("\n")

    if fmt == "txt":
        return (content + "\n") if content else ""

    if fmt == "md":
        return f"```text\n{content}\n```\n"

    raise ValueError(f"Unsupported format: {fmt}")


def render_file(input_path: Path, output_path: Path, fmt: OutputFormat) -> None:
    text = input_path.read_text(encoding="utf-8")
    rendered = render_text(text, fmt)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
