#!/usr/bin/env python3
"""
AI Radar 问 AI 服务启动脚本

用法：
  python start_chat_server.py          # 默认端口 8081
  python start_chat_server.py --port 9000  # 自定义端口

功能：
  - 启动 FastAPI 聊天服务器
  - 自动加载知识库
  - 场景感知模型路由
  - 对话历史管理
"""

import os
import sys
import subprocess

# 添加脚本目录
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    import argparse
    parser = argparse.ArgumentParser(description='启动 AI Radar 问 AI 服务')
    parser.add_argument('--port', type=int, default=8081, help='服务端口（默认 8081）')
    parser.add_argument('--host', default='0.0.0.0', help='绑定地址')
    parser.add_argument('--reload', action='store_true', help='开发模式：自动重载')
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 AI Radar 问 AI 服务")
    print("=" * 60)
    print(f"📡 地址: http://{args.host}:{args.port}")
    print(f"📊 健康检查: http://{args.host}:{args.port}/health")
    print(f"💬 聊天接口: POST http://{args.host}:{args.port}/chat")
    print(f"📚 知识统计: GET http://{args.host}:{args.port}/knowledge/stats")
    print()
    print("提示：")
    print("  - 在浏览器打开 graph.html 即可使用问 AI 功能")
    print("  - 确保 ai_model_router.py 在同一个目录")
    print("  - 按 Ctrl+C 停止服务")
    print("=" * 60)
    print()
    
    # 启动服务器
    server_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_chat_server.py')
    
    cmd = [
        sys.executable, server_script,
        '--port', str(args.port),
        '--host', args.host,
    ]
    
    if args.reload:
        cmd.append('--reload')
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n✅ 服务已停止")
        sys.exit(0)

if __name__ == '__main__':
    main()
