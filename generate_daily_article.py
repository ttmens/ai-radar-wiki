#!/usr/bin/env python3
"""
AI Radar Daily Article Generator (WeChat Optimized)
Generates a high-quality HTML article based on daily intelligence data.
"""

import json
import os
import re
import sys
import time
import httpx
from datetime import datetime, timezone, timedelta

# === Config ===
BJ_TZ = timezone(timedelta(hours=8))
WIKI_DIR = os.path.expanduser("~/ai-radar-wiki")
ARTICLES_DIR = os.path.join(WIKI_DIR, "daily-articles")
DAILY_SUMMARY = os.path.join(WIKI_DIR, "daily_summary.json")
GRAPH_JSON = os.path.join(WIKI_DIR, "graph.json")
ENV_PATH = os.path.expanduser("~/.hermes/.env")

# Load Env
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))
try:
    from ai_model_router import call_llm as router_call_llm
    HAS_ROUTER = True
except ImportError:
    HAS_ROUTER = False

def load_data():
    """Load daily summary and graph data."""
    with open(DAILY_SUMMARY) as f:
        daily = json.load(f).get("daily_summary", {})
    
    items = []
    if os.path.exists(GRAPH_JSON):
        with open(GRAPH_JSON) as f:
            graph = json.load(f)
        today = datetime.now(BJ_TZ).strftime("%Y-%m-%d")
        for node in graph.get("nodes", []):
            if node.get("date", "").startswith(today) and node.get("type") != "concept":
                items.append(node)
    
    items.sort(key=lambda x: x.get("pm_score", 0), reverse=True)
    return daily, items

def generate_prompt(daily, items):
    """Generate the prompt for the LLM."""
    overview = daily.get("overview", "")
    narratives = daily.get("narratives", [])
    
    # Prepare news context
    news_text = ""
    for i, item in enumerate(items[:15], 1):
        news_text += f"- {item.get('label')}: {item.get('summary', '')[:120]}\n"

    # Prepare narrative context
    nav_text = ""
    for n in narratives:
        nav_text += f"Narrative: {n.get('title')}\n{n.get('body')}\n"

    return f"""你是一位顶级的 AI 产业分析师（类似 Ben Thompson 或 Stratechery 风格），为 AI 产品经理撰写深度内参。
**今天是 {datetime.now(BJ_TZ).strftime("%Y年%-m月%-d日")}。文章中涉及的任何日期必须与此一致，不要编造过去的日期。**

## 核心任务
基于今日情报，写一篇**逻辑严密、洞察深刻**的行业分析文章。

## ⚠️ 禁止项（必须遵守）
- **不要**在文章开头生成任何副标题、身份标签（如"顶级分析师"、"深度内参"等）。
- **不要**在文章末尾生成任何签名、版权声明、脚注。
- 直接以 `<h1>` 标题开始，以最后一段内容结束。

## 核心观点
{overview}

## 叙事主线
{nav_text}

## 关键素材
{news_text}

## 写作铁律（必须遵守）

1.  **深度归因，拒绝罗列**：
    - 严禁写成"A 发生了，B 发生了，C 也发生了"。
    - 必须写出逻辑链条：A 现象背后的**根本驱动力**是什么？它如何导致了 B 结果？这对 C 意味着什么？
    - 每一段都必须有明确的**论点**，素材只是用来证明论点的证据。

2.  **结构严谨**：
    - **标题**：专业、客观、一针见血（不要震惊体，不要感叹号）。
    - **开篇**：直接抛出今日最重要的**产业趋势判断**，用"💡 核心判断"卡片包裹。
    - **正文（3 个维度）**：
        1. **商业/产品模式**：分析大厂动作背后的商业逻辑变化。
        2. **技术/工程瓶颈**：分析技术落地面临的真实阻碍。
        3. **安全/治理挑战**：分析规模化应用必须解决的底线问题。
    - 每个维度标题前加 emoji（📊/⚙️/🛡️）。
    - 维度之间用分隔线隔开。
    - **PM 启示**：给产品经理的 3 条具体策略建议，每条用独立灰色卡片包裹。

3.  **语言风格**：
    - **专业、冷峻、客观**。不要用"震惊"、"可怕"等情绪化词汇。
    - **用词精准**：使用行业术语（如：边际成本、端云协同、长尾场景、合规壁垒），术语用淡灰背景标记。
    - **段落紧凑**：每段只讲清楚一个逻辑点，不超过 4 行。
    - **关键论点加粗**：每段的核心观点句用加粗突出。

4.  **输出格式（HTML 内联样式）**：
    - 输出完整的 HTML 片段（包含 <h1>, <p>, <div>, <ul>, <li> 等标签），不需要 <html> 或 <body>。
    - **必须使用内联样式 (Inline Styles)** 以确保微信公众号排版兼容性。
    - **排版规范**（严格执行）：
        a. **核心判断卡片**：开篇第一段"核心产业趋势判断"用卡片包裹：
           `<div style="background:#fff5f6;border:1px solid rgba(255,56,92,0.15);border-radius:10px;padding:16px 18px;margin:16px 0;"><p style="font-size:13px;color:#ff385c;font-weight:600;margin-bottom:8px;">💡 核心判断</p><p style="font-size:16px;line-height:1.8;color:#333;margin:0;">[你的核心判断内容]</p></div>`
        b. **分隔线**：每个维度之间用分隔线隔开：
           `<div style="border-top:1px solid #eee;margin:32px 0;"></div>`
        c. **小标题**：每个维度标题前加 emoji，如"📊 一、商业/产品模式"。
        d. **PM 策略建议卡片**：3 条建议用独立卡片包裹：
           `<div style="background:#fafafa;border-radius:8px;padding:14px 16px;margin:10px 0;"><p style="margin:0;line-height:1.8;color:#333;"><strong style="color:#ff385c;">策略一：</strong>[建议内容]</p></div>`
        e. **术语高亮**：产品名称、技术名词用淡灰背景标记，如 `<span style="background:#f0f0f0;padding:1px 6px;border-radius:3px;">Claude for Small Business</span>`。
    - CSS 要求：
        - 字体：系统默认无衬线字体。
        - 字号：正文 15px，H1 标题 24px，H2 标题 20px，H3 标题 17px。
        - 行高：正文 1.75。
        - 颜色：正文深灰 (#333)，标题黑色 (#1a1a1a)，品牌色 #ff385c。
    - **直接输出 HTML 代码，不要 Markdown 代码块包裹。**
"""

def call_llm(prompt):
    """Call LLM using qwen-plus for best logic."""
    if HAS_ROUTER:
        return router_call_llm(
            prompt=prompt,
            system_prompt="你是顶级 AI 产业分析师，擅长深度商业与技术分析。",
            scene="analysis",
            max_tokens=4000,
            temperature=0.4, # Lower temp for better logic
        )
    else:
        # Fallback
        key = os.environ.get("DASHSCOPE_API_KEY", "")
        if key:
            url = os.environ.get("DASHSCOPE_BASE_URL", "https://coding.dashscope.aliyuncs.com/v1") + "/chat/completions"
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
            resp = httpx.post(url, json={
                "model": "qwen-plus",
                "messages": [
                    {"role": "system", "content": "你是顶级 AI 产业分析师。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.4,
                "max_tokens": 4000,
            }, headers=headers, timeout=180)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        raise RuntimeError("No LLM available")

def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = re.sub(r'\s+', '-', name)
    return name.strip('-')[:50] or "article"

def send_to_feishu(html_content, filename):
    """Send the HTML file to the current chat via Feishu API."""
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        print("⚠️ Feishu credentials missing, skipping file send.")
        return

    try:
        with httpx.Client() as client:
            # 1. Get Token
            resp = client.post(
                "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                json={"app_id": app_id, "app_secret": app_secret}
            )
            token = resp.json().get("tenant_access_token")
            if not token:
                print("⚠️ Failed to get Feishu token.")
                return

            # 2. Upload File
            headers = {"Authorization": f"Bearer {token}"}
            with open(filename, "rb") as f:
                files = {"file": (os.path.basename(filename), f, "text/html")}
                data = {"file_type": "stream"}
                resp = client.post(
                    "https://open.feishu.cn/open-apis/im/v1/files",
                    headers=headers,
                    files=files,
                    data=data
                )
                file_key = resp.json().get("data", {}).get("file_key")
                if not file_key:
                    print("⚠️ Failed to upload file.")
                    return

            # 3. Send Message
            chat_id = "oc_a2aedb3e0b69d55d2c73a83c69427f2e" # Hardcoded current chat
            msg_content = json.dumps({"file_key": file_key})
            resp = client.post(
                "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
                headers={**headers, "Content-Type": "application/json"},
                json={"receive_id": chat_id, "msg_type": "file", "content": msg_content}
            )
            if resp.json().get("code") == 0:
                print("🚀 文件已发送到聊天窗口")
            else:
                print("⚠️ 发送消息失败:", resp.json())
    except Exception as e:
        print(f"⚠️ Send error: {e}")

def main():
    print("🚀 开始生成公众号深度文章...")
    
    # 1. Load Data
    daily, items = load_data()
    date = daily.get("date", datetime.now(BJ_TZ).strftime("%Y-%m-%d"))
    overview = daily.get("overview", "AI Daily")
    
    print(f"📅 日期: {date}")
    print(f"📌 核心观点: {overview}")
    print(f"📊 情报数量: {len(items)} 条")
    
    if not items:
        print("❌ 无情报数据")
        return

    # 2. Generate Article
    print("🤖 正在撰写文章 (使用 qwen-plus)...")
    prompt = generate_prompt(daily, items)
    
    try:
        raw_html = call_llm(prompt)
        # Clean up code blocks if LLM adds them
        raw_html = re.sub(r'^```html\s*', '', raw_html)
        raw_html = re.sub(r'\s*```$', '', raw_html)
        print(f"✅ 文章生成完成 ({len(raw_html)} 字符)")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return

    # 3. Save to Git
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    filename = f"{date}-{sanitize_filename(overview)}.html"
    filepath = os.path.join(ARTICLES_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(raw_html)
    print(f"📝 已保存: {filepath}")

    # Git Push
    os.chdir(WIKI_DIR)
    os.system(f"git add {filepath} && git commit -m 'daily-article: {date} {overview[:50]}' && git push > /dev/null 2>&1")
    print("✅ 已推送到 Git")

    # 4. Rebuild articles archive
    print("📑 Rebuilding articles archive...")
    os.chdir(os.path.expanduser("~/.hermes/scripts"))
    os.system("python3 build_articles_page.py > /dev/null 2>&1")
    os.chdir(WIKI_DIR)
    os.system("git add articles.html articles_template.html daily-articles/ && git commit -m 'articles: add {date} + rebuild archive' && git push > /dev/null 2>&1")
    print("✅ Archive rebuilt and pushed")

    # 5. Send to Chat
    send_to_feishu(raw_html, filepath)

if __name__ == "__main__":
    main()
