# -*- coding: utf-8 -*-
"""UTF-8–safe one-shot: merge NexSight chrome into graph_template.html (no editor mojibake)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "graph_template.html"

OLD_HEAD = """  <!-- Header -->
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
      <div class="subscribe-wrap">"""

NEW_HEAD = """  <!-- Header -->
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
      <button type="button" class="header-btn header-agent-btn" onclick="window.toggleAgentPanel()" aria-label="问 AI">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        问 AI
      </button>
      <div class="subscribe-wrap">"""

MOBILE_INSERT_MARK = """    </div>
  </div>

  <!-- Dashboard (Left) -->
"""

MOBILE_BLOCK = """    </div>
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
    <button type="button" class="mobile-tab-item" id="mobile-agent-tab" onclick="window.toggleAgentPanel()">
      <svg class="mobile-tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
      <span class="mobile-tab-label">问 AI</span>
    </button>
  </nav>

  <!-- Dashboard (Left) -->
"""

OLD_LIBS = """  <!-- Data & Libs -->
  <script id="graph-data" type="application/json">{{DATA}}</script>
  <script src="./assets/vis-network.min.js"></script>
  <script>
"""

AGENT_BLOCK = """  <div id="agent-scrim" class="nex-agent-scrim" hidden aria-hidden="true"></div>
  <div id="agent-panel" class="nex-agent-panel" role="dialog" aria-labelledby="agent-panel-title" aria-modal="true" aria-hidden="true">
    <div class="nex-agent-panel-head">
      <h2 id="agent-panel-title">智瞰问答</h2>
      <button type="button" class="nex-agent-panel-close" id="agent-panel-close" aria-label="关闭">✕</button>
    </div>
    <div class="nex-agent-panel-body">
      <div id="nex-agent-frame-wrap" class="nex-agent-frame-wrap" hidden>
        <iframe id="nex-agent-frame" class="nex-agent-frame" title="智瞰问答"></iframe>
      </div>
      <div id="nex-agent-scaffold" class="nex-agent-scaffold">
        <div class="nex-agent-sources-strip">
          <span class="nex-agent-sources-label">来源 / 上下文</span>
          <p class="nex-agent-sources-text" id="nex-agent-sources-text"></p>
        </div>
        <div class="nex-agent-mid">
          <div id="nex-agent-thread" class="nex-agent-thread nex-agent-thread--idle" role="log" aria-live="polite" aria-relevant="additions" aria-label="对话">
            <div class="nex-agent-empty" id="nex-agent-empty">
              <p class="nex-agent-empty-title">向智瞰提问</p>
              <p class="nex-agent-empty-desc">用自然语言浏览简报与图谱。composer 对齐常见对话 App；应答可来自自托管后端或嵌入 iframe。</p>
            </div>
          </div>
          <div id="nex-agent-chips" class="nex-agent-chips" aria-label="建议问题"></div>
        </div>
        <footer class="nex-agent-composer-wrap">
          <label for="nex-agent-input" class="nex-sr-only">输入问题</label>
          <textarea id="nex-agent-input" class="nex-agent-input" rows="1" placeholder="问问今日情报…" autocomplete="off"></textarea>
          <button type="button" class="nex-agent-send" id="nex-agent-send" aria-label="发送">↑</button>
        </footer>
        <p class="nex-agent-footnote" id="agent-placeholder-msg">
          对标 <a href="https://github.com/AsyncFuncAI/deepwiki-open" target="_blank" rel="noopener">DeepWiki-open</a>：在部署层自托管问答后端（FastAPI / RAG），把可嵌入对话页写入 <code>window.__NEXSIGHT_CONFIG__.agentIframeUrl</code>；亦可监听 <code>nexsight-agent-submit</code> 事件。<strong>密钥请勿写入仓库</strong>。
        </p>
      </div>
    </div>
  </div>
  <button type="button" id="nex-agent-fab" class="nex-agent-fab" aria-controls="agent-panel">问 AI</button>

  <!-- Data & Libs -->
  <script id="graph-data" type="application/json">{{DATA}}</script>
  <script src="./assets/vis-network.min.js"></script>
  <script src="./assets/site-chrome.js"></script>
  <script>
"""

HEAD_NEEDLE = '<link rel="apple-touch-icon" href="./assets/nexsight-mark.svg">\n<style>'
HEAD_REPL = '''<link rel="apple-touch-icon" href="./assets/nexsight-mark.svg">
<link rel="stylesheet" href="./assets/site-chrome.css">
<meta name="view-transition" content="same-origin">
<script>
  window.__NEXSIGHT_CONFIG__ = window.__NEXSIGHT_CONFIG__ || { agentIframeUrl: '', agentApiBase: '' };
</script>
<style>'''


def inject_head_assets(s: str) -> str:
    if 'href="./assets/site-chrome.css"' in s:
        return s
    if HEAD_NEEDLE not in s:
        raise SystemExit("inject_head: apple-touch-icon + <style> needle not found")
    return s.replace(HEAD_NEEDLE, HEAD_REPL, 1)


def inject_brand_scroll_desktop(s: str) -> str:
    needle = """  .header-brand-scroll {
    flex: 1 1 auto;
    min-width: 0;
    display: flex;
    align-items: center;
    overflow: visible;
  }
  #header h1 .header-brand-block {"""
    if needle not in s:
        raise SystemExit("brand-scroll: expected block not found")
    repl = """  .header-brand-scroll {
    flex: 1 1 auto;
    min-width: 0;
    display: flex;
    align-items: center;
    overflow: visible;
  }
  @media (min-width: 901px) {
    .header-brand-scroll {
      flex-wrap: nowrap;
    }
    #header.site-chrome-header .header-brand-scroll > h1 {
      flex: 1 1 auto;
      min-width: 0;
    }
  }
  #header h1 .header-brand-block {"""
    return s.replace(needle, repl, 1)


def main() -> None:
    s = TPL.read_text(encoding="utf-8").replace("\r\n", "\n").strip("\ufeff")
    s = inject_head_assets(s)
    if OLD_HEAD not in s:
        raise SystemExit("header: OLD_HEAD not found — graph_template structure changed")
    s = s.replace(OLD_HEAD, NEW_HEAD, 1)
    if '<nav class="mobile-tab-bar"' not in s:
        if MOBILE_INSERT_MARK not in s:
            raise SystemExit("mobile: insertion marker not found")
        s = s.replace(MOBILE_INSERT_MARK, MOBILE_BLOCK, 1)
    if 'src="./assets/site-chrome.js"' not in s:
        if OLD_LIBS not in s:
            raise SystemExit("libs: OLD_LIBS not found")
        s = s.replace(OLD_LIBS, AGENT_BLOCK, 1)
    s = inject_brand_scroll_desktop(s)
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
        s = s.replace(old_sync, new_sync, 1)
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
        s = s.replace(old_stat, new_stat, 1)
    TPL.write_text(s, encoding="utf-8", newline="\n")
    print("OK wrote", TPL)


if __name__ == "__main__":
    main()
