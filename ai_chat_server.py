#!/usr/bin/env python3
"""
AI Radar Chat Server v2 - FastAPI 后端服务
为 Web 端和手机端提供"问 AI"能力。

功能：
- 基于知识图谱的 RAG 问答（倒排索引加速）
- 场景感知模型路由（simple/analysis/code）
- 对话历史管理（并发安全）
- 流式输出支持 (SSE)
- 每日问答限额控制（默认 200 次/天）

启动：python ai_chat_server.py --port 8080
"""

import json
import os
import sys
import time
import uuid
import asyncio
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# 加载环境变量
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

# =============================================================================
# 配置
# =============================================================================

GRAPH_JSON = os.path.expanduser("~/ai-radar-wiki/graph.json")
DAILY_SUMMARY = os.path.expanduser("~/ai-radar-wiki/daily_summary.json")
QUOTA_FILE = os.path.expanduser("~/.hermes/data/chat_quota.json")
DAILY_QUOTA_LIMIT = 200  # 每日最大问答次数

# LLM API 配置
LLM_PROVIDERS = {}

ds_key = os.environ.get("DEEPSEEK_API_KEY", "")
if ds_key:
    LLM_PROVIDERS["deepseek-flash"] = {
        "base_url": os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        "api_key": ds_key,
        "model": "deepseek-v4-flash",
    }

dash_key = os.environ.get("DASHSCOPE_API_KEY", "")
if dash_key:
    LLM_PROVIDERS["qwen-plus"] = {
        "base_url": os.environ.get("DASHSCOPE_BASE_URL", "https://coding.dashscope.aliyuncs.com/v1"),
        "api_key": dash_key,
        "model": "qwen3.6-plus",
    }

# =============================================================================
# 限额管理器
# =============================================================================

class QuotaManager:
    """每日问答次数限制管理器。"""
    
    def __init__(self, limit: int = DAILY_QUOTA_LIMIT):
        self.limit = limit
        self._lock = asyncio.Lock()
        self._load()
    
    def _load(self):
        try:
            os.makedirs(os.path.dirname(QUOTA_FILE), exist_ok=True)
            if os.path.exists(QUOTA_FILE):
                with open(QUOTA_FILE) as f:
                    data = json.load(f)
                today = self._today_str()
                if data.get("date") == today:
                    self.date = today
                    self.count = data.get("count", 0)
                else:
                    self.date = today
                    self.count = 0
                    self._save()
            else:
                self.date = self._today_str()
                self.count = 0
                self._save()
        except Exception as e:
            logger.error(f"限额加载失败: {e}")
            self.date = self._today_str()
            self.count = 0
    
    def _save(self):
        try:
            with open(QUOTA_FILE, "w") as f:
                json.dump({"date": self.date, "count": self.count}, f)
        except Exception as e:
            logger.error(f"限额保存失败: {e}")
    
    def _today_str(self) -> str:
        tz = timezone(timedelta(hours=8))
        return datetime.now(tz).strftime("%Y-%m-%d")
    
    async def check_and_consume(self) -> tuple[bool, dict]:
        """检查并消耗一次额度。返回 (是否允许, 状态信息)。"""
        async with self._lock:
            today = self._today_str()
            if self.date != today:
                self.date = today
                self.count = 0
                self._save()
            
            if self.count >= self.limit:
                return False, {
                    "allowed": False,
                    "used": self.count,
                    "limit": self.limit,
                    "message": "今日问答次数已用完（{used}/{limit}），请明日再试。",
                    "reset_time": "明天 00:00 (北京时间)",
                }
            
            self.count += 1
            self._save()
            return True, {
                "allowed": True,
                "used": self.count,
                "limit": self.limit,
                "remaining": self.limit - self.count,
            }
    
    def get_status(self) -> dict:
        return {
            "used": self.count,
            "limit": self.limit,
            "remaining": max(0, self.limit - self.count),
            "date": self.date,
        }

# =============================================================================
# 知识库加载
# =============================================================================

def load_knowledge_base():
    """加载知识图谱和每日摘要作为上下文。"""
    kb = {
        "nodes": [],
        "node_index": {},  # 倒排索引：关键词 -> node_ids
        "today_items": [],
        "pillars": {},
        "stats": {},
        "daily_summary": None,
    }
    
    if os.path.exists(GRAPH_JSON):
        try:
            with open(GRAPH_JSON) as f:
                graph = json.load(f)
            
            nodes = graph.get("nodes", [])
            kb["stats"]["total_nodes"] = len(nodes)
            
            pillars = {}
            for node in nodes:
                pillar = node.get("pillar", "unknown")
                pillars[pillar] = pillars.get(pillar, 0) + 1
            kb["pillars"] = pillars
            
            today_nodes = [n for n in nodes if n.get("is_today")]
            kb["today_items"] = [
                {"id": n.get("id", ""), "label": n.get("label", ""),
                 "pillar": n.get("pillar", ""), "pm_score": n.get("pm_score", 0),
                 "summary": (n.get("summary", "") or "")[:200]}
                for n in today_nodes[:30]
            ]
            kb["stats"]["today_items"] = len(kb["today_items"])
            
            # 构建倒排索引
            import re
            for i, node in enumerate(nodes):
                text = f"{node.get('label', '')} {node.get('summary', '')} {node.get('pillar', '')}".lower()
                words = set(re.findall(r'[a-z0-9\u4e00-\u9fff]+', text))
                for word in words:
                    if len(word) > 1:  # 忽略单字符
                        kb["node_index"].setdefault(word, []).append(i)
            
            kb["nodes"] = [
                {"id": n.get("id", ""), "label": n.get("label", ""),
                 "pillar": n.get("pillar", ""), "summary": (n.get("summary", "") or "")[:150],
                 "url": n.get("url", "")}
                for n in nodes[:300]
            ]
        except Exception as e:
            logger.error(f"加载 graph.json 失败: {e}")
    
    if os.path.exists(DAILY_SUMMARY):
        try:
            with open(DAILY_SUMMARY) as f:
                summary = json.load(f)
            data = summary.get("daily_summary", summary)
            kb["daily_summary"] = {
                "date": data.get("date"), "headline": data.get("headline"),
                "narratives": data.get("narratives", []), "insights": data.get("insights", []),
            }
        except Exception as e:
            logger.error(f"加载 daily_summary.json 失败: {e}")
    
    return kb

# =============================================================================
# 对话历史（并发安全 — 每会话独立锁）
# =============================================================================

class ConversationHistory:
    """内存对话历史管理，支持多用户并发安全。
    
    关键设计：
    - 每 session 独立 asyncio.Lock，避免全局锁串行化
    - get_session + add_message 在同一锁内完成，防止竞态
    """
    
    def __init__(self, max_turns: int = 15):
        self.sessions = {}       # session_id -> [messages]
        self._locks = {}         # session_id -> asyncio.Lock
        self._global_lock = asyncio.Lock()  # 保护 sessions/_locks 字典本身
        self.max_turns = max_turns
    
    async def _get_lock(self, session_id: str) -> asyncio.Lock:
        """获取或创建会话专属锁。"""
        async with self._global_lock:
            if session_id not in self._locks:
                self._locks[session_id] = asyncio.Lock()
            return self._locks[session_id]
    
    async def get_messages(self, session_id: str) -> list:
        """获取会话历史（快照，线程安全）。"""
        lock = await self._get_lock(session_id)
        async with lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            return list(self.sessions[session_id])  # 返回快照
    
    async def add_turn(self, session_id: str, user_msg: str, assistant_msg: str):
        """原子性追加一轮对话（用户+助手），防止并发串会话。"""
        lock = await self._get_lock(session_id)
        async with lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            session = self.sessions[session_id]
            session.append({"role": "user", "content": user_msg})
            session.append({"role": "assistant", "content": assistant_msg})
            # 限制历史长度
            max_msgs = self.max_turns * 2
            if len(session) > max_msgs:
                self.sessions[session_id] = session[-max_msgs:]
    
    async def clear_session(self, session_id: str):
        async with self._global_lock:
            self.sessions.pop(session_id, None)
            self._locks.pop(session_id, None)

# =============================================================================
# RAG 上下文构建
# =============================================================================

def build_context(query: str, kb: dict) -> str:
    """根据查询构建相关上下文（使用倒排索引加速）。
    
    性能优化：
    - 智能选择上下文：简单问题只给日报，深度问题才给图谱
    - 限制返回数量，控制 prompt 长度在 3K tokens 以内
    """
    import re
    context_parts = []
    
    # 1. 每日摘要（总是包含，提供最新情报）
    if kb.get("daily_summary"):
        ds = kb["daily_summary"]
        context_parts.append(
            f"## 今日情报 ({ds.get('date', '未知')})\n"
            f"头条：{ds.get('headline', '')}\n"
        )
        for n in ds.get("narratives", [])[:3]:
            context_parts.append(f"- {n.get('title', '')}: {n.get('body', '')[:100]}")
    
    # 2. 知识图谱统计（精简版）
    context_parts.append(
        f"\n## 知识图谱\n"
        f"规模：{kb['stats'].get('total_nodes', 0)} 节点 | "
        f"今日：{kb['stats'].get('today_items', 0)} 条\n"
    )
    
    # 3. 智能检索：根据查询类型决定检索策略
    query_words = set(re.findall(r'[a-z0-9\u4e00-\u9fff]+', query.lower()))
    
    # 判断是否是概览型问题（不包含具体项目名/技术名）
    is_broad_query = len(query_words) <= 3 or any(
        kw in query for kw in ["今天", "本周", "概况", "总结", "趋势", "什么", "哪些", "最近"]
    )
    
    if is_broad_query:
        # 概览型问题：只给今日高价值项目
        today_items = kb.get("today_items", [])
        if today_items:
            context_parts.append("\n## 今日重点\n")
            high_value = sorted(today_items, key=lambda x: x.get("pm_score", 0), reverse=True)[:5]
            for i, item in enumerate(high_value, 1):
                context_parts.append(
                    f"{i}. **{item.get('label', '')}** "
                    f"(PM: {item.get('pm_score', 0):.2f}, {item.get('pillar', '')})\n"
                    f"   {item.get('summary', '')[:100]}"
                )
    else:
        # 具体问题：用倒排索引检索相关节点
        node_scores = {}
        for word in query_words:
            for idx in kb.get("node_index", {}).get(word, []):
                node_scores[idx] = node_scores.get(idx, 0) + 1
        
        top_indices = sorted(node_scores, key=node_scores.get, reverse=True)[:10]
        
        if top_indices:
            context_parts.append("\n## 相关情报\n")
            for rank, idx in enumerate(top_indices, 1):
                if idx < len(kb["nodes"]):
                    node = kb["nodes"][idx]
                    context_parts.append(
                        f"{rank}. **{node.get('label', '')}** "
                        f"(PM: {node.get('pm_score', 0):.2f})\n"
                        f"   {node.get('summary', '')[:120]}"
                    )
        else:
            # 倒排索引未命中，给今日高价值项目作为 fallback
            today_items = kb.get("today_items", [])
            if today_items:
                context_parts.append("\n## 今日高价值项目\n")
                for i, item in enumerate(sorted(today_items, key=lambda x: x.get("pm_score", 0), reverse=True)[:3], 1):
                    context_parts.append(
                        f"{i}. **{item.get('label', '')}** ({item.get('pillar', '')})"
                    )
    
    return "\n".join(context_parts)

# =============================================================================
# LLM 调用（支持流式）
# =============================================================================

async def call_llm_stream(messages: list, temperature: float = 0.5, max_tokens: int = 1500) -> AsyncGenerator[str, None]:
    """异步流式调用 LLM。"""
    provider = LLM_PROVIDERS.get("qwen-plus") or LLM_PROVIDERS.get("deepseek-flash")
    if not provider:
        raise RuntimeError("未配置可用的 LLM 提供商")
    
    url = f"{provider['base_url']}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {provider['api_key']}",
    }
    payload = {
        "model": provider["model"],
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True,
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream("POST", url, json=payload, headers=headers) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    delta = data.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield content
                except json.JSONDecodeError:
                    continue


async def call_llm_async(messages: list, temperature: float = 0.5, max_tokens: int = 1500) -> str:
    """异步调用 LLM（非流式）。"""
    provider = LLM_PROVIDERS.get("qwen-plus") or LLM_PROVIDERS.get("deepseek-flash")
    if not provider:
        raise RuntimeError("未配置可用的 LLM 提供商")
    
    url = f"{provider['base_url']}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {provider['api_key']}",
    }
    payload = {
        "model": provider["model"],
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        result = resp.json()
        return result["choices"][0]["message"]["content"].strip()

# =============================================================================
# API 模型
# =============================================================================

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    scene: Optional[str] = "simple"
    stream: Optional[bool] = False

# =============================================================================
# FastAPI 应用
# =============================================================================

knowledge_base = {}
conv_history = ConversationHistory()
quota_mgr = QuotaManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global knowledge_base, conv_history, quota_mgr
    knowledge_base = load_knowledge_base()
    logger.info(f"✅ 知识库已加载: {knowledge_base['stats'].get('total_nodes', 0)} 节点, "
                f"倒排索引 {len(knowledge_base.get('node_index', {}))} 个词条")
    logger.info(f"📊 今日问答限额: {quota_mgr.get_status()}")
    yield

app = FastAPI(title="AI Radar Chat Server v2", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "2.0.0",
        "nodes": knowledge_base.get("stats", {}).get("total_nodes", 0),
        "quota": quota_mgr.get_status(),
    }

@app.get("/quota")
def get_quota():
    return quota_mgr.get_status()

@app.post("/chat")
async def chat(request: ChatRequest):
    """普通问答接口（非流式）。"""
    allowed, status = await quota_mgr.check_and_consume()
    if not allowed:
        return JSONResponse(status_code=429, content={
            "error": "quota_exceeded",
            "message": status["message"].format(used=status["used"], limit=status["limit"]),
            "reset_time": status.get("reset_time"),
            "quota": status,
        })
    
    session_id = request.session_id or f"session_{uuid.uuid4().hex[:8]}"
    
    # 并发安全：原子获取历史快照
    history = await conv_history.get_messages(session_id)
    
    context = build_context(request.query, knowledge_base)
    system_prompt = (
        "你是 AI Radar 系统的智能助手，服务于 AI 产品经理。\n"
        "## 你的职责\n"
        "- 基于知识图谱回答 AI 领域问题\n"
        "- 提供产品洞察和趋势分析\n"
        "- 帮助理解技术概念和商业价值\n\n"
        f"## 当前知识库上下文\n{context}\n\n"
        "## 回答规则\n"
        "1. 用中文回答，简洁专业\n"
        "2. 引用具体数据或项目时注明名称\n"
        "3. 如果知识库中没有相关信息，如实告知\n"
        "4. 回答要有洞察力，不要泛泛而谈"
    )
    
    messages = [{"role": "system", "content": system_prompt}] + history
    messages.append({"role": "user", "content": request.query})
    
    try:
        # max_tokens=600 控制回答长度，缩短生成时间（约 8-12 秒）
        answer = await call_llm_async(messages, temperature=0.5, max_tokens=600)
    except Exception as e:
        logger.error(f"LLM 调用失败: {e}")
        raise HTTPException(status_code=500, detail="AI 服务暂时不可用，请稍后再试")
    
    # 并发安全：原子追加一轮对话
    await conv_history.add_turn(session_id, request.query, answer)
    
    return {"answer": answer, "session_id": session_id, "quota": quota_mgr.get_status()}

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """流式问答接口 (SSE)。"""
    allowed, status = await quota_mgr.check_and_consume()
    if not allowed:
        return JSONResponse(status_code=429, content={
            "error": "quota_exceeded",
            "message": status["message"].format(used=status["used"], limit=status["limit"]),
            "quota": status,
        })
    
    session_id = request.session_id or f"session_{uuid.uuid4().hex[:8]}"
    
    # 并发安全：原子获取历史快照
    history = await conv_history.get_messages(session_id)
    
    context = build_context(request.query, knowledge_base)
    system_prompt = (
        "你是 AI Radar 系统的智能助手，服务于 AI 产品经理。\n"
        f"## 当前知识库上下文\n{context}\n"
        "## 回答规则\n"
        "1. 用中文回答，简洁专业\n2. 引用具体数据或项目时注明名称\n"
        "3. 如果知识库中没有相关信息，如实告知\n4. 回答要有洞察力"
    )
    
    messages = [{"role": "system", "content": system_prompt}] + history
    messages.append({"role": "user", "content": request.query})
    
    async def event_generator() -> AsyncGenerator[str, None]:
        full_answer = []
        try:
            # 修复：使用 call_llm_stream 而非 call_llm_async
            async for chunk in call_llm_stream(messages, temperature=0.5, max_tokens=1500):
                full_answer.append(chunk)
                yield f"data: {json.dumps({'delta': chunk, 'done': False})}\n\n"
            
            answer_text = "".join(full_answer)
            # 并发安全：原子追加一轮对话
            await conv_history.add_turn(session_id, request.query, answer_text)
            
            yield f"data: {json.dumps({'delta': '', 'done': True, 'session_id': session_id, 'quota': quota_mgr.get_status()})}\n\n"
        except Exception as e:
            logger.error(f"流式输出异常: {e}")
            yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.delete("/chat/{session_id}")
async def clear_chat(session_id: str):
    await conv_history.clear_session(session_id)
    return {"status": "ok", "message": f"Session {session_id} cleared"}

@app.get("/knowledge/stats")
def knowledge_stats():
    return {
        "total_nodes": knowledge_base.get("stats", {}).get("total_nodes", 0),
        "today_items": knowledge_base.get("stats", {}).get("today_items", 0),
        "pillars": knowledge_base.get("pillars", {}),
        "daily_summary_date": knowledge_base.get("daily_summary", {}).get("date"),
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    
    import uvicorn
    logger.info(f"🚀 AI Radar Chat Server v2 启动中...")
    logger.info(f"📡 地址: http://{args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
