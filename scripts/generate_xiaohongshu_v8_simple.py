#!/usr/bin/env python3
"""
小红书内容生成器 v8.1 - 简化版（跳过截图）
基于爆款研究报告，只生成文案，不生成配图
"""

import json
import random
from datetime import datetime
from pathlib import Path

WIKI_DIR = Path("/home/admin/ai-radar-wiki")
SUMMARY_PATH = WIKI_DIR / "daily_summary.json"
OUTPUT_DIR = WIKI_DIR / "xiaohongshu"

# 标题模板
TITLE_TEMPLATES = [
    "这{count}个AI趋势让PM效率翻倍，第{highlight}个绝了",
    "{count}个AI方向决定未来走向，产品经理必看",
    "这{count}条AI情报帮PM省下{hours}小时，太香了",
    "PM用了这个AI分析方法后，同事以为我开挂了",
    "做了{years}年AI产品，说几个反常识的真相",
    "每天10分钟看AI情报，我的产品决策让老板直呼专业",
    "用了这个方法做竞品分析，效率提升300%",
    "大厂PM都在偷偷用的AI分析方法，今天分享给你",
]

# 开头钩子
HOOK_TEMPLATES = [
    "每次做竞品分析都头大？",
    "作为产品经理，最痛苦的不是需求变更，是...",
    "每次写PRD都要花一整天，改到第三版就想辞职...",
    "用这个AI分析方法，我3分钟生成了一份完整的市场调研报告",
    "上周用AI辅助工作，提前2小时下班，老板还夸我效率高",
    "做了3年产品经理，我发现90%的PRD写法都是错的",
    "整理了AI产品经理必备的情报清单，建议收藏",
]

# CTA模板
CTA_TEMPLATES = [
    "💬 你们团队在用哪个AI工具？评论区交流一下～",
    "💬 你觉得AI会取代产品经理吗？说说你的看法",
    "📌 建议先收藏🔖 用到的时候方便找",
    "🔗 转给你身边需要的产品经理朋友～",
]

# PM启示模板
PM_INSIGHT_TEMPLATES = [
    "✅ 行动建议：评估现有工作流程，找出可以用AI提效的环节。优先从重复性工作开始，比如竞品分析、市场调研、文档整理。",
    "✅ 行动建议：关注AI时代PM能力模型的变化。补充技术理解、数据思维、Prompt Engineering等能力。",
    "✅ 行动建议：建立AI学习路线图，平衡深度和广度。优先学习能立即应用的知识，而不是追求全面。",
    "✅ 行动建议：建立AI行业情报收集机制，定期review市场趋势。关注大厂在做什么，但更重要的是理解背后的逻辑。",
    "✅ 行动建议：记录自己的踩坑经历和成功经验，形成可复用的方法论。分享出来，帮助他人也帮助自己。",
]

def load_summary():
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_post(data):
    ds = data.get("daily_summary", {})
    narratives = ds.get("narratives", [])
    insights = ds.get("insights", [])
    
    if not narratives and not insights:
        return None
    
    # 生成标题
    count = len(narratives) + len(insights)
    highlight = random.randint(1, min(3, count))
    hours = random.choice([10, 20, 30, 50])
    years = random.choice([2, 3, 5])
    title_template = random.choice(TITLE_TEMPLATES)
    title = title_template.format(count=count, highlight=highlight, hours=hours, years=years)
    
    # 生成正文
    body_lines = []
    
    # 开头钩子
    hook = random.choice(HOOK_TEMPLATES)
    body_lines.append(hook)
    body_lines.append("")
    body_lines.append("—————————————")
    body_lines.append("")
    
    # 核心内容（3个要点）
    all_items = narratives + insights
    for i, item in enumerate(all_items[:3], 1):
        item_title = item.get("title", "") or item.get("narrative_title", "")
        item_body = item.get("body", "") or item.get("insight", "")
        
        body_lines.append(f"✅ 要点{i}：{item_title}")
        
        if item_body:
            sentences = item_body.split("。")[:2]
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
    cta = random.choice(CTA_TEMPLATES)
    body_lines.append(cta)
    
    body = "\n".join(body_lines)
    
    # PM启示
    pm_action = random.choice(PM_INSIGHT_TEMPLATES)
    
    # 标签
    tags = "#AI工具 #效率提升 #科技数码 #人工智能 #AI产品经理 #AI日报 #AI趋势"
    
    return {
        "title": title,
        "body": body,
        "pm_action": pm_action,
        "tags": tags,
    }

def main():
    print("🔄 生成小红书内容（v8.1 简化版）...\n")
    
    # 加载数据
    data = load_summary()
    ds = data.get("daily_summary", {})
    date_str = ds.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    print(f"📅 日期: {date_str}")
    print(f"📊 Narratives: {len(ds.get('narratives', []))}")
    print(f"💡 Insights: {len(ds.get('insights', []))}")
    print()
    
    # 生成内容
    content = generate_post(data)
    if not content:
        print("❌ 生成失败")
        return
    
    # 保存文案
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
{content['tags']}
"""
    txt_path.write_text(txt_content, encoding='utf-8')
    
    print("✅ 文案生成完成")
    print(f"📁 保存位置: {txt_path}")
    print()
    print("=" * 60)
    print(txt_content)
    print("=" * 60)
    print()
    print("💡 下一步: 复制文案 → 打开小红书 → 粘贴发布")
    print("⏰ 建议发布时间: 20:00-22:00（下班后黄金时段）")

if __name__ == "__main__":
    main()
