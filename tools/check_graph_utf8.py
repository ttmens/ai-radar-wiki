#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail fast if graph HTML lost UTF-8 (Windows cp936 open(), PowerShell redirects, etc.).

Exit 0: OK. Exit 1: corruption patterns found (prints paths + reasons).

Checks (per file):
  - Unicode replacement character U+FFFD
  - ``??`` before ``**`` inside inline JS (broken weekly-summary regex / mojibake)
  - Bursts of ``???`` in HTML text (lossy decoding of CJK → question marks)
  - ``header-title-text">?? NexSight`` (common local mojibake signature)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# HTML text nodes / attributes: ASCII ? bursts often mean lost CJK (Latin-1/cp1252 saves).
_TRIPLE_Q_HTML = re.compile(r">[^<]{0,240}\?\?\?[^<]{0,240}<")
_TITLE_MOJIBAKE = re.compile(r'header-title-text">\?\?+\s+NexSight')

# Same pattern ensure_graph_js_regexes uses.
_MOJIBAKE_REGEX = re.compile(r"\?\?\s*\*\*")


def _check_text(name: str, text: str) -> list[str]:
    errs: list[str] = []
    if "\ufffd" in text:
        errs.append(f"{name}: contains U+FFFD replacement character")
    if _MOJIBAKE_REGEX.search(text):
        errs.append(f"{name}: found `??` before `**` (likely mojibake or broken JS regex)")
    if _TRIPLE_Q_HTML.search(text):
        errs.append(f"{name}: suspicious `???` in HTML text (likely lossy decode)")
    if _TITLE_MOJIBAKE.search(text):
        errs.append(f"{name}: `header-title-text` shows `??` before NexSight (known mojibake signature)")
    return errs


def check_files(paths: list[Path]) -> list[str]:
    out: list[str] = []
    for p in paths:
        if not p.is_file():
            out.append(f"{p}: missing file")
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            out.append(f"{p}: not valid UTF-8 ({e})")
            continue
        out.extend(_check_text(str(p), text))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument(
        "--wiki-root",
        type=Path,
        default=None,
        help="Repo root (default: parent of tools/)",
    )
    args = ap.parse_args()
    root = args.wiki_root or Path(__file__).resolve().parent.parent
    paths = [root / "graph.html", root / "graph_template.html"]
    errs = check_files(paths)
    if errs:
        for e in errs:
            print(e, file=sys.stderr)
        return 1
    for p in paths:
        if p.is_file():
            print("OK", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
