#!/usr/bin/env python3
"""
小红书内容生成器 v6 — 爆款优化版
基于小红书传播策略深度优化：标题、文案、配图全面升级
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
EMOTION_WORDS = ["绝了", "封神", "炸裂", "救命", "真香", "离谱", "太强了", "必收藏", "太重要了", "必看"]

# ── 英文→中文翻译（扩展版）──
EN_ZH_TRANSLATIONS = {
    "Apple targets dozens of OpenAI employees with legal letters": "苹果向OpenAI员工发律师函",
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
    "Vertu高价AI代理体验评测": "Vertu高价AI智能体体验评测",
    "agentic ai": "AI智能体",
    "ai agents": "AI智能体",
    "ai agent": "AI智能体",
    "Setting up your spare Mac for Claude Code to control": "用闲置Mac搭建Claude Code远程控制节点",
    "Kimi: Threat or menace?": "Kimi：威胁还是机遇？",
    "Fable 5 vs. GPT-5.6 Sol on an NP-Hard Problem": "Fable 5与GPT-5.6 Sol在NP难问题上的对决",
    "What AI did to stackoverflow in a graph": "一张图看懂AI对Stack Overflow的冲击",
    "Why do AI company logos look like buttholes?": "为什么AI公司的logo都长得差不多？",
    "Best Model For The Use Case": "按使用场景选最佳模型",
    "AI Mania Is Eviscerating Global Decision-Making": "AI狂热正在摧毁全球决策能力",
    "Mayor Mamdani Says Landlords Can't Use AI Images to Advertis": "旧金山禁止房东用AI生成虚假租房广告",
    # 新增翻译
    "stared into the flatline until everything else converged out of respec": "凝视平坦线直到一切收敛",
    "GPT-5.6 used a prompt to close a 30-year gap in convex optimization": "GPT-5.6用prompt解决凸优化30年难题",
}


def load_summary():
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def translate_title(title):
    """英文标题→完整中文翻译"""
    if not title:
        return ""
    
    if title in EN_ZH_TRANSLATIONS:
        return EN_ZH_TRANSLATIONS[title]
    
    zh_chars = sum(1 for c in title if '\u4e00' <= c <= '\u9fff')
    if zh_chars > len(title) * 0.3:
        return title
    
    lower = title.lower().strip()
    for eng, zh in EN_ZH_TRANSLATIONS.items():
        if eng.lower() in lower or lower in eng.lower():
            return zh
    
    return title


def pick_tags(n=8):
    tags = []
    tags += random.sample(TAG_POOL["large"], min(2, len(TAG_POOL["large"])))
    tags += random.sample(TAG_POOL["medium"], min(2, len(TAG_POOL["medium"])))
    tags += random.sample(TAG_POOL["longtail"], min(2, len(TAG_POOL["longtail"])))
    tags += random.sample(TAG_POOL["trending"], min(1, len(TAG_POOL["trending"])))
    return " ".join(tags[:n])


def simplify_narrative(title):
    """学术标题→口语化中文（小红书风格）"""
    full_replacements = [
        ("AI产业从能力军备竞赛转向生态与合规博弈", "苹果起诉OpenAI，AI人才争夺战升级"),
        ("AI产业从能力竞赛转向生态合规博弈", "苹果起诉OpenAI，AI人才争夺战升级"),
        ("隐私与安全成为AI产品设计的强制性约束", "隐私安全成红线，AI产品必须过这关"),
        ("隐私与安全成为AI产品设计的必须重视", "隐私安全成红线，AI产品必须过这关"),
        ("AI代理从辅助工具演变为自主经济参与者", "AI智能体进化了，能自己赚钱了"),
        ("AI代理从辅助工具演变为能自己赚钱了", "AI智能体进化了，能自己赚钱了"),
        ("Vertu高价AI代理体验评测", "Vertu高价AI智能体体验评测"),
        ("Fable 5 vs. GPT-5.6 Sol on an NP-Hard Problem", "GPT-5.6 Sol攻克NP难题，模型能力分化加剧"),
        ("AI能力分化与自主执行成为新范式", "AI能力分化：从通用大模型到任务专用代理"),
        ("AI应用生态震荡：监管收紧与社区重构", "AI监管收紧，社区生态面临重构"),
        ("AI产品设计趋同与决策依赖风险", "AI产品设计同质化，过度依赖成隐患"),
    ]
    for old, new in full_replacements:
        if old in title:
            return new
    
    en_chars = sum(1 for c in title if c.isalpha() and ord(c) < 128)
    if en_chars > len(title) * 0.3:
        return translate_title(title)
    
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
    """生成开头钩子（小红书爆款风格）"""
    hooks = [
        "🔥 今天AI圈有大动作！",
        "⚠️ 这3条AI消息，条条影响你的工作！",
        "💥 AI圈又出大事了！",
        "📢 今天AI圈发生了不少事，我帮你划重点 👇",
        "🔖 AI趋势速览，建议先收藏",
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


def generate_daily_post(data):
    """生成日报文案（小红书爆款风格）"""
    ds = data.get("daily_summary", {})
    date_str = ds.get("date", datetime.now().strftime("%Y-%m-%d"))
    narratives = ds.get("narratives", [])
    insights = ds.get("insights", [])
    
    if not narratives and not insights:
        return None
    
    all_items = narratives.copy()
    seen_titles = {simplify_narrative(n["title"]) for n in narratives}
    
    for insight in insights:
        if len(all_items) >= 3:
            break
        title = insight.get("narrative_title", "")
        simple = simplify_narrative(title)
        if simple not in seen_titles:
            all_items.append({
                "title": title,
                "type": "insight",
                "pillar": insight.get("pillar", ""),
            })
            seen_titles.add(simple)
    
    # 小红书爆款标题（18-25字，数字+emoji+情绪词）
    title_options = [
        f"🔥 今天AI圈{len(all_items)}件大事，建议先收藏",
        f"💥 {date_str} AI日报｜{len(all_items)}条情报速览",
        f"📢 AI人必看！今天{len(all_items)}条重磅消息",
        f"⚠️ {len(all_items)}条AI趋势，条条影响你的工作",
    ]
    title = random.choice(title_options)
    
    # 小红书爆款正文（emoji分段，每段≤3行）
    body_lines = [
        generate_hook(),
        "",
        f"整理了{len(all_items)}条最重要的 👇",
        "",
    ]
    
    for i, item in enumerate(all_items[:3], 1):
        simple = simplify_narrative(item["title"])
        body_lines.append(f"{'①②③④⑤'[i-1]} {simple}")
    
    # 具体信号（多源数据融合）
    if insights:
        body_lines.append("")
        body_lines.append("🔍 具体信号 👇")
        body_lines.append("")
        
        all_evidence = []
        for insight in insights[:3]:
            for ev in insight.get("evidence", []):
                all_evidence.append(ev)
        
        all_evidence.sort(key=lambda e: (0 if e.get("source_type") == "twitter" else 1, -e.get("score", 0)))
        
        for ev in all_evidence[:5]:
            source_type = ev.get("source_type", "unknown")
            author = ev.get("author", "")
            ev_title = ev.get("title", "")
            
            if source_type == "twitter" and author:
                title_zh = translate_title(ev_title)
                body_lines.append(f"🐦 @{author}: {title_zh}")
            else:
                title_zh = translate_title(ev_title)
                source_label = {"hn": "HN", "techcrunch": "TC", "github": "GitHub", "papers": "论文"}.get(source_type, "")
                if source_label:
                    body_lines.append(f"· [{source_label}] {title_zh}")
                else:
                    body_lines.append(f"· {title_zh}")
    
    body_lines.append("")
    body_lines.append(generate_cta())
    body_lines.append("")
    body_lines.append("📊 完整情报见主页简介")
    
    body = "\n".join(body_lines)
    tags = pick_tags(8)
    
    return {
        "title": title,
        "body": body,
        "tags": tags,
        "date": date_str,
        "narratives": all_items[:3],
        "insights": insights[:3],
    }


def generate_card_html_overview(post):
    """生成日报总览卡片 HTML（小红书爆款风格）"""
    date_str = post["date"]
    narratives = post["narratives"]
    
    items_html = ""
    type_badge = {
        "paradigm_shift": ("范式转变", "#FF385C"),
        "bottleneck": ("瓶颈突破", "#00B894"),
        "maturation": ("走向成熟", "#7C3AED"),
        "emerging": ("新兴趋势", "#F59E0B"),
    }
    
    for i, n in enumerate(narratives, 1):
        simple = simplify_narrative(n["title"])
        t = n.get("type", "")
        badge_text, badge_color = type_badge.get(t, ("趋势", "#666"))
        
        items_html += f"""
        <div class="item">
            <div class="item-num">{i}</div>
            <div class="item-body">
                <div class="item-title">{simple}</div>
                <div class="item-badge" style="background:{badge_color}">{badge_text}</div>
            </div>
        </div>"""
    
    headline = f"{len(narratives)}条AI重磅消息，条条影响你的工作"
    
    # 小红书爆款配图：高饱和度、大字报、填满屏幕
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1080px; height: 1440px;
    font-family: -apple-system, "PingFang SC", sans-serif;
    background: linear-gradient(135deg, #FF385C 0%, #FF6B8A 100%);
    display: flex; align-items: center; justify-content: center;
}}
.card {{
    width: 100%; height: 100%;
    background: white;
    padding: 80px 60px;
    display: flex; flex-direction: column;
}}
.header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 40px;
}}
.logo {{
    font-size: 36px; font-weight: 700; color: #FF385C;
}}
.date {{
    font-size: 28px; color: #999;
}}
.headline {{
    font-size: 56px; font-weight: 700; color: #1a1a1a;
    line-height: 1.3; letter-spacing: -1px;
    margin-bottom: 48px;
    padding-bottom: 32px;
    border-bottom: 5px solid #FF385C;
}}
.item {{
    display: flex; align-items: flex-start; gap: 24px;
    padding: 36px 0;
    border-bottom: 2px solid #f5f5f5;
}}
.item:last-child {{ border-bottom: none; }}
.item-num {{
    width: 64px; height: 64px;
    background: #FF385C; color: white;
    border-radius: 18px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; font-weight: 700;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(255,56,92,0.3);
}}
.item-body {{ flex: 1; }}
.item-title {{
    font-size: 38px; font-weight: 600; color: #1a1a1a;
    line-height: 1.4; margin-bottom: 16px;
}}
.item-badge {{
    display: inline-block;
    padding: 10px 20px;
    border-radius: 12px;
    color: white;
    font-size: 24px;
    font-weight: 600;
}}
.footer {{
    margin-top: auto;
    text-align: center;
    font-size: 26px;
    color: #999;
    padding-top: 40px;
}}
</style></head>
<body>
<div class="card">
    <div class="header">
        <div class="logo">🔥 AI Radar 每日情报</div>
        <div class="date">{date_str}</div>
    </div>
    <div class="headline">{headline}</div>
    {items_html}
    <div class="footer">📊 完整情报见主页简介</div>
</div>
</body></html>"""


def generate_card_html_insight_from_data(date_str, insight, index):
    """从 insight 数据生成洞察卡片 HTML（小红书爆款风格 - 高饱和度渐变）"""
    pillar = insight.get("pillar", "")
    emoji = pillar.split()[0] if pillar else "💡"
    narrative_title = insight.get("narrative_title", "")
    simple_title = simplify_narrative(narrative_title)
    evidence = insight.get("evidence", [])
    
    evidence_html = ""
    for ev in evidence[:3]:
        ev_zh = translate_title(ev["title"])
        evidence_html += f"""
        <div class="evidence">
            <div class="evidence-dot"></div>
            <div class="evidence-text">{ev_zh}</div>
        </div>"""
    
    # 小红书爆款配色：高饱和度渐变背景
    colors = {
        "💰": {"primary": "#7C3AED", "bg": "#F5F3FF", "gradient": "linear-gradient(135deg, #7C3AED 0%, #EC4899 100%)"},
        "🤖": {"primary": "#2563EB", "bg": "#F0F7FF", "gradient": "linear-gradient(135deg, #2563EB 0%, #06B6D4 100%)"},
        "📱": {"primary": "#FF385C", "bg": "#FFF5F5", "gradient": "linear-gradient(135deg, #FF385C 0%, #F59E0B 100%)"},
        "🔧": {"primary": "#059669", "bg": "#ECFDF5", "gradient": "linear-gradient(135deg, #059669 0%, #10B981 100%)"},
    }
    color = colors.get(emoji, colors["💰"])
    
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1080px; height: 1440px;
    font-family: -apple-system, "PingFang SC", sans-serif;
    background: {color['gradient']};
    display: flex; align-items: center; justify-content: center;
}}
.card {{
    width: 100%; height: 100%;
    background: rgba(255,255,255,0.85);
    padding: 80px 60px;
    display: flex; flex-direction: column;
}}
.header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 32px;
}}
.category {{
    background: {color['primary']};
    color: white;
    padding: 12px 24px;
    border-radius: 24px;
    font-size: 28px;
    font-weight: 600;
}}
.date {{
    font-size: 28px;
    color: #999;
}}
.title {{
    font-size: 52px;
    font-weight: 700;
    color: #1a1a1a;
    line-height: 1.3;
    margin-bottom: 32px;
}}
.divider {{
    width: 100px;
    height: 6px;
    background: {color['primary']};
    border-radius: 3px;
    margin-bottom: 40px;
}}
.section {{
    margin-bottom: 40px;
}}
.section-title {{
    font-size: 32px;
    color: {color['primary']};
    font-weight: 600;
    margin-bottom: 24px;
    letter-spacing: 1px;
}}
.evidence {{
    display: flex; align-items: flex-start; gap: 20px;
    padding: 24px 0;
}}
.evidence-dot {{
    width: 18px; height: 18px;
    background: {color['primary']};
    border-radius: 50%;
    margin-top: 16px;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}}
.evidence-text {{
    font-size: 36px;
    color: #333;
    line-height: 1.5;
}}
.impact {{
    background: {color['bg']};
    border-radius: 20px;
    padding: 32px;
    margin-top: auto;
}}
.impact-title {{
    font-size: 32px;
    color: {color['primary']};
    font-weight: 600;
    margin-bottom: 16px;
}}
.impact-text {{
    font-size: 32px;
    color: #333;
    line-height: 1.5;
}}
.footer {{
    margin-top: 32px;
    text-align: center;
    font-size: 26px;
    color: #999;
}}
</style></head>
<body>
<div class="card">
    <div class="header">
        <div class="category">{pillar}</div>
        <div class="date">{date_str}</div>
    </div>
    
    <div class="title">{simple_title}</div>
    <div class="divider"></div>
    
    <div class="section">
        <div class="section-title">📌 关键信号</div>
        {evidence_html}
    </div>
    
    <div class="impact">
        <div class="impact-title">💡 对PM的启示</div>
        <div class="impact-text">这条趋势对你的产品有什么启发？欢迎评论区分享你的看法～</div>
    </div>
    
    <div class="footer">AI Radar · 每日情报</div>
</div>
</body></html>"""


def screenshot_card(html_content, output_path, keep_html=False):
    import subprocess
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        html_path = f.name
    
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
    subprocess.run(["python3", "-c", script], check=True)
    if not keep_html:
        Path(html_path).unlink()
    else:
        # 保存 HTML 到输出目录用于调试
        debug_path = output_path.with_suffix('.html')
        Path(html_path).rename(debug_path)


def main():
    print("🔄 生成小红书内容（v6 爆款优化版）...\n")
    
    data = load_summary()
    post = generate_daily_post(data)
    
    if not post:
        print("❌ 没有内容可生成")
        sys.exit(1)
    
    date_str = post["date"]
    output_dir = OUTPUT_DIR / date_str
    output_dir.mkdir(parents=True, exist_ok=True)
    
    txt_path = output_dir / "post.txt"
    txt_content = f"【标题】\n{post['title']}\n\n【正文】\n{post['body']}\n\n【标签】\n{post['tags']}\n"
    txt_path.write_text(txt_content, encoding='utf-8')
    print(f"✅ post.txt")
    
    cards = [
        ("1_overview.png", generate_card_html_overview(post)),
    ]
    
    for i, insight in enumerate(post["insights"]):
        html = generate_card_html_insight_from_data(post["date"], insight, i)
        if html:
            cards.append((f"{i+2}_insight.png", html))
    
    for filename, html in cards:
        if html:
            output_path = output_dir / filename
            screenshot_card(html, output_path, keep_html=True)
            print(f"✅ {filename}")
    
    print(f"\n📁 目录: {output_dir}")
    print(f"✅ 完成！共生成 1 条文案 + {len(cards)} 张配图")
    print(f"💡 下一步: 查看飞书推送，复制文案+保存配图+发布")
    print(f"⏰ 建议发布时间: 12:00 / 18:30 / 21:00")


if __name__ == "__main__":
    main()
