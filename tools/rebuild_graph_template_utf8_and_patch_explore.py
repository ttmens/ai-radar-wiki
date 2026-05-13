# -*- coding: utf-8 -*-
"""Rebuild graph_template.html from graph.html (UTF-8) and apply Explore mobile/header patches.

Assumes graph.html already includes NexSight chrome. Replaces graph-data JSON with {{DATA}},
then: FAB offset + :root stack; remove 摘要 header button and related CSS/JS; null-safe legend.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GRAPH_DATA_RE = re.compile(
    r'(<script\s+id="graph-data"\s+type="application/json"\s*>)'
    r'.*?'
    r'(</script>)',
    re.DOTALL,
)


def rebuild_template_from_graph_html() -> None:
    gpath = ROOT / "graph.html"
    tpath = ROOT / "graph_template.html"
    raw = gpath.read_text(encoding="utf-8").replace("\r\n", "\n").strip("\ufeff")

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + "{{DATA}}" + m.group(2)

    new, n = GRAPH_DATA_RE.subn(repl, raw, count=1)
    if n != 1:
        raise SystemExit("graph-data script not found in graph.html")
    tpath.write_text(new, encoding="utf-8", newline="\n")
    print("OK rebuilt", tpath, "from", gpath)


def patch_explore_mobile_and_header(s: str) -> str:
    s, n = re.subn(
        r'\n\s*<button type="button" id="header-brief-btn"[^>]*>.*?</button>\s*',
        "\n",
        s,
        count=1,
        flags=re.DOTALL,
    )
    if n == 0 and 'id="header-brief-btn"' in s:
        raise SystemExit("header-brief-btn HTML present but regex did not remove")

    if "--mobile-tab-bar-stack:" not in s:
        old = """    :root {
      /* 节点详情底栏；今日情报高度见 #dashboard 内 50vh/50dvh */
      --bottom-sheet-cap: min(78vh, 620px, calc(100dvh - var(--header-h) - 16px));
    }"""
        new = """    :root {
      /* 节点详情底栏；今日情报高度见 #dashboard 内 50vh/50dvh */
      --bottom-sheet-cap: min(78vh, 620px, calc(100dvh - var(--header-h) - 16px));
      /* 略高于 site-chrome 默认值，避免底栏与 FAB 视觉重叠 */
      --mobile-tab-bar-stack: calc(52px + max(16px, var(--safe-bottom)));
    }"""
        if old not in s:
            raise SystemExit(":root mobile block not found for stack inject")
        s = s.replace(old, new, 1)

    old_fab = """    #dashboard-expand-btn {
      top: auto;
      bottom: calc(22px + var(--safe-bottom));
      left: auto;
      right: calc(14px + var(--safe-right));
      transform: none;"""
    new_fab = """    #dashboard-expand-btn {
      top: auto;
      bottom: calc(var(--mobile-tab-bar-stack) + 32px);
      left: auto;
      right: calc(12px + var(--safe-right));
      z-index: 110;
      transform: none;"""
    if old_fab in s:
        s = s.replace(old_fab, new_fab, 1)
    elif "bottom: calc(var(--mobile-tab-bar-stack) + 32px)" not in s:
        raise SystemExit("FAB mobile block not found / unexpected state")

    if ".header-brief-btn {" in s:
        s, n = re.subn(
            r"\n  \.header-brief-btn \{[\s\S]*?\}\n  \.header-brief-btn:hover \{[\s\S]*?\}\n",
            "\n",
            s,
            count=1,
        )
        if n != 1:
            raise SystemExit("could not remove .header-brief-btn CSS rules")
    s = s.replace("    .header-brief-btn { display: none !important; }\n", "", 1)

    old_apply = """      var expandBtn = document.getElementById('dashboard-expand-btn');
      var briefBtn = document.getElementById('header-brief-btn');
      if (!dash) return;
      dash.classList.remove('hidden');
      dash.style.transform = '';
      legend.classList.remove('shifted');
      if (expandBtn) expandBtn.classList.remove('show');
      if (briefBtn) briefBtn.setAttribute('aria-expanded', 'true');"""
    new_apply = """      var expandBtn = document.getElementById('dashboard-expand-btn');
      if (!dash) return;
      dash.classList.remove('hidden');
      dash.style.transform = '';
      if (legend) legend.classList.remove('shifted');
      if (expandBtn) expandBtn.classList.remove('show');"""
    if old_apply in s:
        s = s.replace(old_apply, new_apply, 1)

    old_toggle = """      const expandBtn = document.getElementById('dashboard-expand-btn');
      const briefBtn = document.getElementById('header-brief-btn');
      const isHidden = dash.classList.contains('hidden');

      if (isHidden) {
        dash.classList.remove('hidden');
        dash.style.transform = '';
        legend.classList.remove('shifted');
        if (expandBtn) expandBtn.classList.remove('show');
        if (briefBtn) briefBtn.setAttribute('aria-expanded', 'true');
      } else {
        dash.classList.add('hidden');
        dash.style.transform = '';
        legend.classList.add('shifted');
        if (expandBtn) expandBtn.classList.add('show');
        if (briefBtn) briefBtn.setAttribute('aria-expanded', 'false');
      }"""
    new_toggle = """      const expandBtn = document.getElementById('dashboard-expand-btn');
      const isHidden = dash.classList.contains('hidden');

      if (isHidden) {
        dash.classList.remove('hidden');
        dash.style.transform = '';
        if (legend) legend.classList.remove('shifted');
        if (expandBtn) expandBtn.classList.remove('show');
      } else {
        dash.classList.add('hidden');
        dash.style.transform = '';
        if (legend) legend.classList.add('shifted');
        if (expandBtn) expandBtn.classList.add('show');
      }"""
    if old_toggle in s:
        s = s.replace(old_toggle, new_toggle, 1)

    s = s.replace(
        "      </button>\n<div class=\"subscribe-wrap\">",
        "      </button>\n      <div class=\"subscribe-wrap\">",
        1,
    )

    return s


def main() -> None:
    rebuild_template_from_graph_html()
    tpl = ROOT / "graph_template.html"
    s = tpl.read_text(encoding="utf-8").replace("\r\n", "\n").strip("\ufeff")
    s = patch_explore_mobile_and_header(s)
    tpl.write_text(s, encoding="utf-8", newline="\n")
    print("OK patched explore FAB / header cleanup ->", tpl)


if __name__ == "__main__":
    main()
