/**
 * NexSight 共用脚本：订阅浮层、复制链接、问 AI（壳层交互 + iframe 嵌入）。
 * DeepWiki-open：后端外置；可监听 CustomEvent nexsight-agent-submit。
 */
(function () {
  if (typeof window.__NEXSIGHT_CONFIG__ === 'undefined') {
    window.__NEXSIGHT_CONFIG__ = {};
  }

  var cfg = window.__NEXSIGHT_CONFIG__;
  if (cfg.agentIframeUrl === undefined) cfg.agentIframeUrl = '';
  if (cfg.agentApiBase === undefined) cfg.agentApiBase = '';
  if (cfg.wikiContextHint === undefined) cfg.wikiContextHint = '';
  if (cfg.suggestedPrompts === undefined) cfg.suggestedPrompts = null;

  var DEFAULT_PROMPTS_ZH = [
    '这周雷达里最关键的范式变化是什么？',
    '把「今日简报」转成 3 条可执行跟进项',
    '解释当前选中节点与本仓库 graph.json 的关联（占位）'
  ];

  window.toggleSubscribePanel = function (ev) {
    if (ev) ev.stopPropagation();
    var p = document.getElementById('subscribe-panel');
    var btn = document.getElementById('header-subscribe-btn');
    if (!p || !btn) return;
    p.hidden = !p.hidden;
    var open = !p.hidden;
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.removeEventListener('click', window.closeSubscribePanelOnOutside, true);
    if (open) {
      setTimeout(function () {
        document.addEventListener('click', window.closeSubscribePanelOnOutside, true);
      }, 200);
    }
  };

  window.closeSubscribePanelOnOutside = function (ev) {
    var p = document.getElementById('subscribe-panel');
    var btn = document.getElementById('header-subscribe-btn');
    if (!p || p.hidden) return;
    if (btn && (ev.target === btn || btn.contains(ev.target))) return;
    if (p.contains(ev.target)) return;
    p.hidden = true;
    if (btn) btn.setAttribute('aria-expanded', 'false');
    document.removeEventListener('click', window.closeSubscribePanelOnOutside, true);
  };

  window.copyGraphPageLink = function () {
    var url = window.location.href.split('#')[0];
    var toast = document.getElementById('subscribe-toast');
    function show(msg) {
      if (!toast) return;
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(function () {
        toast.classList.remove('show');
      }, 2200);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () {
        show('链接已复制');
      }).catch(function () {
        show('请手动复制地址栏链接');
      });
    } else {
      try {
        var ta = document.createElement('textarea');
        ta.value = url;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        show('链接已复制');
      } catch (e) {
        show('请手动复制地址栏链接');
      }
    }
  };

  function toastMsg(text) {
    var toast = document.getElementById('subscribe-toast');
    if (!toast) return;
    toast.textContent = text;
    toast.classList.add('show');
    setTimeout(function () {
      toast.classList.remove('show');
    }, 2200);
  }

  function getWikiContextParagraph() {
    var c = window.__NEXSIGHT_CONFIG__ || {};
    if (c.wikiContextHint && String(c.wikiContextHint).trim())
      return String(c.wikiContextHint).trim();
    var path = '';
    try {
      path = window.location.pathname.split('/').pop() || '';
    } catch (e) {}
    if (/^index/i.test(path) || path === '' || path === 'index.html') {
      return '当前视图：今日简报页。可对齐简报 JSON、周报与 brief_snapshot.items 作为 RAG 片段。';
    }
    if (/graph/i.test(path)) {
      return '当前视图：知识图谱探索页。可对齐 graph.json、节点摘要与所选节点 meta 作为 RAG（DeepWiki-open 范式）。';
    }
    return 'Wiki / 图谱上下文可由部署层注入 __NEXSIGHT_CONFIG__.wikiContextHint（或后续接 MCP）。';
  }

  function suggestedList() {
    var c = window.__NEXSIGHT_CONFIG__ || {};
    if (Array.isArray(c.suggestedPrompts) && c.suggestedPrompts.length)
      return c.suggestedPrompts.map(function (s) {
        return String(s);
      });
    return DEFAULT_PROMPTS_ZH.slice();
  }

  function syncSourcesText() {
    var el = document.getElementById('nex-agent-sources-text');
    if (el) el.textContent = getWikiContextParagraph();
  }

  function syncAgentEmpty() {
    var thread = document.getElementById('nex-agent-thread');
    var empty = document.getElementById('nex-agent-empty');
    var chips = document.getElementById('nex-agent-chips');
    if (!thread || !empty) return;
    var populated = thread.querySelectorAll('.nex-agent-bubble-row').length > 0;
    empty.hidden = populated;
    if (chips) chips.hidden = populated;
    thread.classList.toggle('nex-agent-thread--idle', !populated);
  }

  function renderChips() {
    var chips = document.getElementById('nex-agent-chips');
    if (!chips) return;
    chips.innerHTML = '';
    suggestedList().forEach(function (text, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'nex-agent-chip';
      b.setAttribute('data-prompt-index', String(i));
      b.textContent = text;
      b.addEventListener('click', function () {
        window.NexSightAgent.applySuggestedPrompt(text);
      });
      chips.appendChild(b);
    });
  }

  function appendBubble(role, text, metaLine) {
    var thread = document.getElementById('nex-agent-thread');
    if (!thread) return;
    var row = document.createElement('div');
    row.className =
      'nex-agent-bubble-row ' + (role === 'user' ? 'nex-agent-bubble-row--user' : 'nex-agent-bubble-row--assistant');
    var bubble = document.createElement('div');
    bubble.className = 'nex-agent-bubble nex-agent-bubble--' + (role === 'user' ? 'user' : 'assistant');
    var textWrap = document.createElement('span');
    textWrap.textContent = text;
    bubble.appendChild(textWrap);
    if (metaLine && role !== 'user') {
      var meta = document.createElement('div');
      meta.className = 'nex-agent-bubble-meta';
      meta.textContent = metaLine;
      bubble.appendChild(meta);
    }
    row.appendChild(bubble);
    thread.appendChild(row);
    syncAgentEmpty();
    thread.scrollTop = thread.scrollHeight;
  }

  function resizeComposerTA() {
    var ta = document.getElementById('nex-agent-input');
    if (!ta) return;
    ta.style.height = 'auto';
    var max = 132;
    ta.style.height = Math.min(max, ta.scrollHeight) + 'px';
  }

  function isMobileAgentEntryDisabled() {
    var tab = document.getElementById('mobile-agent-tab');
    if (!tab || tab.getAttribute('aria-disabled') !== 'true') return false;
    try {
      if (window.matchMedia && window.matchMedia('(max-width: 900px)').matches) return true;
    } catch (e) {}
    return window.innerWidth <= 900;
  }

  function setMobileAgentTab(panelOpen) {
    var tab = document.getElementById('mobile-agent-tab');
    if (!tab) return;
    tab.classList.toggle('mobile-tab-item--panel-open', !!panelOpen);
    tab.setAttribute('aria-pressed', panelOpen ? 'true' : 'false');
  }

  window.NexSightAgent = window.NexSightAgent || {};

  window.NexSightAgent.syncContextUi = function () {
    syncSourcesText();
    renderChips();
    syncAgentEmpty();
  };

  window.NexSightAgent.clearThread = function () {
    var thread = document.getElementById('nex-agent-thread');
    if (thread) thread.innerHTML = '';
    syncAgentEmpty();
  };

  window.NexSightAgent.appendUserBubble = function (text) {
    appendBubble('user', text);
  };

  window.NexSightAgent.appendAssistantBubble = function (text, metaLine) {
    appendBubble('assistant', text, metaLine);
  };

  window.NexSightAgent.applySuggestedPrompt = function (text) {
    var ta = document.getElementById('nex-agent-input');
    if (ta) {
      ta.value = text || '';
      resizeComposerTA();
      ta.focus();
    }
    window.NexSightAgent.submitComposer(false);
  };

  window.NexSightAgent.submitComposer = function (fromKeyboard) {
    var ta = document.getElementById('nex-agent-input');
    if (!ta) return;
    var raw = ta.value.trim();
    if (!raw) return;
    ta.value = '';
    resizeComposerTA();
    appendBubble('user', raw);
    try {
      document.dispatchEvent(new CustomEvent('nexsight-agent-submit', { detail: { text: raw } }));
    } catch (e) {}

    var apiBase = (window.__NEXSIGHT_CONFIG__.agentApiBase || '').trim();
    if (!apiBase) {
      appendBubble(
        'assistant',
        '（演示占位）后端未连接。部署时可设置 agentIframeUrl 嵌入完整会话，或接 agentApiBase 流式应答。',
        fromKeyboard ? '' : ''
      );
    } else {
      appendBubble(
        'assistant',
        '已记下你的问题（演示）。请将 agentApiBase 接到你的 FastAPI／RAG，再在此脚本中替换占位应答逻辑。',
        'agentApiBase: ' + apiBase.replace(/(.{48}).*/, '$1…')
      );
    }
    ta.focus();
  };

  window.NexSightAgent.openPanel = function () {
    if (isMobileAgentEntryDisabled()) return;
    var panel = document.getElementById('agent-panel');
    var scrim = document.getElementById('agent-scrim');
    var frame = document.getElementById('nex-agent-frame');
    var wrap = document.getElementById('nex-agent-frame-wrap');
    var scaffold = document.getElementById('nex-agent-scaffold');
    if (!panel || !scrim) return;
    scrim.hidden = false;
    requestAnimationFrame(function () {
      scrim.classList.add('nex-agent-scrim--open');
      panel.classList.add('nex-agent-panel--open');
      panel.setAttribute('aria-hidden', 'false');
      setMobileAgentTab(true);
    });

    syncSourcesText();
    renderChips();
    syncAgentEmpty();

    var c = window.__NEXSIGHT_CONFIG__ || {};
    var u = (c.agentIframeUrl || '').trim();
    if (u && frame) {
      if (wrap) wrap.hidden = false;
      if (scaffold) scaffold.hidden = true;
      if (frame.src !== u) frame.src = u;
    } else {
      if (wrap) wrap.hidden = true;
      if (scaffold) scaffold.hidden = false;
      if (frame) frame.removeAttribute('src');
      setTimeout(function () {
        var input = document.getElementById('nex-agent-input');
        if (input && scaffold && !scaffold.hidden) {
          input.focus({ preventScroll: true });
          try {
            input.focus();
          } catch (e) {}
        }
      }, 320);
    }
  };

  window.NexSightAgent.closePanel = function () {
    var panel = document.getElementById('agent-panel');
    var scrim = document.getElementById('agent-scrim');
    if (!panel || !scrim) return;
    scrim.classList.remove('nex-agent-scrim--open');
    panel.classList.remove('nex-agent-panel--open');
    panel.setAttribute('aria-hidden', 'true');
    setMobileAgentTab(false);
    setTimeout(function () {
      scrim.hidden = true;
    }, 260);
  };

  window.toggleAgentPanel = function () {
    var panel = document.getElementById('agent-panel');
    if (!panel) return;
    if (panel.classList.contains('nex-agent-panel--open')) {
      window.NexSightAgent.closePanel();
    } else {
      window.NexSightAgent.openPanel();
    }
  };

  window.NexSightChrome = window.NexSightChrome || {};
  window.NexSightChrome.toast = toastMsg;

  window.NexSightChrome.syncHeaderHeight = function () {
    var el = document.getElementById('header');
    if (!el || !el.classList.contains('site-chrome-header')) return;
    var minH =
      parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--side-sheet-header-min')) || 64;
    var h = Math.max(minH, Math.ceil(el.getBoundingClientRect().height));
    document.documentElement.style.setProperty('--header-h', h + 'px');
  };

  var resizeHeaderTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeHeaderTimer);
    resizeHeaderTimer = setTimeout(function () {
      window.NexSightChrome.syncHeaderHeight();
    }, 120);
  });

  document.addEventListener('DOMContentLoaded', function () {
    window.NexSightChrome.syncHeaderHeight();
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () {
        window.NexSightChrome.syncHeaderHeight();
        requestAnimationFrame(window.NexSightChrome.syncHeaderHeight);
      });
    }

    var fab = document.getElementById('nex-agent-fab');
    if (fab) {
      fab.addEventListener('click', function () {
        window.toggleAgentPanel();
      });
    }
    var scrim = document.getElementById('agent-scrim');
    if (scrim) {
      scrim.addEventListener('click', function () {
        window.NexSightAgent.closePanel();
      });
    }
    var closeBtn = document.getElementById('agent-panel-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        window.NexSightAgent.closePanel();
      });
    }

    var send = document.getElementById('nex-agent-send');
    var composer = document.getElementById('nex-agent-input');
    if (send && composer) {
      send.addEventListener('click', function () {
        window.NexSightAgent.submitComposer(false);
      });
      composer.addEventListener('input', resizeComposerTA);
      composer.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter' && !ev.shiftKey) {
          ev.preventDefault();
          window.NexSightAgent.submitComposer(true);
        }
      });
    }

    syncSourcesText();
    renderChips();
    syncAgentEmpty();

    window.NexSightChrome.syncHeaderHeight();
  });

  document.addEventListener(
    'keydown',
    function (ev) {
      if (ev.key !== 'Escape' || ev.defaultPrevented) return;
      var panel = document.getElementById('agent-panel');
      if (panel && panel.classList.contains('nex-agent-panel--open')) {
        ev.preventDefault();
        ev.stopPropagation();
        window.NexSightAgent.closePanel();
      }
    },
    true
  );
})();
