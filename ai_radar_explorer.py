#!/usr/bin/env python3
"""
AI Radar Wiki Explorer v3 — AI PM 知识雷达系统

面向 AI 产品经理的 4 大支柱知识体系：
1. 模型与技术能力 (capabilities) — Context, Latency, Cost, Multimodal
2. 产品与交互模式 (patterns) — Chat, Copilot, Agent Workflow
3. 工具与生态 (ecosystem) — Orchestration, VectorDB, Eval Tools
4. 商业与趋势 (business) — Funding, Moat, Growth, Ethics

自进化机制：
- pm_score 动态权重计算（信号强度 + 时效性 + 互动反馈）
- 自动淘汰机制（90天无更新 + 低分节点降权）
- 趋势检测（新标签涌现自动上报）
"""

import json, os, sys, hashlib, time, re, shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from collections import Counter

WIKI_DIR = "/home/admin/ai-radar-wiki"
DOCS_DIR = f"{WIKI_DIR}/docs"
RAW_GITHUB = f"{WIKI_DIR}/raw/github"
RAW_PAPERS = f"{WIKI_DIR}/raw/papers"
RAW_HN = f"{WIKI_DIR}/raw/hn"
RAW_PRODUCTS = f"{WIKI_DIR}/raw/products"
STATE_FILE = "/home/admin/.hermes/cron/explorer_state.json"
FEEDBACK_FILE = f"{WIKI_DIR}/feedback.json"

for d in [RAW_GITHUB, RAW_PAPERS, RAW_HN, RAW_PRODUCTS,
          f"{WIKI_DIR}/wiki/entities"]:
    os.makedirs(d, exist_ok=True)

# Ensure vis-network.min.js exists in wiki dir
VIS_JS = f"{WIKI_DIR}/assets/vis-network.min.js"
if not os.path.exists(VIS_JS):
    # Try to copy from /tmp
    if os.path.exists("/tmp/vis-network.min.js"):
        shutil.copy("/tmp/vis-network.min.js", VIS_JS)
        print("  📦 Copied vis-network.min.js to wiki dir")

PILLAR_KEYWORDS = {
    "capabilities": [
        "context window", "latency", "inference", "token", "benchmark",
        "multimodal", "vision", "audio", "video generation", "reasoning",
        "fine-tuning", "quantization", "gguf", "vllm", "throughput",
        "training", "rlhf", "dpo", "grpo", "sft",
        "embedding", "rerank", "compression", "distillation",
        "safety research", "alignment research", "model architecture",
        "neural network", "transformer", "attention", "parameter",
        "accuracy", "precision", "recall", "loss function", "gradient",
        "optimization", "dataset", "cnn", "rnn", "gan", "diffusion model",
        "llm research", "model training", "pre-training", "post-training",
        "scaling law", "emergent ability", "chain of thought", "retrieval",
        "knowledge graph", "vector search", "similarity", "clustering"
    ],
    "patterns": [
        "agent", "copilot", "workflow", "chatbot", "assistant",
        "autocomplete", "code generation", "text-to-image", "image-to-text",
        "voice", "speech-to-text", "translation", "summarization",
        "rag", "retrieval-augmented", "memory", "tool use",
        "planning", "multi-agent", "autonomous", "background task",
        "human-in-the-loop", "prompt engineering", "prompt chain",
        "function calling", "structured output", "code assistant",
        "ai assistant", "conversational ai", "task automation"
    ],
    "ecosystem": [
        "framework", "sdk", "api", "langchain", "langgraph", "crewai",
        "autogen", "vector database", "chroma", "pinecone", "weaviate",
        "evaluation", "eval", "monitoring", "observability", "logging",
        "deployment", "serving", "open source", "library", "plugin",
        "integration", "mcp", "protocol",
        "devtool", "developer tool", "ci/cd", "version control",
        "git for ai", "agent framework", "orchestration", "pipeline",
        "testing", "debugging", "profiling", "infrastructure"
    ],
    "business": [
        "funding", "valuation", "revenue", "pricing", "market share",
        "competitor analysis", "moat", "startup launch", "acquisition", "ipo",
        "regulation", "policy change", "ethics debate",
        "enterprise adoption", "saas pricing", "user growth", "churn rate",
        "layoff", "hiring", "partnership", "joint venture",
        "data breach", "privacy violation", "security incident",
        "antitrust", "copyright lawsuit", "patent dispute"
    ]
}

AI_KEYWORDS = [
    "ai", "llm", "gpt", "agent", "claude", "openai", "anthropic", "gemini",
    "llama", "mistral", "model", "machine learning", "ml", "deep learning",
    "transformer", "neural", "diffusion", "stable diffusion", "midjourney",
    "copilot", "chatbot", "rag", "vector", "embedding", "fine-tune",
    "inference", "training", "benchmark", "huggingface", "hf",
    "text-to-image", "text-to-video", "voice", "speech", "multimodal",
    "artificial intelligence", "generative", "genai", "agi"
]


def classify_pillar(text):
    text_lower = text.lower()
    matches = {}
    for pillar, keywords in PILLAR_KEYWORDS.items():
        matched = [kw for kw in keywords if kw in text_lower]
        if matched:
            # Weight capabilities higher for technical terms
            weight = 1.2 if pillar == "capabilities" else 1.0
            matches[pillar] = (len(matched), weight * len(matched), matched)
    if not matches:
        # Default to capabilities for research/academic content that doesn't match other pillars
        return ("capabilities", [])
    # Sort by weighted score
    primary = max(matches.keys(), key=lambda p: matches[p][1])
    return (primary, matches[primary][2])


def is_ai_relevant(text):
    text_lower = text.lower()
    return any(kw in text_lower for kw in AI_KEYWORDS)


# v3.8.2: 噪音过滤 — 排除促销、招聘、会议等低价值内容
NOISE_PATTERNS = [
    "get 50% off", "discount", "early bird", "last day", "register now",
    "join us at", "coming to", "conference 2026", "summit 2026",
    "we're hiring", "job opening", "career opportunity",
    "ad:", "sponsored", "promoted",
    "newsletter:", "subscribe to", "sign up for",
]

def is_noise(text):
    """过滤促销、招聘、会议广告等低价值内容"""
    text_lower = text.lower()
    return any(pattern in text_lower for pattern in NOISE_PATTERNS)


# ========== LLM Analysis (DashScope) ==========

def _load_env_file():
    """Load .env file if not already in environment."""
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

_load_env_file()

# LLM API keys now managed by ai_model_router — see below for import
LLM_CACHE_FILE = os.path.join(os.path.dirname(STATE_FILE), "llm_cache.json")

# Unified AI model router (dual-model fallback)
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from ai_model_router import analyze_item as router_analyze_item
    HAS_MODEL_ROUTER = True
except ImportError:
    HAS_MODEL_ROUTER = False
    print("  ⚠️ ai_model_router not found, using direct API calls")


def load_llm_cache():
    """Load LLM analysis cache to avoid re-analyzing same items."""
    if os.path.exists(LLM_CACHE_FILE):
        try:
            with open(LLM_CACHE_FILE) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_llm_cache(cache):
    """Persist LLM analysis cache (with 500-entry capacity limit)."""
    try:
        # Capacity limit: trim oldest entries if over 500
        if len(cache) > 500:
            # Sort by timestamp (oldest first) and keep newest 500
            sorted_items = sorted(cache.items(), key=lambda x: x[1].get("timestamp", 0))
            cache = dict(sorted_items[-500:])
            print(f"  🧹 LLM cache trimmed to 500 entries")
        with open(LLM_CACHE_FILE, "w") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"  ⚠️ Failed to save LLM cache: {e}")


def analyze_item_llm(title, summary, item_type, pillar_guess, retries=3):
    """Call LLM to analyze a single item with retry logic.
    
    v3.15.0: Uses scene-aware routing. Analysis tasks use qwen-plus (primary) 
    with deepseek fallback for better reasoning quality.
    """
    # Try router's specialized analyze_item first
    if HAS_MODEL_ROUTER:
        result = router_analyze_item(title, summary, item_type, pillar_guess)
        if result:
            return result
    
    # Fallback to router's generic call_llm with analysis scene
    try:
        from ai_model_router import call_llm as router_call_llm
        
        prompt = f"""分析以下 AI 领域内容，输出 JSON：

标题: {title}
摘要: {summary[:300]}
类型: {item_type}
初步分类: {pillar_guess}

要求：
1. summary_cn: 用中文总结（120-180字），面向 AI 产品经理，突出技术要点/商业价值/产品创新
2. pillar: 确认分类（capabilities/patterns/ecosystem/business）
3. pm_relevance: PM 相关性评分 1-10
4. concepts: 提取 2-3 个核心概念标签（如 ["AI Memory", "Long-term Context", "Benchmark-driven"]），用于知识聚合
5. entities: 提取涉及的公司/组织/项目名（如 ["MemPalace", "OpenAI"]），最多 3 个
6. patterns: 提取产品/技术模式（如 ["Copilot Pattern", "Local-First AI", "Agent Orchestration"]），最多 2 个

只输出 JSON 格式：
{{"summary_cn": "...", "pillar": "...", "pm_relevance": 5, "concepts": ["概念1", "概念2"], "entities": ["实体1"], "patterns": ["模式1"]}}"""
        
        return router_call_llm(
            prompt=prompt,
            system_prompt="你是 AI 产品分析师，擅长从技术信息中提炼产品经理关注的关键点。",
            scene="analysis",
            temperature=0.3,
            max_tokens=500,
            require_json=True,
            timeout=45,
        )
    except ImportError:
        print("  ⚠️ ai_model_router 不可用，跳过单条分析")
        return None


def batch_analyze_items(items, state, max_concurrent=8):
    """Analyze new items with LLM using controlled concurrency and retries.

    Args:
        items: List of items to analyze
        state: Current pipeline state
        max_concurrent: Maximum number of concurrent LLM requests (default: 5)
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time

    # Check if model router is available for analysis scene
    try:
        from ai_model_router import get_scene_config
        models = get_scene_config("analysis")
        if not models:
            print("  ⚠️ 无可用 AI 模型，跳过 LLM 分析")
            return 0
    except ImportError:
        print("  ⚠️ ai_model_router 不可用，跳过 LLM 分析")
        return 0

    cache = load_llm_cache()
    analyzed = 0
    cache_hit = 0
    cache_miss = 0
    pillar_counts = Counter()
    failed = 0

    # Separate cached vs uncached items
    to_analyze = []
    for item in items:
        title = item.get("title", "") or item.get("name", "") or ""
        cache_key = md5_hash(title + item.get("summary", ""))

        if cache_key in cache:
            cached = cache[cache_key]
            item["summary_cn"] = cached.get("summary_cn", "")
            item["pillar"] = cached.get("pillar", item.get("pillar", "unknown"))
            item["pm_relevance"] = cached.get("pm_relevance", 5)
            item["pillar"] = item.get("pillar", "unknown") or "business"
            # 新增：缓存命中也恢复 concepts/entities/patterns
            item["concepts"] = cached.get("concepts", [])
            item["entities"] = cached.get("entities", [])
            item["patterns"] = cached.get("patterns", [])
            analyzed += 1
            cache_hit += 1
        else:
            item["_cache_key"] = cache_key
            to_analyze.append(item)

    cache_miss = len(to_analyze)

    # Limit LLM calls per run to avoid excessive runtime (200 items = 19 min)
    MAX_LLM_PER_RUN = 30
    if len(to_analyze) > MAX_LLM_PER_RUN:
        # Sort by priority: GitHub stars, then by source relevance
        def item_priority(item):
            stars = item.get("stars", 0)
            score = item.get("score", 0)
            tag_priority = {"GitHub": 3, "TechCrunch": 2, "arxiv": 2, "ProductHunt": 2, "Show HN": 1, "Hacker News": 1}
            return (stars, score * 100, tag_priority.get(item.get("tag", ""), 0))
        to_analyze.sort(key=item_priority, reverse=True)
        skipped = to_analyze[MAX_LLM_PER_RUN:]
        for item in skipped:
            # Fallback for skipped items
            text = " ".join([item.get("title", "") or item.get("name", ""), item.get("summary", "") or item.get("description", "")])
            pillar, _ = classify_pillar(text)
            item["pillar"] = pillar if pillar != "unknown" else "business"
            item["summary_cn"] = ""
            item["pm_relevance"] = 3
            item["concepts"] = []
            item["entities"] = []
            item["patterns"] = []
        to_analyze = to_analyze[:MAX_LLM_PER_RUN]
        print(f"  📊 限制 LLM 分析: 最多 {MAX_LLM_PER_RUN} 条 (按 stars 排序), {len(skipped)} 条走关键词降级")

    if to_analyze:
        print(f"  🤖 LLM 分析: {len(to_analyze)} 条新情报 (并发={max_concurrent}, 重试=3)...")
        print(f"  📊 缓存命中: {cache_hit}/{len(items)}")

        # Concurrent execution with progress tracking
        start = time.time()
        completed = 0

        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            future_map = {}
            for item in to_analyze:
                title = item.get("title", "") or item.get("name", "") or ""
                summary = item.get("summary", "") or item.get("description", "") or ""
                item_type = item.get("tag", "unknown")
                pillar_guess = item.get("pillar", "unknown")

                future = executor.submit(analyze_item_llm, title, summary, item_type, pillar_guess, retries=3)
                future_map[future] = item

            for future in as_completed(future_map):
                item = future_map[future]
                try:
                    result = future.result()
                    if result:
                        item["summary_cn"] = result.get("summary_cn", "")
                        item["pillar"] = result.get("pillar", item.get("pillar", "unknown"))
                        item["pillar"] = item.get("pillar") or "business"
                        item["pm_relevance"] = result.get("pm_relevance", 5)
                        # 新增：提取 concepts/entities/patterns
                        item["concepts"] = result.get("concepts", [])
                        item["entities"] = result.get("entities", [])
                        item["patterns"] = result.get("patterns", [])
                        cache_key = item.get("_cache_key", "")
                        if cache_key:
                            cache[cache_key] = {
                                "summary_cn": item["summary_cn"],
                                "pillar": item["pillar"],
                                "pm_relevance": item["pm_relevance"],
                                # 新增：缓存 concepts/entities/patterns
                                "concepts": item["concepts"],
                                "entities": item["entities"],
                                "patterns": item["patterns"],
                            }
                        analyzed += 1
                        pillar_counts[item["pillar"]] += 1
                    else:
                        # Fallback to keyword classification
                        text = " ".join([
                            item.get("title", "") or item.get("name", ""),
                            item.get("summary", "") or item.get("description") or "",
                        ])
                        pillar, _ = classify_pillar(text)
                        item["pillar"] = pillar if pillar != "unknown" else "business"
                        item["summary_cn"] = ""
                        item["pm_relevance"] = 3
                        item["concepts"] = []
                        item["entities"] = []
                        item["patterns"] = []
                        failed += 1
                except Exception as e:
                    failed += 1

                completed += 1
                # Progress bar every 5 items
                if completed % 5 == 0 or completed == cache_miss:
                    elapsed = time.time() - start
                    rate = completed / elapsed if elapsed > 0 else 0
                    eta = (cache_miss - completed) / rate if rate > 0 else 0
                    print(f"  ⏳ {completed}/{cache_miss} 完成 ({elapsed:.0f}s, 剩余{eta:.0f}s)")

        elapsed = time.time() - start
        print(f"  ⏱️  LLM 总耗时: {elapsed:.0f}s ({cache_miss}条, {elapsed/max(1,cache_miss):.1f}s/条)")

    # Clean up internal keys
    for item in items:
        item.pop("_cache_key", None)

    save_llm_cache(cache)
    print(f"  ✅ 分析完成: 总计 {analyzed}/{len(items)} (缓存命中 {cache_hit}, 新分析 {cache_miss - failed}, 降级 {failed})")
    if pillar_counts:
        print(f"  📊 分类分布: {dict(pillar_counts)}")
    return analyzed


def calculate_pm_score(item):
    """Calculate PM-focused score with LLM-enhanced relevance."""
    score = 0.0

    # 1. Engagement signal (stars/HN score) - max 0.3
    if item.get("stars"):
        stars = item["stars"]
        if stars >= 10000: score += 0.3
        elif stars >= 5000: score += 0.25
        elif stars >= 1000: score += 0.2
        elif stars >= 500: score += 0.15
        elif stars >= 100: score += 0.1
        else: score += 0.05
    elif item.get("score"):
        hn_score = item["score"]
        if hn_score >= 500: score += 0.25
        elif hn_score >= 200: score += 0.2
        elif hn_score >= 100: score += 0.15
        elif hn_score >= 50: score += 0.1
        else: score += 0.05

    # 2. Discussion signal - max 0.15
    if item.get("comments", 0) >= 200: score += 0.15
    elif item.get("comments", 0) >= 100: score += 0.12
    elif item.get("comments", 0) >= 50: score += 0.1
    elif item.get("comments", 0) >= 20: score += 0.05

    # 3. Timeliness - max 0.2
    pub_date = item.get("published") or item.get("created") or item.get("pub_date") or item.get("created_at", "")
    if pub_date:
        try:
            # Try ISO format first
            pub_dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00").split("+")[0])
            days_old = (datetime.now() - pub_dt).days
        except (ValueError, AttributeError):
            try:
                # Fallback: RFC 822 format (e.g., "Thu, 07 May 2026 22:24:50")
                from email.utils import parsedate_to_datetime
                pub_dt = parsedate_to_datetime(pub_date)
                if pub_dt.tzinfo:
                    pub_dt = pub_dt.replace(tzinfo=None)
                days_old = (datetime.now() - pub_dt).days
            except Exception:
                # Last fallback: try strptime for common formats
                for fmt in ["%a, %d %b %Y %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%B %d, %Y"]:
                    try:
                        pub_dt = datetime.strptime(pub_date.strip(), fmt)
                        days_old = (datetime.now() - pub_dt).days
                        break
                    except ValueError:
                        continue
                else:
                    pub_dt = None
                    days_old = 7  # default
        
        if pub_dt is not None:
            if days_old <= 1: score += 0.2
            elif days_old <= 7: score += 0.15
            elif days_old <= 30: score += 0.1
            elif days_old <= 90: score += 0.05
        else:
            score += 0.05

    # 4. LLM PM relevance - max 0.35 (most important!)
    pm_rel = item.get("pm_relevance", 0)
    if pm_rel:
        score += (pm_rel / 10.0) * 0.35
    else:
        # Fallback: keyword-based relevance
        text = " ".join([item.get("name", "") or "", item.get("title", "") or "", item.get("description", "") or "", item.get("summary", "") or "", " ".join(item.get("topics", []) or [])])
        if is_ai_relevant(text): score += 0.15
        pillar, _ = classify_pillar(text)
        if pillar != "unknown": score += 0.1

    return min(round(score, 3), 1.0)


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:80].strip('-') or "untitled"


def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()[:12]


def rebuild_seen_from_raw():
    """Rebuild dedup seen set from all raw JSON files across sources."""
    seen = set()
    raw_dirs = [RAW_GITHUB, RAW_PAPERS, RAW_HN, RAW_PRODUCTS,
                f"{WIKI_DIR}/raw/techcrunch", f"{WIKI_DIR}/raw/showhn"]
    for raw_dir in raw_dirs:
        if not os.path.exists(raw_dir):
            continue
        for fname in os.listdir(raw_dir):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(raw_dir, fname)
            try:
                with open(fpath) as f:
                    data = json.load(f)
                # Use URL as primary dedup key
                url = data.get("url") or data.get("hn_url") or ""
                if url:
                    seen.add(md5_hash(url))
            except Exception:
                pass
    return seen


def clean_old_raw(ttl_days=30):
    """Delete raw JSON files older than ttl_days to prevent disk bloat."""
    cutoff = time.time() - (ttl_days * 86400)
    raw_dirs = [RAW_GITHUB, RAW_PAPERS, RAW_HN, RAW_PRODUCTS,
                f"{WIKI_DIR}/raw/techcrunch", f"{WIKI_DIR}/raw/showhn"]
    removed = 0
    for raw_dir in raw_dirs:
        if not os.path.exists(raw_dir):
            continue
        for fname in os.listdir(raw_dir):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(raw_dir, fname)
            try:
                if os.path.getmtime(fpath) < cutoff:
                    os.remove(fpath)
                    removed += 1
            except Exception as e:
                print(f"  ⚠️ Error in clean_old_raw: failed to remove {fpath}: {e}")
    if removed > 0:
        print(f"  🧹 Cleaned {removed} old raw files (>{ttl_days} days)")
    return removed


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)
        state.setdefault("seen", [])
        state.setdefault("stats", {"total_items": 0, "by_source": {}})
        state.setdefault("evolution", {"pruned": 0, "merged": 0, "trending_tags": []})
        # Rebuild seen from raw/ directory to fix stale/incomplete dedup
        raw_seen = rebuild_seen_from_raw()
        # Merge: keep existing seen hashes + add from raw files
        state["seen"] = list(set(state["seen"]) | raw_seen)
        return state
    # Fresh state: build seen entirely from raw/ directory
    raw_seen = rebuild_seen_from_raw()
    return {"seen": list(raw_seen), "last_run": None, "stats": {"total_items": 0, "by_source": {}}, "evolution": {"pruned": 0, "merged": 0, "trending_tags": []}}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def is_new(url, state):
    if not url: return True
    h = md5_hash(url)
    if h in state["seen"]: return False
    state["seen"].append(h)
    if len(state["seen"]) > 5000: state["seen"] = state["seen"][-3000:]
    return True


def save_raw(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath


# ========== Data Collection ==========

def fetch_github():
    import requests
    items = []
    seen_repos = set()
    try:
        # GitHub API doesn't support OR in topic queries, so run separate queries
        queries = [
            "stars:>50 pushed:>2026-04-01 topic:llm",
            "stars:>50 pushed:>2026-04-01 topic:artificial-intelligence",
            "stars:>50 pushed:>2026-04-01 topic:ai",
            "stars:>50 pushed:>2026-04-01 topic:machine-learning",
            "stars:>50 pushed:>2026-04-01 topic:deep-learning",
        ]
        headers = {"User-Agent": "AI-Radar-Explorer/1.0", "Accept": "application/vnd.github+json"}
        for query in queries:
            for page in range(1, 3):
                r = requests.get("https://api.github.com/search/repositories",
                    params={"q": query, "sort": "stars", "order": "desc", "per_page": 30, "page": page},
                    headers=headers, timeout=20)
                if r.status_code != 200:
                    print(f"  ⚠️ GitHub API returned status {r.status_code} for '{query}'")
                    break
                repos = r.json().get("items", [])
                if not repos:
                    break
                for repo in repos:
                    full_name = repo["full_name"]
                    if full_name in seen_repos:
                        continue
                    seen_repos.add(full_name)
                    desc = repo.get("description", "") or ""
                    topics = repo.get("topics", [])
                    kw_text = " ".join([full_name, desc] + topics).lower()
                    if any(kw in kw_text for kw in AI_KEYWORDS):
                        pillar, keywords = classify_pillar(kw_text)
                        items.append({
                            "name": full_name, "description": desc,
                            "stars": repo["stargazers_count"],
                            "language": repo.get("language", ""),
                            "topics": topics, "url": repo["html_url"],
                            "created": repo.get("created_at", ""),
                            "tag": "GitHub", "pillar": pillar, "pillar_keywords": keywords
                        })
                if len(repos) < 30:
                    break
    except Exception as e:
        print(f"  ⚠️ Error in fetch_github: {e}")
    return items


def fetch_arxiv():
    import requests
    items = []
    try:
        url = "https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=15"
        r = requests.get(url, timeout=20, headers={"User-Agent": "AI-Radar-Explorer/1.0"})
        if r.status_code != 200: return items
        root = ET.fromstring(r.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns)[:12]:
            title = " ".join(entry.find("atom:title", ns).text.strip().split())
            summary = entry.find("atom:summary", ns).text.strip()
            link = entry.find("atom:id", ns).text
            published = entry.find("atom:published", ns).text if entry.find("atom:published", ns) is not None else ""
            authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns) if a.find("atom:name", ns) is not None][:5]
            pillar, keywords = classify_pillar(title + " " + summary)
            items.append({"title": title, "summary": summary, "url": link, "authors": authors, "published": published, "tag": "Paper", "pillar": pillar, "pillar_keywords": keywords})
    except Exception as e:
        print(f"  ⚠️ arXiv fetch error: {e}")
    return items


def fetch_hackernews():
    import requests
    items = []
    try:
        r = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=15)
        for sid in r.json()[:50]:
            sr = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10)
            story = sr.json()
            if not story: continue
            title = story.get("title", "")
            score = story.get("score", 0)
            if score >= 30 and is_ai_relevant(title):
                pillar, keywords = classify_pillar(title)
                items.append({"title": title, "score": score, "comments": story.get("descendants", 0), "url": story.get("url") or f"https://news.ycombinator.com/item?id={sid}", "hn_url": f"https://news.ycombinator.com/item?id={sid}", "tag": "HN", "pillar": pillar, "pillar_keywords": keywords})
    except Exception as e:
        print(f"  ⚠️ HN fetch error: {e}")
    return items


def fetch_product_hunt():
    """Product Hunt AI products — tries multiple sources, returns explicit fallback."""
    import requests
    items = []
    # Try 1: Product Hunt AI topics page (scrape for public data)
    try:
        r = requests.get("https://www.producthunt.com/topics/artificial-intelligence",
                         timeout=20,
                         headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"})
        if r.status_code == 200:
            # Extract product titles/links from meta tags or structured data
            og_pattern = re.compile(r'<meta[^>]+property="og:[^"]*"[^>]+content="([^"]*)"', re.DOTALL)
            title_matches = og_pattern.findall(r.text)
            if title_matches and any(is_ai_relevant(t) for t in title_matches):
                items.append({
                    "title": "Product Hunt — AI Topics",
                    "description": f"AI products on Product Hunt. Top titles: {', '.join(title_matches[:5])}",
                    "url": "https://www.producthunt.com/topics/artificial-intelligence",
                    "pub_date": datetime.now().isoformat(),
                    "tag": "Product", "pillar": "business", "pillar_keywords": ["product hunt", "ai products"]
                })
    except Exception as e:
        print(f"  ⚠️ Error in fetch_product_hunt (PH scrape): {e}")

    # Try 2: Betalist API as fallback
    if not items:
        try:
            r = requests.get("https://betalist.com/topics/artificial-intelligence.json", timeout=15)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    for entry in data[:10]:
                        title = entry.get("name", "")
                        tagline = entry.get("tagline", "")
                        if is_ai_relevant(title + " " + tagline):
                            pillar, keywords = classify_pillar(title + " " + tagline)
                            items.append({
                                "title": title, "description": tagline,
                                "url": entry.get("url", ""), "pub_date": entry.get("created_at", ""),
                                "tag": "Product", "pillar": pillar, "pillar_keywords": keywords
                            })
        except Exception as e:
            print(f"  ⚠️ Error in fetch_product_hunt (Betalist): {e}")

    # If all sources failed, mark as unavailable instead of silent failure
    if not items:
        print("  ⚠️ Product Hunt: 暂不可用 (all sources failed)")
        items.append({
            "title": "Product Hunt — 暂不可用",
            "description": "Product Hunt data source is currently unavailable. Check back later.",
            "url": "https://www.producthunt.com/topics/artificial-intelligence",
            "pub_date": datetime.now().isoformat(),
            "tag": "Product", "pillar": "business", "pillar_keywords": ["unavailable"]
        })
    return items


def fetch_techcrunch():
    """TechCrunch AI: 商业/融资/产品动态 (Business + Ecosystem pillars)"""
    import requests
    items = []
    try:
        r = requests.get("https://techcrunch.com/category/artificial-intelligence/feed/",
                         timeout=20, headers={"User-Agent": "AI-Radar-Explorer/1.0"})
        if r.status_code != 200: return items
        text = r.text
        # TechCrunch RSS format: <item>...\n\t\t<title>...</title>\n\t\t<link>...</link>\n...<pubDate>...</pubDate>
        item_pattern = re.compile(r'<item>(.*?)</item>', re.DOTALL)
        title_pattern = re.compile(r'<title>(.*?)</title>', re.DOTALL)
        link_pattern = re.compile(r'<link>(.*?)</link>', re.DOTALL)
        pubdate_pattern = re.compile(r'<pubDate>(.*?)</pubDate>', re.DOTALL)
        desc_pattern = re.compile(r'<description><!\[CDATA\[(.*?)\]\]>', re.DOTALL)
        
        count = 0
        for item_block in item_pattern.findall(text):
            if count >= 15: break
            tm = title_pattern.search(item_block)
            lm = link_pattern.search(item_block)
            dm = desc_pattern.search(item_block)
            pm = pubdate_pattern.search(item_block)
            if not tm or not lm: continue
            title = tm.group(1).strip()
            link = lm.group(1).strip()
            desc = dm.group(1).strip()[:500] if dm else ""
            desc = re.sub(r'<[^>]+>', '', desc).strip()[:500]
            pub_date = pm.group(1).strip() if pm else ""
            if not title: continue
            pillar, keywords = classify_pillar(title + " " + desc)
            if pillar == "unknown":
                pillar = "business"
                keywords = ["ai news"]
            items.append({"title": title, "description": desc, "url": link,
                          "pub_date": pub_date, "tag": "TechCrunch",
                          "pillar": pillar, "pillar_keywords": keywords})
            count += 1
    except Exception as e:
        print(f"  ⚠️ TechCrunch fetch error: {e}")
    return items


def fetch_hn_show():
    """Hacker News Show HN: 新产品/工具发布 (Ecosystem + Patterns)"""
    import requests
    items = []
    try:
        r = requests.get("https://hacker-news.firebaseio.com/v0/showstories.json", timeout=15)
        for sid in r.json()[:30]:
            sr = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10)
            story = sr.json()
            if not story: continue
            title = story.get("title", "")
            score = story.get("score", 0)
            if score >= 10 and is_ai_relevant(title):
                pillar, keywords = classify_pillar(title)
                if pillar == "unknown":
                    pillar = "ecosystem"  # Show HN is usually tools/frameworks
                items.append({"title": title, "score": score,
                              "comments": story.get("descendants", 0),
                              "url": story.get("url") or f"https://news.ycombinator.com/item?id={sid}",
                              "hn_url": f"https://news.ycombinator.com/item?id={sid}",
                              "tag": "ShowHN", "pillar": pillar, "pillar_keywords": keywords})
    except Exception as e:
        print(f"  ⚠️ Show HN fetch error: {e}")
    return items


# ========== Self-Evolution ==========

def generate_daily_digest(all_items, state):
    """生成每日 AI 雷达摘要，面向 PM 提炼关键信息（从 graph.json 读取完整当天数据）"""
    if not all_items:
        return
    
    from datetime import timezone, timedelta
    BJ_TZ = timezone(timedelta(hours=8))
    today = datetime.now(BJ_TZ).strftime("%Y-%m-%d")
    digest_dir = f"{WIKI_DIR}/daily-digest"
    os.makedirs(digest_dir, exist_ok=True)
    digest_path = f"{digest_dir}/{today}.md"
    
    # 从 graph.json 读取今天的所有节点（完整当天数据，不只是新增的）
    graph_path = f"{WIKI_DIR}/graph.json"
    today_nodes = []
    if os.path.exists(graph_path):
        try:
            with open(graph_path, encoding="utf-8") as f:
                graph_data = json.load(f)
            for node in graph_data.get("nodes", []):
                if node.get("date", "").startswith(today) and node.get("type") != "concept":
                    # 转换为 digest 格式
                    today_nodes.append({
                        "title": node.get("label", ""),
                        "name": node.get("label", ""),
                        "pillar": node.get("pillar", "unknown"),
                        "pm_score": node.get("pm_score", 0),
                        "url": node.get("url", ""),
                        "description": node.get("summary", ""),
                        "summary": node.get("summary", ""),
                        "type": node.get("type", ""),
                    })
        except Exception as e:
            print(f"  ⚠️ 读取 graph.json 失败: {e}")
    
    # 如果没有今天的节点，用传入的 items
    all_items_merged = today_nodes if today_nodes else all_items
    if not all_items_merged:
        return
    
    # 检查 digest 是否已存在且数据量一致（避免重复生成）
    if os.path.exists(digest_path):
        with open(digest_path) as f:
            existing = f.read()
        # 如果已有内容中包含今天的节点数，且一致则跳过
        import re
        m = re.search(r'\*\*新增情报\*\*: (\d+) 条', existing)
        if m and int(m.group(1)) == len(all_items_merged):
            print(f"  ℹ️ 今日 digest 已存在（{len(all_items_merged)} 条），跳过")
            return
    
    # 统计
    pillar_counts = Counter([i.get("pillar", "unknown") for i in all_items_merged])
    top_items = sorted(all_items_merged, key=lambda x: x.get("pm_score", 0), reverse=True)
    high_signal = [i for i in top_items if i.get("pm_score", 0) >= 0.35]
    
    # 按支柱分组
    by_pillar = {}
    for item in all_items_merged:
        p = item.get("pillar", "unknown")
        if p not in by_pillar: by_pillar[p] = []
        by_pillar[p].append(item)
    
    pillar_names = {"capabilities": "🤖 模型与技术能力", "patterns": "📱 产品与交互模式", "ecosystem": "🔧 工具与生态", "business": "💰 商业与趋势"}
    
    # 构建摘要内容
    content = f"""# 📅 AI 雷达日报 · {today}

> 面向 AI 产品经理的每日情报摘要

## 📊 今日概览
- **新增情报**: {len(all_items_merged)} 条
- **高价值信号**: {len(high_signal)} 条 (PM Score ≥ 0.35)
- **分布**: {', '.join([f"{pillar_names.get(p, p)} {c}条" for p, c in pillar_counts.items()])}

## 🔥 今日高价值信号 (PM 重点关注)
"""
    if not high_signal:
        content += "> 今日暂无高分情报，持续关注中。\n"
    else:
        for item in high_signal[:5]:
            # Use pre-computed pm_score (items from graph.json already have it)
            score = item.get("pm_score", 0)
            pillar = pillar_names.get(item.get("pillar", "unknown"), item.get("pillar", "未知"))
            title = item.get("title") or item.get("name") or "Unknown"
            desc = (item.get("description") or item.get("summary") or "")[:150]
            content += f"- **[{score:.2f}] {title}**\n  - {pillar} · [来源]({item.get('url') or item.get('hn_url')})\n  - {desc}\n"
    
    content += "\n## 📂 分支柱情报\n"
    for p, name in pillar_names.items():
        if p in by_pillar:
            content += f"\n### {name}\n"
            for item in by_pillar[p][:3]:
                title = item.get("title") or item.get("name") or "Unknown"
                content += f"- {title} ([链接]({item.get('url') or item.get('hn_url')}))\n"
    
    content += f"""
---
> 自动生成 | 详细图谱: https://ttmens.github.io/ai-radar-wiki/graph.html
> 数据源: GitHub, arXiv, Hacker News, TechCrunch AI, Product Hunt
"""
    
    with open(digest_path, "w") as f:
        f.write(content)
    
    # 更新 index 中的 digest 链接
    ai_index_path = f"{WIKI_DIR}/ai-index.json"
    if os.path.exists(ai_index_path):
        with open(ai_index_path) as f:
            ai_index = json.load(f)
        ai_index["latest_digest"] = digest_path
        ai_index["digest_date"] = today
        with open(ai_index_path, "w") as f:
            json.dump(ai_index, f, indent=2, ensure_ascii=False)
    
    print(f"  📝 Daily Digest generated: {digest_path} ({len(all_items)} items)")
    return digest_path


def run_self_evolution():
    """自动进化：淘汰低分旧内容 + 趋势检测 + 重复合并"""
    log_entries = []
    now = datetime.now()
    
    # 1. 内容淘汰：标记 90 天无更新且 pm_score < 0.15 的节点
    pruned_count = 0
    for subdir in ["wiki/entities", "wiki/concepts"]:
        path = f"{WIKI_DIR}/{subdir}"
        if not os.path.exists(path): continue
        for fname in os.listdir(path):
            if not fname.endswith(".md"): continue
            filepath = f"{path}/{fname}"
            try:
                with open(filepath) as f: content = f.read()
                m_updated = re.search(r'^updated:\s*(\d{4}-\d{2}-\d{2})$', content, re.MULTILINE)
                m_score = re.search(r'^pm_score:\s*([0-9.]+)$', content, re.MULTILINE)
                m_deprecated = re.search(r'^deprecated:\s*true$', content, re.MULTILINE)
                
                if m_deprecated: continue  # Already deprecated
                
                if m_updated and m_score:
                    updated = datetime.strptime(m_updated.group(1), "%Y-%m-%d")
                    score = float(m_score.group(1))
                    days_old = (now - updated).days
                    if days_old > 90 and score < 0.15:
                        # Mark as deprecated (don't delete, just flag)
                        new_content = content.replace("updated:", "deprecated: true\nupdated:")
                        with open(filepath, "w") as f: f.write(new_content)
                        pruned_count += 1
                        log_entries.append(f"  🗑️ Deprecated: {fname} ({days_old}d old, score={score})")
            except Exception as e:
                print(f"  ⚠️ Error in run_self_evolution (deprecation check): {e}")
    
    if pruned_count > 0:
        log_entries.append(f"  📊 {pruned_count} nodes deprecated (90d+ and score < 0.15)")
    
    # 2. 趋势检测：统计当前所有 pillar 分布，上报新标签
    pillar_counts = Counter()
    all_tags = Counter()
    for subdir in ["wiki/entities", "wiki/concepts"]:
        path = f"{WIKI_DIR}/{subdir}"
        if not os.path.exists(path): continue
        for fname in os.listdir(path):
            if not fname.endswith(".md"): continue
            try:
                with open(f"{path}/{fname}") as f: content = f.read()
                mp = re.search(r'^pillar:\s*(.+)$', content, re.MULTILINE)
                mt = re.search(r'^tags:\s*\[(.+)\]$', content, re.MULTILINE)
                if mp: pillar_counts[mp.group(1).strip()] += 1
                if mt:
                    tags = [t.strip().strip('"').strip("'") for t in mt.group(1).split(",")]
                    all_tags.update(tags)
            except Exception as e:
                print(f"  ⚠️ Error in run_self_evolution (trend detection): {e}")
    
    # 3. 更新 evolution log
    ts = now.strftime("%Y-%m-%d %H:%M")
    evo_path = f"{DOCS_DIR}/evolution.md"
    with open(evo_path) as f: evo_content = f.read()
    
    trending = all_tags.most_common(10)
    trending_section = "\n".join(f"- `{tag}`: {count} 次" for tag, count in trending[:5])
    
    new_entry = f"\n## [{ts}] Evolution Run\n- Deprecated: {pruned_count} nodes\n- Pillar distribution: {dict(pillar_counts)}\n- Top tags: {dict(trending[:5])}\n{''.join(log_entries) if log_entries else '- No actions needed'}\n"
    
    # Append before the last "##" section (keep header)
    if "## 运行日志" in evo_content:
        evo_content = evo_content.replace("## 运行日志", f"## 运行日志\n{new_entry}")
    else:
        evo_content += new_entry
    
    with open(evo_path, "w") as f: f.write(evo_content)
    
    if pruned_count > 0:
        print(f"  🧬 Evolution: {pruned_count} deprecated, pillars: {dict(pillar_counts)}")
    else:
        print(f"  🧬 Evolution: no pruning needed, pillars: {dict(pillar_counts)}")
    
    return {"pruned": pruned_count, "pillars": dict(pillar_counts)}


# ========== Wiki Generation ==========

def build_wiki_pages(items, state):
    updates = []
    timestamp = datetime.now().strftime("%Y-%m-%d")
    # 确保必要目录存在
    os.makedirs(f"{WIKI_DIR}/wiki/entities", exist_ok=True)
    os.makedirs(f"{WIKI_DIR}/wiki/concepts", exist_ok=True)
    os.makedirs(f"{WIKI_DIR}/daily-digest", exist_ok=True)
    os.makedirs(f"{WIKI_DIR}/summary_archive", exist_ok=True)
    for item in items:
        tag = item.get("tag", "Unknown")
        pm_score = calculate_pm_score(item)
        pillar = item.get("pillar", "unknown")
        if tag == "GitHub":
            name = item["name"]
            slug = slugify(name)
            filepath = f"{WIKI_DIR}/wiki/entities/{slug}.md"
            if os.path.exists(filepath):
                with open(filepath) as f: content = f.read()
                if item["url"] not in content:
                    update_section = f"\n\n## 更新 {timestamp}\n- ⭐ Stars: {item['stars']}\n- 🎯 PM Score: {pm_score}\n- 🏷️ Pillar: {pillar}"
                    parts = content.split("---\n", 2)
                    if len(parts) >= 3: content = parts[0] + "---\n" + parts[1] + "---\n" + parts[2].rstrip() + update_section
                    else: content += update_section
                    with open(filepath, "w") as f: f.write(content)
                    updates.append(("update", filepath))
            else:
                topics_str = ', '.join(item.get('topics', [])[:10]) or "无"
                content = f"""---
title: {name}
created: {timestamp}
updated: {timestamp}
type: entity
pillar: {pillar}
pm_score: {pm_score}
tags: ["project", "{(item.get('language') or '').lower() or 'other'}"]
sources: ["raw/github/{slug}.json"]
---

# {name}

## 概览
{item['description'] or '暂无描述'}

## 中文摘要
{item.get('summary_cn', '') or '暂无中文摘要'}

## PM 关注指标
- ⭐ Stars: {item['stars']}
- 🎯 PM Score: {pm_score}
- 🏷️ Pillar: {pillar}
- 🔑 Keywords: {', '.join(item.get('pillar_keywords', [])[:5])}

## 基本信息
- 🌐 语言: {item['language'] or '未指定'}
- 🔗 链接: {item['url']}
- 🏷️ Topics: {topics_str}

## 数据
> 原始数据: [{slug}.json](../raw/github/{slug}.json)

## 关系
- 相关概念: TBD
"""
                with open(filepath, "w") as f: f.write(content)
                save_raw(f"{RAW_GITHUB}/{slug}.json", item)
                updates.append(("create", filepath))
        elif tag == "Paper":
            title = item["title"]
            slug = slugify(title)
            filepath = f"{WIKI_DIR}/wiki/concepts/{slug}.md"
            if not os.path.exists(filepath):
                authors_str = ", ".join(item.get("authors", []))
                summary_short = item['summary'][:300] + ("..." if len(item['summary']) > 300 else "")
                content = f"""---
title: {title[:80]}
created: {timestamp}
updated: {timestamp}
type: concept
pillar: {pillar}
pm_score: {pm_score}
tags: ["research", "{pillar}"]
sources: ["raw/papers/{slug}.json"]
---

# {title}

## 中文摘要
{item.get('summary_cn', '') or '暂无中文摘要'}

## PM 关注指标
- 🎯 PM Score: {pm_score}
- 🏷️ Pillar: {pillar}
- 🔑 Keywords: {', '.join(item.get('pillar_keywords', [])[:5])}

## 作者
{authors_str or '未知'}

## 摘要
{summary_short}

## 中文摘要
{item.get('summary_cn', '') or '暂无中文摘要'}

## 链接
- 📄 arXiv: {item['url']}

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
"""
                with open(filepath, "w") as f: f.write(content)
                save_raw(f"{RAW_PAPERS}/{slug}.json", item)
                updates.append(("create", filepath))
        elif tag == "HN":
            title = item["title"]
            slug = slugify(title)
            filepath = f"{WIKI_DIR}/wiki/entities/{slug}.md"
            if not os.path.exists(filepath):
                content = f"""---
title: {title[:80]}
created: {timestamp}
updated: {timestamp}
type: entity
pillar: {pillar}
pm_score: {pm_score}
tags: ["discussion", "hacker-news", "{pillar}"]
sources: ["raw/hn/{slug}.json"]
---

# {title}

## 中文摘要
{item.get('summary_cn', '') or '暂无中文摘要'}

## PM 关注指标
- 🔥 HN Score: {item['score']}
- 💬 Comments: {item['comments']}
- 🎯 PM Score: {pm_score}
- 🏷️ Pillar: {pillar}

## 链接
- 🔗 HN 讨论: {item['hn_url']}
- 🔗 原文: {item['url']}
"""
                with open(filepath, "w") as f: f.write(content)
                save_raw(f"{RAW_HN}/{slug}.json", item)
                updates.append(("create", filepath))
        elif tag == "Product":
            title = item["title"]
            slug = slugify(title)
            filepath = f"{WIKI_DIR}/wiki/entities/{slug}.md"
            if not os.path.exists(filepath):
                desc_short = (item.get('description', '') or '')[:300]
                content = f"""---
title: {title[:80]}
created: {timestamp}
updated: {timestamp}
type: entity
pillar: {pillar}
pm_score: {pm_score}
tags: ["product", "product-hunt", "{pillar}"]
sources: ["raw/products/{slug}.json"]
---

# {title}

## 中文摘要
{item.get('summary_cn', '') or '暂无中文摘要'}

## PM 关注指标
- 🎯 PM Score: {pm_score}
- 🏷️ Pillar: {pillar}

## 产品描述
{desc_short or '暂无描述'}

## 链接
- 🔗 Product Hunt: {item['url']}
"""
                with open(filepath, "w") as f: f.write(content)
                save_raw(f"{RAW_PRODUCTS}/{slug}.json", item)
                updates.append(("create", filepath))
        elif tag == "TechCrunch":
            title = item["title"]
            slug = slugify(title)
            filepath = f"{WIKI_DIR}/wiki/entities/{slug}.md"
            if not os.path.exists(filepath):
                desc_short = (item.get('description', '') or '')[:300]
                pub_date = item.get('pub_date', '')
                content = f"""---
title: {title[:80]}
created: {timestamp}
updated: {timestamp}
type: entity
pillar: {pillar}
pm_score: {pm_score}
tags: ["news", "techcrunch", "{pillar}"]
sources: ["raw/techcrunch/{slug}.json"]
---

# {title}

## 中文摘要
{item.get('summary_cn', '') or '暂无中文摘要'}

## PM 关注指标
- 🎯 PM Score: {pm_score}
- 🏷️ Pillar: {pillar}
- 🔑 Keywords: {', '.join(item.get('pillar_keywords', [])[:5])}

## 新闻摘要
{desc_short or '暂无摘要'}

## 链接
- 🔗 Source: {item['url']}
- 📅 Published: {pub_date}
"""
                with open(filepath, "w") as f: f.write(content)
                os.makedirs(f"{WIKI_DIR}/raw/techcrunch", exist_ok=True)
                save_raw(f"{WIKI_DIR}/raw/techcrunch/{slug}.json", item)
                updates.append(("create", filepath))
        elif tag == "ShowHN":
            title = item["title"]
            slug = slugify(title)
            filepath = f"{WIKI_DIR}/wiki/entities/{slug}.md"
            if not os.path.exists(filepath):
                content = f"""---
title: {title[:80]}
created: {timestamp}
updated: {timestamp}
type: entity
pillar: {pillar}
pm_score: {pm_score}
tags: ["show-hn", "product", "{pillar}"]
sources: ["raw/showhn/{slug}.json"]
---

# {title}

## 中文摘要
{item.get('summary_cn', '') or '暂无中文摘要'}

## PM 关注指标
- 🔥 HN Score: {item['score']}
- 💬 Comments: {item['comments']}
- 🎯 PM Score: {pm_score}
- 🏷️ Pillar: {pillar}

## 链接
- 🔗 HN: {item['hn_url']}
- 🔗 原文: {item['url']}
"""
                with open(filepath, "w") as f: f.write(content)
                os.makedirs(f"{WIKI_DIR}/raw/showhn", exist_ok=True)
                save_raw(f"{WIKI_DIR}/raw/showhn/{slug}.json", item)
                updates.append(("create", filepath))
    return updates



def _resolve_paper_url(node_id, label=""):
    """Resolve paper URL from raw data or arxiv ID extraction."""
    import glob
    # 1. Try to find in raw/papers data
    for fpath in glob.glob(f"{WIKI_DIR}/raw/papers/*.json"):
        try:
            with open(fpath) as f:
                raw = json.load(f)
            if raw.get("title") and slugify(raw["title"]) == node_id:
                return raw.get("url", "")
        except:
            pass
    # 2. Try to extract arxiv ID from label/title
    arxiv_match = re.search(r'(\d{4}\.\d{4,7}(?:v\d+)?)', label)
    if arxiv_match:
        return f"https://arxiv.org/abs/{arxiv_match.group(1)}"
    # 3. Fallback: use node_id if it looks like an arxiv ID
    if re.match(r'\d{4}\.\d', node_id):
        return f"https://arxiv.org/abs/{node_id.split('.')[0]}.{node_id.split('.')[1][:4]}" if '.' in node_id else ""
    return ""

def build_graph_json(items):
    """Build graph.json — merge new items with existing data to avoid data loss"""
    # Load existing graph to preserve historical nodes
    existing_nodes = []
    existing_edges = []
    existing_ids = set()
    if os.path.exists(f"{WIKI_DIR}/graph.json"):
        try:
            with open(f"{WIKI_DIR}/graph.json", encoding="utf-8") as f:
                existing_data = json.load(f)
            existing_nodes = existing_data.get("nodes", [])
            existing_edges = existing_data.get("edges", [])
            existing_ids = {n["id"] for n in existing_nodes}
        except Exception as e:
            print(f"  ⚠️ Failed to load existing graph: {e}")

    nodes = []
    edges = []
    node_ids = set()
    # Scan wiki entity locations
    for subdir in ["wiki/entities", "wiki/concepts"]:
        path = f"{WIKI_DIR}/{subdir}"
        if not os.path.exists(path): continue
        for fname in os.listdir(path):
            if not fname.endswith(".md"): continue
            filepath = f"{path}/{fname}"
            try:
                with open(filepath) as f: content = f.read()
                m_title = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
                m_type = re.search(r'^type:\s*(.+)$', content, re.MULTILINE)
                m_pillar = re.search(r'^pillar:\s*(.+)$', content, re.MULTILINE)
                m_score = re.search(r'^pm_score:\s*([0-9.]+)$', content, re.MULTILINE)
                m_sources = re.search(r'^sources:\s*\["raw/(\w+)/', content, re.MULTILINE)
                m_created = re.search(r'^created:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
                m_updated = re.search(r'^updated:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
                m_url = re.search(r'^- 🔗 (链接|Source|HN 讨论|原文):\s*(.+)$', content, re.MULTILINE)

                node_id = fname.replace(".md", "")
                label = m_title.group(1).strip() if m_title else node_id
                node_type = m_type.group(1).strip() if m_type else "concept"
                pillar = m_pillar.group(1).strip() if m_pillar else "capabilities"
                pm_score = float(m_score.group(1)) if m_score else 0.1
                source_type = m_sources.group(1) if m_sources else "unknown"
                node_date = m_updated.group(1) if m_updated else (m_created.group(1) if m_created else "")
                node_url = m_url.group(2).strip() if m_url else ""

                # Skip low-value concept nodes (source tags, not real concepts)
                low_value_labels = {"papers", "techcrunch", "hn", "showhn", "github", "concept", "unknown", "product hunt"}
                if node_type == "concept" and label.lower() in low_value_labels:
                    continue

                # Skip if already seen (from another directory)
                if node_id in node_ids:
                    continue
                node_ids.add(node_id)

                # Extract summary from various sections (优先中文摘要)
                summary = ""
                # First try Chinese summary
                m_zh = re.search(r'## 中文摘要\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
                if m_zh:
                    summary = m_zh.group(1).strip()[:300]
                    if not summary or '暂无' in summary:
                        summary = ""
                # Fallback to other sections
                if not summary:
                    for section in ["## 概览", "## 新闻摘要", "## 产品描述", "## 摘要", "## 讨论热度", "## PM 视角解读"]:
                        m = re.search(re.escape(section) + r'\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
                        if m:
                            summary = m.group(1).strip()[:300]
                            summary = re.sub(r'^[-*>\s]+', '', summary).strip()
                            break

                if not summary:
                    parts = content.split("---\n", 2)
                    if len(parts) >= 3:
                        body = parts[2].strip()
                        lines = body.split("\n")
                        for line in lines:
                            line = line.strip()
                            if line and not line.startswith("#") and not line.startswith(">") and not line.startswith("-"):
                                summary = line[:300]
                                break

                # Extract raw content (original wiki body, minus frontmatter and metadata sections)
                raw_content = ""
                parts = content.split("---\n", 2)
                if len(parts) >= 3:
                    body = parts[2].strip()
                    # Remove metadata sections, keep only the core content
                    lines = body.split("\n")
                    content_lines = []
                    skip_sections = ["## PM 关注指标", "## 基本信息", "## 更新 "]
                    in_skip = False
                    for line in lines:
                        for skip in skip_sections:
                            if line.startswith(skip):
                                in_skip = True
                                break
                        if line.startswith("## ") and not any(line.startswith(s) for s in skip_sections):
                            in_skip = False
                        if not in_skip and not line.startswith("## 中文摘要"):
                            content_lines.append(line)
                    raw_content = "\n".join(content_lines).strip()[:500]

                if pillar == "unknown":
                    p, kws = classify_pillar(label + " " + summary)
                    pillar = p  # classify_pillar now defaults to 'capabilities', never 'unknown'

                # Ensure date/url never empty
                if not node_date:
                    node_date = m_created.group(1) if m_created else datetime.now().strftime("%Y-%m-%d")

                nodes.append({
                    "id": node_id, "label": label[:80], "type": {"entity": source_type, "concept": source_type}.get(node_type, node_type),
                    "pillar": pillar, "pm_score": pm_score, "tags": [source_type, pillar],
                    "summary": summary, "raw_content": raw_content, "source_type": source_type,
                    "date": node_date, "url": node_url
                })
            except Exception as e:
                print(f"  ⚠️ Error in build_graph_json: {e}")

    # Scan wiki/ root for concept nodes (papers from old concepts/)
    wiki_root_path = f"{WIKI_DIR}/wiki"
    if os.path.exists(wiki_root_path):
        for fname in os.listdir(wiki_root_path):
            if not fname.endswith(".md"): continue
            filepath = f"{wiki_root_path}/{fname}"
            try:
                with open(filepath) as f: content = f.read()
                m_title = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
                if not m_title: continue
                m_pillar = re.search(r'^pillar:\s*(.+)$', content, re.MULTILINE)
                m_score = re.search(r'^pm_score:\s*([0-9.]+)$', content, re.MULTILINE)
                m_created = re.search(r'^created:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
                m_updated = re.search(r'^updated:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)

                node_id = fname.replace(".md", "")
                if node_id in node_ids: continue
                node_ids.add(node_id)

                label = m_title.group(1).strip()
                pillar = m_pillar.group(1).strip() if m_pillar else "capabilities"
                if pillar == "unknown":
                    p, _ = classify_pillar(label)
                    pillar = p
                pm_score = float(m_score.group(1)) if m_score else 0.1
                node_date = m_updated.group(1) if m_updated else (m_created.group(1) if m_created else "")

                # Extract summary (优先中文摘要)
                summary = ""
                m_zh = re.search(r'## 中文摘要\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
                if m_zh:
                    summary = m_zh.group(1).strip()[:300]
                    if not summary or '暂无' in summary:
                        summary = ""
                if not summary:
                    for section in ["## 概览", "## 新闻摘要", "## 产品描述", "## 摘要", "## 讨论热度", "## PM 视角解读"]:
                        m = re.search(re.escape(section) + r'\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
                        if m:
                            summary = m.group(1).strip()[:300]
                            summary = re.sub(r'^[-*>\s]+', '', summary).strip()
                            break

                if not summary:
                    parts = content.split("---\n", 2)
                    if len(parts) >= 3:
                        body = parts[2].strip()
                        for line in body.split("\n"):
                            line = line.strip()
                            if line and not line.startswith("#") and not line.startswith(">") and not line.startswith("-"):
                                summary = line[:300]
                                break

                nodes.append({
                    "id": node_id, "label": label[:80], "type": "paper",
                    "pillar": pillar, "pm_score": pm_score, "tags": ["papers", pillar],
                    "summary": summary, "raw_content": "", "source_type": "papers",
                    "date": node_date or datetime.now().strftime("%Y-%m-%d"), "url": _resolve_paper_url(node_id, label)
                })
            except Exception as e:
                print(f"  ⚠️ Error scanning wiki root: {e}")

    # Add new items from current fetch — with title-based dedup
    # v3.8.2: 防止同一文章因不同来源产生重复节点
    seen_titles = {}  # normalized_title -> best_item
    for item in items:
        title = item.get("title", "") or item.get("name", "") or ""
        norm_title = re.sub(r'[^a-z0-9\u4e00-\u9fff]', '', title.lower())
        if norm_title in seen_titles:
            # Keep the one with higher score/better data
            existing = seen_titles[norm_title]
            existing_score = existing.get("score", 0) or existing.get("stars", 0)
            new_score = item.get("score", 0) or item.get("stars", 0)
            if new_score > existing_score:
                seen_titles[norm_title] = item
            continue
        seen_titles[norm_title] = item
    
    deduped_items = list(seen_titles.values())
    
    for item in deduped_items:
        tag = item.get("tag", "Unknown")
        pm_score = calculate_pm_score(item)
        pillar = item.get("pillar", "unknown")
        # Extract date
        node_date = item.get("created") or item.get("published") or item.get("pub_date") or ""
        if node_date:
            # Normalize to YYYY-MM-DD
            if "T" in node_date:
                node_date = node_date.split("T")[0].split("+")[0]
            elif "," in node_date:
                # RFC2822: "Sun, 10 May 2026 02:00:00 "
                from email.utils import parsedate_to_datetime
                try:
                    node_date = parsedate_to_datetime(node_date).strftime("%Y-%m-%d")
                except Exception:
                    node_date = datetime.now().strftime("%Y-%m-%d")
            # Fallback: if still not YYYY-MM-DD, use today
            if len(node_date) != 10 or node_date[4] != "-" or node_date[7] != "-":
                node_date = datetime.now().strftime("%Y-%m-%d")
        
        if tag == "GitHub": node_id, summary = slugify(item["name"]), item.get("summary_cn", "") or item.get("description", "") or "AI 开源项目"
        elif tag == "Paper": node_id, summary = slugify(item["title"]), item.get("summary_cn", "") or (item.get("summary", "") or "")[:300]
        elif tag == "HN": node_id, summary = slugify(item["title"]), item.get("summary_cn", "") or f"HN 热门讨论，{item.get('score', 0)} 分，{item.get('comments', 0)} 条评论"
        elif tag == "Product": node_id, summary = slugify(item["title"]), item.get("summary_cn", "") or (item.get("description", "") or "新 AI 产品")[:300]
        elif tag == "TechCrunch": node_id, summary = slugify(item["title"]), item.get("summary_cn", "") or (item.get("description", "") or "商业动态")[:300]
        elif tag == "ShowHN": node_id, summary = slugify(item["title"]), item.get("summary_cn", "") or f"Show HN 项目，{item.get('score', 0)} 分"
        else: continue

        node_label = item.get("name", "") or item.get("title", "")
        node_url = item.get("url") or item.get("hn_url", "")

        # Fix: arXiv papers should have arxiv.org URL
        if tag == "Paper" and not node_url and item.get("title"):
            # 尝试从 raw 数据或 title 中匹配 arxiv ID
            node_url = _resolve_paper_url(slugify(item["title"]), item["title"])

        if node_id not in node_ids:
            node_ids.add(node_id)
            # Ensure date is never empty — fallback to today
            if not node_date:
                node_date = datetime.now().strftime("%Y-%m-%d")
            nodes.append({
                "id": node_id, "label": node_label[:80], "type": {"GitHub": "project", "Paper": "paper", "HN": "discussion", "Product": "product", "TechCrunch": "news", "ShowHN": "project"}.get(tag, "concept"),
                "pillar": pillar, "pm_score": pm_score, "tags": [tag.lower(), pillar],
                "summary": summary, "raw_content": summary[:500], "date": node_date, "url": node_url,
                "stars": item.get("stars"), "score": item.get("score"), "comments": item.get("comments"),
                # 新增：保存 concepts/entities/patterns 用于后续构建概念节点
                "_concepts": item.get("concepts", []),
                "_entities": item.get("entities", []),
                "_patterns": item.get("patterns", [])
            })

    # ===== 新增：构建概念节点体系 (L2 Information Layer) =====
    # 从所有 items 中提取 concepts，构建概念节点和 BELONGS_TO 边
    concept_map = {}  # concept_label -> {nodes: [], pillar_counts: {}, max_pm: 0}
    for item in items:
        # 获取 concepts（LLM 提取）或降级到关键词提取
        concepts = item.get("concepts", [])
        if not concepts:
            # 降级：从 title/summary 中提取关键词
            text = (item.get("title", "") or item.get("name", "")) + " " + (item.get("summary_cn", "") or item.get("summary", "") or "")
            # 简单的关键词提取（匹配常见 AI 概念模式）
            keyword_patterns = ["AI Agent", "LLM", "RAG", "Memory", "Multi-Agent", "Fine-tuning", "Prompt", "Embedding", "Vector", "Transformer", "Diffusion", "Computer Vision", "NLP", "Reinforcement Learning", "Knowledge Graph"]
            for kw in keyword_patterns:
                if kw.lower() in text.lower():
                    concepts.append(kw)
            # 去重
            concepts = list(set(concepts))[:3]

        for concept in concepts:
            if not concept or len(concept) < 2: continue
            concept_key = slugify(concept)
            if concept_key not in concept_map:
                concept_map[concept_key] = {"label": concept, "nodes": [], "pillar_counts": Counter(), "max_pm": 0.0, "first_seen": datetime.now().strftime("%Y-%m-%d")}
            # 找到对应的 node_id
            tag = item.get("tag", "")
            if tag == "GitHub": nid = slugify(item["name"])
            elif tag in ("Paper", "HN", "Product", "TechCrunch", "ShowHN"): nid = slugify(item.get("title", ""))
            else: continue
            concept_map[concept_key]["nodes"].append(nid)
            concept_map[concept_key]["pillar_counts"][item.get("pillar", "unknown")] += 1
            pm = calculate_pm_score(item)
            if pm > concept_map[concept_key]["max_pm"]:
                concept_map[concept_key]["max_pm"] = pm

    # 只保留关联了 >=2 个节点的概念（避免概念爆炸）
    for concept_key, data in concept_map.items():
        if len(data["nodes"]) < 2: continue
        if concept_key in node_ids: continue  # 已存在则跳过

        # 确定概念的主 pillar（取关联节点最多的 pillar）
        main_pillar = data["pillar_counts"].most_common(1)[0][0] if data["pillar_counts"] else "unknown"
        if main_pillar == "unknown": main_pillar = "capabilities"

        # 生成概念摘要
        related_labels = []
        for nid in data["nodes"][:5]:
            for n in nodes:
                if n["id"] == nid:
                    related_labels.append(n["label"][:30])
                    break
        concept_summary = f"关联项目: {', '.join(related_labels)}" if related_labels else f"概念: {data['label']}"

        node_ids.add(concept_key)
        nodes.append({
            "id": concept_key,
            "label": data["label"][:80],
            "type": "concept",
            "pillar": main_pillar,
            "pm_score": round(data["max_pm"], 2),
            "tags": ["concept", main_pillar],
            "summary": concept_summary,
            "raw_content": "",
            "date": data["first_seen"],
            "url": "",
            # 概念节点特有字段
            "related_nodes": data["nodes"],
            "node_count": len(data["nodes"]),
        })

        # 创建 BELONGS_TO 边（项目 → 概念）
        for nid in data["nodes"]:
            edges.append({
                "id": f"edge_{nid}_{concept_key}",
                "from": nid,
                "to": concept_key,
                "type": "BELONGS_TO",
                "relation": "belongs_to"
            })

    # Build edges...
    valid_pillars = {"capabilities", "patterns", "ecosystem", "business"}
    for node in nodes:
        for tag in node.get("tags", []):
            tag_key = slugify(tag)
            # Only create concept nodes for valid pillar tags, not source tags
            if tag in valid_pillars:
                if tag_key not in node_ids:
                    node_ids.add(tag_key)
                    nodes.append({"id": tag_key, "label": tag, "type": "concept", "pillar": tag, "pm_score": 0.1, "tags": ["concept"], "summary": f"概念标签: {tag}", "date": datetime.now().strftime("%Y-%m-%d"), "url": "", "raw_content": ""})
                edges.append({"source": node["id"], "target": tag_key, "relation": "belongs_to", "type": "KEYWORD", "pm_relevance": node["pm_score"] * 0.5})
            # Skip edges to source tags (papers, techcrunch, hn, etc.) to reduce noise
            # Only add edges for pillar tags
    pillar_groups = {}
    for node in nodes:
        p = node.get("pillar", "unknown")
        if p not in pillar_groups: pillar_groups[p] = []
        pillar_groups[p].append(node["id"])
    for pillar, group in pillar_groups.items():
        if pillar == "unknown": continue
        for i in range(min(3, len(group) - 1)):
            edges.append({"source": group[i], "target": group[i + 1], "relation": f"same_pillar:{pillar}", "type": "PILLAR", "pm_relevance": 0.3})
    nodes.sort(key=lambda n: n.get("pm_score", 0), reverse=True)

    # Merge with existing data: add old nodes/edges not already included
    all_nodes = list(nodes)  # start with new nodes
    all_edges = list(edges)   # start with new edges
    new_node_ids = {n["id"] for n in nodes}

    # Title-based dedup: build a map of label -> best_node for new nodes
    new_by_title = {}
    for n in nodes:
        title = n.get("label", "")
        if title and (title not in new_by_title or n.get("pm_score", 0) > new_by_title[title].get("pm_score", 0)):
            new_by_title[title] = n

    for en in existing_nodes:
        # Skip if same ID
        if en["id"] in new_node_ids:
            continue
        # Skip if same title (already covered by new node with full ID)
        en_title = en.get("label", "")
        if en_title and en_title in new_by_title:
            continue
        all_nodes.append(en)

    for ee in existing_edges:
        all_edges.append(ee)

    # Sort final: high score first
    all_nodes.sort(key=lambda n: n.get("pm_score", 0), reverse=True)

    graph_data = {"nodes": all_nodes, "edges": all_edges, "generated_at": datetime.now().isoformat(), "generator": "ai-radar-explorer-v3", "schema_version": "4-pillar-pm-focused"}
    with open(f"{WIKI_DIR}/graph.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    return graph_data


def _strip_illegal_controls(obj):
    """递归清理会破坏 HTML 内联 JSON 解析的 ASCII 控制字符（保留 \\t \\n \\r）。
    与 tools/inject_graph_data.py 逐行等价，确保定时任务注入安全。
    """
    if isinstance(obj, str):
        return ''.join(' ' if (ord(ch) < 32 and ch not in '\t\n\r') or ord(ch) == 0x7F else ch for ch in obj)
    if isinstance(obj, list):
        return [_strip_illegal_controls(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _strip_illegal_controls(v) for k, v in obj.items()}
    return obj


def generate_graph_html(graph_data):
    # Copy vis-network to wiki dir if not present
    if not os.path.exists(VIS_JS) and os.path.exists("/tmp/vis-network.min.js"):
        os.makedirs(f"{WIKI_DIR}/assets", exist_ok=True)
        shutil.copy("/tmp/vis-network.min.js", VIS_JS)
        print("  📦 Copied vis-network.min.js to wiki dir (assets/)")

    template_path = f"{WIKI_DIR}/graph_template.html"
    graph_html_path = f"{WIKI_DIR}/graph.html"

    # DESIGN §9.3 + §6.4: 控制字符清理 + 紧凑单行格式
    clean_data = _strip_illegal_controls(graph_data)
    data_json = json.dumps(clean_data, ensure_ascii=False, separators=(',', ':'))
    
    # v3.13.0 FIX: Always regenerate from template to ensure UI/CSS updates are applied.
    # Regex replacement on graph.html risks locking in stale CSS/JS and ignoring template updates.
    
    if not os.path.exists(template_path):
        print(f"  ⚠️ graph_template.html not found at {template_path}")
        return
    
    with open(template_path, encoding="utf-8") as f:
        html_template = f.read()
    
    if "{{DATA}}" not in html_template:
        print(f"  ⚠️ graph_template.html missing {{DATA}} placeholder")
        return
    
    html = html_template.replace("{{DATA}}", data_json)
    with open(graph_html_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"  ✅ graph.html generated from template: {len(graph_data['nodes'])} nodes, {len(graph_data['edges'])} edges")
    return graph_html_path


def update_index():
    entities = []
    concepts = []
    for subdir, lst in [("wiki/entities", entities), ("wiki/concepts", concepts)]:
        path = f"{WIKI_DIR}/{subdir}"
        if not os.path.exists(path): continue
        for fname in sorted(os.listdir(path)):
            if not fname.endswith(".md"): continue
            filepath = f"{path}/{fname}"
            with open(filepath) as f: content = f.read()
            m = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
            title = m.group(1).strip() if m else fname.replace(".md", "").replace("-", " ").title()
            mp = re.search(r'^pillar:\s*(.+)$', content, re.MULTILINE)
            pillar = mp.group(1).strip() if mp else "unknown"
            ms = re.search(r'^pm_score:\s*([0-9.]+)$', content, re.MULTILINE)
            score = float(ms.group(1)) if ms else 0
            lst.append(f"- [[{fname}]] {title} `pillar:{pillar}` `score:{score}`")
    
    all_pages = entities + concepts
    def by_pillar(name):
        items = [l for l in all_pages if f'pillar:{name}' in l.lower()]
        return chr(10).join(items) if items else '> 暂无内容'
    unknown = [l for l in all_pages if 'pillar:unknown' in l.lower()]
    
    index = f"""# AI Radar Wiki — Index
> 面向 AI 产品经理的 4 大支柱知识库
> Last updated: {datetime.now().strftime("%Y-%m-%d")} | Total pages: {len(all_pages)}

## 🤖 Capabilities (模型与技术能力)
> Context, Latency, Cost, Multimodal, Reasoning
{by_pillar('capabilities')}

## 📱 Patterns (产品与交互模式)
> Chat, Copilot, Agent Workflow, Background Automation
{by_pillar('patterns')}

## 🔧 Ecosystem (工具与生态)
> Orchestration, VectorDB, Evaluation, Open Source
{by_pillar('ecosystem')}

## 💰 Business (商业与趋势)
> Funding, Moat, Growth, Ethics, Regulation
{by_pillar('business')}

## 📚 Concepts (未分类)
{chr(10).join(unknown) if unknown else '> 暂无内容'}
"""
    with open(f"{WIKI_DIR}/index.md", "w") as f: f.write(index)


def update_readme(graph_data):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    nodes = graph_data.get('nodes', [])
    edges = graph_data.get('edges', [])
    node_count = len(nodes)
    edge_count = len(edges)
    cn_count = sum(1 for n in nodes if any('\u4e00' <= c <= '\u9fff' for c in n.get('summary', '')))
    
    # Count by pillar
    pillars = {}
    for n in nodes:
        p = n.get('pillar', 'unknown')
        pillars[p] = pillars.get(p, 0) + 1
    
    # Count by type
    types = {}
    for n in nodes:
        t = n.get('type', 'unknown')
        types[t] = types.get(t, 0) + 1
    
    readme = f"""# 🧠 AI Radar — AI 产品设计雷达

> 自动化 AI 技术情报系统，面向 AI 产品经理的 4 支柱知识图谱

[![Graph](https://img.shields.io/badge/📊_Knowledge_Graph-Live-blue)](https://ttmens.github.io/ai-radar-wiki/graph.html)
[![Update](https://img.shields.io/badge/🔄_Every_6h-green)]()
[![RSS](https://img.shields.io/badge/📡_RSS_Feed-orange)](https://ttmens.github.io/ai-radar-wiki/feed.xml)
[![Chinese](https://img.shields.io/badge/🇨🇳_{cn_count}_中文摘要-red)]()

---

## 📊 实时统计

| 指标 | 数值 |
|------|------|
| 总节点 | {node_count} |
| 总边 | {edge_count} |
| 中文摘要 | {cn_count} ({cn_count*100//max(node_count,1)}%) |
| 最后更新 | {ts} |

### 四支柱分布

| 支柱 | 节点数 | 说明 |
|------|--------|------|
| 🤖 技术能力 | {pillars.get('capabilities', 0)} | 新模型、算法、技术突破 |
| 📱 产品模式 | {pillars.get('patterns', 0)} | 交互方式、工作流、AI 应用 |
| 🔧 工具生态 | {pillars.get('ecosystem', 0)} | 框架、SDK、库、平台 |
| 💰 商业动态 | {pillars.get('business', 0)} | 融资、产品发布、市场 |

---

## 🚀 快速访问

| 资源 | 链接 |
|------|------|
| 📊 交互式知识图谱 | [Open Graph](https://ttmens.github.io/ai-radar-wiki/graph.html) |
| 📋 图谱数据 | [graph.json](https://ttmens.github.io/ai-radar-wiki/graph.json) |
| 📚 Wiki 索引 | [index.md](https://ttmens.github.io/ai-radar-wiki/index.md) |
| 📡 RSS 订阅 | [feed.xml](https://ttmens.github.io/ai-radar-wiki/feed.xml) |
| 📅 今日日报 | [daily_summary.json](https://ttmens.github.io/ai-radar-wiki/daily_summary.json) |
| 📖 设计文档 | [DESIGN.md](https://ttmens.github.io/ai-radar-wiki/DESIGN.md) |

---

*AI Radar Explorer v3 · Self-evolving Knowledge Graph · Last updated: {ts}*
"""
    with open(f"{WIKI_DIR}/README.md", "w") as f: f.write(readme)


def git_push():
    import subprocess
    try:
        os.chdir(WIKI_DIR)
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
        result = subprocess.run(["git", "diff", "--cached", "--stat"], capture_output=True, text=True)
        if not result.stdout.strip():
            print("  ℹ️  无变更，跳过推送")
            return False
        subprocess.run(["git", "commit", "-m", f"🔍 auto-sync v3 {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
        print(f"  ✅ 已推送到 GitHub")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Git error: {e.stderr.decode() if e.stderr else str(e)}")
        return False


def main():
    print(f"🔍 AI Radar Explorer v3 — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    state = load_state()
    sources = [
        ("GitHub", fetch_github, "url"),
        ("arXiv", fetch_arxiv, "url"),
        ("Hacker News", fetch_hackernews, "hn_url"),
        ("Product Hunt", fetch_product_hunt, "url"),
        ("TechCrunch AI", fetch_techcrunch, "url"),
        ("Show HN", fetch_hn_show, "hn_url"),
    ]
    all_items = []
    total_stats = {"found": 0, "new": 0}
    pillar_stats = Counter()
    for name, func, url_key in sources:
        items = func()
        total_stats["found"] += len(items)
        # v3.8.2: 过滤噪音内容
        clean_items = [i for i in items if not is_noise(i.get("title", "") or i.get("name", "") or i.get("description", "") or "")]
        filtered = len(items) - len(clean_items)
        if filtered > 0:
            print(f"  🔇 {name}: 过滤 {filtered} 条噪音")
        new_items = [i for i in clean_items if is_new(i.get(url_key, ""), state)]
        new_count = len(new_items)
        total_stats["new"] += new_count
        all_items.extend(new_items)
        for item in new_items: pillar_stats[item.get("pillar", "unknown")] += 1
        if name not in state["stats"]["by_source"]: state["stats"]["by_source"][name] = 0
        state["stats"]["by_source"][name] += new_count
        print(f"  {name}: {len(items)} found, {len(clean_items)} clean, {new_count} new")
    print(f"  📊 Pillar distribution: {dict(pillar_stats)}")

    # Step 2: LLM Analysis (translate, classify, PM score)
    if all_items:
        batch_analyze_items(all_items, state)
    
    updates = build_wiki_pages(all_items, state) if all_items else []
    if all_items: print(f"  📝 Wiki: {len(updates)} updates")
    
    graph_data = build_graph_json(all_items)
    print(f"  🕸️ Graph: {len(graph_data['nodes'])} nodes, {len(graph_data['edges'])} edges")
    
    # Generate structured daily summary AFTER graph.json is rebuilt
    # (must read from graph.json to get today's dated nodes)
    print("  📰 生成结构化每日摘要...")
    import subprocess
    try:
        subprocess.run(["python3", os.path.expanduser("~/.hermes/scripts/generate_daily_summary.py")],
                      timeout=180, capture_output=True, text=True)
        print("  ✅ 结构化摘要已生成")
    except Exception as e:
        print(f"  ⚠️ 摘要生成失败: {e}")
    
    generate_graph_html(graph_data)
    update_index()
    update_readme(graph_data)
    
    # Self-evolution
    run_self_evolution()
    
    # Generate daily digest for PMs
    generate_daily_digest(all_items, state)
    
    if all_items:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n## [{ts}] sync v3 | {len(all_items)} new | pillars: {dict(pillar_stats)}\n"
        for action, path in updates: entry += f"- {action}: {os.path.basename(path)}\n"
        with open(f"{DOCS_DIR}/log.md", "a") as f: f.write(entry)
    
    state["last_run"] = datetime.now().isoformat()
    state["stats"]["total_items"] += total_stats["new"]
    save_state(state)
    
    # Clean up old raw files (TTL)
    clean_old_raw(ttl_days=30)
    
    # Generate weekly trends from summary archive
    try:
        subprocess.run(["python3", os.path.expanduser("~/.hermes/scripts/weekly_trends.py")],
                      timeout=60, capture_output=True, text=True)
        print("  📊 Weekly trends updated")
    except Exception as e:
        print(f"  ⚠️ Weekly trends failed: {e}")

    import subprocess as _sub
    try:
        _snap = os.path.join(WIKI_DIR, "scripts", "generate_brief_snapshot.py")
        if os.path.isfile(_snap):
            _r = _sub.run(
                ["python3", _snap, "--wiki-root", WIKI_DIR],
                timeout=60, capture_output=True, text=True)
            if _r.returncode == 0:
                print("  📸 brief_snapshot.json 已更新")
            else:
                print(f"  ⚠️ brief_snapshot 异常: {_r.stderr or _r.stdout or _r.returncode}")
    except Exception as e:
        print(f"  ⚠️ brief_snapshot 失败: {e}")
    
    git_push()
    print(f"\n📊 Summary: {total_stats['found']} total, {total_stats['new']} new")


if __name__ == "__main__":
    main()
