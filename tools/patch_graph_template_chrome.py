# -*- coding: utf-8 -*-
"""One-off-safe UTF-8 patches for graph_template.html chrome (avoid editor encoding pitfalls).

Reads/writes use encoding=utf-8 only. For Windows default-encoding pitfalls and PowerShell,
see tools/README_GRAPH_UTF8.md."""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "graph.html"
TPL = ROOT / "graph_template.html"
INDEX = ROOT / "index.html"

sys.path.insert(0, str(ROOT / "tools"))
from nex_agent_panel_markup import (  # noqa: E402
    SITE_CHROME_ASSET_VER,
    graph_agent_with_toast_block,
    graph_data_libs_scripts_block,
    upgrade_agent_panel_markup,
)


def bump_site_chrome_asset_versions(s: str) -> str:
    return re.sub(
        r"(site-chrome\.(?:css|js))\?v=\d+",
        rf"\1?v={SITE_CHROME_ASSET_VER}",
        s,
    )


def upgrade_agent_in_html_files(paths: list[Path]) -> None:
    for path in paths:
        if not path.is_file():
            print("skip (missing):", path)
            continue
        blob = path.read_text(encoding="utf-8").replace("\r\n", "\n").strip("\ufeff")
        upgraded, changed = upgrade_agent_panel_markup(blob)
        upgraded = bump_site_chrome_asset_versions(upgraded)
        if changed or upgraded != blob:
            path.write_text(upgraded, encoding="utf-8", newline="\n")
            print("OK upgraded agent chrome:", path)
        else:
            print("unchanged:", path)


def regenerate_template_from_graph_html() -> None:
    html = GRAPH.read_text(encoding="utf-8").replace("\r\n", "\n")
    pat = re.compile(
        r'<script\s+id="graph-data"\s+type="application/json"\s*>.*?</script>',
        re.DOTALL,
    )
    if not pat.search(html):
        raise SystemExit("regenerate: graph.html missing <script id=\"graph-data\"> JSON block")
    out = pat.sub('<script id="graph-data" type="application/json">{{DATA}}</script>', html, count=1)
    TPL.write_text(out, encoding="utf-8", newline="\n")


def inject_head_assets(s: str) -> str:
    if './assets/site-chrome.css' not in s:
        needle = '<link rel="apple-touch-icon" href="./assets/nexsight-mark.svg">\n<style>'
        if needle not in s:
            raise SystemExit("patch: expected apple-touch-icon line before embedded <style>")
        s = s.replace(
            needle,
            '''<link rel="apple-touch-icon" href="./assets/nexsight-mark.svg">
<link rel="stylesheet" href="./assets/site-chrome.css?v=12">
<meta name="view-transition" content="same-origin">
<script>
  window.__NEXSIGHT_CONFIG__ = window.__NEXSIGHT_CONFIG__ || { agentIframeUrl: '', agentApiBase: '' };
</script>
<style>''',
            1,
        )
    elif 'name="view-transition"' not in s:
        s = s.replace(
            '<meta name="theme-color" content="#ff385c">',
            '<meta name="theme-color" content="#ff385c">\n<meta name="view-transition" content="same-origin">',
            1,
        )
    return s


def strip_header_brief_styles(s: str) -> str:
    s = re.sub(
        r"\n  \.header-brief-btn \{[^}]*\}\n  \.header-brief-btn:hover \{[^}]*\}\n",
        "\n",
        s,
        count=1,
    )
    s = re.sub(
        r"\n    \.header-brief-btn \{ display: none !important; \}\n",
        "\n",
        s,
        count=1,
    )
    return s


def apply_chrome_patches_to_template_string(s: str) -> str:
    old_hdr = """<body>

  <div id="panel-scrim" role="presentation" aria-hidden="true" onclick="hidePanel()"></div>

  <!-- Header -->
  <div id="header">
    <div class="header-brand-scroll">
    <h1>
      <span class="header-brand-block">
        <img class="brand-mark" src="./assets/nexsight-mark.svg" width="30" height="30" alt="" decoding="async" aria-hidden="true" />
        <span class="header-text-stack">
          <span class="header-title-text">智瞰 NexSight</span>
          <span class="header-sub">面向产品经理的AI全景情报</span>
        </span>
      </span>
    </h1>
    </div>
    <div id="header-controls">
      <button type="button" id="header-brief-btn" class="header-brief-btn" onclick="toggleDashboard()" aria-controls="dashboard" aria-expanded="true">摘要</button>
      <div class="subscribe-wrap">"""

    new_hdr = """<body>

  <div id="panel-scrim" role="presentation" aria-hidden="true" onclick="hidePanel()"></div>

  <!-- Header -->
  <div id="header" class="site-chrome-header">
    <div class="header-brand-scroll">
      <h1>
        <a href="./index.html" class="header-brand-block">
          <img class="brand-mark" src="./assets/nexsight-mark.svg" width="30" height="30" alt="" decoding="async" aria-hidden="true" />
          <span class="header-text-stack">
            <span class="header-title-text">智瞰 NexSight</span>
            <span class="header-sub">面向产品经理的AI全景情报</span>
          </span>
        </a>
      </h1>
      <nav class="site-nav" aria-label="主导航">
        <span class="site-nav-thumb" aria-hidden="true"></span>
        <a href="./index.html" class="site-nav-link">简报</a>
        <a href="./graph.html" class="site-nav-link site-nav-link--active" aria-current="page">探索</a>
      </nav>
    </div>
    <div id="header-controls">
      <button type="button" class="header-btn header-agent-btn" onclick="window.toggleAgentPanel()" aria-label="问 AI" aria-expanded="false" aria-haspopup="dialog" aria-controls="agent-panel">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;flex-shrink:0" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        <span class="header-agent-label">问&nbsp;AI</span>
      </button>
      <button type="button" id="header-brief-btn" class="header-btn header-brief-btn" onclick="toggleDashboard()" aria-controls="dashboard" aria-expanded="true">摘要</button>
      <div class="subscribe-wrap">"""

    if "class=\"site-chrome-header\"" not in s:
        if old_hdr not in s:
            raise SystemExit("patch: header block not found — graph_template out of sync")
        s = s.replace(old_hdr, new_hdr)

    marker = """    </div>
  </div>

  <!-- Dashboard (Left) -->
"""
    mobile = """    </div>
  </div>

  <nav class="mobile-tab-bar" aria-label="主导航">
    <a href="./index.html" class="mobile-tab-item">
      <svg class="mobile-tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
      <span class="mobile-tab-label">简报</span>
    </a>
    <a href="./graph.html" class="mobile-tab-item mobile-tab-item--active" aria-current="page">
      <svg class="mobile-tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
      <span class="mobile-tab-label">探索</span>
    </a>
    <button type="button" class="mobile-tab-item" id="mobile-agent-tab">
      <svg class="mobile-tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
      <span class="mobile-tab-label">问 AI</span>
    </button>
  </nav>

  <!-- Dashboard (Left) -->
"""
    # Match actual markup only (CSS comments mention .mobile-tab-bar and must not skip insertion).
    if '<nav class="mobile-tab-bar"' not in s:
        if marker not in s:
            raise SystemExit("patch: mobile-tab insertion point missing")
        s = s.replace(marker, mobile, 1)

    old_libs = """  <!-- Data & Libs -->
  <script id="graph-data" type="application/json">{{DATA}}</script>
  <script src="./assets/vis-network.min.js"></script>
  <script>
"""
    agent_block = graph_agent_with_toast_block() + graph_data_libs_scripts_block()
    if 'assets/site-chrome.js' not in s:
        if old_libs not in s:
            raise SystemExit("patch: Data & Libs block not found")
        s = s.replace(old_libs, agent_block)

    old_sync = """    function syncHeaderHeight() {
      const el = document.getElementById('header');
      if (!el) return;
      const minH = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--side-sheet-header-min')) || 64;
      const h = Math.max(minH, Math.ceil(el.getBoundingClientRect().height));
      document.documentElement.style.setProperty('--header-h', h + 'px');
    }"""
    new_sync = """    function syncHeaderHeight() {
      if (window.NexSightChrome && typeof window.NexSightChrome.syncHeaderHeight === 'function') {
        window.NexSightChrome.syncHeaderHeight();
        return;
      }
      const el = document.getElementById('header');
      if (!el) return;
      const minH = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--side-sheet-header-min')) || 64;
      const h = Math.max(minH, Math.ceil(el.getBoundingClientRect().height));
      document.documentElement.style.setProperty('--header-h', h + 'px');
    }"""
    if old_sync in s:
        s = s.replace(old_sync, new_sync)

    old_stat = """      if (nodeHud) nodeHud.textContent = nodeLabel;
      if (edgeHud) edgeHud.textContent = edgeLabel;
      // 更新概念计数（如果有这个元素）"""
    new_stat = """      if (nodeHud) nodeHud.textContent = nodeLabel;
      if (edgeHud) edgeHud.textContent = edgeLabel;
      if (window.NexSightChrome && window.NexSightChrome.syncHeaderHeight) {
        requestAnimationFrame(function () {
          window.NexSightChrome.syncHeaderHeight();
        });
      }
      // 更新概念计数（如果有这个元素）"""
    if old_stat in s:
        s = s.replace(old_stat, new_stat)

    old_mob = """    function applyMobileBriefDefaultLayout() {
      if (!window.matchMedia('(max-width: 900px)').matches) return;
      var dash = document.getElementById('dashboard');
      var legend = document.getElementById('legend');
      var expandBtn = document.getElementById('dashboard-expand-btn');
      var briefBtn = document.getElementById('header-brief-btn');
      if (!dash) return;
      dash.classList.remove('hidden');
      dash.style.transform = '';
      legend.classList.remove('shifted');
      if (expandBtn) expandBtn.classList.remove('show');
      if (briefBtn) briefBtn.setAttribute('aria-expanded', 'true');
    }"""
    new_mob = """    function applyMobileBriefDefaultLayout() {
      if (!window.matchMedia('(max-width: 900px)').matches) return;
      var dash = document.getElementById('dashboard');
      var legend = document.getElementById('legend');
      var expandBtn = document.getElementById('dashboard-expand-btn');
      if (!dash) return;
      dash.classList.remove('hidden');
      dash.style.transform = '';
      legend.classList.remove('shifted');
      if (expandBtn) expandBtn.classList.remove('show');
    }"""
    if old_mob in s:
        s = s.replace(old_mob, new_mob)

    if "\n    function toggleSubscribePanel(ev)" in s:
        s2, sub_n = re.subn(
            r"\n    function toggleSubscribePanel\(ev\) \{.*?\n    // ===== 5\. TOGGLE DASHBOARD =====",
            "\n    // ===== 5. TOGGLE DASHBOARD =====",
            s,
            count=1,
            flags=re.DOTALL,
        )
        if sub_n != 1:
            raise SystemExit("patch: subscribe duplicate block not matched by regex")
        s = s2

    old_td = '''    function toggleDashboard() {
      const dash = document.getElementById('dashboard');
      const legend = document.getElementById('legend');
      const expandBtn = document.getElementById('dashboard-expand-btn');
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
      }
      syncHeaderHeight();
    }'''
    new_td = '''    function toggleDashboard() {
      const dash = document.getElementById('dashboard');
      const legend = document.getElementById('legend');
      const expandBtn = document.getElementById('dashboard-expand-btn');
      const isHidden = dash.classList.contains('hidden');

      if (isHidden) {
        dash.classList.remove('hidden');
        dash.style.transform = '';
        legend.classList.remove('shifted');
        if (expandBtn) expandBtn.classList.remove('show');
      } else {
        dash.classList.add('hidden');
        dash.style.transform = '';
        legend.classList.add('shifted');
        if (expandBtn) expandBtn.classList.add('show');
      }
      syncHeaderHeight();
    }'''
    if old_td in s:
        s = s.replace(old_td, new_td)

    old_esc = """          document.removeEventListener('click', closeSubscribePanelOnOutside, true);"""
    new_esc = """          if (typeof window.closeSubscribePanelOnOutside === 'function') {
            document.removeEventListener('click', window.closeSubscribePanelOnOutside, true);
          }"""
    if old_esc in s:
        s = s.replace(old_esc, new_esc)

    # Keep exactly one toast host for site-chrome.js (do not strip the block inserted above).
    if 'id="subscribe-toast"' not in s:
        marker = "  <!-- Data & Libs -->\n"
        ins = (
            '  <div id="subscribe-toast" role="status" aria-live="polite"></div>\n\n'
            + marker
        )
        if marker not in s:
            raise SystemExit("patch: missing <!-- Data & Libs --> for subscribe-toast insert")
        s = s.replace(marker, ins, 1)

    s, _ = upgrade_agent_panel_markup(s)
    s = patch_detail_panel_close(s)
    return s


def patch_detail_panel_close(s: str) -> str:
    """统一节点详情右上角关闭按钮与情报摘要 headline 收起钮（dash-close-btn--icon）。"""
    old_cs = """  .panel-header { padding: 22px 22px 18px; border-bottom: 1px solid var(--hairline-soft); position: relative; }
  .panel-close {
    position: absolute; top: 14px; right: 14px;
    background: var(--surface-soft);
    border: 1px solid var(--hairline);
    color: var(--muted);
    width: 40px; height: 40px;
    border-radius: var(--radius-full);
    cursor: pointer;
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.15s, color 0.15s;
  }
  .panel-close:hover { background: var(--surface-strong); color: var(--ink); }"""
    new_cs = """  .panel-header { padding: 22px 22px 18px; border-bottom: 1px solid var(--hairline-soft); position: relative; }
  /* 与 headline 收起钮共用 .dash-close-btn--icon；保留 .panel-close 供 querySelector */
  #detail-panel .panel-header > .panel-close.dash-close-btn--icon {
    position: absolute;
    top: 14px;
    right: 14px;
    z-index: 1;
  }"""
    if old_cs in s:
        s = s.replace(old_cs, new_cs)
    legacy_cs = """  .panel-header { padding: 22px 22px 18px; border-bottom: 1px solid var(--hairline-soft); position: relative; }
  #detail-panel .panel-header > .dash-close-btn--icon {
    position: absolute;
    top: 14px;
    right: 14px;
    z-index: 1;
  }"""
    if legacy_cs in s:
        s = s.replace(legacy_cs, new_cs)

    mob_old = """    .panel-close {
      width: 40px;
      height: 40px;
      top: 12px;
      right: 12px;
    }
"""
    mob_new = """    #detail-panel .panel-header > .panel-close.dash-close-btn--icon {
      top: 12px;
      right: 12px;
    }
"""
    if mob_old in s:
        s = s.replace(mob_old, mob_new)
    legacy_mob = """    #detail-panel .panel-header > .dash-close-btn--icon {
      top: 12px;
      right: 12px;
    }
"""
    if legacy_mob in s:
        s = s.replace(legacy_mob, mob_new)

    s = s.replace(
        """    .dash-close-btn--icon,
    .panel-close,
""",
        """    .dash-close-btn--icon,
""",
    )

    btn_old = (
        '      <button type="button" class="panel-close" onclick="hidePanel()" aria-label="\u5173\u95ed\u8282\u70b9\u8be6\u60c5">\u2715</button>'
    )
    btn_new = (
        '      <button type="button" class="panel-close dash-close-btn dash-close-btn--icon" '
        'onclick="hidePanel()" aria-label="\u5173\u95ed\u8282\u70b9\u8be6\u60c5" title="\u6536\u8d77">\xd7</button>'
    )
    if btn_old in s:
        s = s.replace(btn_old, btn_new)
    btn_legacy_icon = (
        '      <button type="button" class="dash-close-btn dash-close-btn--icon" '
        'onclick="hidePanel()" aria-label="\u5173\u95ed\u8282\u70b9\u8be6\u60c5" title="\u6536\u8d77">\xd7</button>'
    )
    if btn_legacy_icon in s:
        s = s.replace(btn_legacy_icon, btn_new)
    return s


def main() -> None:
    ap = argparse.ArgumentParser(description="Merge NexSight chrome into graph_template.html (UTF-8 safe).")
    ap.add_argument(
        "--regenerate-from-graph-html",
        action="store_true",
        help="Overwrite graph_template.html from graph.html, replacing inlined JSON with {{DATA}}.",
    )
    ap.add_argument(
        "--ensure-regex",
        action="store_true",
        help="After patching, run tools/ensure_graph_js_regexes.py (hardened parseWeeklySummaryText).",
    )
    ap.add_argument(
        "--upgrade-agent",
        action="store_true",
        help="Replace legacy Ask-AI panel markup in graph.html, graph_template.html, and index.html.",
    )
    args = ap.parse_args()
    if args.regenerate_from_graph_html:
        regenerate_template_from_graph_html()

    if args.upgrade_agent:
        upgrade_agent_in_html_files([GRAPH, TPL, INDEX])
        return

    blob = TPL.read_text(encoding="utf-8").replace("\r\n", "\n").strip("\ufeff")
    blob = inject_head_assets(blob)
    blob = apply_chrome_patches_to_template_string(blob)
    blob = strip_header_brief_styles(blob)
    blob = bump_site_chrome_asset_versions(blob)
    TPL.write_text(blob, encoding="utf-8", newline="\n")
    print("OK patched", TPL)

    if args.ensure_regex:
        import subprocess
        import sys

        script = ROOT / "tools" / "ensure_graph_js_regexes.py"
        subprocess.run([sys.executable, str(script)], cwd=str(ROOT), check=True)


if __name__ == "__main__":
    main()
