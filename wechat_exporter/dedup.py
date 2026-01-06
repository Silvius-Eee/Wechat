from __future__ import annotations

from pathlib import Path
from typing import Iterable, List


def _split_blocks(text: str) -> List[str]:
    """Split text into blocks separated by blank lines."""
    blocks: List[str] = []
    current: List[str] = []

    for line in text.splitlines():
        if line.strip():
            current.append(line.rstrip())
        elif current:
            blocks.append("\n".join(current).rstrip())
            current = []

    if current:
        blocks.append("\n".join(current).rstrip())

    return blocks


def _dedup_blocks(blocks: Iterable[str]) -> List[str]:
    """Return blocks preserving order while removing duplicates."""
    seen: set[str] = set()
    unique: List[str] = []

    for block in blocks:
        key = block.strip()
        if not key:
            continue
        if key in seen:
            continue
        seen.add(key)
        unique.append(block)

    return unique


def dedup_text(text: str) -> str:
    """Deduplicate screens separated by blank lines."""
    blocks = _split_blocks(text)
    unique = _dedup_blocks(blocks)
    return "\n\n".join(unique).rstrip() + ("\n" if unique else "")


def dedup_file(input_path: Path, output_path: Path) -> None:
    text = input_path.read_text(encoding="utf-8")
    deduped = dedup_text(text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(deduped, encoding="utf-8")
