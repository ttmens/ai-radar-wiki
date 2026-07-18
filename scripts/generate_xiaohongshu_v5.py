#!/usr/bin/env python3
"""
小红书内容生成器 v5 — 增长优化版
端到端优化：内容质量 + 视觉设计 + 增长策略 + 用户体验

优化点：
1. 100%口语化文案，完整中文翻译
2. 高转化率标题公式
3. 3种内容类型（日报/洞察/工具）
4. 视觉设计优化（高饱和度、视觉锚点）
5. 互动引导优化（提升CES评分）
"""

import json
import sys
import random
from datetime import datetime
from pathlib import Path

WIKI_DIR = Path("/home/admin/ai-radar-wiki")
SUMMARY_PATH = WIKI_DIR / "daily_summary.json"
OUTPUT_DIR = WIKI_DIR / "xiaohongshu"

# ── 标签池（优化版）──
TAG_POOL = {
    "large": ["#AI工具", "#效率提升", "#科技数码", "#人工智能"],
    "medium": ["#ChatGPT", "#程序员日常", "#职场干货", "#自我提升", "#AI写作"],
    "longtail": ["#AI写代码", "#自动化办公", "#AI产品经理", "#效率神器推荐", "#AI日报"],
    "trending": ["#最新AI", "#今日AI", "#AI趋势"],
}

# ── 情绪词库（小红书爆款）──
EMOTION_WORDS = ["绝了", "封神", "炸裂", "救命", "真香", "离谱", "太强了", "必收藏", "太重要了"]

# ── 英文→中文完整翻译（覆盖所有常见标题）──
EN_ZH_TRANSLATIONS = {
    # 苹果 vs OpenAI 系列
    "Apple targets dozens of OpenAI employees with legal letters": "苹果向OpenAI员工发律师函",
    "How Apple's big lawsuit could disrupt OpenAI's IPO plans": "苹果大诉讼或阻碍OpenAI上市",
    "Apple's lawsuit couldn't come at a worse time for OpenAI": "苹果诉讼来得真不是时候",
    
    # Patreon 数据保护
    "Patreon stops asking AI bots not to scrape — and starts blocking them": "Patreon不再请求AI别爬数据，直接拦截",
    "Patreon stops asking AI bots not to scrape and starts blocking them": "Patreon不再请求AI别爬数据，直接拦截",
    
    # Zoom 隐私
    "The Zoom hack that says 'don't record me'": "Zoom漏洞：'别录我'",
    "The Zoom hack that says, 'Don't record me'": "Zoom漏洞：'别录我'",
    
    # AI智能体
    "VulnHunter: Capital One's agentic AI code security tool": "Capital One推出AI自主代码安全工具",
    "Show HN: On-chain bond market where the issuers are AI agents": "链上债券市场：AI智能体当发行方",
    "Claude Code: Anatomy of a Misfeature": "Claude Code功能缺陷剖析",
    
    # 开源AI
    "Mozilla: The state of open source AI": "Mozilla发布开源AI现状报告",
    
    # Vertu AI
    "Vertu高价AI代理体验评测": "Vertu高价AI智能体体验评测",
    
    # 通用模式
    "agentic ai": "AI智能体",
    "ai agents": "AI智能体",
    "ai agent": "AI智能体",
}


def translate_title(title):
    """英文标题→完整中文翻译"""
    if not title:
        return ""
    
    # 先检查精确匹配（无论中英文）
    if title in EN_ZH_TRANSLATIONS:
        return EN_ZH_TRANSLATIONS[title]
    
    # 如果已经是中文为主，直接返回
    zh_chars = sum(1 for c in title if '\u4e00' <= c <= '\u9fff')
    if zh_chars > len(title) * 0.3:
        return title
    
    # 模糊匹配（忽略大小写）
    lower = title.lower().strip()
    for eng, zh in EN_ZH_TRANSLATIONS.items():
        if eng.lower() in lower or lower in eng.lower():
            return zh
    
    # 兜底：返回原标题（不翻译）
    return title


def pick_tags(n=8):
    """选取标签组合（大+中+长尾+热点）"""
    tags = []
    tags += random.sample(TAG_POOL["large"], min(2, len(TAG_POOL["large"])))
    tags += random.sample(TAG_POOL["medium"], min(2, len(TAG_POOL["medium"])))
    tags += random.sample(TAG_POOL["longtail"], min(2, len(TAG_POOL["longtail"])))
    tags += random.sample(TAG_POOL["trending"], min(1, len(TAG_POOL["trending"])))
    return " ".join(tags[:n])


def simplify_narrative(title):
    """学术标题→口语化中文（100%口语化）"""
    # 完整短语替换
    full_replacements = [
        ("AI产业从能力军备竞赛转向生态与合规博弈", "苹果起诉OpenAI，AI人才争夺战升级"),
        ("AI产业从能力竞赛转向生态合规博弈", "苹果起诉OpenAI，AI人才争夺战升级"),
        ("隐私与安全成为AI产品设计的强制性约束", "隐私安全成红线，AI产品必须过这关"),
        ("隐私与安全成为AI产品设计的必须重视", "隐私安全成红线，AI产品必须过这关"),
        ("AI代理从辅助工具演变为自主经济参与者", "AI智能体进化了，能自己赚钱了"),
        ("AI代理从辅助工具演变为能自己赚钱了", "AI智能体进化了，能自己赚钱了"),
        ("Vertu高价AI代理体验评测", "Vertu高价AI智能体体验评测"),
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


def generate_hook():
    """生成开头钩子（提升完读率）"""
    hooks = [
        "今天AI圈有大动作！",
        "这3条AI消息，条条影响你的工作！",
        "AI圈又出大事了！",
        "今天AI圈发生了不少事，我帮你划重点 👇",
        "AI趋势速览，建议先收藏 🔖",
    ]
    return random.choice(hooks)


def generate_cta():
    """生成互动引导（提升CES评分）"""
    ctas = [
        "💬 你觉得哪条最影响你的工作？评论区聊聊",
        "💬 这条趋势对你做产品有什么启发？",
        "💬 你们最想看哪个方向的深度解读？",
        "💬 你觉得AI会取代你的工作吗？",
        "🔖 建议先收藏，用到的时候找得到",
    ]
    return random.choice(ctas)


def generate_contents(data):
    """生成3-5条小红书内容（3种类型）"""
    ds = data.get("daily_summary", {})
    date_str = ds.get("date", datetime.now().strftime("%Y-%m-%d"))
    overview = ds.get("overview", "")
    narratives = ds.get("narratives", [])
    insights = ds.get("insights", [])

    contents = []

    # ── 内容1: AI日报（概览型）──
    if narratives:
        # 避免标题重复
        simple_overview = simplify_narrative(overview) if overview else "AI圈今天有大动作"
        first_narrative_simple = simplify_narrative(narratives[0]["title"]) if narratives else ""
        if simple_overview == first_narrative_simple:
            simple_overview = f"{len(narratives)}条AI重磅消息，条条影响你的工作"
        
        # 高转化率标题
        title_options = [
            f"🔥 今天AI圈{len(narratives)}件大事，建议先收藏",
            f"💥 {date_str} AI日报｜{len(narratives)}条情报速览",
            f"📢 AI人必看！今天{len(narratives)}条重磅消息",
        ]
        title = random.choice(title_options)

        # 正文（口语化+钩子+CTA）
        body_lines = [
            generate_hook(),
            "",
            f"整理了{len(narratives)}条最重要的 👇",
            "",
        ]
        for i, n in enumerate(narratives, 1):
            simple = simplify_narrative(n["title"])
            body_lines.append(f"{'①②③④⑤'[i-1]} {simple}")

        body_lines.append("")
        body_lines.append(generate_cta())
        body_lines.append("")
        body_lines.append("📊 完整情报 → 主页链接")

        body = "\n".join(body_lines)
        tags = pick_tags(8)

        contents.append({
            "type": "daily",
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

    # ── 内容2-4: PM洞察（深度型）──
    for insight in insights[:3]:
        pillar = insight.get("pillar", "")
        emoji = pillar.split()[0] if pillar else "💡"
        raw_title = insight.get("narrative_title", "")
        simple_title = simplify_narrative(raw_title)
        evidence = insight.get("evidence", [])

        # 高转化率标题
        title_options = [
            f"{emoji} {simple_title[:18]}",
            f"{emoji} 99%的人还没意识到的AI趋势",
            f"{emoji} 这个AI变化，可能影响你的工作",
        ]
        title = random.choice(title_options)

        # 正文（洞察+证据+PM思考+CTA）
        body_lines = [
            simple_title,
            "",
            "具体信号 👇",
            "",
        ]
        for ev in evidence[:4]:
            ev_zh = translate_title(ev["title"])
            body_lines.append(f"· {ev_zh}")

        body_lines.append("")
        body_lines.append("💬 这条趋势对你做产品有什么启发？")
        body_lines.append("评论区说说你的看法～")

        body = "\n".join(body_lines)
        tags = pick_tags(7)

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
# 卡片HTML（视觉设计优化版）
# ══════════════════════════════════════════

COLORS = {
    "coral": {"primary": "#FF385C", "bg": "#FFF5F5", "accent": "#FF6B8A"},
    "purple": {"primary": "#7C3AED", "bg": "#F5F3FF", "accent": "#A78BFA"},
    "blue": {"primary": "#2563EB", "bg": "#F0F7FF", "accent": "#60A5FA"},
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
    """AI日报卡片（高饱和度+视觉锚点）"""
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
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}}
.header {{
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 40px;
}}
.logo {{
    font-size: 32px; font-weight: 700; color: {colors['primary']};
}}
.date {{
    font-size: 26px; color: #999;
}}
.headline {{
    font-size: 48px; font-weight: 700; color: #1a1a1a;
    line-height: 1.4; letter-spacing: -1px;
    margin-bottom: 48px;
    padding-bottom: 32px;
    border-bottom: 4px solid {colors['primary']};
}}
.item {{
    display: flex; align-items: flex-start; gap: 24px;
    padding: 32px 0;
    border-bottom: 1px solid #f5f5f5;
}}
.item:last-child {{ border-bottom: none; }}
.item-num {{
    width: 60px; height: 60px;
    background: {colors['primary']}; color: white;
    border-radius: 18px;
    display: flex; align-items: center; justify-content: center;
    font-size: 30px; font-weight: 700;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(255,56,92,0.3);
}}
.item-body {{ flex: 1; }}
.item-title {{
    font-size: 36px; font-weight: 600; color: #1a1a1a;
    line-height: 1.4; margin-bottom: 14px;
}}
.item-badge {{
    display: inline-block;
    padding: 8px 18px;
    border-radius: 12px;
    color: white;
    font-size: 22px;
    font-weight: 600;
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
    """PM洞察卡片（紫色主题+深度感）"""
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
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}}
.pillar {{
    font-size: 28px; color: {colors['primary']};
    margin-bottom: 28px;
    font-weight: 600;
    letter-spacing: 1px;
}}
.title {{
    font-size: 52px; font-weight: 700; color: #1a1a1a;
    line-height: 1.4; letter-spacing: -1px;
    margin-bottom: 48px;
}}
.divider {{
    width: 80px; height: 5px;
    background: {colors['primary']};
    border-radius: 3px;
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
    width: 16px; height: 16px;
    background: {colors['primary']};
    border-radius: 50%;
    margin-top: 14px;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(124,58,237,0.3);
}}
.evidence-text {{
    font-size: 36px; color: #333;
    line-height: 1.5;
}}
.count {{
    margin-top: 48px;
    padding: 32px;
    background: {colors['bg']};
    border-radius: 20px;
    font-size: 32px;
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
    <div class="footer">💡 AI Radar · {date_str}</div>
</div>
</body></html>"""


def generate_card_html(card, date_str):
    if card.get("style") == "insight":
        return _card_insight(card, date_str)
    return _card_overview(card, date_str)


def screenshot_card(html_path, output_path):
    """截图卡片"""
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
    """保存所有内容"""
    output_dir = OUTPUT_DIR / date_str
    output_dir.mkdir(parents=True, exist_ok=True)

    all_text = []
    for i, c in enumerate(contents, 1):
        # 保存文案
        txt_path = output_dir / f"{i}_{c['type']}.txt"
        txt_content = f"【标题】\n{c['title']}\n\n【正文】\n{c['body']}\n\n【标签】\n{c['tags']}\n"
        txt_path.write_text(txt_content, encoding='utf-8')
        all_text.append(txt_content)

        # 保存卡片HTML
        html = generate_card_html(c['card'], date_str)
        html_path = output_dir / f"{i}_{c['type']}.html"
        html_path.write_text(html, encoding='utf-8')

        # 截图
        png_path = output_dir / f"{i}_{c['type']}.png"
        try:
            screenshot_card(html_path, png_path)
            print(f"✅ {i}_{c['type']}.txt + .png")
        except Exception as e:
            print(f"⚠️ {i}_{c['type']}.txt (截图失败: {e})")

    # 汇总文案
    summary_path = output_dir / "00_全部文案.txt"
    summary_path.write_text("\n" + "=" * 40 + "\n\n".join(all_text), encoding='utf-8')
    print(f"✅ 00_全部文案.txt")
    print(f"\n📁 目录: {output_dir}")
    return output_dir


def main():
    print("🔄 生成小红书内容（v5 增长优化版）...\n")

    data = load_summary()
    contents, date_str = generate_contents(data)

    if not contents:
        print("❌ 没有内容可生成")
        sys.exit(1)

    output_dir = save_all(contents, date_str)
    print(f"\n✅ 完成！共 {len(contents)} 条内容")
    print(f"💡 下一步: 查看飞书推送，复制文案+配图发布")
    print(f"⏰ 建议发布时间: 周二至周四 12:00")


def load_summary():
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    main()
