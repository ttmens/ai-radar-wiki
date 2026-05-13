#!/usr/bin/env python3
"""
AI Radar 微信公众号日报生成器
- 读取 daily_summary.json + weekly_trends.json
- 生成公众号风格文章（Markdown + 飞书 + HTML）
- HTML 支持直接复制粘贴到公众号编辑器
"""

import json
import os
import re
import sys
import time
import requests
from datetime import datetime, timezone, timedelta

# === Config ===
WIKI_DIR = "/home/admin/ai-radar-wiki"
ARTICLES_DIR = f"{WIKI_DIR}/articles"
ENV_PATH = "/home/admin/.hermes/.env"
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "").strip()
if not FEISHU_APP_ID:
    raise EnvironmentError("FEISHU_APP_ID not set")
FEISHU_FOLDER = "SUACfJyNRlPdJhdoeUecBioXnoh"  # 文档目标文件夹（非敏感资源标识）
DATA_URL = "http://archwang.top/graph.html"

CJST = timezone(timedelta(hours=8))
BRAND_COLOR = "#ff385c"  # 雷达站品牌色

os.makedirs(ARTICLES_DIR, exist_ok=True)

def log(msg):
    ts = datetime.now(CJST).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def get_app_secret():
    with open(ENV_PATH) as f:
        for line in f:
            if line.startswith("FEISHU_APP_SECRET="):
                val = line.strip().split("=", 1)[1]
                return val.lstrip("*")
    raise ValueError("FEISHU_APP_SECRET not found")

def get_tenant_token(max_retries=3):
    secret = get_app_secret()
    for attempt in range(max_retries):
        try:
            resp = requests.post(
                "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                json={"app_id": FEISHU_APP_ID, "app_secret": secret},
                timeout=10,
            )
            data = resp.json()
            if data.get("code") == 0:
                return data["tenant_access_token"]
            log(f"Token error: {data}")
        except Exception as e:
            log(f"Token request failed ({attempt+1}): {e}")
        time.sleep(2)
    raise RuntimeError("Failed to get Feishu tenant token")

def load_data():
    with open(f"{WIKI_DIR}/daily_summary.json") as f:
        daily = json.load(f).get("daily_summary", {})
    try:
        with open(f"{WIKI_DIR}/weekly_trends.json") as f:
            weekly = json.load(f)
    except:
        weekly = {"narrative_chains": [], "pillar_trends": {}, "contradictions": []}
    return daily, weekly

def build_narrative_tracker(weekly):
    tracker = {}
    for chain in weekly.get("narrative_chains", []):
        title = chain.get("title", "")
        if title:
            tracker[title] = {
                "lifecycle": chain.get("lifecycle", "unknown"),
                "days": len(chain.get("days", [])),
                "days_list": chain.get("days", []),
                "type": chain.get("type", ""),
            }
    return tracker

def score_threshold():
    return 0.35

# =========================================================
# WeChat HTML Generator
# =========================================================

def generate_wechat_html(daily, weekly):
    """生成带内联样式的 HTML，适配公众号编辑器"""
    date = daily.get("date", "unknown")
    overview = daily.get("overview", "")
    total = daily.get("total_items", 0)
    narratives = daily.get("narratives", [])
    insights = daily.get("insights", [])
    tracker = build_narrative_tracker(weekly)
    threshold = score_threshold()
    
    pillar_names = {
        "capabilities": "🤖 技术能力",
        "patterns": "📱 产品模式",
        "ecosystem": "🔧 工具生态",
        "business": "💰 商业趋势",
    }
    type_labels = {
        "paradigm_shift": "🔄 范式转移",
        "bottleneck": "⚠️ 核心瓶颈",
        "maturation": "📈 行业成熟",
        "validation": "💡 模式验证",
    }
    
    html_parts = []
    
    # Wrapper
    html_parts.append(f'<section style="max-width: 100%; box-sizing: border-box; padding: 15px; margin: 0 auto; background-color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Microsoft YaHei&quot;, sans-serif; font-size: 15px; color: #3f3f3f; line-height: 1.75; letter-spacing: 0.034em; word-spacing: 0.034em; text-align: justify;">')
    
    # 1. Title
    html_parts.append(f'<h1 style="font-size: 22px; font-weight: bold; text-align: center; margin: 20px 0 10px; color: {BRAND_COLOR}; letter-spacing: 0.05em;">📱 AI雷达日报 · {date}</h1>')
    
    # Divider
    html_parts.append(f'<section style="height: 1px; width: 60px; background-color: {BRAND_COLOR}; margin: 0 auto 20px; border-radius: 1px;"></section>')
    
    # 2. Overview
    if overview:
        html_parts.append(f'<p style="font-size: 16px; font-weight: bold; color: #222; margin-bottom: 20px; text-align: center;">一句话看今天：{overview}。</p>')
        
    # PM Insights Top Block
    high_value_score = 0.35
    
    # Categorize High Value Items
    tech_items = []
    pattern_items = []
    market_items = []
    
    for ins in insights:
        pillar_key = ins.get("pillar_key", "")
        evidence = ins.get("evidence", [])
        
        # Get high score items
        top_evs = [e for e in evidence if e.get("score", 0) >= high_value_score]
        
        for ev in top_evs:
            title = ev['title']
            score = ev['score']
            item = f"<strong>{title}</strong> (PM {score:.2f})"
            
            # Logic to categorize
            if pillar_key in ["capabilities", "ecosystem"]:
                tech_items.append(item)
            elif pillar_key == "patterns":
                pattern_items.append(item)
            elif pillar_key == "business":
                market_items.append(item)

    if tech_items or pattern_items or market_items:
        # Load Summaries
        summary_file = "/home/admin/ai-radar-wiki/articles/category_summaries.json"
        summaries = {"pattern": "", "tech": "", "market": ""}
        if os.path.exists(summary_file):
            try:
                with open(summary_file) as f: summaries.update(json.load(f))
            except: pass

        html_parts.append('<section style="background: #fdf2f8; padding: 15px; border-radius: 8px; margin-bottom: 25px; border: 1px solid #fbcfe8;">')
        html_parts.append('<h3 style="margin: 0 0 15px; color: #be185d; font-size: 18px; font-weight: bold;">🎯 PM 决策线索 (Actionable Insights)</h3>')
        
        if pattern_items:
            html_parts.append('<p style="margin-bottom: 8px; font-weight: bold; color: #444;">📱 <strong>可借鉴模式：</strong></p>')
            if summaries.get("pattern"):
                html_parts.append(f'<div style="background: #fff; padding: 12px; border-radius: 6px; margin-bottom: 10px; border-left: 4px solid #f472b6; font-size: 14px; color: #444; line-height: 1.6;">{summaries["pattern"]}</div>')
            for item in pattern_items:
                html_parts.append(f'<p style="margin: 0 0 6px; padding-left: 10px; color: #666; font-size: 13px; line-height: 1.5;">• {item}</p>')
            html_parts.append('<p style="height: 10px;"></p>')
            
        if tech_items:
            html_parts.append('<p style="margin-bottom: 8px; font-weight: bold; color: #444;">🛠️ <strong>技术红利：</strong></p>')
            if summaries.get("tech"):
                html_parts.append(f'<div style="background: #fff; padding: 12px; border-radius: 6px; margin-bottom: 10px; border-left: 4px solid #f472b6; font-size: 14px; color: #444; line-height: 1.6;">{summaries["tech"]}</div>')
            for item in tech_items:
                html_parts.append(f'<p style="margin: 0 0 6px; padding-left: 10px; color: #666; font-size: 13px; line-height: 1.5;">• {item}</p>')
            html_parts.append('<p style="height: 10px;"></p>')
            
        if market_items:
            html_parts.append('<p style="margin-bottom: 8px; font-weight: bold; color: #444;">⚠️ <strong>市场/竞争信号：</strong></p>')
            if summaries.get("market"):
                html_parts.append(f'<div style="background: #fff; padding: 12px; border-radius: 6px; margin-bottom: 10px; border-left: 4px solid #f472b6; font-size: 14px; color: #444; line-height: 1.6;">{summaries["market"]}</div>')
            for item in market_items:
                html_parts.append(f'<p style="margin: 0 0 6px; padding-left: 10px; color: #666; font-size: 13px; line-height: 1.5;">• {item}</p>')
            
        html_parts.append('</section>')

    # 3. Narratives
    html_parts.append(f'<h2 style="font-size: 18px; font-weight: bold; color: #222; border-left: 4px solid {BRAND_COLOR}; padding-left: 10px; margin: 30px 0 15px; display: flex; align-items: center;">🔥 今日叙事主线</h2>')
    
    for n in narratives:
        title = n.get("title", "")
        n_type = n.get("type", "")
        body = n.get("body", "")
        action = n.get("action", "")
        type_label = type_labels.get(n_type, "📌 趋势")
        
        track_info = tracker.get(title)
        
        # Type & Title
        html_parts.append(f'<h3 style="font-size: 17px; font-weight: bold; color: #333; margin: 20px 0 10px;">{type_label}：{title}</h3>')
        
        # Lifecycle badge
        if track_info and track_info["days"] >= 2:
            icons = {"emerging": "🌱", "rising": "🔥", "hot": "⚡", "declining": "📉"}
            icon = icons.get(track_info["lifecycle"], "📌")
            html_parts.append(f'<p style="font-size: 13px; color: #888; margin-bottom: 8px; font-style: italic;">{icon} {track_info["lifecycle"]} · 连续追踪 {track_info["days"]}天</p>')
        
        # Body
        html_parts.append(f'<p style="margin-bottom: 10px;">{body}</p>')
        
        # Action
        if action:
            clean = action.replace("建议：", "").strip()
            html_parts.append(f'<section style="background-color: #f7f8fa; padding: 10px 12px; border-radius: 6px; margin: 10px 0; border-left: 3px solid {BRAND_COLOR};"><p style="font-size: 14px; color: #666; margin: 0;"><strong>💡 行动建议：</strong>{clean}</p></section>')
            
    # 4. Insights
    html_parts.append(f'<h2 style="font-size: 18px; font-weight: bold; color: #222; border-left: 4px solid {BRAND_COLOR}; padding-left: 10px; margin: 40px 0 15px; display: flex; align-items: center;">📊 分领域情报</h2>')
    
    for ins in insights:
        pillar_key = ins.get("pillar_key", "")
        pillar = ins.get("pillar", pillar_names.get(pillar_key, pillar_key))
        evidence = ins.get("evidence", [])
        high_val = [e for e in evidence if e.get("score", 0) >= threshold]
        if not high_val:
            continue
            
        html_parts.append(f'<h3 style="font-size: 16px; font-weight: bold; color: #555; margin: 20px 0 8px; border-bottom: 1px dashed #eee; padding-bottom: 5px;">{pillar}</h3>')
        
        # 添加核心观点
        if ins.get("insight"):
            html_parts.append(f'<p style="background: #fff5f7; color: #444; padding: 10px 12px; border-radius: 6px; margin-bottom: 12px; font-size: 14px; line-height: 1.65; border-left: 3px solid #ffb3c1;">{ins["insight"]}</p>')
        
        for i, ev in enumerate(high_val, 1):
            score_str = f"{ev['score']:.2f}"
            # Check if title is cut off
            title = ev['title']
            if len(title) > 50: title = title[:50] + "..."
            html_parts.append(f'<p style="margin-bottom: 6px; font-size: 15px;"><span style="display: inline-block; width: 22px; height: 22px; background-color: #f0f0f0; color: #666; border-radius: 4px; text-align: center; line-height: 22px; margin-right: 8px; font-size: 12px; font-weight: bold;">{i}</span>{title} <span style="color: {BRAND_COLOR}; font-size: 12px; font-weight: bold;">[PM {score_str}]</span></p>')
        html_parts.append('<p style="height: 8px;"></p>')
        
    # 5. Watch List
    html_parts.append(f'<h2 style="font-size: 18px; font-weight: bold; color: #222; border-left: 4px solid {BRAND_COLOR}; padding-left: 10px; margin: 30px 0 15px; display: flex; align-items: center;">📌 持续关注</h2>')
    
    watch_items = []
    for t_title, info in sorted(tracker.items(), key=lambda x: -x[1]["days"]):
        if info["days"] >= 2 or info["lifecycle"] in ("rising", "hot"):
            prefix = "🔥" if info["lifecycle"] in ("rising", "hot") else "📌"
            watch_items.append(f"{prefix} 连续{info['days']}天：{t_title}")
    watch_items.append("AI 的电力/存储成本问题从商业角度持续发酵")
    watch_items.append("社区对 AI PR 刷屏的抵触情绪值得关注")
    
    for item in watch_items:
        html_parts.append(f'<p style="margin-bottom: 8px; padding-left: 10px; position: relative;"><span style="position: absolute; left: 0; color: {BRAND_COLOR};">●</span>{item}</p>')
    
    # 6. Footer
    html_parts.append(f'<section style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; text-align: center;">')
    html_parts.append(f'<p style="font-size: 14px; color: #888; margin-bottom: 5px;">扫码关注，每日情报推送直达。</p>')
    html_parts.append(f'<p style="font-size: 14px;"><a href="{DATA_URL}" style="color: {BRAND_COLOR}; text-decoration: none; font-weight: bold;">更多AI情报，欢迎关注</a></p>')
    html_parts.append(f'</section>')
    
    html_parts.append('</section>')
    
    return "\n".join(html_parts)


# =========================================================
# Feishu Functions
# =========================================================

def create_feishu_document(token, title, folder_token):
    resp = requests.post(
        "https://open.feishu.cn/open-apis/docx/v1/documents",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"folder_token": folder_token, "title": title},
        timeout=10,
    )
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"Failed to create doc: {data}")
    return data["data"]["document"]["document_id"]

def safe_json(resp):
    text = resp.text
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(text[start:end])
    return resp.json()

def write_blocks(token, doc_id, blocks, batch_size=10):
    for i in range(0, len(blocks), batch_size):
        batch = blocks[i : i + batch_size]
        resp = requests.post(
            f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"children": batch, "index": -1},
            timeout=15,
        )
        data = safe_json(resp)
        if data.get("code") != 0:
            log(f"Block write error: {data}")
            raise RuntimeError(f"Block write failed: {data}")
        time.sleep(0.3)

def build_feishu_blocks(daily, weekly, markdown_text):
    blocks = []
    tracker = build_narrative_tracker(weekly)
    date = daily.get("date", "unknown")
    overview = daily.get("overview", "")
    narratives = daily.get("narratives", [])
    insights = daily.get("insights", [])
    threshold = score_threshold()
    
    pillar_names = {"capabilities": "🤖 技术能力", "patterns": "📱 产品模式", "ecosystem": "🔧 工具生态", "business": "💰 商业趋势"}
    type_labels = {"paradigm_shift": "🔄 范式转移", "bottleneck": "⚠️ 核心瓶颈", "maturation": "📈 行业成熟", "validation": "💡 模式验证"}
    
    def text_block(content, bold=False, italic=False, text_color=None):
        el = {"text_run": {"content": content}}
        style = {}
        if bold: style["bold"] = True
        if italic: style["italic"] = True
        if text_color: style["text_color"] = text_color
        if style: el["text_run"]["text_element_style"] = style
        return {"block_type": 2, "text": {"elements": [el]}}
        
    def heading1(content): return {"block_type": 3, "heading1": {"elements": [{"text_run": {"content": content, "text_element_style": {"bold": True}}}]}}
    def heading2(content): return {"block_type": 4, "heading2": {"elements": [{"text_run": {"content": content}}]}}
    def bullet_block(content): return {"block_type": 12, "bullet": {"elements": [{"text_run": {"content": content}}]}}
    
    blocks.append(text_block(f"AI雷达日报 · {date}", bold=True, text_color=1)) # 1 is dark red in Feishu usually
    blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": " "}}]}})
    if overview:
        blocks.append(text_block(f"一句话看今天：{overview}。"))
        blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": " "}}]}})
        
    blocks.append(heading1("🔥 今日叙事主线"))
    for n in narratives:
        title = n.get("title", "")
        n_type = n.get("type", "")
        body = n.get("body", "")
        action = n.get("action", "")
        type_label = type_labels.get(n_type, "📌 趋势")
        track_info = tracker.get(title)
        
        if track_info and track_info["days"] >= 2:
            icons = {"emerging": "🌱", "rising": "🔥", "hot": "⚡", "declining": "📉"}
            icon = icons.get(track_info["lifecycle"], "📌")
            blocks.append(text_block(f"{icon} {track_info['lifecycle']} · 连续追踪 {track_info['days']}天", italic=True, text_color=7))
            
        blocks.append(heading2(f"{type_label}：{title}"))
        blocks.append(text_block(body))
        if action:
            clean = action.replace("建议：", "").strip()
            blocks.append(text_block(f"💡 行动建议：{clean}", italic=True, text_color=7))
        blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": " "}}]}})
        
    blocks.append(heading1("📊 分领域情报"))
    for ins in insights:
        pillar_key = ins.get("pillar_key", "")
        pillar = ins.get("pillar", pillar_names.get(pillar_key, pillar_key))
        evidence = ins.get("evidence", [])
        high_val = [e for e in evidence if e.get("score", 0) >= threshold]
        if not high_val: continue
        
        blocks.append(heading2(pillar))
        for i, ev in enumerate(high_val, 1):
            blocks.append(bullet_block(f"#{i}  {ev['title']}  [PM {ev['score']:.2f}]"))
        blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": " "}}]}})
        
    blocks.append(heading1("📌 持续关注"))
    for t_title, info in sorted(tracker.items(), key=lambda x: -x[1]["days"]):
        if info["days"] >= 2 or info["lifecycle"] in ("rising", "hot"):
            blocks.append(bullet_block(f"连续{info['days']}天：{t_title}"))
    blocks.append(bullet_block("AI 的电力/存储成本问题从商业角度持续发酵"))
    blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": " "}}]}})
    blocks.append(text_block(f"更多AI情报，欢迎关注 {DATA_URL}", italic=True, text_color=7))
    
    return blocks

def main():
    log("=== AI Radar 公众号日报生成 ===")
    daily, weekly = load_data()
    
    # 1. Date Verification
    today_str = datetime.now(CJST).strftime("%Y-%m-%d")
    file_date = daily.get("date", "")
    if file_date != today_str:
        log(f"⚠️ 警告：数据日期 ({file_date}) 与今天 ({today_str}) 不符！可能未生成新报告。")
        # Fallback: Use today's date anyway for the filename, but warn
    
    date = file_date if file_date else today_str
    
    # 2. HTML (For WeChat)
    log("生成公众号 HTML...")
    html = generate_wechat_html(daily, weekly)
    html_path = f"{ARTICLES_DIR}/ai-radar-daily-{date}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    log(f"✅ HTML 已保存: {html_path}")
    
    # 3. Markdown
    log("生成 Markdown...")
    md = generate_article_markdown(daily, weekly)
    md_path = f"{ARTICLES_DIR}/ai-radar-daily-{date}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    log(f"Markdown 已保存: {md_path}")
    
    # 4. Feishu
    log("获取飞书 Token...")
    token = get_tenant_token()
    doc_title = f"AI雷达日报 · {date}"
    log(f"创建飞书文档: {doc_title}")
    doc_id = create_feishu_document(token, doc_title, FEISHU_FOLDER)
    doc_url = f"https://open.feishu.cn/docx/{doc_id}"
    
    log("写入文章内容...")
    blocks = build_feishu_blocks(daily, weekly, md)
    write_blocks(token, doc_id, blocks)
    log(f"✅ 写入 {len(blocks)} 个 blocks")
    
    print(f"\n{'='*50}")
    print(f"📄 AI雷达日报 · {date}")
    print(f"🔗 飞书文档: {doc_url}")
    print(f"🌐 公众号 HTML: file://{html_path}")
    print(f"   👉 操作：打开 HTML -> 全选(Ctrl+A) -> 复制 -> 粘贴到公众号")
    print(f"{'='*50}")

def generate_article_markdown(daily, weekly):
    date = daily.get("date", "unknown")
    overview = daily.get("overview", "")
    total = daily.get("total_items", 0)
    narratives = daily.get("narratives", [])
    insights = daily.get("insights", [])
    tracker = build_narrative_tracker(weekly)
    md = [f"# AI雷达日报 · {date}\n"]
    if overview:
        md.append(f"**一句话看今天：{overview}。**")
        md.append("")
    md.append("## 🔥 今日叙事主线\n")
    type_labels = {"paradigm_shift": "🔄 范式转移", "bottleneck": "⚠️ 核心瓶颈", "maturation": "📈 行业成熟", "validation": "💡 模式验证"}
    for n in narratives:
        title = n.get("title", "")
        track_info = tracker.get(title)
        type_label = type_labels.get(n.get("type", ""), "📌 趋势")
        if track_info and track_info["days"] >= 2:
            icons = {"emerging": "🌱", "rising": "🔥", "hot": "⚡", "declining": "📉"}
            md.append(f"**{icons.get(track_info['lifecycle'], '📌')} {track_info['lifecycle']} · 连续追踪 {track_info['days']}天**")
        md.append(f"### {type_label}：{title}")
        md.append(n.get("body", ""))
        if n.get("action"):
            md.append(f"💡 **行动建议**：{n['action'].replace('建议：', '')}")
        md.append("---\n")
    md.append("## 📊 分领域情报\n")
    pillar_names = {"capabilities": "🤖 技术能力", "patterns": "📱 产品模式", "ecosystem": "🔧 工具生态", "business": "💰 商业趋势"}
    for ins in insights:
        pillar = ins.get("pillar", pillar_names.get(ins.get("pillar_key", ""), ""))
        high_val = [e for e in ins.get("evidence", []) if e.get("score", 0) >= 0.35]
        if high_val:
            md.append(f"### {pillar}")
            for i, ev in enumerate(high_val, 1):
                md.append(f"{i}. {ev['title']} (PM {ev['score']:.2f})")
            md.append("")
    md.append("## 📌 持续关注\n")
    for t_title, info in sorted(tracker.items(), key=lambda x: -x[1]["days"]):
        if info["days"] >= 2 or info["lifecycle"] in ("rising", "hot"):
            md.append(f"- **连续{info['days']}天**：{t_title}")
    md.append(f"\n更多AI情报，欢迎关注 {DATA_URL}\n")
    return "\n".join(md)

if __name__ == "__main__":
    main()