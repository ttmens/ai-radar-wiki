#!/usr/bin/env python3
"""
Feishu Message Card Push — 每日 AI Radar 摘要推送到飞书群聊

用法:
  python3 feishu_push.py                    # 使用环境变量中的 token
  python3 feishu_push.py --chat-id <id>     # 指定群聊 ID
  python3 feishu_push.py --test             # 测试模式（只打印卡片内容）
"""

import json
import os
import sys
import requests
import urllib.request
from datetime import datetime, timezone, timedelta

BJ_TZ = timezone(timedelta(hours=8))
SUMMARY_PATH = os.path.expanduser("~/ai-radar-wiki/daily_summary.json")
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "").strip()
if not FEISHU_APP_ID:
    raise EnvironmentError("FEISHU_APP_ID not set")

# 尝试从 .env 读取 FEISHU_APP_SECRET
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
_env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(_env_path) and not FEISHU_APP_SECRET:
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() == "FEISHU_APP_SECRET":
                    FEISHU_APP_SECRET = v.strip().strip("'\"")

# 默认目标群聊（需要配置）
DEFAULT_CHAT_ID = os.environ.get("FEISHU_CHAT_ID", "")

GRAPH_URL = "https://ttmens.github.io/ai-radar-wiki/graph.html"

TREND_EMOJI = {"up": "📈", "down": "📉", "stable": "➡️", "new": "🆕"}
NARRATIVE_EMOJI = {
    "paradigm_shift": "🔄",
    "bottleneck": "⚠️",
    "maturation": "📈",
    "validation": "💡"
}


def get_tenant_token():
    """获取飞书 tenant_access_token"""
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        print("⚠️ FEISHU_APP_ID or FEISHU_APP_SECRET not set")
        return None

    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET,
    }).encode("utf-8")

    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        return result.get("tenant_access_token")
    except Exception as e:
        print(f"⚠️ Failed to get tenant token: {e}")
        return None


def build_card(summary):
    """构建飞书交互卡片"""
    ds = summary.get("daily_summary", {})
    if not ds or not ds.get("headline"):
        return None

    elements = []

    # 叙事主线
    for n in ds.get("narratives", [])[:3]:
        emoji = NARRATIVE_EMOJI.get(n.get("type", ""), "📌")
        block = {
            "tag": "markdown",
            "content": f"**{emoji} {n.get('title', '')}**\n{n.get('body', '')[:100]}..."
        }
        elements.append(block)

        if n.get("action"):
            elements.append({
                "tag": "markdown",
                "content": f"💡 *{n['action']}*"
            })

    elements.append({"tag": "hr"})

    # 趋势看板
    trend_lines = []
    for ins in ds.get("insights", []):
        emoji = TREND_EMOJI.get(ins.get("trend", "new"), "❓")
        trend_lines.append(f"{emoji} **{ins['pillar']}**: {len(ins.get('evidence', []))} 条情报")

    elements.append({
        "tag": "markdown",
        "content": "\n".join(trend_lines)
    })

    elements.append({"tag": "hr"})

    # 底部按钮
    elements.append({
        "tag": "action",
        "actions": [{
            "tag": "button",
            "text": {"tag": "plain_text", "content": "📊 查看完整图谱"},
            "type": "primary",
            "url": GRAPH_URL,
        }]
    })

    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"📊 AI Radar 日报 · {ds.get('date', '')}"},
            "template": "blue"
        },
        "elements": elements,
    }

    return card


def send_to_feishu(chat_id, card):
    """发送卡片到飞书群聊"""
    token = get_tenant_token()
    if not token:
        print("⚠️ Cannot send: no tenant token")
        return False

    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = json.dumps({
        "receive_id": chat_id,
        "msg_type": "interactive",
        "content": json.dumps(card),
    }).encode("utf-8")

    req = urllib.request.Request(
        url, data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        if result.get("code") == 0:
            print(f"✅ Sent to chat {chat_id}")
            return True
        else:
            print(f"❌ Failed: {result}")
            return False
    except Exception as e:
        print(f"❌ Send failed: {e}")
        return False


def main():
    test_mode = "--test" in sys.argv
    chat_id = None
    for i, arg in enumerate(sys.argv):
        if arg == "--chat-id" and i + 1 < len(sys.argv):
            chat_id = sys.argv[i + 1]

    if not os.path.exists(SUMMARY_PATH):
        print(f"❌ Summary not found: {SUMMARY_PATH}")
        sys.exit(1)

    with open(SUMMARY_PATH) as f:
        summary = json.load(f)

    card = build_card(summary)
    if not card:
        print("❌ No card to send")
        sys.exit(1)

    if test_mode:
        print("=== Test Mode: Card Content ===")
        print(json.dumps(card, ensure_ascii=False, indent=2))
        return

    target = chat_id or DEFAULT_CHAT_ID
    if not target:
        print("⚠️ No chat ID specified. Use --chat-id <id> or set FEISHU_CHAT_ID env var")
        print("=== Card Content (dry run) ===")
        print(json.dumps(card, ensure_ascii=False, indent=2))
        return

    success = send_to_feishu(target, card)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
