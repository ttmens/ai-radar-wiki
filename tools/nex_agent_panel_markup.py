# -*- coding: utf-8 -*-
"""Canonical NexSight「问 AI」面板 HTML — shared by patch scripts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTIAL = ROOT / "assets" / "partials" / "nex-agent-panel.html"

SITE_CHROME_ASSET_VER = "15"

LEGACY_MARKERS = (
    "nex-agent-sources-strip",
    "agent-placeholder-msg",
    "DeepWiki-open",
    "nex-agent-sources-label",
    "nex-agent-footnote",
)

_AGENT_PANEL_RE = re.compile(
    r"  <div id=\"agent-scrim\"[\s\S]*?"
    r"<button type=\"button\" id=\"nex-agent-fab\"[^>]*>\s*问 AI\s*</button>",
    re.MULTILINE,
)


def load_agent_panel_markup() -> str:
    if not PARTIAL.is_file():
        raise FileNotFoundError(f"missing canonical partial: {PARTIAL}")
    return PARTIAL.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n") + "\n"


def has_legacy_agent_markup(s: str) -> bool:
    return any(m in s for m in LEGACY_MARKERS)


def needs_agent_panel_upgrade(s: str) -> bool:
    if "id=\"agent-scrim\"" not in s:
        return True
    if has_legacy_agent_markup(s):
        return True
    if "nex-agent-composer-inner" not in s:
        return True
    m = _AGENT_PANEL_RE.search(s)
    if not m:
        return True
    canonical = load_agent_panel_markup()
    return m.group(0).strip() != canonical.strip()


def upgrade_agent_panel_markup(s: str, *, force: bool = False) -> tuple[str, bool]:
    """Replace #agent-scrim … #nex-agent-fab block with canonical partial."""
    canonical = load_agent_panel_markup()
    m = _AGENT_PANEL_RE.search(s)
    if m is None:
        if force and "id=\"agent-scrim\"" not in s:
            return s, False
        return s, False
    if not force and not needs_agent_panel_upgrade(s):
        return s, False
    upgraded = s[: m.start()] + canonical + s[m.end() :]
    return upgraded, True


def graph_agent_with_toast_block() -> str:
    """Agent panel + subscribe toast (graph first-time insert prefix)."""
    return (
        load_agent_panel_markup()
        + '  <div id="subscribe-toast" role="status" aria-live="polite"></div>\n\n'
    )


def graph_data_libs_scripts_block() -> str:
    return (
        "  <!-- Data & Libs -->\n"
        '  <script id="graph-data" type="application/json">{{DATA}}</script>\n'
        '  <script src="./assets/vis-network.min.js"></script>\n'
        f'  <script src="./assets/site-chrome.js?v={SITE_CHROME_ASSET_VER}"></script>\n'
        "  <script>\n"
    )