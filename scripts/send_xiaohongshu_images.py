#!/usr/bin/env python3
"""
发送小红书配图到飞书
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

# 飞书配置
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET=*** "")
FEISHU_CHAT_ID = os.environ.get("FEISHU_CHAT_ID", "oc_a2aedb3e0b69d55d2c73a83c69427f2e")

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
                elif k == "FEISHU_CHAT_ID":
                    FEISHU_CHAT_ID = v

def get_tenant_token():
    """获取飞书 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET,
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result.get("tenant_access_token")

def upload_image(token, image_path):
    """上传图片到飞书"""
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    
    # 读取图片
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # 构建 multipart/form-data
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = []
    body.append(f'--{boundary}'.encode())
    body.append(b'Content-Disposition: form-data; name="image_type"')
    body.append(b'')
    body.append(b'message')
    body.append(f'--{boundary}'.encode())
    body.append(b'Content-Disposition: form-data; name="image"; filename="image.png"')
    body.append(b'Content-Type: image/png')
    body.append(b'')
    body.append(image_data)
    body.append(f'--{boundary}--'.encode())
    
    body_data = b'\r\n'.join(body)
    
    req = urllib.request.Request(
        url, data=body_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        }
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    
    return result.get("data", {}).get("image_key")

def send_image_message(token, chat_id, image_key):
    """发送图片消息到飞书"""
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    
    # 使用正确的消息格式
    content = json.dumps({"image_key": image_key})
    payload = json.dumps({
        "receive_id": chat_id,
        "msg_type": "image",
        "content": content,
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url, data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}",
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("code") == 0:
                return True
            else:
                print(f"    API错误: {result}")
                return False
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"    HTTP错误 {e.code}: {error_body}")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法: python3 send_xiaohongshu_images.py <图片路径1> [图片路径2] ...")
        sys.exit(1)
    
    image_paths = sys.argv[1:]
    
    print("🔑 获取飞书 token...")
    token = get_tenant_token()
    if not token:
        print("❌ 获取 token 失败")
        sys.exit(1)
    
    print(f"✅ Token 获取成功\n")
    
    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"❌ 图片不存在: {image_path}")
            continue
        
        print(f"📤 上传: {os.path.basename(image_path)}")
        try:
            image_key = upload_image(token, image_path)
            if not image_key:
                print(f"  ❌ 上传失败")
                continue
            
            print(f"  ✅ 上传成功: {image_key}")
            
            print(f"  📤 发送到飞书...")
            success = send_image_message(token, FEISHU_CHAT_ID, image_key)
            if success:
                print(f"  ✅ 发送成功")
            else:
                print(f"  ❌ 发送失败")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        
        print()

if __name__ == "__main__":
    main()
