#!/usr/bin/env python3
"""
小红书内容生成器 - 最终版
生成1条组合笔记（1个日报文案 + 4张配图）

输出：
- 1个日报文案（包含3条核心洞察）
- 4张配图（1张日报总览 + 3张洞察细节）
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
    "medium": ["#ChatGPT", "#程序员日常", "#职场干货", "#自我提升", "#AI写作"],
    "longtail": ["#AI写代码", "#自动化办公", "#AI产品经理", "#效率神器推荐", "#AI日报"],
    "trending": ["#最新AI", "#今日AI", "#AI趋势"],
}

# ── 英文→中文翻译 ──
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
    # 7/19 新增
    "Setting up your spare Mac for Claude Code to control": "用闲置Mac搭建Claude Code远程控制节点",
    "Kimi: Threat or menace?": "Kimi：威胁还是机遇？",
    "Fable 5 vs. GPT-5.6 Sol on an NP-Hard Problem": "Fable 5与GPT-5.6 Sol在NP难问题上的对决",
    "What AI did to stackoverflow in a graph": "一张图看懂AI对Stack Overflow的冲击",
    "Why do AI company logos look like buttholes?": "为什么AI公司的logo都长得差不多？",
    "Best Model For The Use Case": "按使用场景选最佳模型",
    "AI Mania Is Eviscerating Global Decision-Making": "AI狂热正在摧毁全球决策能力",
    "Mayor Mamdani Says Landlords Can't Use AI Images to Advertis": "旧金山禁止房东用AI生成虚假租房广告",
}


def load_summary():
    """加载 daily_summary.json"""
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


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
    
    # 兜底：返回原标题
    return title


def pick_tags(n=8):
    """选取标签组合"""
    tags = []
    tags += random.sample(TAG_POOL["large"], min(2, len(TAG_POOL["large"])))
    tags += random.sample(TAG_POOL["medium"], min(2, len(TAG_POOL["medium"])))
    tags += random.sample(TAG_POOL["longtail"], min(2, len(TAG_POOL["longtail"])))
    tags += random.sample(TAG_POOL["trending"], min(1, len(TAG_POOL["trending"])))
    return " ".join(tags[:n])


def simplify_narrative(title):
    """学术标题→口语化中文"""
    full_replacements = [
        ("AI产业从能力军备竞赛转向生态与合规博弈", "苹果起诉OpenAI，AI人才争夺战升级"),
        ("AI产业从能力竞赛转向生态合规博弈", "苹果起诉OpenAI，AI人才争夺战升级"),
        ("隐私与安全成为AI产品设计的强制性约束", "隐私安全成红线，AI产品必须过这关"),
        ("隐私与安全成为AI产品设计的必须重视", "隐私安全成红线，AI产品必须过这关"),
        ("AI代理从辅助工具演变为自主经济参与者", "AI智能体进化了，能自己赚钱了"),
        ("AI代理从辅助工具演变为能自己赚钱了", "AI智能体进化了，能自己赚钱了"),
        ("Vertu高价AI代理体验评测", "Vertu高价AI智能体体验评测"),
        # LLM 生成的标题也需要翻译
        ("Fable 5 vs. GPT-5.6 Sol on an NP-Hard Problem", "GPT-5.6 Sol攻克NP难题，模型能力分化加剧"),
        ("AI能力分化与自主执行成为新范式", "AI能力分化：从通用大模型到任务专用代理"),
        ("AI应用生态震荡：监管收紧与社区重构", "AI监管收紧，社区生态面临重构"),
        ("AI产品设计趋同与决策依赖风险", "AI产品设计同质化，过度依赖成隐患"),
    ]
    for old, new in full_replacements:
        if old in title:
            return new
    
    # 如果标题主要是英文，尝试翻译
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
    """生成开头钩子"""
    hooks = [
        "今天AI圈有大动作！",
        "这3条AI消息，条条影响你的工作！",
        "AI圈又出大事了！",
        "今天AI圈发生了不少事，我帮你划重点 👇",
        "AI趋势速览，建议先收藏 🔖",
    ]
    return random.choice(hooks)


def generate_cta():
    """生成互动引导"""
    ctas = [
        "💬 你觉得哪条最影响你的工作？评论区聊聊",
        "💬 这条趋势对你做产品有什么启发？",
        "💬 你们最想看哪个方向的深度解读？",
        "💬 你觉得AI会取代你的工作吗？",
        "🔖 建议先收藏，用到的时候找得到",
    ]
    return random.choice(ctas)


def generate_daily_post(data):
    """生成日报文案（包含3条核心洞察）"""
    ds = data.get("daily_summary", {})
    date_str = ds.get("date", datetime.now().strftime("%Y-%m-%d"))
    narratives = ds.get("narratives", [])
    insights = ds.get("insights", [])
    
    if not narratives and not insights:
        return None
    
    # 如果 narratives 少于3条，从 insights 中补充（去重）
    all_items = narratives.copy()
    existing_titles = {n.get("title", "") for n in narratives}
    
    for insight in insights:
        if len(all_items) >= 3:
            break
        insight_title = insight.get("narrative_title", "")
        # 跳过已存在的标题
        if insight_title in existing_titles:
            continue
        # 将 insight 转换为 narrative 格式
        all_items.append({
            "title": insight_title,
            "type": "insight",
            "pillar": insight.get("pillar", ""),
        })
        existing_titles.add(insight_title)
    
    # 标题
    title_options = [
        f"💥 {date_str} AI日报｜{len(all_items)}条情报速览",
        f"🔥 今天AI圈{len(all_items)}件大事，建议先收藏",
        f"📢 AI人必看！今天{len(all_items)}条重磅消息",
    ]
    title = random.choice(title_options)
    
    # 正文
    body_lines = [
        generate_hook(),
        "",
        f"整理了{len(all_items)}条最重要的 👇",
        "",
    ]
    
    for i, item in enumerate(all_items[:3], 1):
        simple = simplify_narrative(item["title"])
        body_lines.append(f"{'①②③④⑤'[i-1]} {simple}")
    
    # 添加细节（从 insights 中提取 evidence，融入多源数据和 KOL 观点）
    if insights:
        body_lines.append("")
        body_lines.append("具体信号 👇")
        body_lines.append("")
        
        # 收集所有 evidence，优先展示 Twitter KOL 观点
        all_evidence = []
        for insight in insights[:3]:
            for ev in insight.get("evidence", []):
                all_evidence.append(ev)
        
        # 排序：Twitter 优先（KOL 观点更有吸引力）
        all_evidence.sort(key=lambda e: (0 if e.get("source_type") == "twitter" else 1, -e.get("score", 0)))
        
        # 展示前5条
        for ev in all_evidence[:5]:
            source_type = ev.get("source_type", "unknown")
            author = ev.get("author", "")
            ev_title = ev.get("title", "")
            
            if source_type == "twitter" and author:
                # Twitter KOL 观点：显示作者和翻译后的内容
                title_zh = translate_title(ev_title)
                body_lines.append(f"🐦 @{author}: {title_zh}")
            else:
                # 其他来源：翻译英文标题
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
    """生成日报总览卡片 HTML"""
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
    
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1080px; height: 1440px;
    font-family: -apple-system, "PingFang SC", sans-serif;
    background: #FFF5F5;
    display: flex; align-items: center; justify-content: center;
}}
.card {{
    width: 960px;
    background: white;
    border-radius: 32px;
    padding: 64px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}}
.header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 40px;
}}
.logo {{
    font-size: 32px; font-weight: 700; color: #FF385C;
}}
.date {{
    font-size: 26px; color: #999;
}}
.headline {{
    font-size: 48px; font-weight: 700; color: #1a1a1a;
    line-height: 1.4; letter-spacing: -1px;
    margin-bottom: 48px;
    padding-bottom: 32px;
    border-bottom: 4px solid #FF385C;
}}
.item {{
    display: flex; align-items: flex-start; gap: 24px;
    padding: 32px 0;
    border-bottom: 1px solid #f5f5f5;
}}
.item:last-child {{ border-bottom: none; }}
.item-num {{
    width: 60px; height: 60px;
    background: #FF385C; color: white;
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
    <div class="headline">{headline}</div>
    {items_html}
    <div class="footer">📊 完整情报见主页简介</div>
</div>
</body></html>"""


def generate_card_html_insight(post, index):
    """生成洞察卡片 HTML"""
    date_str = post["date"]
    insights = post["insights"]
    
    if index >= len(insights):
        return None
    
    insight = insights[index]
    return generate_card_html_insight_from_data(date_str, insight, index)


def generate_card_html_insight_from_data(date_str, insight, index):
    """从 insight 数据生成洞察卡片 HTML"""
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
    
    colors = {
        "💰": {"primary": "#7C3AED", "bg": "#F5F3FF"},
        "🤖": {"primary": "#2563EB", "bg": "#F0F7FF"},
        "📱": {"primary": "#FF385C", "bg": "#FFF5F5"},
        "🔧": {"primary": "#059669", "bg": "#ECFDF5"},
    }
    color = colors.get(emoji, {"primary": "#7C3AED", "bg": "#F5F3FF"})
    
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1080px; height: 1440px;
    font-family: -apple-system, "PingFang SC", sans-serif;
    background: {color['bg']};
    display: flex; align-items: center; justify-content: center;
}}
.card {{
    width: 960px;
    background: white;
    border-radius: 32px;
    padding: 56px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}}
.header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 32px;
}}
.category {{
    background: {color['primary']};
    color: white;
    padding: 8px 20px;
    border-radius: 20px;
    font-size: 24px;
    font-weight: 600;
}}
.date {{
    font-size: 24px;
    color: #999;
}}
.title {{
    font-size: 48px;
    font-weight: 700;
    color: #1a1a1a;
    line-height: 1.4;
    margin-bottom: 24px;
}}
.divider {{
    width: 80px;
    height: 5px;
    background: {color['primary']};
    border-radius: 3px;
    margin-bottom: 32px;
}}
.section {{
    margin-bottom: 32px;
}}
.section-title {{
    font-size: 26px;
    color: {color['primary']};
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: 1px;
}}
.event {{
    background: #F9FAFB;
    border-left: 4px solid {color['primary']};
    padding: 20px;
    margin-bottom: 16px;
    border-radius: 8px;
}}
.event-title {{
    font-size: 30px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 8px;
}}
.event-detail {{
    font-size: 26px;
    color: #666;
    line-height: 1.5;
}}
.impact {{
    background: {color['bg']};
    border-radius: 16px;
    padding: 24px;
    margin-top: 32px;
}}
.impact-title {{
    font-size: 26px;
    color: {color['primary']};
    font-weight: 600;
    margin-bottom: 12px;
}}
.impact-text {{
    font-size: 28px;
    color: #333;
    line-height: 1.5;
}}
.footer {{
    margin-top: 32px;
    text-align: center;
    font-size: 22px;
    color: #bbb;
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


def screenshot_card(html_content, output_path):
    """截图卡片"""
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
    Path(html_path).unlink()


def main():
    print("🔄 生成小红书内容（最终版）...\n")
    
    data = load_summary()
    post = generate_daily_post(data)
    
    if not post:
        print("❌ 没有内容可生成")
        sys.exit(1)
    
    date_str = post["date"]
    output_dir = OUTPUT_DIR / date_str
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存文案
    txt_path = output_dir / "post.txt"
    txt_content = f"【标题】\n{post['title']}\n\n【正文】\n{post['body']}\n\n【标签】\n{post['tags']}\n"
    txt_path.write_text(txt_content, encoding='utf-8')
    print(f"✅ post.txt")
    
    # 生成并截图卡片
    cards = [
        ("1_overview.png", generate_card_html_overview(post)),
    ]
    
    # 为每个 insight 生成一张图
    for i, insight in enumerate(post["insights"]):
        html = generate_card_html_insight_from_data(post["date"], insight, i)
        if html:
            cards.append((f"{i+2}_insight.png", html))
    
    for filename, html in cards:
        if html:
            output_path = output_dir / filename
            screenshot_card(html, output_path)
            print(f"✅ {filename}")
    
    print(f"\n📁 目录: {output_dir}")
    print(f"✅ 完成！共生成 1 条文案 + {len(cards)} 张配图")
    print(f"💡 下一步: 查看飞书推送，复制文案+保存配图+发布")
    print(f"⏰ 建议发布时间: 周二至周四 12:00")


if __name__ == "__main__":
    main()
