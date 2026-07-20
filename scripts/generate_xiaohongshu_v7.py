#!/usr/bin/env python3
"""
小红书内容生成器 v7 — LLM 驱动的内容创作系统

核心理念：从"信息搬运"到"内容创作"
- 用 LLM 进行深度分析和内容创作
- 生成有洞察、有价值的内容
- 符合小红书平台调性

架构：
1. 数据准备：从 daily_summary.json 提取 narratives + insights
2. LLM 深度分析：识别核心趋势、提炼 PM 关心的洞察
3. LLM 内容创作：生成标题、正文、PM启示、互动引导
4. 配图生成：设计符合小红书审美的卡片
5. 输出：post.txt + 4张配图
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 添加 ai_model_router 路径
sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))
from ai_model_router import call_llm

WIKI_DIR = Path("/home/admin/ai-radar-wiki")
SUMMARY_PATH = WIKI_DIR / "daily_summary.json"
OUTPUT_DIR = WIKI_DIR / "xiaohongshu"


def load_summary():
    """加载 daily_summary.json"""
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def llm_deep_analysis(data):
    """
    Phase 2: LLM 深度分析
    
    输入：daily_summary.json（narratives + insights）
    输出：内容创作 brief（核心趋势 + PM洞察 + 创作角度）
    """
    ds = data.get("daily_summary", {})
    narratives = ds.get("narratives", [])
    insights = ds.get("insights", [])
    
    # 构建 narratives 文本
    narratives_text = ""
    for i, n in enumerate(narratives, 1):
        narratives_text += f"{i}. {n.get('title', '')}\n"
        narratives_text += f"   {n.get('body', '')[:200]}\n\n"
    
    # 构建 insights 文本
    insights_text = ""
    for i, ins in enumerate(insights, 1):
        insights_text += f"{i}. [{ins.get('pillar', '')}] {ins.get('narrative_title', '')}\n"
        insights_text += f"   {ins.get('insight', '')[:200]}\n"
        evidence = ins.get('evidence', [])
        if evidence:
            insights_text += f"   证据：{evidence[0].get('title', '')}\n"
        insights_text += "\n"
    
    prompt = f"""基于以下AI情报，生成小红书内容创作brief。

Narratives:
{narratives_text}

Insights:
{insights_text}

输出JSON格式：
{{
  "core_trends": ["趋势1", "趋势2", "趋势3"],
  "pm_insights": [
    {{
      "phenomenon": "现象",
      "cause": "原因",
      "impact": "影响",
      "action": "具体行动建议"
    }}
  ],
  "content_angle": "内容角度",
  "hook_idea": "开头钩子",
  "interaction_strategy": "互动策略"
}}"""

    print("🔍 LLM 深度分析中...")
    result = call_llm(
        prompt=prompt,
        system_prompt="你是AI内容创作专家，擅长深度分析和内容策划。输出有效的JSON。",
        model_type="analysis",
        temperature=0.5,
        max_tokens=2000,
        require_json=True
    )
    
    if not result:
        print("❌ LLM 分析失败，使用降级方案")
        # 降级方案：基于规则生成 brief
        return {
            "core_trends": [n.get("title", "") for n in narratives[:3]],
            "pm_insights": [
                {
                    "phenomenon": ins.get("narrative_title", ""),
                    "cause": ins.get("insight", "")[:100],
                    "impact": "对PM的产品决策有重要影响",
                    "action": "深入分析这一趋势，评估对产品的影响"
                }
                for ins in insights[:3]
            ],
            "content_angle": "深度解读AI趋势，为PM提供 actionable insights",
            "hook_idea": "用具体案例和数据吸引PM注意",
            "interaction_strategy": "提出开放性问题，引发PM讨论"
        }
    
    print("✅ LLM 分析完成")
    return result


def llm_content_creation(brief, data):
    """
    Phase 3: LLM 内容创作
    
    输入：内容创作 brief + 原始数据
    输出：标题 + 正文 + PM启示 + 互动引导 + 标签
    """
    ds = data.get("daily_summary", {})
    date_str = ds.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    # 构建 brief 文本
    brief_text = f"""核心趋势：
{chr(10).join(f'• {t}' for t in brief.get('core_trends', []))}

PM洞察：
{chr(10).join(f'• 现象：{i.get("phenomenon", "")}{chr(10)}  原因：{i.get("cause", "")}{chr(10)}  影响：{i.get("impact", "")}{chr(10)}  行动：{i.get("action", "")}' for i in brief.get('pm_insights', []))}

内容角度：{brief.get('content_angle', '')}
开头钩子：{brief.get('hook_idea', '')}
互动策略：{brief.get('interaction_strategy', '')}"""
    
    prompt = f"""基于以下brief，创作小红书内容。

Brief:
{brief_text}

日期: {date_str}

输出JSON格式：
{{
  "title": "标题（18-25字，数字+情绪词+悬念）",
  "body": "正文（300-500字，emoji分段，每段≤3行）",
  "pm_action": "PM启示（具体可操作的行动建议，50-80字）",
  "cta": "互动引导（20-30字）",
  "tags": ["标签1", "标签2", "标签3", "标签4", "标签5", "标签6", "标签7"]
}}"""

    print("✍️ LLM 内容创作中...")
    result = call_llm(
        prompt=prompt,
        system_prompt="你是小红书爆款内容创作专家，擅长为PM群体创作高质量内容。输出有效的JSON。",
        model_type="analysis",
        temperature=0.6,
        max_tokens=2000,
        require_json=True
    )
    
    if not result:
        print("❌ LLM 创作失败，使用降级方案")
        # 降级方案：基于 brief 生成内容
        core_trends = brief.get("core_trends", [])
        pm_insights = brief.get("pm_insights", [])
        
        title = f"🔥 今日AI圈{len(core_trends)}件大事，PM必看"
        
        body_lines = ["💡 今天AI圈有大动作！", ""]
        body_lines.append(f"整理了{len(core_trends)}条最重要的 👇")
        body_lines.append("")
        
        for i, trend in enumerate(core_trends, 1):
            body_lines.append(f"{'①②③④⑤'[i-1]} {trend}")
        
        body_lines.append("")
        body_lines.append("💬 你最关心哪条？评论区聊聊")
        body_lines.append("")
        body_lines.append("📊 完整情报见主页简介")
        
        body = "\n".join(body_lines)
        
        pm_action = pm_insights[0].get("action", "深入分析AI趋势，评估对产品的影响") if pm_insights else "深入分析AI趋势"
        
        return {
            "title": title,
            "body": body,
            "pm_action": pm_action,
            "cta": "💬 你最关心哪条？评论区聊聊",
            "tags": ["#AI工具", "#效率提升", "#科技数码", "#人工智能", "#AI产品经理", "#AI日报", "#AI趋势"]
        }
    
    print("✅ LLM 创作完成")
    return result


def generate_card_html_overview(content, date_str):
    """生成总览卡片 HTML"""
    title = content.get("title", "")
    body = content.get("body", "")
    
    # 提取正文前3行作为核心内容
    body_lines = [line for line in body.split('\n') if line.strip()][:3]
    core_content = '\n'.join(body_lines)
    
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
    background: rgba(255,255,255,0.95);
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
.title {{
    font-size: 56px; font-weight: 700; color: #1a1a1a;
    line-height: 1.3; letter-spacing: -1px;
    margin-bottom: 48px;
}}
.content {{
    font-size: 36px; color: #333;
    line-height: 1.6;
    margin-bottom: 48px;
}}
.footer {{
    margin-top: auto;
    text-align: center;
    font-size: 26px;
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


def generate_card_html_insight(content, brief, index, date_str):
    """生成洞察卡片 HTML"""
    pm_insights = brief.get("pm_insights", [])
    
    if index >= len(pm_insights):
        return None
    
    insight = pm_insights[index]
    phenomenon = insight.get("phenomenon", "")
    cause = insight.get("cause", "")
    impact = insight.get("impact", "")
    action = insight.get("action", "")
    
    # 配色方案
    colors = [
        {"primary": "#FF385C", "bg": "#FFF5F5", "gradient": "linear-gradient(135deg, #FF385C 0%, #F59E0B 100%)"},
        {"primary": "#2563EB", "bg": "#F0F7FF", "gradient": "linear-gradient(135deg, #2563EB 0%, #06B6D4 100%)"},
        {"primary": "#059669", "bg": "#ECFDF5", "gradient": "linear-gradient(135deg, #059669 0%, #10B981 100%)"},
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
    padding: 80px 60px;
    display: flex; flex-direction: column;
}}
.header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 32px;
}}
.badge {{
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
.section {{
    margin-bottom: 32px;
}}
.section-title {{
    font-size: 32px;
    color: {color['primary']};
    font-weight: 600;
    margin-bottom: 16px;
}}
.section-content {{
    font-size: 34px;
    color: #333;
    line-height: 1.5;
}}
.action {{
    background: {color['bg']};
    border-radius: 20px;
    padding: 32px;
    margin-top: auto;
}}
.action-title {{
    font-size: 32px;
    color: {color['primary']};
    font-weight: 600;
    margin-bottom: 16px;
}}
.action-content {{
    font-size: 34px;
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
        <div class="badge">💡 PM洞察 {index+1}</div>
        <div class="date">{date_str}</div>
    </div>
    
    <div class="section">
        <div class="section-title">📌 现象</div>
        <div class="section-content">{phenomenon}</div>
    </div>
    
    <div class="section">
        <div class="section-title">🔍 原因</div>
        <div class="section-content">{cause}</div>
    </div>
    
    <div class="section">
        <div class="section-title">⚡ 影响</div>
        <div class="section-content">{impact}</div>
    </div>
    
    <div class="action">
        <div class="action-title">✅ 行动建议</div>
        <div class="action-content">{action}</div>
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
    print("🔄 生成小红书内容（v7 LLM驱动版）...\n")
    
    # Phase 1: 数据准备
    print("📂 Phase 1: 数据准备")
    data = load_summary()
    ds = data.get("daily_summary", {})
    date_str = ds.get("date", datetime.now().strftime("%Y-%m-%d"))
    print(f"   日期: {date_str}")
    print(f"   Narratives: {len(ds.get('narratives', []))}")
    print(f"   Insights: {len(ds.get('insights', []))}")
    print()
    
    # Phase 2: LLM 深度分析
    print("🔍 Phase 2: LLM 深度分析")
    brief = llm_deep_analysis(data)
    if not brief:
        print("❌ 深度分析失败，退出")
        sys.exit(1)
    print()
    
    # Phase 3: LLM 内容创作
    print("✍️ Phase 3: LLM 内容创作")
    content = llm_content_creation(brief, data)
    if not content:
        print("❌ 内容创作失败，退出")
        sys.exit(1)
    print()
    
    # Phase 4: 配图生成
    print("🎨 Phase 4: 配图生成")
    output_dir = OUTPUT_DIR / date_str
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存文案
    txt_path = output_dir / "post.txt"
    txt_content = f"""【标题】
{content['title']}

【正文】
{content['body']}

【PM启示】
{content['pm_action']}

【互动引导】
{content['cta']}

【标签】
{' '.join(content['tags'])}
"""
    txt_path.write_text(txt_content, encoding='utf-8')
    print(f"   ✅ post.txt")
    
    # 生成配图
    cards = [
        ("1_overview.png", generate_card_html_overview(content, date_str)),
    ]
    
    for i in range(3):
        html = generate_card_html_insight(content, brief, i, date_str)
        if html:
            cards.append((f"{i+2}_insight.png", html))
    
    for filename, html in cards:
        if html:
            output_path = output_dir / filename
            try:
                screenshot_card(html, output_path)
                print(f"   ✅ {filename}")
            except Exception as e:
                print(f"   ⚠️ {filename} 生成失败: {e}")
                # 检查是否有旧版本
                if output_path.exists():
                    print(f"   ℹ️ 使用旧版本: {output_path}")
    
    print()
    print(f"📁 目录: {output_dir}")
    print(f"✅ 完成！共生成 1 条文案 + {len(cards)} 张配图")
    print(f"💡 下一步: 查看飞书推送，复制文案+保存配图+发布")
    print(f"⏰ 建议发布时间: 12:00 / 18:30 / 21:00")


if __name__ == "__main__":
    main()
