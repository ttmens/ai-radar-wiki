#!/usr/bin/env python3
"""
发送小红书图片和文案到飞书
"""

import json
import os
import requests
from pathlib import Path

# 飞书配置
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET=*** "")
FEISHU_CHAT_ID = "oc_a2aedb3e0b69d55d2c73a83c69427f2e"

# 从 .env 读取
env_path = Path.home() / ".hermes" / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k == "FEISHU_APP_ID":
                    FEISHU_APP_ID = v
                elif k == "FEISHU_APP_SECRET":
                    FEISHU_APP_SECRET = v

def get_tenant_token():
    """获取飞书 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET,
    }
    response = requests.post(url, json=payload)
    return response.json().get("tenant_access_token")

def upload_image(token, image_path):
    """上传图片到飞书"""
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    
    with open(image_path, 'rb') as f:
        files = {
            'image_type': (None, 'message'),
            'image': ('image.png', f, 'image/png')
        }
        response = requests.post(url, headers=headers, files=files)
    
    result = response.json()
    return result.get("data", {}).get("image_key")

def send_image_message(token, chat_id, image_key):
    """发送图片消息到飞书"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": "chat_id"}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "receive_id": chat_id,
        "msg_type": "image",
        "content": json.dumps({"image_key": image_key}),
    }
    
    response = requests.post(url, params=params, headers=headers, json=payload)
    result = response.json()
    return result.get("code") == 0

def send_text_message(token, chat_id, text):
    """发送文本消息到飞书"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": "chat_id"}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}),
    }
    
    response = requests.post(url, params=params, headers=headers, json=payload)
    result = response.json()
    return result.get("code") == 0

def main():
    # 读取文案
    post_path = "/home/admin/ai-radar-wiki/xiaohongshu/2026-07-20/post.txt"
    with open(post_path, 'r', encoding='utf-8') as f:
        post_content = f.read()
    
    # 图片路径
    image_paths = [
        "/home/admin/ai-radar-wiki/xiaohongshu/2026-07-20/1_overview.png",
        "/home/admin/ai-radar-wiki/xiaohongshu/2026-07-20/2_insight.png",
        "/home/admin/ai-radar-wiki/xiaohongshu/2026-07-20/3_insight.png",
        "/home/admin/ai-radar-wiki/xiaohongshu/2026-07-20/4_insight.png",
    ]
    
    print("🔑 获取飞书 token...")
    token = get_tenant_token()
    if not token:
        print("❌ 获取 token 失败")
        return
    
    print("✅ Token 获取成功\n")
    
    # 发送文案
    print("📝 发送文案...")
    if send_text_message(token, FEISHU_CHAT_ID, post_content):
        print("✅ 文案发送成功\n")
    else:
        print("❌ 文案发送失败\n")
    
    # 发送图片
    for image_path in image_paths:
        filename = os.path.basename(image_path)
        print(f"📤 上传并发送: {filename}")
        
        try:
            # 上传图片
            image_key = upload_image(token, image_path)
            if not image_key:
                print(f"  ❌ 上传失败")
                continue
            
            print(f"  ✅ 上传成功: {image_key}")
            
            # 发送图片
            if send_image_message(token, FEISHU_CHAT_ID, image_key):
                print(f"  ✅ 发送成功")
            else:
                print(f"  ❌ 发送失败")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        
        print()
    
    print("✅ 完成！请查看飞书消息")

if __name__ == "__main__":
    main()
