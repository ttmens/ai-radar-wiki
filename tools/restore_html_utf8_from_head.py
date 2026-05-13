#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restore graph.html / graph_template.html UTF-8 from git HEAD while keeping
recent shell + mobile layout deltas. Run from repo root: python tools/restore_html_utf8_from_head.py

When editors or scripts save HTML as ANSI/Windows-1252 (or corrupt UTF-8), multi-byte
CJK/fullwidth chars become ``??`` and regex literals such as ``/（/`` turn into invalid ``/??/``.

Never push huge HTML through PowerShell ``Set-Content`` / ``Out-File`` / ``>`` without
``-Encoding utf8`` (prefer BOM-less UTF-8). Prefer Python tools under ``tools/`` with
explicit ``encoding="utf-8"``. See ``tools/README_GRAPH_UTF8.md``."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH_DATA_RE = re.compile(
    r'(<script\s+id="graph-data"\s+type="application/json"\s*>)'
    r'(.*?)'
    r'(</script>)',
    re.DOTALL,
)

HEAD_AFTER_THEME = """

<meta name="view-transition" content="same-origin">"""

APPLE_TOUCH = '<link rel="apple-touch-icon" href="./assets/nexsight-mark.svg">'

CHROME_INJECT = """

<link rel="stylesheet" href="./assets/site-chrome.css">
<script>
  window.__NEXSIGHT_CONFIG__ = window.__NEXSIGHT_CONFIG__ || { agentIframeUrl: '', agentApiBase: '' };
</script>"""

# Legacy clamp inserted by older restores; omit so #mynetwork stays full-bleed below header (sheets overlay).
LEGACY_MOBILE_NETWORK_CLAMP = """

    /* Mobile graph: ~2/5 viewport; height stays above the 60dvh bottom sheet (min with 40dvh). Desktop keeps base #mynetwork bottom:0. */
    #mynetwork {
      bottom: auto;
      height: clamp(
        200px,
        min(40dvh, calc(100dvh - var(--header-h) - 60dvh)),
        100dvh
      );
    }
"""


def _git_show(path: str) -> str:
    b = subprocess.check_output(['git', 'show', f'HEAD:{path}'], cwd=ROOT)
    return b.decode('utf-8')


def _extract_graph_json(worktree_html: str) -> str | None:
    m = GRAPH_DATA_RE.search(worktree_html)
    return m.group(2) if m else None


def _inject_head(base: str) -> str:
    tag = '<meta name="theme-color" content="#ff385c">'
    if tag not in base:
        raise SystemExit(f'missing {tag!r} in HEAD blob')
    if (
        'view-transition' in base
        and './assets/site-chrome.css' in base
        and '__NEXSIGHT_CONFIG__' in base
    ):
        return base
    if 'view-transition' not in base:
        base = base.replace(tag, tag + HEAD_AFTER_THEME, 1)
    if APPLE_TOUCH not in base:
        raise SystemExit('missing apple-touch-icon link')
    if './assets/site-chrome.css' not in base:
        base = base.replace(APPLE_TOUCH, APPLE_TOUCH + CHROME_INJECT, 1)
    return base


def _inject_mobile_network(base: str) -> str:
    anchor_zh = '\n\n    /* 窄屏遮罩：opacity 过渡，避免 display 切换引起整页重排/跳动 */\n    #panel-scrim {'
    if anchor_zh not in base:
        raise SystemExit('anchor for mobile #mynetwork insert not found')
    if LEGACY_MOBILE_NETWORK_CLAMP in base:
        base = base.replace(LEGACY_MOBILE_NETWORK_CLAMP, '', 1)
    return base


def _merge_graph_data(base: str, json_inner: str) -> str:
    m = GRAPH_DATA_RE.search(base)
    if not m:
        raise SystemExit('HEAD graph.html missing graph-data script')
    return base[: m.start(2)] + json_inner + base[m.end(2) :]


def main() -> int:
    cur_graph = (ROOT / 'graph.html').read_text(encoding='utf-8')
    json_inner = _extract_graph_json(cur_graph)
    if not json_inner:
        raise SystemExit('Could not read graph-data from worktree graph.html')

    g = _git_show('graph.html')
    g = _inject_head(g)
    g = _inject_mobile_network(g)
    g = _merge_graph_data(g, json_inner)
    (ROOT / 'graph.html').write_text(g, encoding='utf-8', newline='\n')

    tpl = _git_show('graph_template.html')
    tpl = _inject_head(tpl)
    tpl = _inject_mobile_network(tpl)
    if '{{DATA}}' not in tpl:
        raise SystemExit('graph_template missing {{DATA}}')
    (ROOT / 'graph_template.html').write_text(tpl, encoding='utf-8', newline='\n')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
