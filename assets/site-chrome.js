
/**
 * NexSight 共用脚本：订阅浮层、复制链接、问 AI（壳层交互 + iframe 嵌入）。
 * DeepWiki-open：后端外置；可监听 CustomEvent nexsight-agent-submit。
 * 更新：实现真实的 API 调用。
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
    if (/^graph/i.test(path) || /graph/.test(path)) {
      return '当前视图：知识图谱探索页。可对齐 graph.json、节点摘要与所选节点 meta 作为 RAG（DeepWiki-open 范式）。';
    }
    return '';
  }

  /* ================= 问 AI 面板 ================= */
  var _nexsightChatSessionId = 'nex_' + Date.now();

  function getChips() {
    var c = window.__NEXSIGHT_CONFIG__ || {};
    if (c.suggestedPrompts && Array.isArray(c.suggestedPrompts)) return c.suggestedPrompts;
    return DEFAULT_PROMPTS_ZH;
  }

  function syncSourcesText() {
    var el = document.getElementById('nex-agent-sources-text');
    if (!el) return;
    el.textContent = getWikiContextParagraph() || '';
  }

  function renderChips() {
    var wrap = document.getElementById('nex-agent-chips');
    if (!wrap) return;
    wrap.innerHTML = '';
    getChips().forEach(function (txt) {
      var btn = document.createElement('button');
      btn.className = 'nex-agent-chip';
      btn.textContent = txt;
      btn.addEventListener('click', function () {
        var ta = document.getElementById('nex-agent-input');
        if (ta) {
          ta.value = txt;
          resizeComposerTA();
        }
        window.NexSightAgent.submitComposer(false);
      });
      wrap.appendChild(btn);
    });
  }

  function appendBubble(role, text, metaLine) {
    var thread = document.getElementById('nex-agent-thread');
    if (!thread) return;
    var msg = document.createElement('div');
    msg.className = 'nex-agent-message nex-agent-message--' + role;
    var b = document.createElement('div');
    b.className = 'nex-agent-bubble';
    b.textContent = text;
    msg.appendChild(b);
    if (metaLine) {
      var m = document.createElement('div');
      m.className = 'nex-agent-meta';
      m.textContent = metaLine;
      msg.appendChild(m);
    }
    thread.appendChild(msg);
    thread.scrollTop = thread.scrollHeight;
    syncAgentEmpty();
  }

  function showTyping() {
    var thread = document.getElementById('nex-agent-thread');
    if (!thread) return null;
    var msg = document.createElement('div');
    msg.className = 'nex-agent-message nex-agent-message--assistant nex-agent-typing';
    msg.id = 'typing-indicator';
    var b = document.createElement('div');
    b.className = 'nex-agent-bubble';
    b.textContent = '思考中...';
    msg.appendChild(b);
    thread.appendChild(msg);
    thread.scrollTop = thread.scrollHeight;
    return msg;
  }

  function removeTyping() {
    var el = document.getElementById('typing-indicator');
    if (el && el.parentNode) el.parentNode.removeChild(el);
  }

  function syncAgentEmpty() {
    var thread = document.getElementById('nex-agent-thread');
    if (!thread) return;
    var empty = document.getElementById('nex-agent-empty');
    if (!empty) return;
    if (thread.querySelectorAll('.nex-agent-message').length > 0) {
      empty.style.display = 'none';
    } else {
      empty.style.display = '';
    }
  }

  function resizeComposerTA() {
    var ta = document.getElementById('nex-agent-input');
    if (!ta) return;
    ta.style.height = 'auto';
    ta.style.height = Math.min(ta.scrollHeight, 120) + 'px';
  }

  function setMobileAgentTab(isOpen) {
    var t = document.getElementById('mobile-agent-tab');
    if (!t) return;
    if (isOpen) t.classList.add('mobile-tab-item--panel-open');
    else t.classList.remove('mobile-tab-item--panel-open');
  }

  function isMobileAgentEntryDisabled() {
    var t = document.getElementById('mobile-agent-tab');
    if (!t) return false;
    return t.classList.contains('mobile-tab-item--disabled') || t.getAttribute('aria-disabled') === 'true';
  }

  window.NexSightAgent = window.NexSightAgent || {};

  window.NexSightAgent.syncContextUi = function () {
    syncSourcesText();
  };

  window.NexSightAgent.clearThread = function () {
    var thread = document.getElementById('nex-agent-thread');
    if (!thread) return;
    thread.querySelectorAll('.nex-agent-message').forEach(function (n) { n.remove(); });
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
      ta.value = text;
      resizeComposerTA();
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
    
    var typing = showTyping();
    
    var apiBase = (window.__NEXSIGHT_CONFIG__.agentApiBase || '').trim();
    
    // 如果配置了 API Base，尝试真实调用
    if (apiBase) {
      // 超时控制：30秒
      var controller = new AbortController();
      var timeoutId = setTimeout(function() { controller.abort(); }, 30000);
      
      fetch(apiBase + '/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: raw,
          session_id: _nexsightChatSessionId,
          scene: 'simple'
        }),
        signal: controller.signal
      })
      .then(function(res) {
        clearTimeout(timeoutId);
        if (!res.ok) throw new Error('Network response was not ok (' + res.status + ')');
        return res.json();
      })
      .then(function(data) {
        removeTyping();
        appendBubble('assistant', data.answer, 'AI Radar');
      })
      .catch(function(err) {
        clearTimeout(timeoutId);
        removeTyping();
        var msg = err.name === 'AbortError' ? '请求超时，请稍后重试' : '请求失败：' + err.message;
        appendBubble('assistant', '⚠️ ' + msg);
      });
    } else {
      // 未配置 API Base 时显示提示
      removeTyping();
      appendBubble('assistant', '（演示模式）请在配置中设置 agentApiBase 以连接真实后端。');
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
    
    // 给 body 加类以调整布局
    document.body.classList.add('agent-panel-open');
    
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
    
    // 移除 body 类
    document.body.classList.remove('agent-panel-open');

    panel.classList.remove('nex-agent-panel--open');
    scrim.classList.remove('nex-agent-scrim--open');
    panel.setAttribute('aria-hidden', 'true');
    setMobileAgentTab(false);
    setTimeout(function () {
      scrim.hidden = true;
    }, 300);
  };

  function bindAgentEvents() {
    var fab = document.getElementById('nex-agent-fab');
    var closeBtn = document.getElementById('agent-panel-close');
    var scrim = document.getElementById('agent-scrim');
    var sendBtn = document.getElementById('nex-agent-send');
    var input = document.getElementById('nex-agent-input');
    var mobileTab = document.getElementById('mobile-agent-tab');

    if (fab) fab.addEventListener('click', function () { window.NexSightAgent.openPanel(); });
    if (closeBtn) closeBtn.addEventListener('click', window.NexSightAgent.closePanel);
    if (scrim) scrim.addEventListener('click', window.NexSightAgent.closePanel);

    if (sendBtn) sendBtn.addEventListener('click', function () {
      window.NexSightAgent.submitComposer(false);
    });

    if (input) {
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          window.NexSightAgent.submitComposer(true);
        }
      });
      input.addEventListener('input', resizeComposerTA);
    }

    // 手机端 Tab 入口
    if (mobileTab) {
      mobileTab.addEventListener('click', function () {
        if (!isMobileAgentEntryDisabled()) {
          window.NexSightAgent.openPanel();
        }
      });
    }

    document.addEventListener('click', function (ev) {
      var panel = document.getElementById('agent-panel');
      if (!panel || !panel.classList.contains('nex-agent-panel--open')) return;
      if (ev.target === scrim || ev.target === closeBtn || (closeBtn && closeBtn.contains(ev.target))) {
        window.NexSightAgent.closePanel();
      }
    });
    
    // ESC 关闭
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        var panel = document.getElementById('agent-panel');
        if (panel && panel.classList.contains('nex-agent-panel--open')) {
          window.NexSightAgent.closePanel();
        }
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindAgentEvents);
  } else {
    bindAgentEvents();
  }
})();
