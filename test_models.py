#!/usr/bin/env python3
"""测试所有 AI 模型是否可用"""

import os
import sys
import json
import time

# 添加脚本目录到路径
sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))

# 加载 .env
env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key not in os.environ:
                    os.environ[key] = val

def mask_key(key):
    """脱敏 API key"""
    if not key:
        return "(未配置)"
    if len(key) <= 8:
        return "****"
    return key[:8] + "..." + key[-4:]

def test_model(name, base_url, api_key, model, timeout=30):
    """测试单个模型"""
    print(f"\n{'='*60}")
    print(f"测试: {name} / {model}")
    print(f"Base URL: {base_url}")
    print(f"API Key: {mask_key(api_key)}")
    print(f"{'='*60}")
    
    if not api_key or api_key == "***":
        print("❌ API Key 未配置")
        return False
    
    import requests
    
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个简洁的助手。"},
            {"role": "user", "content": "请用一句话回答：1+1 等于几？"}
        ],
        "temperature": 0.1,
        "max_tokens": 50,
    }
    
    start = time.time()
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        result = response.json()
        
        elapsed = time.time() - start
        content = result["choices"][0]["message"]["content"].strip()
        tokens = result.get("usage", {}).get("total_tokens", "?")
        
        print(f"✅ 成功! 耗时: {elapsed:.1f}s, tokens: {tokens}")
        print(f"   回答: {content}")
        return True
        
    except requests.exceptions.Timeout:
        print(f"❌ 超时 (>{timeout}s)")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误: {e}")
        print(f"   响应: {response.text[:200]}")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_router():
    """测试 ai_model_router 模块"""
    print(f"\n{'='*60}")
    print("测试: ai_model_router 模块")
    print(f"{'='*60}")
    
    try:
        from ai_model_router import call_llm, get_model_configs
        
        primary, fallback = get_model_configs()
        print(f"主模型: {primary.name}/{primary.model} - {'✅' if primary.is_available() else '❌'}")
        print(f"降级模型: {fallback.name}/{fallback.model} - {'✅' if fallback.is_available() else '❌'}")
        
        # 测试调用
        print("\n测试 call_llm...")
        result = call_llm(
            prompt="1+1 等于几？用一句话回答。",
            system_prompt="你是一个简洁的助手。",
            temperature=0.1,
            max_tokens=50,
        )
        
        if result:
            print(f"✅ Router 调用成功: {result}")
            return True
        else:
            print("❌ Router 调用失败")
            return False
            
    except Exception as e:
        print(f"❌ Router 模块错误: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("AI Radar 模型验证测试")
    print("=" * 60)
    
    results = {}
    
    # 测试 DashScope
    results["dashscope"] = test_model(
        name="DashScope",
        base_url=os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        api_key=os.environ.get("DASHSCOPE_API_KEY", ""),
        model="qwen3.6-plus",
    )
    
    # 测试 DeepSeek
    results["deepseek"] = test_model(
        name="DeepSeek",
        base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
        model="deepseek-v4-flash",
    )
    
    # 测试 Router
    results["router"] = test_router()
    
    # 总结
    print(f"\n{'='*60}")
    print("测试总结")
    print(f"{'='*60}")
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(results.values())
    print(f"\n总体: {'✅ 全部通过' if all_passed else '❌ 部分失败'}")
