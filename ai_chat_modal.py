#!/usr/bin/env python3
"""
AI Radar Chat Server - Modal Cloud Deployment
为 Web 端和手机端提供公网可访问的"问 AI"能力。

功能：
- 基于知识图谱的 RAG 问答
- 场景感知模型路由（simple/analysis/code）
- 对话历史管理

部署：
    modal deploy ai_chat_modal.py
"""

import json
import os
import time
import logging
from typing import Optional

import modal
import requests

# =============================================================================
# Modal Image & App Configuration
# =============================================================================

image = modal.Image.debian_slim(python_version="3.12").pip_install(
    "fastapi", "pydantic", "requests"
)

app = modal.App("ai-radar-chat")

# Secrets: 从本地 .env 文件加载 API Keys
# 部署时会自动带上 ~/.hermes/.env 中的变量
secret = modal.Secret.from_dotenv(os.path.expanduser("~/.hermes/.env"))

# =============================================================================
# Data Loading (从 GitHub Pages 拉取最新数据)
# =============================================================================

GRAPH_URL = "https://archwang.top/graph.json"
DAILY_SUMMARY_URL = "https://archwang.top/daily_summary.json"

def load_data():
    """加载知识图谱和每日摘要作为上下文。"""
    kb = {"nodes": [], "today_items": [], "pillars": {}, "stats": {}}

    try:
        r = requests.get(GRAPH_URL, timeout=30)
        graph = r.json()
        nodes = graph.get("nodes", [])
        kb["stats"]["total_nodes"] = len(nodes)

        pillars = {}
        for node in nodes:
            pillar = node.get("pillar", "unknown")
            pillars[pillar] = pillars.get(pillar, 0) + 1
        kb["pillars"] = pillars

        today_nodes = [n for n in nodes if n.get("is_today")]
        kb["today_items"] = [
            {
                "id": n.get("id", ""),
                "label": n.get("label", ""),
                "pillar": n.get("pillar", ""),
                "pm_score": n.get("pm_score", 0),
                "summary": (n.get("summary", "") or "")[:200],
            }
            for n in today_nodes[:30]
        ]
        kb["stats"]["today_items"] = len(kb["today_items"])

        kb["nodes"] = [
            {
                "id": n.get("id", ""),
                "label": n.get("label", ""),
                "pillar": n.get("pillar", ""),
                "summary": (n.get("summary", "") or "")[:150],
                "url": n.get("url", ""),
            }
            for n in nodes[:200]
        ]
    except Exception as e:
        logging.warning(f"⚠️ 加载 graph.json 失败: {e}")

    try:
        r = requests.get(DAILY_SUMMARY_URL, timeout=30)
        summary = r.json()
        data = summary.get("daily_summary", summary)
        kb["daily_summary"] = {
            "date": data.get("date"),
            "headline": data.get("headline"),
            "narratives": data.get("narratives", []),
            "insights": data.get("insights", []),
        }
    except Exception as e:
        logging.warning(f"⚠️ 加载 daily_summary.json 失败: {e}")

    return kb

# =============================================================================
# Model Router Logic (Inline to avoid import issues on Modal)
# =============================================================================

SCENES = {
    "simple": ["deepseek-flash", "deepseek-pro", "qwen-plus"],
    "analysis": ["deepseek-flash", "deepseek-pro", "qwen-plus"],
    "summary": ["deepseek-flash", "deepseek-pro", "qwen-plus"],
    "code": ["qwen-coder", "qwen-plus", "deepseek-pro"],
    "default": ["deepseek-flash", "deepseek-pro", "qwen-plus"],
}

MODELS = {}

def _init_models():
    global MODELS
    ds_key = os.environ.get("DEEPSEEK_API_KEY", "")
    ds_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    if ds_key:
        MODELS["deepseek-flash"] = {
            "name": "deepseek-flash", "base_url": ds_url,
            "api_key": ds_key, "model": "deepseek-v4-flash", "timeout": 45,
        }
        MODELS["deepseek-pro"] = {
            "name": "deepseek-pro", "base_url": ds_url,
            "api_key": ds_key, "model": "deepseek-v4-pro", "timeout": 60,
        }

    ds_api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    ds_api_url = os.environ.get("DASHSCOPE_BASE_URL", "https://coding.dashscope.aliyuncs.com/v1")
    if ds_api_key:
        MODELS["qwen-plus"] = {
            "name": "qwen-plus", "base_url": ds_api_url,
            "api_key": ds_api_key, "model": "qwen3.6-plus", "timeout": 60,
        }
        MODELS["qwen-coder"] = {
            "name": "qwen-coder", "base_url": ds_api_url,
            "api_key": ds_api_key, "model": "qwen3-coder-plus", "timeout": 90,
        }

def call_llm(prompt: str, system_prompt: str = "你是助手。", scene: str = "default") -> Optional[str]:
    if not MODELS:
        _init_models()
    
    model_names = SCENES.get(scene, SCENES["default"])
    chain = [MODELS[n] for n in model_names if n in MODELS]
    
    if not chain:
        return "❌ 没有可用的模型配置"
        
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    
    for cfg in chain:
        try:
            url = f"{cfg['base_url']}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {cfg['api_key']}",
            }
            payload = {
                "model": cfg["model"],
                "messages": messages,
                "temperature": 0.5,
                "max_tokens": 1500,
            }
            resp = requests.post(url, json=payload, headers=headers, timeout=cfg["timeout"])
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.warning(f"Model {cfg['name']} failed: {e}")
            continue
            
    return "❌ 所有模型调用均失败"

# =============================================================================
# Web Endpoint
# =============================================================================

from pydantic import BaseModel
from fastapi import HTTPException

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    scene: Optional[str] = "simple"

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    model_used: str

# Simple in-memory session store (works per-container, good enough for demo)
sessions = {}

@app.cls(
    image=image,
    secrets=[secret],
    cpu=0.5,
    memory=512,
)
class ChatService:
    @modal.enter()
    def setup(self):
        print("✅ 正在加载知识库...")
        self.kb = load_data()
        print(f"✅ 知识库加载完成: {self.kb['stats'].get('total_nodes', 0)} 节点")

    @modal.fastapi_endpoint(method="POST")
    def chat(self, req: ChatRequest) -> ChatResponse:
        if not req.session_id:
            req.session_id = f"session_{int(time.time())}"
        
        # 构建上下文
        context_parts = []
        ds = self.kb.get("daily_summary")
        if ds:
            context_parts.append(f"## 今日情报概览 ({ds.get('date', '未知')})\n标题：{ds.get('headline', '')}\n")
            for n in ds.get("narratives", [])[:3]:
                context_parts.append(f"- {n.get('title', '')}: {n.get('body', '')[:100]}...")
        
        # 简单关键词匹配
        query_lower = req.query.lower()
        relevant = [
            n for n in self.kb.get("nodes", [])[:50]
            if any(w in (n.get("label", "") or "").lower() or w in (n.get("summary", "") or "").lower()
                   for w in query_lower.split()[:5])
        ]
        
        if relevant:
            context_parts.append("\n## 相关情报节点\n")
            for i, node in enumerate(relevant[:10], 1):
                context_parts.append(
                    f"{i}. **{node.get('label', '')}** (PM: {node.get('pm_score', 0):.2f})\n"
                    f"   {node.get('summary', '')[:150]}"
                )
        
        system_prompt = f"""你是 AI Radar 系统的智能助手，服务于 AI 产品经理。
## 知识库上下文
{chr(10).join(context_parts)}
## 回答规则
1. 用中文回答，简洁专业
2. 引用具体数据或项目时注明名称
3. 如果知识库中没有相关信息，如实告知"""

        # 获取历史
        history = sessions.get(req.session_id, [])
        messages_content = [{"role": m["role"], "content": m["content"]} for m in history]
        messages_content.append({"role": "user", "content": req.query})
        
        # 调用 LLM
        result = call_llm(
            prompt=req.query,
            system_prompt=system_prompt,
            scene=req.scene or "simple",
        )
        
        # 更新历史
        if req.session_id not in sessions:
            sessions[req.session_id] = []
        sessions[req.session_id].append({"role": "user", "content": req.query})
        sessions[req.session_id].append({"role": "assistant", "content": str(result)})
        if len(sessions[req.session_id]) > 40:
            sessions[req.session_id] = sessions[req.session_id][-40:]
            
        return ChatResponse(
            answer=str(result),
            session_id=req.session_id,
            model_used=req.scene or "simple",
        )

    @modal.fastapi_endpoint(method="GET")
    def health(self):
        return {
            "status": "ok",
            "nodes": self.kb["stats"].get("total_nodes", 0),
            "today_items": self.kb["stats"].get("today_items", 0),
        }
