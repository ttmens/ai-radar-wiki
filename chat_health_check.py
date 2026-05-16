#!/usr/bin/env python3
"""
AI Chat Server Health Monitor
- 检查后端服务是否存活
- 检查 Cloudflare Tunnel 是否在线
- 自动重启失败的服务
- 如果 Tunnel URL 变化，自动更新前端配置并推送
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERMES_SCRIPTS = Path.home() / ".hermes" / "scripts"
WIKI_DIR = Path.home() / "ai-radar-wiki"
BACKEND_PORT = 8081
HEALTH_URL = f"http://localhost:{BACKEND_PORT}/health"
MAX_RETRIES = 3

def log(msg):
    print(f"[health-check] {msg}", flush=True)

def check_backend():
    """检查后端服务是否存活"""
    try:
        import urllib.request
        req = urllib.request.Request(HEALTH_URL, method='GET')
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read())
                return True, data
    except Exception as e:
        return False, str(e)
    return False, "Unknown error"

def check_tunnel():
    """检查 Cloudflare Tunnel 是否在线"""
    try:
        import urllib.request
        # 通过公网 URL 检查
        resp = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
             "https://band-guests-camps-deliver.trycloudflare.com/health"],
            capture_output=True, text=True, timeout=10
        )
        return resp.stdout.strip() == "200"
    except:
        return False

def get_tunnel_url():
    """获取当前 Tunnel URL"""
    # 从 cloudflared 进程获取 URL
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:4040/api/tunnels"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if "tunnels" in data and len(data["tunnels"]) > 0:
                return data["tunnels"][0].get("public_url", "")
    except:
        pass
    return ""

def restart_backend():
    """重启后端服务"""
    log("正在重启后端服务...")
    
    # 停止旧进程
    subprocess.run(["pkill", "-f", "ai_chat_server.py"], capture_output=True)
    time.sleep(2)
    
    # 启动新进程
    env = os.environ.copy()
    env_path = Path.home() / ".hermes" / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    
    subprocess.Popen(
        ["python3", str(HERMES_SCRIPTS / "ai_chat_server.py"), "--port", str(BACKEND_PORT)],
        cwd=str(HERMES_SCRIPTS),
        env=env,
        stdout=open(str(HERMES_SCRIPTS / "chat_server.log"), "a"),
        stderr=subprocess.STDOUT,
    )
    
    # 等待启动
    for i in range(10):
        time.sleep(2)
        ok, _ = check_backend()
        if ok:
            log("后端服务启动成功")
            return True
    log("后端服务启动失败")
    return False

def update_frontend_url(new_url):
    """更新前端配置中的 API URL"""
    if not new_url:
        return False
    
    # 移除末尾的斜杠
    base_url = new_url.rstrip('/')
    
    files_to_update = [
        WIKI_DIR / "graph.html",
        WIKI_DIR / "index.html",
    ]
    
    updated = False
    for f in files_to_update:
        if not f.exists():
            continue
        content = f.read_text()
        if base_url not in content:
            # 替换旧 URL
            import re
            content = re.sub(
                r"agentApiBase:\s*'[https://](https://)[^']+'",
                f"agentApiBase: '{base_url}'",
                content
            )
            f.write_text(content)
            log(f"已更新 {f.name}")
            updated = True
    
    if updated:
        # 推送更新
        os.chdir(str(WIKI_DIR))
        subprocess.run(["git", "add", "-A"], capture_output=True)
        result = subprocess.run(
            ["git", "commit", "-m", f"chore: 更新 API URL -> {base_url}"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            subprocess.run(["git", "push"], capture_output=True)
            log("已推送前端配置更新")
    
    return updated

def main():
    log("开始健康检查...")
    
    # 检查后端
    backend_ok, backend_info = check_backend()
    if not backend_ok:
        log(f"后端服务异常: {backend_info}")
        if not restart_backend():
            log("后端重启失败，退出")
            sys.exit(1)
    else:
        log(f"后端正常 (节点数: {backend_info.get('nodes', '?')})")
    
    # 检查 Tunnel
    tunnel_ok = check_tunnel()
    if not tunnel_ok:
        log("Tunnel 异常，但后端正常。Tunnel 可能需要手动重启。")
        # Tunnel 重启需要交互式操作，这里只报警
        sys.exit(1)
    else:
        log("Tunnel 正常")
    
    log("健康检查完成")

if __name__ == "__main__":
    main()
