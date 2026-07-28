#!/usr/bin/env python3
"""
Push xiaohongshu daily content to Feishu chat.
"""

import json
import os
import sys
import glob
import urllib.request
from datetime import datetime

# Load env
def load_env():
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))

load_env()

FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
FEISHU_CHAT_ID = os.environ.get("FEISHU_HOME_CHANNEL", "")

TODAY = datetime.now().strftime("%Y-%m-%d")
XHS_DIR = os.path.expanduser(f"~/ai-radar-wiki/xiaohongshu/{TODAY}")
POST_FILE = os.path.join(XHS_DIR, "post.txt")


def get_tenant_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET,
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result.get("tenant_access_token")


def upload_image(token, image_path):
    """Upload image to Feishu and return image_key"""
    import mimetypes
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    filename = os.path.basename(image_path)
    content_type = mimetypes.guess_type(image_path)[0] or "image/png"
    
    with open(image_path, "rb") as f:
        file_data = f.read()
    
    # Build multipart form data
    body = b""
    # image_type field
    body += f"--{boundary}\r\n".encode()
    body += b'Content-Disposition: form-data; name="image_type"\r\n\r\n'
    body += b'message\r\n'
    # image file
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'.encode()
    body += f'Content-Type: {content_type}\r\n\r\n'.encode()
    body += file_data
    body += f"\r\n--{boundary}--\r\n".encode()
    
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    req = urllib.request.Request(
        url, data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        }
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    
    if result.get("code") == 0:
        return result["data"]["image_key"]
    else:
        raise Exception(f"Upload failed: {result}")


def send_text_message(token, chat_id, text):
    """Send text message to Feishu chat"""
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = json.dumps({
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}),
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url, data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
    )
    
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    
    if result.get("code") == 0:
        print(f"✅ Text message sent")
        return True
    else:
        print(f"❌ Text send failed: {result}")
        return False


def send_image_message(token, chat_id, image_key):
    """Send image message to Feishu chat"""
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = json.dumps({
        "receive_id": chat_id,
        "msg_type": "image",
        "content": json.dumps({"image_key": image_key}),
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url, data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
    )
    
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    
    if result.get("code") == 0:
        print(f"✅ Image sent: {image_key}")
        return True
    else:
        print(f"❌ Image send failed: {result}")
        return False


def main():
    if not os.path.exists(POST_FILE):
        print(f"❌ Post file not found: {POST_FILE}")
        sys.exit(1)
    
    # Read post content
    with open(POST_FILE, "r") as f:
        post_content = f.read().strip()
    
    # Find images
    images = sorted(glob.glob(os.path.join(XHS_DIR, "*.png")))
    
    # Build the message text
    message = f"""📋 今日小红书内容 ({TODAY})

{post_content}

💡 操作步骤：
1. 长按配图 → 保存到手机相册
2. 复制文案 → 打开小红书 → 粘贴
3. 上传配图 → 发布
4. 30分钟内回复评论

⏰ 建议发布时间：今天12:00（午休高峰）"""
    
    # Get token
    print("🔑 Getting Feishu token...")
    token = get_tenant_token()
    if not token:
        print("❌ Failed to get tenant token")
        sys.exit(1)
    print("✅ Token obtained")
    
    # Send text message
    print("📤 Sending text message...")
    send_text_message(token, FEISHU_CHAT_ID, message)
    
    # Upload and send images
    for img_path in images:
        img_name = os.path.basename(img_path)
        print(f"📤 Uploading image: {img_name}")
        try:
            image_key = upload_image(token, img_path)
            print(f"✅ Uploaded: {image_key}")
            send_image_message(token, FEISHU_CHAT_ID, image_key)
        except Exception as e:
            print(f"❌ Failed to upload {img_name}: {e}")
    
    print("\n🎉 Done! All content pushed to Feishu.")


if __name__ == "__main__":
    main()
