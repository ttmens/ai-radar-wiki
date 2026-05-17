/**
 * NexSight 共用脚本：顶栏订阅、复制链接、「问 AI」侧栏与会话前端。
 */

(function () {
  if (typeof window.__NEXSIGHT_CONFIG__ === 'undefined') {
    window.__NEXSIGHT_CONFIG__ = {};
  }

  var cfg = window.__NEXSIGHT_CONFIG__;
  if (cfg.agentIframeUrl === undefined) cfg.agentIframeUrl = '';
  if (cfg.agentApiBase === undefined) cfg.agentApiBase = '';
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

  /* ================= 问 AI 面板 ================= */

  /** 移除旧版来源条 / DeepWiki 脚注；补齐 composer-inner 结构 */
  function pruneLegacyAgentChrome() {
    var scaffold = document.getElementById('nex-agent-scaffold');
    if (!scaffold) return;
    scaffold.querySelectorAll(
      '.nex-agent-sources-strip, .nex-agent-footnote, #agent-placeholder-msg'
    ).forEach(function (el) {
      el.remove();
    });
    var composerWrap = scaffold.querySelector('.nex-agent-composer-wrap');
    if (composerWrap && !composerWrap.querySelector('.nex-agent-composer-inner')) {
      var inner = document.createElement('div');
      inner.className = 'nex-agent-composer-inner';
      while (composerWrap.firstChild) {
        inner.appendChild(composerWrap.firstChild);
      }
      composerWrap.appendChild(inner);
    }
  }

  // [P1-3] 会话 ID 持久化
  var _nexsightChatSessionId = localStorage.getItem('nexsight_session_id');
  if (!_nexsightChatSessionId) {
    _nexsightChatSessionId = 'nex_' + Date.now();
    localStorage.setItem('nexsight_session_id', _nexsightChatSessionId);
  }

  // [P1-4] 场景模式（快速 / 深度）
  var _currentScene = 'simple';

  // [P0-2] 防重复发送 + 停止控制
  var _nexsightIsStreaming = false;
  var _abortController = null;

  // [P3-10] chips 已渲染标记
  var _chipsRendered = false;

  function getChips() {
    var c = window.__NEXSIGHT_CONFIG__ || {};
    if (c.suggestedPrompts && Array.isArray(c.suggestedPrompts)) return c.suggestedPrompts;
    return DEFAULT_PROMPTS_ZH;
  }

  function renderChips() {
    if (_chipsRendered) return;
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
    _chipsRendered = true;
  }

  // 用户开始对话后隐藏 chips
  function hideChips() {
    var wrap = document.getElementById('nex-agent-chips');
    if (wrap) wrap.style.display = 'none';
  }

  function appendBubble(role, text, metaLine, isHtml, hideFeedback) {
    var thread = document.getElementById('nex-agent-thread');
    if (!thread) return;
    var msg = document.createElement('div');
    msg.className = 'nex-agent-message nex-agent-message--' + role;
    var b = document.createElement('div');
    b.className = 'nex-agent-bubble';
    if (isHtml) {
      b.innerHTML = text;
    } else {
      b.innerHTML = renderMarkdown(escapeHtmlForInner(text).replace(/\n/g, '<br>'));
    }
    msg.appendChild(b);
    if (metaLine) {
      var m = document.createElement('div');
      m.className = 'nex-agent-meta';
      m.textContent = metaLine;
      msg.appendChild(m);
    }
    // 反馈按钮 — 仅 AI 最终回复时显示
    if (role === 'assistant' && !hideFeedback) {
      var fb = document.createElement('div');
      fb.className = 'nex-agent-feedback';
      fb.innerHTML = '<button type="button" class="nex-agent-feedback-btn" data-fb="up" title="有帮助">\ud83d\udc4d</button>' +
                     '<button type="button" class="nex-agent-feedback-btn" data-fb="down" title="需改进">\ud83d\udc4e</button>';
      msg.appendChild(fb);
      fb.addEventListener('click', function (e) {
        var btn = e.target.closest('.nex-agent-feedback-btn');
        if (!btn) return;
        var type = btn.getAttribute('data-fb');
        var form = msg.querySelector('.nex-agent-feedback-form');
        if (type === 'up') {
          fb.innerHTML = '<span class="nex-agent-feedback-done">\u2705 \u5df2\u8bb0\u5f55</span>';
        } else if (type === 'down') {
          if (form) {
            form.hidden = !form.hidden;
          } else {
            var f = document.createElement('div');
            f.className = 'nex-agent-feedback-form';
            f.innerHTML = '<button type="button" data-r="inaccurate">\u4e0d\u51c6\u786e</button>' +
                          '<button type="button" data-r="incomplete">\u4e0d\u5b8c\u6574</button>' +
                          '<button type="button" data-r="irrelevant">\u4e0d\u76f8\u5173</button>';
            msg.appendChild(f);
            f.addEventListener('click', function (e2) {
              var rbtn = e2.target.closest('button');
              if (!rbtn) return;
              var reason = rbtn.getAttribute('data-r');
              fb.innerHTML = '<span class="nex-agent-feedback-done">\u2705 \u5df2\u8bb0\u5f55\uff1a' + rbtn.textContent + '</span>';
              f.remove();
            });
          }
        }
      });
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

  function removeLastBubble() {
    var thread = document.getElementById('nex-agent-thread');
    if (!thread) return;
    var messages = thread.querySelectorAll('.nex-agent-message');
    if (messages.length > 0) {
      var last = messages[messages.length - 1];
      last.parentNode.removeChild(last);
    }
  }

  function updateLastBubble(text, isHtml) {
    var thread = document.getElementById('nex-agent-thread');
    if (!thread) return;
    var messages = thread.querySelectorAll('.nex-agent-message');
    if (messages.length === 0) return;
    var last = messages[messages.length - 1];
    var bubble = last.querySelector('.nex-agent-bubble');
    if (bubble) {
      if (isHtml) {
        bubble.innerHTML = text;
      } else {
        bubble.innerHTML = renderMarkdown(escapeHtmlForInner(text).replace(/\n/g, '<br>'));
      }
    }
  }

  // 在最后一条 AI 消息上追加反馈按钮（流式完成后调用）
  function appendFeedbackToLast() {
    var thread = document.getElementById('nex-agent-thread');
    if (!thread) return;
    var messages = thread.querySelectorAll('.nex-agent-message');
    if (messages.length === 0) return;
    var last = messages[messages.length - 1];
    if (last.querySelector('.nex-agent-feedback')) return;
    var fb = document.createElement('div');
    fb.className = 'nex-agent-feedback';
    fb.innerHTML = '<button type="button" class="nex-agent-feedback-btn" data-fb="up" title="有帮助">\ud83d\udc4d</button>' +
                   '<button type="button" class="nex-agent-feedback-btn" data-fb="down" title="需改进">\ud83d\udc4e</button>';
    last.appendChild(fb);
    fb.addEventListener('click', function (e) {
      var btn = e.target.closest('.nex-agent-feedback-btn');
      if (!btn) return;
      var type = btn.getAttribute('data-fb');
      var form = last.querySelector('.nex-agent-feedback-form');
      if (type === 'up') {
        fb.innerHTML = '<span class="nex-agent-feedback-done">\u2705 \u5df2\u8bb0\u5f55</span>';
      } else if (type === 'down') {
        if (form) {
          form.hidden = !form.hidden;
        } else {
          var f = document.createElement('div');
          f.className = 'nex-agent-feedback-form';
          f.innerHTML = '<button type="button" data-r="inaccurate">\u4e0d\u51c6\u786e</button>' +
                        '<button type="button" data-r="incomplete">\u4e0d\u5b8c\u6574</button>' +
                        '<button type="button" data-r="irrelevant">\u4e0d\u76f8\u5173</button>';
          last.appendChild(f);
          f.addEventListener('click', function (e2) {
            var rbtn = e2.target.closest('button');
            if (!rbtn) return;
            fb.innerHTML = '<span class="nex-agent-feedback-done">\u2705 \u5df2\u8bb0\u5f55\uff1a' + rbtn.textContent + '</span>';
            f.remove();
          });
        }
      }
    });
  }

  function scrollToBottom() {
    var thread = document.getElementById('nex-agent-thread');
    if (thread) {
      thread.scrollTop = thread.scrollHeight;
    }
  }

  function escapeHtmlForInner(t) {
    if (t == null) return '';
    var d = document.createElement('div');
    d.textContent = String(t);
    return d.innerHTML;
  }

  function syncAgentEmpty() {
    var thread = document.getElementById('nex-agent-thread');
    if (!thread) return;
    var empty = document.getElementById('nex-agent-empty');
    if (!empty) return;
    if (thread.querySelectorAll('.nex-agent-message').length > 0) {
      empty.style.display = 'none';
      thread.classList.remove('nex-agent-thread--idle');
    } else {
      empty.style.display = '';
      thread.classList.add('nex-agent-thread--idle');
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

  /** Web 顶栏「问 AI」展开态 — 对齐移动端底部 Tab 的 panel-open 高亮 */
  function syncHeaderAgentEntryHighlight(isOpen) {
    var b = document.querySelector('.header-agent-btn');
    if (!b) return;
    if (isOpen) b.classList.add('header-agent-btn--panel-open');
    else b.classList.remove('header-agent-btn--panel-open');
    b.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  }

  function isMobileAgentEntryDisabled() {
    var t = document.getElementById('mobile-agent-tab');
    if (!t) return false;
    return t.classList.contains('mobile-tab-item--disabled') || t.getAttribute('aria-disabled') === 'true';
  }

  var _agentChromeSyncTimer = null;

  /** 与 CSS `(max-width: 900px)` 对齐；优先 matchMedia，无 API 时用 innerWidth */
  function isMobileViewport() {
    try {
      if (window.matchMedia) {
        return window.matchMedia('(max-width: 900px)').matches;
      }
    } catch (e) {}
    return (typeof window.innerWidth === 'number' ? window.innerWidth : 901) <= 900;
  }

  function syncAgentLayoutMode(open) {
    document.body.classList.toggle('nex-agent-layout-mobile', !!(open && isMobileViewport()));
    document.body.classList.toggle('nex-agent-layout-desktop', !!(open && !isMobileViewport()));
  }

  function syncMobileFullpage(open) {
    var tabBar = document.querySelector('.mobile-tab-bar');
    var backBtn = document.getElementById('agent-back-btn');
    var closeBtn = document.getElementById('agent-panel-close');
    var panel = document.getElementById('agent-panel');
    if (!panel) return;
    if (isMobileViewport() && open) {
      if (tabBar) tabBar.classList.add('mobile-tab-bar--hidden');
      panel.classList.add('nex-agent-panel--mobile-fullpage');
      if (backBtn) {
        backBtn.removeAttribute('hidden');
        backBtn.hidden = false;
      }
      if (closeBtn) closeBtn.hidden = true;
    } else {
      if (tabBar) tabBar.classList.remove('mobile-tab-bar--hidden');
      panel.classList.remove('nex-agent-panel--mobile-fullpage');
      if (backBtn) {
        backBtn.hidden = true;
      }
      if (closeBtn) closeBtn.hidden = false;
    }
    syncAgentLayoutMode(open);
  }

  /** 面板打开后延迟再同步顶栏 chrome（适配第二次打开、输入法、地址栏收起等视口变化） */
  function scheduleAgentChromeResync() {
    clearTimeout(_agentChromeSyncTimer);
    _agentChromeSyncTimer = setTimeout(function () {
      _agentChromeSyncTimer = null;
      var panel = document.getElementById('agent-panel');
      if (!panel || !panel.classList.contains('nex-agent-panel--open')) return;
      syncMobileFullpage(true);
    }, 60);
  }

  // [P0-2 + Phase 2] 设置 streaming 状态，同步 UI（停止/发送图标切换）
  function setStreaming(on) {
    _nexsightIsStreaming = on;
    var sendBtn = document.getElementById('nex-agent-send');
    var input = document.getElementById('nex-agent-input');
    if (sendBtn) {
      sendBtn.disabled = false; // 停止按钮始终可点
      sendBtn.setAttribute('aria-label', on ? '停止生成' : '发送');
      if (on) {
        sendBtn.classList.add('nex-agent-send--stop');
        sendBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>';
      } else {
        sendBtn.classList.remove('nex-agent-send--stop');
        sendBtn.innerHTML =
          '<svg class="nex-agent-send-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>' +
          '<svg class="nex-agent-stop-icon" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>';
      }
    }
    if (input) input.readOnly = on;
  }

  /* ================= Markdown 轻量渲染 ================= */

  function renderMarkdown(html) {
    // 先处理代码块 <code>...</code> 保护
    var codeBlocks = [];
    html = html.replace(/&lt;code&gt;([\s\S]*?)&lt;\/code&gt;/g, function (m, inner) {
      codeBlocks.push(m);
      return '\x00CODE' + (codeBlocks.length - 1) + '\x00';
    });

    // 加粗
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // 斜体
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    // 行内代码（已被保护的不再处理）
    // 标题（# 开头）
    html = html.replace(/^### (.+)$/gm, '<strong style="font-size:13px">$1</strong>');
    html = html.replace(/^## (.+)$/gm, '<strong style="font-size:14px">$1</strong>');
    // 无序列表
    html = html.replace(/^(?:[-*] )(.+)$/gm, '<li style="margin-left:16px;list-style:disc">$1</li>');
    // 有序列表
    html = html.replace(/^\d+\. (.+)$/gm, '<li style="margin-left:16px;list-style:decimal">$1</li>');
    // 分隔线
    html = html.replace(/^---$/gm, '<hr style="border:none;border-top:1px solid var(--hairline-soft);margin:8px 0">');

    // 恢复代码块
    for (var i = 0; i < codeBlocks.length; i++) {
      html = html.replace('\x00CODE' + i + '\x00', codeBlocks[i]);
    }

    return html;
  }

  /* ================= 提交请求 ================= */

  window.NexSightAgent = window.NexSightAgent || {};

  window.NexSightAgent.syncContextUi = function () {};

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

  window.NexSightAgent.getScene = function () {
    return _currentScene;
  };

  window.NexSightAgent.setScene = function (scene) {
    if (scene === 'simple' || scene === 'analysis') {
      _currentScene = scene;
    }
  };

  // [Phase 2] 停止生成
  window.NexSightAgent.stopGeneration = function () {
    if (_abortController) {
      _abortController.abort();
      _abortController = null;
    }
  };

  window.NexSightAgent.submitComposer = function (fromKeyboard) {
    if (_nexsightIsStreaming) {
      // 停止按钮：中断当前流
      window.NexSightAgent.stopGeneration();
      return;
    }

    var ta = document.getElementById('nex-agent-input');
    if (!ta) return;
    var raw = ta.value.trim();
    if (!raw) return;
    ta.value = '';
    resizeComposerTA();
    hideChips();
    appendBubble('user', raw);

    var apiBase = (window.__NEXSIGHT_CONFIG__.agentApiBase || '').trim();

    if (apiBase) {
      _abortController = new AbortController();
      setStreaming(true);
      var timeoutId = setTimeout(function() { _abortController.abort(); }, 60000);

      // [Phase 2] 阶段提示气泡
      var thinkingBubble = appendBubble('assistant',
        '<span class="thinking-indicator">' +
          '<span class="thinking-dots"><span></span><span></span><span></span></span>' +
          ' <span class="thinking-text">\u6b63\u5728\u5206\u6790\u6570\u636e...</span>' +
        '</span>', '', true, true);

      fetch(apiBase + '/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: raw,
          session_id: _nexsightChatSessionId,
          stream: true
        }),
        signal: _abortController.signal
      })
      .then(function(res) {
        clearTimeout(timeoutId);
        if (res.status === 429) {
          return res.json().then(function(data) {
            removeLastBubble();
            var msg = '\u4eca\u65e5\u95ee\u7b54\u6b21\u6570\u5df2\u7528\u5b8c\uff0c\u8bf7\u660e\u5929\u518d\u8bd5\u3002';
            if (data && data.message) msg = data.message;
            var used = '?';
            var limit = 200;
            try {
              if (data.quota) {
                used = data.quota.used != null ? data.quota.used : '?';
                limit = data.quota.limit != null ? data.quota.limit : 200;
              }
            } catch(e) {}
            appendBubble('assistant',
              '\u23f3 ' + msg + '\n\n\u5df2\u4f7f\u7528\uff1a' + used + ' / ' + limit,
              'AI Radar'
            );
          }).catch(function() {
            removeLastBubble();
            appendBubble('assistant',
              '\u23f3 \u4eca\u65e5\u95ee\u7b54\u6b21\u6570\u5df2\u7528\u5b8c\uff0c\u8bf7\u660e\u5929\u518d\u8bd5\u3002',
              'AI Radar'
            );
          });
        }
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.body;
      })
      .then(function(body) {
        if (!body) return;

        var reader = body.getReader();
        var decoder = new TextDecoder();
        var buffer = '';
        var fullAnswer = '';
        var firstTokenReceived = false;

        // [P1-5] 时间节流
        var lastUpdateTs = 0;
        var pendingUpdate = '';

        function flushPending() {
          if (pendingUpdate) {
            updateLastBubble(pendingUpdate + '<span class="typing-cursor">\u258c</span>', true);
            scrollToBottom();
            pendingUpdate = '';
          }
        }

        function readStream() {
          reader.read().then(function(result) {
            if (result.done) {
              if (fullAnswer) {
                updateLastBubble(fullAnswer, false);
                appendFeedbackToLast();
              }
              _abortController = null;
              setStreaming(false);
              scrollToBottom();
              return;
            }

            // [Phase 2] 第一个 token 到达，更新阶段提示
            if (!firstTokenReceived) {
              firstTokenReceived = true;
              var thinkingText = document.querySelector('.thinking-text');
              if (thinkingText) thinkingText.textContent = '\u6b63\u5728\u751f\u6210\u56de\u7b54...';
            }

            buffer += decoder.decode(result.value, { stream: true });
            var lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (var i = 0; i < lines.length; i++) {
              var line = lines[i].trim();
              if (line.startsWith('data: ')) {
                try {
                  var data = JSON.parse(line.slice(6));
                  if (data.done) {
                    updateLastBubble(fullAnswer, false);
                    appendFeedbackToLast();
                    _abortController = null;
                    setStreaming(false);
                    scrollToBottom();
                    return;
                  }
                  if (data.delta) {
                    fullAnswer += data.delta;
                    var now = Date.now();
                    if (now - lastUpdateTs >= 80) {
                      lastUpdateTs = now;
                      pendingUpdate = fullAnswer;
                      flushPending();
                    } else {
                      pendingUpdate = fullAnswer;
                    }
                  }
                  if (data.error) {
                    removeLastBubble();
                    appendBubble('assistant', '\u26a0\ufe0f ' + data.error, 'AI Radar');
                    _abortController = null;
                    setStreaming(false);
                    return;
                  }
                } catch(e) {}
              }
            }

            readStream();
          }).catch(function(err) {
            // 流读取中断
            if (err.name !== 'AbortError') {
              removeLastBubble();
              appendBubble('assistant', '\u26a0\ufe0f \u8bfb\u53d6\u54cd\u5e94\u5931\u8d25\uff1a' + err.message);
            }
            _abortController = null;
            setStreaming(false);
          });
        }

        readStream();
      })
      .catch(function(err) {
        clearTimeout(timeoutId);
        removeLastBubble();
        _abortController = null;
        if (err.name === 'AbortError') {
          // 用户主动停止
          appendBubble('assistant', '\u23f9\ufe0f \u751f\u6210\u5df2\u505c\u6b62\u3002');
        } else {
          appendBubble('assistant', '\u26a0\ufe0f \u8bf7\u6c42\u5931\u8d25\uff1a' + err.message);
        }
        setStreaming(false);
      });
    } else {
      appendBubble('assistant', '\uff08\u6f14\u793a\u6a21\u5f0f\uff09\u8bf7\u5728\u914d\u7f6e\u4e2d\u8bbe\u7f6e agentApiBase \u4ee5\u8fde\u63a5\u771f\u5b9e\u540e\u7aef\u3002');
    }

    ta.focus();
  };

  window.NexSightAgent.openPanel = function () {
    /* isMobileAgentEntryDisabled 仅限制底部 Tab；桌面顶栏「问 AI」始终可开 */
    if (isMobileAgentEntryDisabled() && isMobileViewport()) return;
    var panel = document.getElementById('agent-panel');
    var scrim = document.getElementById('agent-scrim');
    var frame = document.getElementById('nex-agent-frame');
    var wrap = document.getElementById('nex-agent-frame-wrap');
    var scaffold = document.getElementById('nex-agent-scaffold');
    if (!panel || !scrim) return;

    document.body.classList.add('agent-panel-open');

    scrim.hidden = false;
    requestAnimationFrame(function () {
      scrim.classList.add('nex-agent-scrim--open');
      panel.classList.add('nex-agent-panel--open');
      panel.setAttribute('aria-hidden', 'false');
      setMobileAgentTab(true);
      syncHeaderAgentEntryHighlight(true);
      syncMobileFullpage(true);
      scheduleAgentChromeResync();
    });
    scheduleAgentChromeResync();

    pruneLegacyAgentChrome();
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
        scheduleAgentChromeResync();
      }, 320);
    }
  };

  window.NexSightAgent.closePanel = function () {
    var panel = document.getElementById('agent-panel');
    var scrim = document.getElementById('agent-scrim');
    if (!panel || !scrim) return;

    document.body.classList.remove('agent-panel-open');

    panel.classList.remove('nex-agent-panel--open');
    scrim.classList.remove('nex-agent-scrim--open');
    panel.setAttribute('aria-hidden', 'true');
    setMobileAgentTab(false);
    syncHeaderAgentEntryHighlight(false);
    syncMobileFullpage(false);
    setTimeout(function () {
      scrim.hidden = true;
    }, 300);
  };

  window.toggleAgentPanel = function () {
    if (isMobileAgentEntryDisabled() && isMobileViewport()) return;
    var panel = document.getElementById('agent-panel');
    if (!panel) return;
    if (panel.classList.contains('nex-agent-panel--open')) {
      window.NexSightAgent.closePanel();
    } else {
      window.NexSightAgent.openPanel();
    }
  };

  function bindAgentEvents() {
    pruneLegacyAgentChrome();
    var fab = document.getElementById('nex-agent-fab');
    var closeBtn = document.getElementById('agent-panel-close');
    var scrim = document.getElementById('agent-scrim');
    var sendBtn = document.getElementById('nex-agent-send');
    var input = document.getElementById('nex-agent-input');
    var mobileTab = document.getElementById('mobile-agent-tab');

    if (fab) fab.addEventListener('click', function () { window.toggleAgentPanel(); });
    if (closeBtn) closeBtn.addEventListener('click', function () { window.toggleAgentPanel(); });
    if (scrim) scrim.addEventListener('click', window.NexSightAgent.closePanel);

    if (sendBtn) sendBtn.addEventListener('click', function () {
      if (_nexsightIsStreaming) {
        window.NexSightAgent.stopGeneration();
      } else {
        window.NexSightAgent.submitComposer(false);
      }
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

    if (mobileTab) {
      mobileTab.addEventListener('click', function () {
        if (!isMobileAgentEntryDisabled()) {
          window.toggleAgentPanel();
        }
      });
    }

    var otherTabs = document.querySelectorAll('.mobile-tab-item:not(#mobile-agent-tab)');
    for (var i = 0; i < otherTabs.length; i++) {
      otherTabs[i].addEventListener('click', function () {
        var panel = document.getElementById('agent-panel');
        if (panel && panel.classList.contains('nex-agent-panel--open')) {
          window.NexSightAgent.closePanel();
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

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        var panel = document.getElementById('agent-panel');
        if (panel && panel.classList.contains('nex-agent-panel--open')) {
          window.NexSightAgent.closePanel();
        }
      }
    });

    window.addEventListener('resize', scheduleAgentChromeResync, { passive: true });
    window.addEventListener('orientationchange', scheduleAgentChromeResync, { passive: true });
    if (window.visualViewport && window.visualViewport.addEventListener) {
      window.visualViewport.addEventListener('resize', scheduleAgentChromeResync, { passive: true });
    }
    try {
      var mqAgent = window.matchMedia('(max-width: 900px)');
      if (mqAgent.addEventListener) mqAgent.addEventListener('change', scheduleAgentChromeResync);
      else if (mqAgent.addListener) mqAgent.addListener(scheduleAgentChromeResync);
    } catch (eMq) {}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindAgentEvents);
  } else {
    bindAgentEvents();
  }
})();
