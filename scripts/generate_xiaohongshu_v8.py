#!/usr/bin/env python3
"""
小红书内容生成器 v8 - 基于爆款研究报告优化

核心改进：
1. 使用研究报告中的5种标题结构模式
2. 使用黄金正文结构（钩子+要点+总结+CTA）
3. 基于PM关注的5个核心点生成PM启示
4. 使用研究报告中的互动技巧
5. 配图使用高饱和度配色，3:4竖版
"""

import json
import sys
import random
from datetime import datetime
from pathlib import Path

WIKI_DIR = Path("/home/admin/ai-radar-wiki")
SUMMARY_PATH = WIKI_DIR / "daily_summary.json"
OUTPUT_DIR = WIKI_DIR / "xiaohongshu"

# ── 标题结构模式（基于研究报告）──
TITLE_PATTERNS = {
    "数字+利益+身份": [
        "这{count}个AI趋势让PM效率翻倍，第{highlight}个绝了",
        "{count}个AI方向决定未来走向，产品经理必看",
        "这{count}条AI情报帮PM省下{hours}小时，太香了",
    ],
    "身份+反差+悬念": [
        "PM用了这个AI分析方法后，同事以为我开挂了",
        "做了{years}年AI产品，说几个反常识的真相",
        "AI产品经理的日常工作，90%的人不知道",
    ],
    "时间+收益+情绪": [
        "每天10分钟看AI情报，我的产品决策让老板直呼专业",
        "用了这个方法做竞品分析，效率提升300%",
        "后悔没早知道！这个AI趋势帮我省了{hours}小时",
    ],
    "对比+颠覆": [
        "还在手动做市场调研？这个AI方法3分钟搞定",
        "别再交智商税了！这{count}个AI工具完全免费",
        "传统PM vs AI PM，差距竟然这么大",
    ],
    "权威+稀缺": [
        "大厂PM都在偷偷用的AI分析方法，今天分享给你",
        "2026年最值得关注的{count}个AI趋势，第{highlight}个太重要了",
        "AI产品经理必备的情报清单，建议收藏",
    ],
}

# ── 开头钩子模板（基于研究报告）──
HOOK_TEMPLATES = {
    "痛点共鸣": [
        "每次做竞品分析都头大？",
        "作为产品经理，最痛苦的不是需求变更，是...",
        "每次写PRD都要花一整天，改到第三版就想辞职...",
    ],
    "成果展示": [
        "用这个AI分析方法，我3分钟生成了一份完整的市场调研报告",
        "上周用AI辅助工作，提前2小时下班，老板还夸我效率高",
        "自从用了这几个AI工具，我的工作效率直接翻倍",
    ],
    "反常识": [
        "做了3年产品经理，我发现90%的PRD写法都是错的",
        "别再学Python了，2026年PM最该学的AI技能是这个",
        "AI时代最值钱的5种能力，90%的人不知道",
    ],
    "故事经历": [
        "上个月面试字节，面试官问了一个让我懵掉的AI问题...",
        "从传统PM转型AI产品经理，这半年我经历了什么",
        "做了3年AI产品，有些话不吐不快",
    ],
    "清单框架": [
        "整理了AI产品经理必备的情报清单，建议收藏",
        "这份AI学习路线图，帮你少走3年弯路",
        "分享一个我用AI做竞品分析的标准流程",
    ],
}

# ── CTA模板（基于研究报告）──
CTA_TEMPLATES = {
    "引发评论": [
        "💬 你们团队在用哪个AI工具？评论区交流一下～",
        "💬 你觉得AI会取代产品经理吗？说说你的看法",
        "💬 这几个趋势你同意哪个？反对哪个？评论区battle一下",
    ],
    "引导收藏": [
        "📌 建议先收藏🔖 用到的时候方便找",
        "📌 码住！以后一定用得上",
        "📌 收藏=学会，下次用的时候不用翻找了",
    ],
    "促进转发": [
        "🔗 转给你身边需要的产品经理朋友～",
        "🔗 @你那个还在手动写PRD的同事",
        "🔗 分享给团队，大家一起提效",
    ],
}

# ── PM启示模板（基于PM关注的5个核心点）──
PM_INSIGHT_TEMPLATES = {
    "效率提升": [
        "✅ 行动建议：评估现有工作流程，找出可以用AI提效的环节。优先从重复性工作开始，比如竞品分析、市场调研、文档整理。",
        "✅ 行动建议：建立AI工具评估体系，按场景选择最优工具。关注可量化的时间节省，而不是模糊的效率提升。",
    ],
    "职业发展": [
        "✅ 行动建议：关注AI时代PM能力模型的变化。补充技术理解、数据思维、Prompt Engineering等能力。",
        "✅ 行动建议：不要为了追风口而转型，先问问自己是否真的对AI产品感兴趣。这条路不容易，但值得。",
    ],
    "技能学习": [
        "✅ 行动建议：建立AI学习路线图，平衡深度和广度。优先学习能立即应用的知识，而不是追求全面。",
        "✅ 行动建议：关注AI产品经理的核心技能：理解模型能力边界、设计评估指标、和算法同学有效沟通。",
    ],
    "行业洞察": [
        "✅ 行动建议：建立AI行业情报收集机制，定期review市场趋势。关注大厂在做什么，但更重要的是理解背后的逻辑。",
        "✅ 行动建议：深入分析AI产品的设计逻辑，不只是看功能，要看它解决了什么问题、如何平衡技术限制和用户需求。",
    ],
    "实战经验": [
        "✅ 行动建议：记录自己的踩坑经历和成功经验，形成可复用的方法论。分享出来，帮助他人也帮助自己。",
        "✅ 行动建议：关注别人的实战案例，学习可复用的方法。但要注意场景差异，不要盲目照搬。",
    ],
}


def load_summary():
    """加载 daily_summary.json"""
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_title(narratives, insights):
    """基于研究报告生成爆款标题"""
    count = len(narratives) + len(insights)
    highlight = random.randint(1, min(3, count))
    hours = random.choice([10, 20, 30, 50])
    years = random.choice([2, 3, 5])
    
    # 随机选择一种标题模式
    pattern_name = random.choice(list(TITLE_PATTERNS.keys()))
    templates = TITLE_PATTERNS[pattern_name]
    template = random.choice(templates)
    
    # 填充模板
    title = template.format(count=count, highlight=highlight, hours=hours, years=years)
    
    return title


def generate_hook():
    """基于研究报告生成开头钩子"""
    hook_type = random.choice(list(HOOK_TEMPLATES.keys()))
    templates = HOOK_TEMPLATES[hook_type]
    return random.choice(templates)


def generate_body(narratives, insights):
    """基于研究报告生成正文"""
    body_lines = []
    
    # 开头钩子
    hook = generate_hook()
    body_lines.append(hook)
    body_lines.append("")
    body_lines.append("—————————————")
    body_lines.append("")
    
    # 核心内容（3-5个要点）
    all_items = narratives + insights
    for i, item in enumerate(all_items[:3], 1):
        title = item.get("title", "") or item.get("narrative_title", "")
        body = item.get("body", "") or item.get("insight", "")
        
        # 小标题
        body_lines.append(f"✅ 要点{i}：{title}")
        
        # 2-3句说明
        if body:
            sentences = body.split("。")[:2]
            for sent in sentences:
                if sent.strip():
                    body_lines.append(sent.strip() + "。")
        
        body_lines.append("")
    
    body_lines.append("—————————————")
    body_lines.append("")
    
    # 总结
    body_lines.append("💡 总结：")
    body_lines.append("AI是工具，不是目的。")
    body_lines.append("做产品的核心能力永远不变：理解用户、定义问题、创造价值。")
    body_lines.append("")
    
    # CTA
    cta_type = random.choice(list(CTA_TEMPLATES.keys()))
    cta = random.choice(CTA_TEMPLATES[cta_type])
    body_lines.append(cta)
    
    return "\n".join(body_lines)


def generate_pm_insight(insights):
    """基于PM关注的5个核心点生成PM启示"""
    if not insights:
        return random.choice(PM_INSIGHT_TEMPLATES["效率提升"])
    
    # 根据insight内容选择最相关的PM启示
    first_insight = insights[0]
    title = first_insight.get("narrative_title", "").lower()
    
    if "效率" in title or "工具" in title or "方法" in title:
        return random.choice(PM_INSIGHT_TEMPLATES["效率提升"])
    elif "转型" in title or "职业" in title or "能力" in title:
        return random.choice(PM_INSIGHT_TEMPLATES["职业发展"])
    elif "学习" in title or "技能" in title:
        return random.choice(PM_INSIGHT_TEMPLATES["技能学习"])
    elif "趋势" in title or "行业" in title or "洞察" in title:
        return random.choice(PM_INSIGHT_TEMPLATES["行业洞察"])
    else:
        return random.choice(PM_INSIGHT_TEMPLATES["实战经验"])


def generate_cta():
    """基于研究报告生成CTA"""
    cta_type = random.choice(list(CTA_TEMPLATES.keys()))
    templates = CTA_TEMPLATES[cta_type]
    return random.choice(templates)


def generate_tags():
    """生成标签"""
    return [
        "#AI工具",
        "#效率提升",
        "#科技数码",
        "#人工智能",
        "#AI产品经理",
        "#AI日报",
        "#AI趋势",
    ]


def generate_post(data):
    """生成完整的小红书帖子"""
    ds = data.get("daily_summary", {})
    narratives = ds.get("narratives", [])
    insights = ds.get("insights", [])
    
    if not narratives and not insights:
        return None
    
    title = generate_title(narratives, insights)
    body = generate_body(narratives, insights)
    pm_action = generate_pm_insight(insights)
    cta = generate_cta()
    tags = generate_tags()
    
    return {
        "title": title,
        "body": body,
        "pm_action": pm_action,
        "cta": cta,
        "tags": tags,
    }


def generate_card_html_overview(content, date_str):
    """生成总览卡片HTML（基于研究报告的配图设计原则）"""
    title = content.get("title", "")
    body = content.get("body", "")
    
    # 提取正文前3行作为核心内容
    body_lines = [line for line in body.split('\n') if line.strip()][:3]
    core_content = '\n'.join(body_lines)
    
    # 高饱和度配色（科技风格）
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1080px; height: 1440px;
    font-family: -apple-system, "PingFang SC", sans-serif;
    background: linear-gradient(135deg, #1A237E 0%, #00BCD4 100%);
    display: flex; align-items: center; justify-content: center;
}}
.card {{
    width: 100%; height: 100%;
    background: rgba(255,255,255,0.95);
    padding: 100px 80px;
    display: flex; flex-direction: column;
}}
.header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 60px;
}}
.logo {{
    font-size: 42px; font-weight: 700; color: #1A237E;
}}
.date {{
    font-size: 32px; color: #666;
}}
.title {{
    font-size: 56px; font-weight: 700; color: #1a1a1a;
    line-height: 1.3; letter-spacing: -1px;
    margin-bottom: 60px;
}}
.content {{
    font-size: 36px; color: #333;
    line-height: 1.6;
    margin-bottom: 60px;
}}
.footer {{
    margin-top: auto;
    text-align: center;
    font-size: 28px;
    color: #999;
}}
</style></head>
<body>
<div class="card">
    <div class="header">
        <div class="logo">🔥 AI Radar</div>
        <div class="date">{date_str}</div>
    </div>
    <div class="title">{title}</div>
    <div class="content">{core_content}</div>
    <div class="footer">📊 完整情报见主页简介</div>
</div>
</body></html>"""


def generate_card_html_insight(content, insights, index, date_str):
    """生成洞察卡片HTML（基于研究报告的配图设计原则）"""
    if index >= len(insights):
        return None
    
    insight = insights[index]
    title = insight.get("narrative_title", "")
    body = insight.get("insight", "")
    
    # 提取body前2句
    sentences = body.split("。")[:2]
    core_content = "。".join(sentences) + "。" if sentences else ""
    
    # 高饱和度配色（每个卡片不同主色）
    colors = [
        {"primary": "#FF6B35", "bg": "#FFF5F0", "gradient": "linear-gradient(135deg, #FF6B35 0%, #FF9A56 100%)"},
        {"primary": "#2196F3", "bg": "#F0F7FF", "gradient": "linear-gradient(135deg, #2196F3 0%, #64B5F6 100%)"},
        {"primary": "#9C27B0", "bg": "#F5F0FF", "gradient": "linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%)"},
    ]
    color = colors[index % len(colors)]
    
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
    background: rgba(255,255,255,0.95);
    padding: 100px 80px;
    display: flex; flex-direction: column;
}}
.header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 60px;
}}
.badge {{
    background: {color['primary']};
    color: white;
    padding: 16px 32px;
    border-radius: 32px;
    font-size: 32px;
    font-weight: 600;
}}
.date {{
    font-size: 32px;
    color: #666;
}}
.title {{
    font-size: 52px;
    font-weight: 700;
    color: #1a1a1a;
    line-height: 1.3;
    margin-bottom: 60px;
}}
.content {{
    font-size: 36px;
    color: #333;
    line-height: 1.6;
    margin-bottom: 60px;
}}
.footer {{
    margin-top: auto;
    text-align: center;
    font-size: 28px;
    color: #999;
}}
</style></head>
<body>
<div class="card">
    <div class="header">
        <div class="badge">💡 洞察 {index+1}</div>
        <div class="date">{date_str}</div>
    </div>
    <div class="title">{title}</div>
    <div class="content">{core_content}</div>
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
    try:
        subprocess.run(["python3", "-c", script], check=True, timeout=30)
        Path(html_path).unlink()
        return True
    except Exception as e:
        print(f"   ⚠️ 截图失败: {e}")
        Path(html_path).unlink(missing_ok=True)
        return False


def main():
    print("🔄 生成小红书内容（v8 爆款优化版）...\n")
    
    # 加载数据
    print("📂 加载数据...")
    data = load_summary()
    ds = data.get("daily_summary", {})
    date_str = ds.get("date", datetime.now().strftime("%Y-%m-%d"))
    narratives = ds.get("narratives", [])
    insights = ds.get("insights", [])
    print(f"   日期: {date_str}")
    print(f"   Narratives: {len(narratives)}")
    print(f"   Insights: {len(insights)}")
    print()
    
    # 生成内容
    print("✍️ 生成内容...")
    content = generate_post(data)
    if not content:
        print("❌ 生成失败")
        sys.exit(1)
    print("   ✅ 内容生成完成")
    print()
    
    # 保存文案
    print("💾 保存文案...")
    output_dir = OUTPUT_DIR / date_str
    output_dir.mkdir(parents=True, exist_ok=True)
    
    txt_path = output_dir / "post.txt"
    txt_content = f"""【标题】
{content['title']}

【正文】
{content['body']}

【PM启示】
{content['pm_action']}

【标签】
{' '.join(content['tags'])}
"""
    txt_path.write_text(txt_content, encoding='utf-8')
    print(f"   ✅ post.txt")
    print()
    
    # 生成配图
    print("🎨 生成配图...")
    cards = [
        ("1_overview.png", generate_card_html_overview(content, date_str)),
    ]
    
    for i in range(3):
        html = generate_card_html_insight(content, insights, i, date_str)
        if html:
            cards.append((f"{i+2}_insight.png", html))
    
    for filename, html in cards:
        if html:
            output_path = output_dir / filename
            if screenshot_card(html, output_path):
                print(f"   ✅ {filename}")
            else:
                # 检查是否有旧版本
                if output_path.exists():
                    print(f"   ℹ️ {filename} 使用旧版本")
    print()
    
    print(f"📁 目录: {output_dir}")
    print(f"✅ 完成！共生成 1 条文案 + {len(cards)} 张配图")
    print(f"💡 下一步: 查看飞书推送，复制文案+保存配图+发布")
    print(f"⏰ 建议发布时间: 20:00-22:00（下班后黄金时段）")


if __name__ == "__main__":
    main()
