#!/usr/bin/env python3
"""One-off batch: replace legacy Airbnb/Rausch colors with Anmunuo brand palette."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Order matters: longer / more specific patterns first where needed.
REPLACEMENTS: list[tuple[str, str]] = [
    ("#FF385C", "#7B3FF2"),
    ("#ff385c", "#7B3FF2"),
    ("#E00B41", "#4A5BFF"),
    ("#e00b41", "#4A5BFF"),
    ("#428bff", "#00F5FF"),
    ("#428BFF", "#00F5FF"),
]

GLOB_DIRS = [
    ROOT / "daily-articles",
    ROOT / "articles",
]
GLOB_FILES = [
    ROOT / "ai-radar-daily-2026-05-13.html",
]


def migrate_text(text: str) -> tuple[str, int]:
    n = 0
    for old, new in REPLACEMENTS:
        if old in text:
            count = text.count(old)
            text = text.replace(old, new)
            n += count
    return text, n


def main() -> int:
    paths: list[Path] = list(GLOB_FILES)
    for d in GLOB_DIRS:
        if d.is_dir():
            paths.extend(sorted(d.glob("*.html")))

    total_files = 0
    total_repls = 0
    for path in paths:
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated, n = migrate_text(raw)
        if n:
            path.write_text(updated, encoding="utf-8", newline="\n")
            print(f"  {path.relative_to(ROOT)}: {n} replacements")
            total_files += 1
            total_repls += n

    print(f"Done: {total_files} files, {total_repls} replacements.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
