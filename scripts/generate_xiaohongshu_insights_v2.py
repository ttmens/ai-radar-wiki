#!/usr/bin/env python3
"""
小红书洞察卡片生成器 v2 — 细节增强版
为每条洞察生成更详细的卡片（包含具体数据、事件背景、影响分析）
"""

import json
from pathlib import Path
from datetime import datetime

WIKI_DIR = Path("/home/admin/ai-radar-wiki")
SUMMARY_PATH = WIKI_DIR / "daily_summary.json"
OUTPUT_DIR = WIKI_DIR / "xiaohongshu" / datetime.now().strftime("%Y-%m-%d")

# 英文→中文翻译
EN_ZH = {
    "Apple targets dozens of OpenAI employees with legal letters": "苹果向OpenAI员工发律师函",
    "How Apple's big lawsuit could disrupt OpenAI's IPO plans": "苹果大诉讼或阻碍OpenAI上市",
    "Apple's lawsuit couldn't come at a worse time for OpenAI": "苹果诉讼来得真不是时候",
    "Patreon stops asking AI bots not to scrape — and starts blocking them": "Patreon不再请求AI别爬数据，直接拦截",
    "The Zoom hack that says 'don't record me'": "Zoom漏洞：'别录我'",
    "VulnHunter: Capital One's agentic AI code security tool": "Capital One推出AI自主代码安全工具",
    "Show HN: On-chain bond market where the issuers are AI agents": "链上债券市场：AI智能体当发行方",
    "Claude Code: Anatomy of a Misfeature": "Claude Code功能缺陷剖析",
}

def translate(title):
    return EN_ZH.get(title, title)

def load_summary():
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_insight_card_2(data):
    """洞察卡片2：苹果 vs OpenAI（商业趋势）"""
    date_str = data["daily_summary"]["date"]
    
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1080px; height: 1440px;
    font-family: -apple-system, "PingFang SC", sans-serif;
    background: #F5F3FF;
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
    background: #7C3AED;
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
    background: #7C3AED;
    border-radius: 3px;
    margin-bottom: 32px;
}}
.section {{
    margin-bottom: 32px;
}}
.section-title {{
    font-size: 26px;
    color: #7C3AED;
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: 1px;
}}
.event {{
    background: #F9FAFB;
    border-left: 4px solid #7C3AED;
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
    background: #FEF3C7;
    border-radius: 16px;
    padding: 24px;
    margin-top: 32px;
}}
.impact-title {{
    font-size: 26px;
    color: #D97706;
    font-weight: 600;
    margin-bottom: 12px;
}}
.impact-text {{
    font-size: 28px;
    color: #92400E;
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
        <div class="category">💰 商业趋势</div>
        <div class="date">{date_str}</div>
    </div>
    
    <div class="title">苹果起诉OpenAI，AI人才争夺战升级</div>
    <div class="divider"></div>
    
    <div class="section">
        <div class="section-title">📌 关键事件</div>
        
        <div class="event">
            <div class="event-title">苹果向OpenAI员工发律师函</div>
            <div class="event-detail">阻止核心人才流动，保护商业秘密</div>
        </div>
        
        <div class="event">
            <div class="event-title">诉讼可能阻碍OpenAI上市</div>
            <div class="event-detail">IPO计划面临法律风险，时机敏感</div>
        </div>
    </div>
    
    <div class="impact">
        <div class="impact-title">💡 对PM的启示</div>
        <div class="impact-text">AI人才成为核心资产，大厂通过法律手段构建人才壁垒。产品经理需要关注：1）技术供应链风险；2）开源vs闭源生态选择；3）合规与数据治理能力。</div>
    </div>
    
    <div class="footer">AI Radar · 每日情报</div>
</div>
</body></html>"""

def generate_insight_card_3(data):
    """洞察卡片3：隐私安全（技术能力）"""
    date_str = data["daily_summary"]["date"]
    
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1080px; height: 1440px;
    font-family: -apple-system, "PingFang SC", sans-serif;
    background: #F0F7FF;
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
    background: #2563EB;
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
    background: #2563EB;
    border-radius: 3px;
    margin-bottom: 32px;
}}
.section {{
    margin-bottom: 32px;
}}
.section-title {{
    font-size: 26px;
    color: #2563EB;
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: 1px;
}}
.event {{
    background: #F9FAFB;
    border-left: 4px solid #2563EB;
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
    background: #DBEAFE;
    border-radius: 16px;
    padding: 24px;
    margin-top: 32px;
}}
.impact-title {{
    font-size: 26px;
    color: #1E40AF;
    font-weight: 600;
    margin-bottom: 12px;
}}
.impact-text {{
    font-size: 28px;
    color: #1E3A8A;
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
        <div class="category">🤖 技术能力</div>
        <div class="date">{date_str}</div>
    </div>
    
    <div class="title">隐私安全成红线，AI产品必须过这关</div>
    <div class="divider"></div>
    
    <div class="section">
        <div class="section-title">📌 关键事件</div>
        
        <div class="event">
            <div class="event-title">Zoom会议被黑客入侵</div>
            <div class="event-detail">黑客提示"别录我"，暴露隐私风险</div>
        </div>
        
        <div class="event">
            <div class="event-title">Patreon直接拦截AI爬虫</div>
            <div class="event-detail">不再协商，技术强制执行数据保护</div>
        </div>
    </div>
    
    <div class="impact">
        <div class="impact-title">💡 对PM的启示</div>
        <div class="impact-text">隐私安全从"可选"变为"必选"。产品经理需要：1）重新设计数据流与用户授权机制；2）引入可控性（用户可选择是否记录）；3）技术强制执行替代协议协商。</div>
    </div>
    
    <div class="footer">AI Radar · 每日情报</div>
</div>
</body></html>"""

def generate_insight_card_4(data):
    """洞察卡片4：AI智能体（产品模式）"""
    date_str = data["daily_summary"]["date"]
    
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
    padding: 56px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}}
.header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 32px;
}}
.category {{
    background: #FF385C;
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
    background: #FF385C;
    border-radius: 3px;
    margin-bottom: 32px;
}}
.section {{
    margin-bottom: 32px;
}}
.section-title {{
    font-size: 26px;
    color: #FF385C;
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: 1px;
}}
.event {{
    background: #F9FAFB;
    border-left: 4px solid #FF385C;
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
    background: #FEE2E2;
    border-radius: 16px;
    padding: 24px;
    margin-top: 32px;
}}
.impact-title {{
    font-size: 26px;
    color: #DC2626;
    font-weight: 600;
    margin-bottom: 12px;
}}
.impact-text {{
    font-size: 28px;
    color: #991B1B;
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
        <div class="category">📱 产品模式</div>
        <div class="date">{date_str}</div>
    </div>
    
    <div class="title">AI智能体进化了，能自己赚钱了</div>
    <div class="divider"></div>
    
    <div class="section">
        <div class="section-title">📌 关键事件</div>
        
        <div class="event">
            <div class="event-title">Capital One推出AI自主代码安全工具</div>
            <div class="event-detail">VulnHunter自主扫描并修复代码漏洞，减少人工审计</div>
        </div>
        
        <div class="event">
            <div class="event-title">链上债券市场让AI智能体当发行方</div>
            <div class="event-detail">AI代理拥有独立决策与经济行为，推动Agent经济落地</div>
        </div>
    </div>
    
    <div class="impact">
        <div class="impact-title">💡 对PM的启示</div>
        <div class="impact-text">AI从"辅助工具"进化为"自主经济参与者"。产品经理需要关注：1）代理的信用、身份与责任界定；2）Agent-to-Agent交易模式；3）代理经济中的新商业模式。</div>
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
    data = load_summary()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成3张洞察卡片
    cards = [
        ("2_insight_detail.png", generate_insight_card_2(data)),
        ("3_insight_detail.png", generate_insight_card_3(data)),
        ("4_insight_detail.png", generate_insight_card_4(data)),
    ]
    
    for filename, html in cards:
        output_path = OUTPUT_DIR / filename
        screenshot_card(html, output_path)
        print(f"✅ {filename}")
    
    print(f"\n📁 目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
