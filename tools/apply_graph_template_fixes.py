#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post-restore tweaks for graph_template.html (UTF-8-safe).

Run after tools/restore_html_utf8_from_head.py when editing template:
  - normalize charset declaration to lowercase utf-8
  - disable vis-network improvedLayout (silences layout warning)

Then regenerate graph.html: python tools/inject_graph_data.py --from-template
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    p = ROOT / "graph_template.html"
    text = p.read_text(encoding="utf-8")
    text = text.replace("<meta charset=\"UTF-8\">", "<meta charset=\"utf-8\">", 1)

    old = """      network = new vis.Network(document.getElementById('mynetwork'), { nodes, edges }, {
        physics:"""

    new = """      network = new vis.Network(document.getElementById('mynetwork'), { nodes, edges }, {
        layout: { improvedLayout: false },
        physics:"""

    if old not in text:
        raise SystemExit("apply_graph_template_fixes: vis.Network block not found")
    text = text.replace(old, new, 1)
    p.write_text(text, encoding="utf-8", newline="\n")
    print(f"OK patched {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
