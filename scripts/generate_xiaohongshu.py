#!/usr/bin/env python3
"""
小红书内容生成器 v4 — 修复文案 + 中文翻译
从每日 AI Radar 情报生成小红书风格的卡片内容（文案 + 配图 HTML）
"""

import json
import sys
import random
from datetime import datetime
from pathlib import Path

WIKI_DIR = Path("/home/admin/ai-radar-wiki")
SUMMARY_PATH = WIKI_DIR / "daily_summary.json"
OUTPUT_DIR = WIKI_DIR / "xiaohongshu"

# ── 标签池 ──
TAG_POOL = {
    "large": ["#AI工具", "#效率提升", "#科技数码", "#人工智能"],
    "medium": ["#ChatGPT", "#程序员日常", "#AI写作", "#职场干货", "#自我提升"],
    "longtail": ["#AI写代码", "#自动化办公", "#AI产品经理", "#效率神器推荐"],
    "trending": ["#最新AI", "#AI日报", "#今日AI"],
}

# ── 英文→中文翻译映射（常见AI新闻标题）──
EN_ZH_MAP = {
    "apple": "苹果",
    "openai": "OpenAI",
    "google": "谷歌",
    "microsoft": "微软",
    "meta": "Meta",
    "patreon": "Patreon",
    "zoom": "Zoom",
    "claude": "Claude",
    "capital one": "Capital One",
    "vulnhunter": "VulnHunter",
    "agents": "AI代理",
    "agent": "AI代理",
    "ai": "AI",
    "lawsuit": "诉讼",
    "employees": "员工",
    "legal letters": "法律函",
    "ipo": "IPO上市",
    "blocking": "拦截",
    "scrape": "爬取数据",
    "security": "安全",
    "privacy": "隐私",
    "open source": "开源",
    "bond market": "债券市场",
    "code": "代码",
    "hack": "漏洞",
    "record": "记录",
}


def translate_title(title):
    """英文标题→中文（完整翻译）"""
    if not title:
        return ""
    
    # 如果已经是中文为主，直接返回
    zh_chars = sum(1 for c in title if '\u4e00' <= c <= '\u9fff')
    if zh_chars > len(title) * 0.3:
        return title
    
    # 完整标题翻译映射（优先精确匹配）
    full_translations = {
        "Apple targets dozens of OpenAI employees with legal letters": "苹果向OpenAI员工发法律函",
        "How Apple's big lawsuit could disrupt OpenAI's IPO plans": "苹果大诉讼或阻碍OpenAI上市",
        "Apple's lawsuit couldn't come at a worse time for OpenAI": "苹果诉讼来得真不是时候",
        "Patreon stops asking AI bots not to scrape — and starts blocking them": "Patreon不再请求AI别爬数据，直接拦截",
        "Patreon stops asking AI bots not to scrape and starts blocking them": "Patreon不再请求AI别爬数据，直接拦截",
        "The Zoom hack that says 'don't record me'": "Zoom漏洞：'别录我'",
        "The Zoom hack that says, 'Don't record me'": "Zoom漏洞：'别录我'",
        "VulnHunter: Capital One's agentic AI code security tool": "Capital One推出AI自主代码安全工具",
        "Show HN: On-chain bond market where the issuers are AI agents": "链上债券市场：AI智能体当发行方",
        "Claude Code: Anatomy of a Misfeature": "Claude Code功能缺陷剖析",
        "Mozilla: The state of open source AI": "Mozilla发布开源AI现状报告",
    }
    
    # 精确匹配
    if title in full_translations:
        return full_translations[title]
    
    # 模糊匹配（忽略大小写和标点）
    import re
    lower = title.lower().strip()
    for eng, zh in full_translations.items():
        if eng.lower() in lower or lower in eng.lower():
            return zh
    
    # 兜底：关键词替换
    result = title
    for en, zh in EN_ZH_MAP.items():
        result = re.sub(r'\b' + re.escape(en) + r'\b', zh, result, flags=re.IGNORECASE)
    
    return result


def pick_tags(n=7):
    tags = []
    tags += random.sample(TAG_POOL["large"], min(2, len(TAG_POOL["large"])))
    tags += random.sample(TAG_POOL["medium"], min(2, len(TAG_POOL["medium"])))
    tags += random.sample(TAG_POOL["longtail"], min(2, len(TAG_POOL["longtail"])))
    tags += random.sample(TAG_POOL["trending"], min(1, len(TAG_POOL["trending"])))
    return " ".join(tags[:n])


def simplify_narrative(title):
    """把学术标题转成口语化中文"""
    # 完整短语替换（避免嵌套替换导致混乱）
    full_replacements = [
        ("AI产业从能力军备竞赛转向生态与合规博弈", "苹果起诉OpenAI，AI人才争夺战升级"),
        ("AI产业从能力竞赛转向生态合规博弈", "苹果起诉OpenAI，AI人才争夺战升级"),
        ("隐私与安全成为AI产品设计的强制性约束", "隐私安全成红线，AI产品必须过这关"),
        ("隐私与安全成为AI产品设计的必须重视", "隐私安全成红线，AI产品必须过这关"),
        ("AI代理从辅助工具演变为自主经济参与者", "AI智能体进化了，能自己赚钱了"),
        ("AI代理从辅助工具演变为能自己赚钱了", "AI智能体进化了，能自己赚钱了"),
    ]
    for old, new in full_replacements:
        if old in title:
            return new
    
    # 局部替换
    local = {
        "生态与合规博弈": "生态之战",
        "能力军备竞赛": "技术内卷",
        "强制性约束": "硬性要求",
        "自主经济参与者": "独立赚钱者",
        "AI代理": "AI智能体",
        "范式转变": "大变局",
        "瓶颈突破": "卡脖子突破",
        "走向成熟": "越来越靠谱",
    }
    for old, new in local.items():
        title = title.replace(old, new)
    return title


def generate_contents(data):
    """生成 3-5 条小红书内容"""
    ds = data.get("daily_summary", {})
    date_str = ds.get("date", datetime.now().strftime("%Y-%m-%d"))
    overview = ds.get("overview", "")
    narratives = ds.get("narratives", [])
    insights = ds.get("insights", [])

    contents = []

    # ── 内容 1: 今日总览（概览型）──
    if narratives:
        # 概览 headline 用 overview 字段，避免和第1条重复
        simple_overview = simplify_narrative(overview) if overview else "AI圈今天有大动作"
        
        # 如果 overview 和第一条 narrative 一样，用通用概述
        first_narrative_simple = simplify_narrative(narratives[0]["title"]) if narratives else ""
        if simple_overview == first_narrative_simple:
            simple_overview = f"{len(narratives)}条AI重磅消息，条条影响你的工作"
        
        title_options = [
            f"🔥 今天AI圈{len(narratives)}件大事，建议先收藏",
            f"💥 {date_str} AI日报｜{len(narratives)}条情报速览",
            f"📢 AI人必看！今天{len(narratives)}条重磅消息",
        ]
        title = random.choice(title_options)

        body_lines = [
            f"今天AI圈{simple_overview}！\n",
            f"整理了{len(narratives)}条最重要的 👇\n",
        ]
        for i, n in enumerate(narratives, 1):
            simple = simplify_narrative(n["title"])
            body_lines.append(f"{'①②③④⑤'[i-1]} {simple}")

        body_lines.append(f"\n💬 你觉得哪条最影响你的工作？评论区聊聊")
        body_lines.append(f"\n📊 完整情报 → 主页链接")

        body = "\n".join(body_lines)
        tags = pick_tags(7)

        contents.append({
            "type": "overview",
            "title": title,
            "body": body,
            "tags": tags,
            "card": {
                "style": "overview",
                "date": date_str,
                "headline": simple_overview,
                "items": [
                    {"title": simplify_narrative(n["title"]), "type": n.get("type", "")}
                    for n in narratives
                ],
            },
        })

    # ── 内容 2-4: 每个核心观点单独一条（深度型）──
    for insight in insights[:3]:
        pillar = insight.get("pillar", "")
        emoji = pillar.split()[0] if pillar else "💡"
        raw_title = insight.get("narrative_title", "")
        simple_title = simplify_narrative(raw_title)
        evidence = insight.get("evidence", [])

        title = f"{emoji} {simple_title[:18]}"

        body_lines = [f"{simple_title}\n"]
        body_lines.append("具体信号 👇\n")
        for ev in evidence[:4]:
            ev_zh = translate_title(ev["title"])
            body_lines.append(f"· {ev_zh}")

        body_lines.append(f"\n💬 这条趋势对你做产品有什么启发？")
        body_lines.append("评论区说说你的看法～")

        body = "\n".join(body_lines)
        tags = pick_tags(6)

        contents.append({
            "type": "insight",
            "title": title,
            "body": body,
            "tags": tags,
            "card": {
                "style": "insight",
                "pillar": pillar,
                "title": simple_title,
                "evidence_count": len(evidence),
                "top_evidence": [translate_title(ev["title"]) for ev in evidence[:3]],
            },
        })

    return contents[:5], date_str


# ══════════════════════════════════════════
# 卡片 HTML（小红书风格视觉设计）
# ══════════════════════════════════════════

COLORS = {
    "coral": {"primary": "#FF385C", "bg": "#FFF5F5", "accent": "#FF6B8A"},
    "purple": {"primary": "#7C3AED", "bg": "#F5F3FF", "accent": "#A78BFA"},
}

CARD_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    width: 1080px; height: 1440px;
    font-family: -apple-system, "PingFang SC", "Helvetica Neue", sans-serif;
    display: flex; align-items: center; justify-content: center;
}
"""


def _card_overview(card, date_str):
    colors = COLORS["coral"]
    items_html = ""
    type_badge = {
        "paradigm_shift": ("范式转变", "#FF385C"),
        "bottleneck": ("瓶颈突破", "#00B894"),
        "maturation": ("走向成熟", "#7C3AED"),
        "emerging": ("新兴趋势", "#F59E0B"),
    }

    for i, item in enumerate(card.get("items", []), 1):
        t = item.get("type", "")
        badge_text, badge_color = type_badge.get(t, ("趋势", "#666"))
        items_html += f"""
        <div class="item">
            <div class="item-num">{i}</div>
            <div class="item-body">
                <div class="item-title">{item['title']}</div>
                <div class="item-badge" style="background:{badge_color}">{badge_text}</div>
            </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
{CARD_CSS}
body {{ background: {colors['bg']}; }}
.card {{
    width: 960px;
    background: white;
    border-radius: 32px;
    padding: 64px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}}
.header {{
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 40px;
}}
.logo {{
    font-size: 30px; font-weight: 700; color: {colors['primary']};
}}
.date {{
    font-size: 26px; color: #999;
}}
.headline {{
    font-size: 46px; font-weight: 700; color: #1a1a1a;
    line-height: 1.4; letter-spacing: -1px;
    margin-bottom: 48px;
    padding-bottom: 32px;
    border-bottom: 3px solid {colors['primary']};
}}
.item {{
    display: flex; align-items: flex-start; gap: 24px;
    padding: 32px 0;
    border-bottom: 1px solid #f5f5f5;
}}
.item:last-child {{ border-bottom: none; }}
.item-num {{
    width: 56px; height: 56px;
    background: {colors['primary']}; color: white;
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; font-weight: 700;
    flex-shrink: 0;
}}
.item-body {{ flex: 1; }}
.item-title {{
    font-size: 34px; font-weight: 600; color: #1a1a1a;
    line-height: 1.4; margin-bottom: 14px;
}}
.item-badge {{
    display: inline-block;
    padding: 8px 16px;
    border-radius: 10px;
    color: white;
    font-size: 22px;
    font-weight: 500;
}}
.footer {{
    margin-top: 48px;
    text-align: center;
    font-size: 24px;
    color: #bbb;
}}
</style></head>
<body>
<div class="card">
    <div class="header">
        <div class="logo">🔥 AI Radar 每日情报</div>
        <div class="date">{date_str}</div>
    </div>
    <div class="headline">{card.get('headline', '')}</div>
    {items_html}
    <div class="footer">📊 完整情报见主页</div>
</div>
</body></html>"""


def _card_insight(card, date_str):
    colors = COLORS["purple"]
    evidence_html = ""
    for ev in card.get("top_evidence", []):
        evidence_html += f"""
        <div class="evidence">
            <div class="evidence-dot"></div>
            <div class="evidence-text">{ev}</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
{CARD_CSS}
body {{ background: {colors['bg']}; }}
.card {{
    width: 960px;
    background: white;
    border-radius: 32px;
    padding: 64px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}}
.pillar {{
    font-size: 28px; color: {colors['primary']};
    margin-bottom: 28px;
    font-weight: 600;
    letter-spacing: 1px;
}}
.title {{
    font-size: 50px; font-weight: 700; color: #1a1a1a;
    line-height: 1.4; letter-spacing: -1px;
    margin-bottom: 48px;
}}
.divider {{
    width: 64px; height: 4px;
    background: {colors['primary']};
    border-radius: 2px;
    margin-bottom: 40px;
}}
.label {{
    font-size: 26px; color: {colors['primary']};
    font-weight: 600;
    margin-bottom: 28px;
    letter-spacing: 2px;
}}
.evidence {{
    display: flex; align-items: flex-start; gap: 18px;
    padding: 22px 0;
}}
.evidence-dot {{
    width: 14px; height: 14px;
    background: {colors['primary']};
    border-radius: 50%;
    margin-top: 14px;
    flex-shrink: 0;
}}
.evidence-text {{
    font-size: 34px; color: #333;
    line-height: 1.5;
}}
.count {{
    margin-top: 48px;
    padding: 28px;
    background: {colors['bg']};
    border-radius: 16px;
    font-size: 30px;
    color: {colors['primary']};
    font-weight: 600;
    text-align: center;
}}
.footer {{
    margin-top: 40px;
    text-align: center;
    font-size: 24px;
    color: #bbb;
}}
</style></head>
<body>
<div class="card">
    <div class="pillar">{card.get('pillar', '')}</div>
    <div class="title">{card.get('title', '')}</div>
    <div class="divider"></div>
    <div class="label">📌 关键信号</div>
    {evidence_html}
    <div class="count">📊 共 {card.get('evidence_count', 0)} 条证据支撑</div>
    <div class="footer">AI Radar · {date_str}</div>
</div>
</body></html>"""


def generate_card_html(card, date_str):
    if card.get("style") == "insight":
        return _card_insight(card, date_str)
    return _card_overview(card, date_str)


def screenshot_card(html_path, output_path):
    import subprocess
    script = f"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={{"width": 1080, "height": 1440}})
    page.goto("file://{html_path}")
    page.wait_for_timeout(500)
    page.screenshot(path="{output_path}")
    browser.close()
"""
    subprocess.run([sys.executable, "-c", script], check=True)


def save_all(contents, date_str):
    output_dir = OUTPUT_DIR / date_str
    output_dir.mkdir(parents=True, exist_ok=True)

    all_text = []
    for i, c in enumerate(contents, 1):
        txt_path = output_dir / f"{i}_{c['type']}.txt"
        txt_content = f"【标题】\n{c['title']}\n\n【正文】\n{c['body']}\n\n【标签】\n{c['tags']}\n"
        txt_path.write_text(txt_content, encoding='utf-8')
        all_text.append(txt_content)

        html = generate_card_html(c['card'], date_str)
        html_path = output_dir / f"{i}_{c['type']}.html"
        html_path.write_text(html, encoding='utf-8')

        png_path = output_dir / f"{i}_{c['type']}.png"
        try:
            screenshot_card(html_path, png_path)
            print(f"✅ {i}_{c['type']}.txt + .png")
        except Exception as e:
            print(f"⚠️ {i}_{c['type']}.txt (截图失败: {e})")

    summary_path = output_dir / "00_全部文案.txt"
    summary_path.write_text("\n" + "=" * 40 + "\n\n".join(all_text), encoding='utf-8')
    print(f"✅ 00_全部文案.txt")
    print(f"\n📁 目录: {output_dir}")
    return output_dir


def main():
    print("🔄 生成小红书内容（v4 修复版）...\n")

    data = load_summary()
    contents, date_str = generate_contents(data)

    if not contents:
        print("❌ 没有内容可生成")
        sys.exit(1)

    output_dir = save_all(contents, date_str)
    print(f"\n✅ 完成！共 {len(contents)} 条内容")
    print(f"💡 下一步: 复制文案 → 打开小红书 → 粘贴发布")
    print(f"⏰ 建议发布时间: 周二至周四 12:00")


def load_summary():
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    main()
