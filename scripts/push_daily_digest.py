#!/usr/bin/env python3
"""
Push daily AI Radar digest (markdown) to Feishu group chat as interactive card.
"""
import json
import urllib.request
import os
import re
from datetime import datetime, timezone, timedelta

# Credentials
APP_ID = "cli_a92b1c361ab8dcee"
APP_SECRET="kBOi1igKy0xFDLBBodUzkb65h5BIl2w7"
CHAT_ID = "oc_cd712bb35afd0e7ce151f7f5d1a81ddf"
# Auto-detect latest digest
import glob
digest_files = sorted(glob.glob(os.path.expanduser("~/ai-radar-wiki/daily-digest/*.md")))
DIGEST_PATH = digest_files[-1] if digest_files else os.path.expanduser("~/ai-radar-wiki/daily-digest/latest.md")
DATE = os.path.basename(DIGEST_PATH).replace(".md", "")
GRAPH_URL = "https://ttmens.github.io/ai-radar-wiki/graph.html"

def get_tenant_token():
    token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    token_payload = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode("utf-8")
    token_req = urllib.request.Request(token_url, data=token_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(token_req, timeout=10) as resp:
        token_result = json.loads(resp.read().decode("utf-8"))
    return token_result.get("tenant_access_token")

def build_card_markdown():
    with open(DIGEST_PATH) as f:
        md_content = f.read()

    lines = md_content.strip().split('\n')
    
    card_md = []
    card_md.append(f"🌅 **AI 雷达日报 · {DATE}** 已更新，请查收今日情报 👇")
    card_md.append("")
    
    # Parse overview
    overview_lines = []
    high_value_items = []
    in_overview = False
    in_high_value = False
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith("## 📊 今日概览"):
            in_overview = True
            in_high_value = False
            continue
        
        if stripped.startswith("## 🔥 今日高价值信号"):
            in_overview = False
            in_high_value = True
            continue
        
        if stripped.startswith("## 📂"):
            in_overview = False
            in_high_value = False
            continue
        
        if in_overview and stripped.startswith("-"):
            overview_lines.append(stripped)
            continue
        
        if in_high_value:
            if stripped.startswith("- **"):
                high_value_items.append({"title": stripped, "meta": [], "summary": ""})
            elif high_value_items:
                if "来源" in stripped or any(e in stripped for e in ["🤖", "💰", "📱", "🔧"]):
                    high_value_items[-1]["meta"].append(stripped)
                elif stripped.startswith("- "):
                    high_value_items[-1]["summary"] = stripped[2:]
    
    # Overview section
    if overview_lines:
        for o in overview_lines:
            card_md.append(o)
        card_md.append("")
    
    # High value signals
    card_md.append("**🔥 今日高价值信号 (PM 重点关注)**")
    card_md.append("")
    
    for item in high_value_items[:5]:
        title_line = item["title"]
        match = re.match(r'- \*\*\[(\d+\.\d+)\] (.+?)\*\*', title_line)
        if match:
            score = match.group(1)
            title = match.group(2)
            card_md.append(f"🎯 **[{score}] {title}**")
            
            for m in item["meta"]:
                link_match = re.search(r'\[来源\]\((.+?)\)', m)
                cat_match = re.match(r'- (🤖|💰|📱|🔧) (.+?) ·', m)
                if cat_match and link_match:
                    emoji = cat_match.group(1)
                    cat_text = cat_match.group(2)
                    link = link_match.group(1)
                    card_md.append(f"   {emoji} {cat_text} · [详情]({link})")
                elif cat_match:
                    emoji = cat_match.group(1)
                    cat_text = cat_match.group(2)
                    card_md.append(f"   {emoji} {cat_text}")
            
            if item["summary"]:
                summary = item["summary"]
                if len(summary) > 150:
                    summary = summary[:147] + "..."
                card_md.append(f"   📝 {summary}")
            
            card_md.append("")
    
    # Footer
    card_md.append("---")
    card_md.append("")
    card_md.append(f"🔗 **详细知识图谱**: [{GRAPH_URL}]({GRAPH_URL})")
    card_md.append("")
    card_md.append("> 数据源: GitHub, arXiv, Hacker News, TechCrunch AI, Product Hunt")
    
    return "\n".join(card_md)

def main():
    print("Step 1: Getting tenant token...")
    tenant_token = get_tenant_token()
    if not tenant_token:
        print("❌ Failed to get tenant token")
        return
    
    print("Step 2: Building card markdown...")
    card_md = build_card_markdown()
    print(f"Card markdown: {len(card_md)} chars")
    
    # Build interactive card
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"📊 AI Radar 日报 · {DATE}"},
            "template": "blue"
        },
        "elements": [
            {"tag": "markdown", "content": card_md},
            {
                "tag": "action",
                "actions": [{
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "📊 查看完整图谱"},
                    "type": "primary",
                    "url": GRAPH_URL,
                }]
            }
        ]
    }
    
    # Send to Feishu
    print("Step 3: Sending to Feishu group...")
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = json.dumps({
        "receive_id": CHAT_ID,
        "msg_type": "interactive",
        "content": json.dumps(card, ensure_ascii=False),
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url, data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {tenant_token}",
        }
    )
    
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    
    if result.get("code") == 0:
        msg_id = result.get("data", {}).get("message_id", "N/A")
        print(f"✅ Successfully sent to Feishu group!")
        print(f"Message ID: {msg_id}")
    else:
        print(f"❌ Failed: {json.dumps(result, ensure_ascii=False, indent=2)}")

if __name__ == "__main__":
    main()
