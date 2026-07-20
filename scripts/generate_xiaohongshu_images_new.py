#!/usr/bin/env python3
"""
小红书图片生成器 - 基于最新文案生成配图
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

WIKI_DIR = Path("/home/admin/ai-radar-wiki")
OUTPUT_DIR = WIKI_DIR / "xiaohongshu" / "2026-07-20"

def load_post():
    """加载最新文案"""
    post_path = OUTPUT_DIR / "post.txt"
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析文案
    lines = content.split('\n')
    title = ""
    body = ""
    pm_action = ""
    tags = ""
    
    current_section = None
    for line in lines:
        if line.startswith("【标题】"):
            current_section = "title"
        elif line.startswith("【正文】"):
            current_section = "body"
        elif line.startswith("【PM启示】"):
            current_section = "pm_action"
        elif line.startswith("【标签】"):
            current_section = "tags"
        elif current_section == "title" and line.strip():
            title = line.strip()
        elif current_section == "body":
            body += line + "\n"
        elif current_section == "pm_action" and line.strip():
            pm_action = line.strip()
        elif current_section == "tags" and line.strip():
            tags = line.strip()
    
    return {
        "title": title,
        "body": body.strip(),
        "pm_action": pm_action,
        "tags": tags
    }

def generate_overview_html(post):
    """生成总览卡片 HTML"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: 1080px;
            height: 1440px;
            font-family: -apple-system, "PingFang SC", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
        }}
        .card {{
            width: 100%;
            height: 100%;
            background: white;
            border-radius: 32px;
            padding: 60px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
        }}
        .logo {{
            font-size: 32px;
            font-weight: 700;
            color: #667eea;
        }}
        .date {{
            font-size: 24px;
            color: #999;
        }}
        .title {{
            font-size: 48px;
            font-weight: 700;
            color: #1a1a1a;
            line-height: 1.3;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 4px solid #667eea;
        }}
        .content {{
            font-size: 28px;
            color: #333;
            line-height: 1.6;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 24px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="logo">🔥 AI Radar</div>
            <div class="date">2026-07-20</div>
        </div>
        <div class="title">{post['title']}</div>
        <div class="content">{post['body'][:300]}...</div>
        <div class="footer">📊 完整情报见主页简介</div>
    </div>
</body>
</html>"""

def generate_insight_html(post, index):
    """生成洞察卡片 HTML"""
    # 提取要点
    lines = post['body'].split('\n')
    points = []
    for line in lines:
        if line.startswith("✅ 要点"):
            points.append(line)
    
    if index >= len(points):
        return None
    
    point = points[index]
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: 1080px;
            height: 1440px;
            font-family: -apple-system, "PingFang SC", sans-serif;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
        }}
        .card {{
            width: 100%;
            height: 100%;
            background: white;
            border-radius: 32px;
            padding: 60px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
        }}
        .badge {{
            background: #f5576c;
            color: white;
            padding: 12px 24px;
            border-radius: 24px;
            font-size: 28px;
            font-weight: 600;
        }}
        .date {{
            font-size: 24px;
            color: #999;
        }}
        .title {{
            font-size: 44px;
            font-weight: 700;
            color: #1a1a1a;
            line-height: 1.3;
            margin-bottom: 40px;
        }}
        .content {{
            font-size: 28px;
            color: #333;
            line-height: 1.6;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 24px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="badge">💡 洞察 {index+1}</div>
            <div class="date">2026-07-20</div>
        </div>
        <div class="title">{point}</div>
        <div class="content">{post['pm_action']}</div>
        <div class="footer">AI Radar · 每日情报</div>
    </div>
</body>
</html>"""

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
        print(f"  ⚠️ 截图失败: {e}")
        Path(html_path).unlink(missing_ok=True)
        return False

def main():
    print("🔄 生成小红书配图（基于最新文案）...\n")
    
    # 加载最新文案
    post = load_post()
    print(f"✅ 加载文案成功")
    print(f"   标题: {post['title'][:30]}...")
    print()
    
    # 生成图片
    cards = [
        ("1_overview.png", generate_overview_html(post)),
    ]
    
    for i in range(3):
        html = generate_insight_html(post, i)
        if html:
            cards.append((f"{i+2}_insight.png", html))
    
    for filename, html in cards:
        if html:
            output_path = OUTPUT_DIR / filename
            print(f"📤 生成: {filename}")
            if screenshot_card(html, output_path):
                print(f"   ✅ 成功")
            else:
                print(f"   ❌ 失败")
    
    print()
    print("✅ 完成！")

if __name__ == "__main__":
    main()
