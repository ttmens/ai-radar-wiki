#!/usr/bin/env python3
"""
Unified AI Model Router for AI Radar System v2.

All LLM calls across the system should go through this module.
Features:
- Scene-aware model routing (simple→flash, code→qwen-coder, analysis→qwen-plus)
- Automatic fallback per scene
- API key management (loads from .env, never exposes in logs)
- Configurable timeouts and retries
- Usage logging for cost tracking

Scene Types:
- simple: Quick tasks, translations, summaries (DeepSeek flash)
- analysis: Deep analysis, classification (qwen3.6-plus)
- summary: Long-form summary generation (qwen3.6-plus)
- code: Code generation/review (qwen-coder or qwen-plus)
- default: General purpose (DeepSeek flash)

Usage:
    from ai_model_router import call_llm
    
    # Simple task → uses flash model
    result = call_llm(prompt="Translate this...", scene="simple")
    
    # Deep analysis → uses qwen-plus
    result = call_llm(prompt="Analyze...", scene="analysis", require_json=True)
"""

import json
import logging
import os
import re
import time
from dataclasses import dataclass
from typing import Optional

# Suppress API keys in logs
API_KEY_PATTERN = re.compile(r'sk-[a-zA-Z0-9]+')

logger = logging.getLogger(__name__)


# =============================================================================
# Model Configuration
# =============================================================================

@dataclass
class ModelConfig:
    name: str
    base_url: str
    api_key: str
    model: str
    timeout: int = 60
    max_retries: int = 2
    
    def is_available(self) -> bool:
        return bool(self.api_key and self.base_url and self.model)
    
    def __repr__(self):
        return f"ModelConfig({self.name}, {self.model})"


@dataclass
class SceneConfig:
    """Defines which models to use for a specific scene."""
    name: str
    primary: str      # Model name for primary
    fallback: str     # Model name for fallback
    timeout: int = 60
    max_tokens: int = 2000
    temperature: float = 0.3


# =============================================================================
# Environment Loading
# =============================================================================

def _load_env_file():
    """Load .env file if not already in environment."""
    env_path = os.path.expanduser("~/.hermes/.env")
    if not os.path.exists(env_path):
        return
    
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key not in os.environ:
                    os.environ[key] = val


def _get_all_models() -> dict:
    """Get all configured models."""
    _load_env_file()
    
    models = {}
    
    # DeepSeek models (fast, cost-effective)
    ds_key = os.environ.get("DEEPSEEK_API_KEY", "")
    ds_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    if ds_key:
        models["deepseek-flash"] = ModelConfig(
            name="deepseek-flash",
            base_url=ds_url,
            api_key=ds_key,
            model="deepseek-v4-flash",
            timeout=45,
            max_retries=1,
        )
        models["deepseek-pro"] = ModelConfig(
            name="deepseek-pro",
            base_url=ds_url,
            api_key=ds_key,
            model="deepseek-v4-pro",
            timeout=60,
            max_retries=2,
        )
    
    # DashScope models (qwen series)
    ds_api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    ds_api_url = os.environ.get("DASHSCOPE_BASE_URL", "https://coding.dashscope.aliyuncs.com/v1")
    if ds_api_key:
        models["qwen-plus"] = ModelConfig(
            name="qwen-plus",
            base_url=ds_api_url,
            api_key=ds_api_key,
            model="qwen3.6-plus",
            timeout=60,
            max_retries=2,
        )
        # Optional: qwen-coder for code tasks
        models["qwen-coder"] = ModelConfig(
            name="qwen-coder",
            base_url=ds_api_url,
            api_key=ds_api_key,
            model="qwen3-coder-plus",
            timeout=90,
            max_retries=2,
        )
    
    return models


def get_scene_config(scene: str) -> list:
    """Get model chain for a specific scene.
    
    Returns list of ModelConfigs in priority order.
    """
    models = _get_all_models()
    
    # Scene definitions
    # Priority: DeepSeek flash is fastest and most reliable for most tasks
    scenes = {
        "simple": ["deepseek-flash", "deepseek-pro", "qwen-plus"],
        "analysis": ["deepseek-flash", "deepseek-pro", "qwen-plus"],
        "summary": ["deepseek-flash", "deepseek-pro", "qwen-plus"],
        "code": ["qwen-coder", "qwen-plus", "deepseek-pro"],
        "default": ["deepseek-flash", "deepseek-pro", "qwen-plus"],
    }
    
    scene_models = scenes.get(scene, scenes["default"])
    return [models[m] for m in scene_models if m in models and models[m].is_available()]


# =============================================================================
# Core LLM Calling Logic
# =============================================================================

def _make_request(config: ModelConfig, messages: list, temperature: float, 
                  max_tokens: int, timeout: int = None) -> dict:
    """Make a single LLM API request."""
    import requests
    
    url = f"{config.base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.api_key}",
    }
    payload = {
        "model": config.model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    effective_timeout = timeout or config.timeout
    response = requests.post(url, json=payload, headers=headers, timeout=effective_timeout)
    response.raise_for_status()
    return response.json()


def _extract_json(content: str) -> dict:
    """Extract JSON from LLM response (handles markdown code blocks)."""
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        # Remove opening code fence
        if lines[0].strip().startswith("```"):
            lines = lines[1:]
        # Remove closing code fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines)
    return json.loads(content)


def call_llm(
    prompt: str,
    system_prompt: str = "你是一个AI助手。",
    scene: str = "default",
    model_type: str = None,  # Legacy: maps to scene
    temperature: float = None,
    max_tokens: int = 2000,
    require_json: bool = False,
    timeout: Optional[int] = None,
) -> Optional[dict | str]:
    """
    Unified LLM call with scene-aware model routing.
    
    Scene mapping (auto-selects best model):
    - simple: Quick tasks → DeepSeek flash (~1s)
    - analysis: Deep analysis → qwen3.6-plus (~6s)
    - summary: Long summaries → qwen3.6-plus (~6s)
    - code: Code tasks → qwen-coder (~10s)
    - default: General → DeepSeek flash
    
    Args:
        prompt: User prompt
        system_prompt: System prompt
        scene: Task scene (simple|analysis|summary|code|default)
        model_type: Legacy param, maps to scene if scene not set
        temperature: Sampling temperature (scene default if None)
        max_tokens: Max output tokens
        require_json: If True, parse response as JSON
        timeout: Override timeout in seconds
    
    Returns:
        Parsed JSON dict (if require_json=True) or raw string response.
        None if all models fail.
    """
    # Legacy compatibility: model_type → scene
    if scene == "default" and model_type:
        type_to_scene = {
            "analysis": "analysis",
            "summary": "summary",
            "translation": "simple",
        }
        scene = type_to_scene.get(model_type, "default")
    
    # Get scene defaults
    scene_defaults = {
        "simple": {"temperature": 0.3, "max_tokens": 500},
        "analysis": {"temperature": 0.3, "max_tokens": 500},
        "summary": {"temperature": 0.4, "max_tokens": 4000},
        "code": {"temperature": 0.1, "max_tokens": 4000},
        "default": {"temperature": 0.3, "max_tokens": 2000},
    }
    defaults = scene_defaults.get(scene, scene_defaults["default"])
    
    if temperature is None:
        temperature = defaults["temperature"]
    if max_tokens == 2000 and scene != "default":  # User didn't override
        max_tokens = defaults["max_tokens"]
    
    # Get model chain for this scene
    model_chain = get_scene_config(scene)
    if not model_chain:
        logger.error("No models available for any scene")
        return None
    
    # Build messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    
    last_error = None
    
    for config in model_chain:
        if not config.is_available():
            continue
        
        effective_timeout = timeout or config.timeout
        
        for attempt in range(config.max_retries + 1):
            try:
                if attempt > 0:
                    wait = (attempt + 1) * 2
                    logger.info(f"Retrying {config.name} (attempt {attempt+1}) in {wait}s...")
                    time.sleep(wait)
                
                start = time.time()
                result = _make_request(config, messages, temperature, max_tokens, effective_timeout)
                elapsed = time.time() - start
                
                # Extract content
                content = result["choices"][0]["message"]["content"].strip()
                
                # Log usage (without exposing keys)
                model_display = f"{config.name}/{config.model}"
                usage = result.get('usage', {})
                logger.info(
                    f"LLM [{scene}] {model_display} succeeded in {elapsed:.1f}s "
                    f"(tokens: {usage.get('total_tokens', '?')})"
                )
                
                # Parse if JSON required
                if require_json:
                    try:
                        return _extract_json(content)
                    except json.JSONDecodeError as e:
                        logger.warning(f"JSON parse failed for {config.name}: {e}")
                        if attempt < config.max_retries:
                            continue
                        return None
                
                return content
                
            except Exception as e:
                last_error = e
                logger.warning(f"{config.name} attempt {attempt+1} failed: {str(e)[:100]}")
                continue
    
    logger.error(f"All models failed for scene '{scene}'. Last error: {last_error}")
    return None


# =============================================================================
# Convenience Functions for AI Radar
# =============================================================================

def analyze_item(title: str, summary: str, item_type: str = "unknown", 
                 pillar_guess: str = "unknown") -> Optional[dict]:
    """Analyze a single AI item for pillar classification and PM relevance."""
    prompt = f"""分析以下 AI 领域内容，输出 JSON：

标题: {title}
摘要: {summary[:300]}
类型: {item_type}
初步分类: {pillar_guess}

要求：
1. summary_cn: 用中文总结（120-180字），面向 AI 产品经理，突出技术要点/商业价值/产品创新
2. pillar: 确认分类（capabilities/patterns/ecosystem/business）
3. pm_relevance: PM 相关性评分 1-10
4. concepts: 提取 2-3 个核心概念标签（如 ["AI Memory", "Long-term Context"]），用于知识聚合
5. entities: 提取涉及的公司/组织/项目名（如 ["MemPalace", "OpenAI"]），最多 3 个
6. patterns: 提取产品/技术模式（如 ["Copilot Pattern", "Local-First AI"]），最多 2 个

只输出 JSON 格式：
{{"summary_cn": "...", "pillar": "...", "pm_relevance": 5, "concepts": ["概念1", "概念2"], "entities": ["实体1"], "patterns": ["模式1"]}}"""

    return call_llm(
        prompt=prompt,
        system_prompt="你是 AI 产品分析师，擅长从技术信息中提炼产品经理关注的关键点。",
        model_type="analysis",
        temperature=0.3,
        max_tokens=500,
        require_json=True,
    )


def generate_daily_summary(items: list) -> Optional[dict]:
    """Generate daily AI Radar summary."""
    item_list = ""
    for i, item in enumerate(items[:20], 1):
        pillar = item.get("pillar", "unknown")
        score = item.get("pm_score", 0)
        title = item.get("label", "")[:70]
        summary_text = (item.get("summary", "") or "")[:200]
        tags = ", ".join(item.get("tags", []) or [])
        item_list += f"{i}. [ID:{item.get('id','')}] [{pillar}] {title} (PM {score:.2f})\n   {summary_text}\n"
        if tags:
            item_list += f"   标签: {tags}\n"
    
    from datetime import datetime, timezone, timedelta
    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    
    prompt = f"""你是AI产品设计雷达的首席情报官，服务于AI产品经理。请基于今日情报生成深度分析摘要。

## 核心要求

**不要逐条描述！** 你需要做跨节点综合分析，识别：
1. **跨节点叙事主线**：今天多条情报是否指向同一个大趋势？
2. **行业拐点信号**：哪些变化标志着行业进入新阶段？
3. **PM行动启示**：这些趋势对AI产品经理意味着什么？

## 今日情报
{item_list}

## 输出格式
{{
  "date": "{today}",
  "headline": "今日 AI 情报 · {today}",
  "overview": "用一句话概括今天最重要的跨节点趋势或信号（15-30字）",
  "narratives": [
    {{
      "title": "叙事标题",
      "body": "2-3句深度分析",
      "type": "paradigm_shift|bottleneck|maturation|validation",
      "pillar_key": "最相关的pillar"
    }}
  ],
  "insights": [
    {{
      "pillar": "📱 产品模式",
      "pillar_key": "patterns",
      "narrative_title": "对应的叙事标题",
      "insight": "以叙事标题开头：'{{narrative_title}}。该方向的具体信号：...'",
      "evidence": [
        {{"id": "节点ID", "title": "标题", "score": 0.0}}
      ]
    }}
  ],
  "stats": "技术能力: X | 产品模式: Y | 工具生态: Z | 商业趋势: W",
  "total_items": 总数,
  "high_value_count": PM Score >= 0.3 的数量
}}

只输出JSON，不要其他内容。"""

    return call_llm(
        prompt=prompt,
        system_prompt="你是AI情报分析师，擅长跨节点综合研判，输出纯JSON。",
        model_type="summary",
        temperature=0.4,
        max_tokens=4000,
        require_json=True,
    )


# =============================================================================
# CLI Testing
# =============================================================================

if __name__ == "__main__":
    print("=== AI Model Router v2 Test ===\n")
    
    # Show all available models
    models = _get_all_models()
    print(f"Configured models ({len(models)}):")
    for name, cfg in models.items():
        status = "✅" if cfg.is_available() else "❌"
        print(f"  {status} {name}: {cfg.model} (timeout={cfg.timeout}s)")
    
    # Test different scenes
    scenes = ["simple", "analysis", "default"]
    
    for scene in scenes:
        print(f"\n--- Test Scene: {scene} ---")
        chain = get_scene_config(scene)
        print(f"  Model chain: {[c.name for c in chain]}")
        
        if scene == "simple":
            prompt = "用一句话回答：1+1等于几？"
            result = call_llm(
                prompt=prompt,
                system_prompt="你是一个简洁的助手，回答不超过10个字。",
                scene=scene,
                temperature=0.1,
                max_tokens=50,
            )
        elif scene == "analysis":
            result = call_llm(
                prompt="分析以下 AI 趋势：GPT-5 发布，支持 1M tokens 上下文",
                system_prompt="你是 AI 产品分析师",
                scene=scene,
                require_json=True,
            )
        else:
            result = call_llm(
                prompt="你好",
                system_prompt="你是助手",
                scene=scene,
            )
        
        print(f"  Response: {str(result)[:100]}...")
