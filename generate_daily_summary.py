#!/usr/bin/env python3
"""
Generate daily summary for AI Radar — v3.6.0
面向AI产品经理的情报摘要：先观点，后证据。
- LLM模式：深度洞察分析（跨节点综合研判）
- Fallback模式：基于模式识别的智能分析（非模板匹配）
"""

import json, os, re
from datetime import datetime, timezone, timedelta
from collections import Counter

BJ_TZ = timezone(timedelta(hours=8))

GRAPH_JSON = os.path.expanduser("~/ai-radar-wiki/graph.json")

# v3.14.0: Use unified ai_model_router with dual-model fallback
import sys
sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))
try:
    from ai_model_router import call_llm as router_call_llm
    HAS_MODEL_ROUTER = True
except ImportError:
    HAS_MODEL_ROUTER = False

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

# v3.15.0: Check model router availability for summary scene
def _is_model_available():
    """Check if at least one model is configured for summary scene."""
    try:
        from ai_model_router import get_scene_config
        models = get_scene_config("summary")
        return len(models) > 0
    except ImportError:
        return False

PILLAR_NAMES = {
    "capabilities": "🤖 技术能力",
    "patterns": "📱 产品模式",
    "ecosystem": "🔧 工具生态",
    "business": "💰 商业趋势",
}


def get_today_items():
    if not os.path.exists(GRAPH_JSON):
        return []
    with open(GRAPH_JSON, "r") as f:
        data = json.load(f)
    today = datetime.now(BJ_TZ).strftime("%Y-%m-%d")
    items = [n for n in data.get("nodes", [])
             if n.get("date", "").startswith(today) and n.get("type") != "concept"]
    items.sort(key=lambda x: x.get("pm_score", 0), reverse=True)
    return items


# =====================================================================
# FALLBACK: 智能模式识别（替代过时的模板匹配）
# =====================================================================

# 跨节点主题信号库：关键词 → 主题归类
# v3.14.0 修复：收紧关键词，减少误匹配。移除过于宽泛的词（auto、local、model、cloud、startup、raised）
SIGNAL_THEMES = {
    # Agent/自主操作 — 移除 "auto"/"自动化"（太宽泛），保留明确的 Agent 概念词
    "agent": {"keywords": ["ai agent", "agent framework", "autonomous agent", "multi-agent", "智能体", "agent workflow", "agent orchestration", "agentic", "autonomous system"],
              "theme": "AI Agent"},
    "cli": {"keywords": ["cli tool", "command line ai", "terminal ai", "命令行"],
            "theme": "CLI/终端交互"},
    # 桌面/本地化 — 移除 "mac"/"local"/"本地"（太宽泛），保留明确的端侧/桌面 AI 概念
    "desktop": {"keywords": ["desktop ai", "personal computer", "local llm", "on-device", "edge ai", "端侧"],
                "theme": "桌面/本地化"},
    "voice": {"keywords": ["voice ai", "speech-to-text", "text-to-speech", "语音交互", "audio ai", "voice assistant"],
              "theme": "语音交互"},
    "security": {"keywords": ["ai security", "adversarial", "jailbreak", "prompt injection", "漏洞", "exploit", "提权", "attack surface", "ai safety"],
                 "theme": "安全/漏洞"},
    "trust": {"keywords": ["ai alignment", "hallucination", "幻觉", "ai ethics", "ai regulation", "content moderation", "ai bias", "responsible ai"],
              "theme": "信任/合规"},
    "infra": {"keywords": ["kubernetes", "mlops", "inference serving", "gpu cluster", "vllm", "tensorrt", "model deployment", "ai infrastructure"],
              "theme": "基础设施"},
    # 融资/投资 — 移除 "startup"/"raised"（太宽泛），保留明确的融资事件信号
    "funding": {"keywords": ["funding round", "series a", "series b", "series c", "seed round", "a16z", "sequoia", "领投", "acquisition by", "ipo", "valuation"],
                "theme": "融资/投资"},
    "open_source": {"keywords": ["open source release", "开源发布", "new version", "v2.", "v3.", "major release"],
                    "theme": "开源发布"},
    # 模型能力 — 移除单独 "model"/"llm"/"gpt"（太宽泛），保留明确的模型突破信号
    "model": {"keywords": ["new model architecture", "model breakthrough", "sota", "state-of-the-art", "reasoning capability", "context window", "token limit", "推理能力突破"],
              "theme": "模型能力"},
}


def extract_signals(items):
    """从所有情报中提取信号主题"""
    signal_counts = {}
    signal_items = {}

    for item in items:
        text = ((item.get("label", "") or "") + " " +
                (item.get("summary", "") or "") + " " +
                " ".join(item.get("tags", []) or [])).lower()

        for signal_key, signal_def in SIGNAL_THEMES.items():
            for kw in signal_def["keywords"]:
                if kw in text:
                    if signal_key not in signal_counts:
                        signal_counts[signal_key] = 0
                        signal_items[signal_key] = []
                    signal_counts[signal_key] += 1
                    if item not in signal_items[signal_key]:
                        signal_items[signal_key].append(item)
                    break

    return signal_counts, signal_items


def detect_cross_cutting_narratives(signal_counts, signal_items, all_items):
    """识别跨节点的叙事主线（这是产生深度洞察的关键）
    
    v3.8.2 修复：不再使用硬编码叙事模板。改为基于当天真实数据动态生成叙事，
    确保叙事标题和正文都与实际证据直接相关。
    """
    narratives = []
    all_text = " ".join([
        (i.get("label", "") or "") + " " + (i.get("summary", "") or "")
        for i in all_items
    ]).lower()

    # 叙事模式1: "AI Agent 生态工具涌现"（原: AI从对话走向自主操作）
    agent_items = signal_items.get("agent", []) + signal_items.get("cli", []) + signal_items.get("desktop", [])
    agent_count = sum(signal_counts.get(k, 0) for k in ["agent", "cli", "desktop"])
    if agent_count >= 2 and agent_items:
        # 基于真实证据生成叙事
        titles = [i.get("title", "") or i.get("label", "") for i in agent_items[:3]]
        signals = []
        if signal_counts.get("agent", 0) > 0: signals.append("AI Agent")
        if signal_counts.get("cli", 0) > 0: signals.append("CLI/终端")
        if signal_counts.get("desktop", 0) > 0: signals.append("桌面/本地化")
        
        body = f"今日{agent_count}条情报涉及AI Agent及相关工具生态。"
        if titles:
            # Deduplicate titles
            seen_t = set()
            unique_titles = []
            for t in titles:
                if t and t not in seen_t:
                    seen_t.add(t)
                    unique_titles.append(t)
            body += f"典型项目包括：{', '.join(t[:40] for t in unique_titles[:3])}。"
        body += f"具体信号：{', '.join(signals) if signals else 'Agent相关'}。"
        body += "这表明Agent开发工具和协作流程正在快速成熟，PM应关注Agent工程化的基础设施需求。"
        
        narratives.append({
            "type": "paradigm_shift",
            "title": "AI Agent 工具链与协作流程快速成熟",
            "body": body,
            "signals": ["agent", "cli", "desktop"],
        })

    # 叙事模式2: "AI安全与信任挑战"（原: 基础设施安全成为瓶颈）
    security_items = signal_items.get("security", []) + signal_items.get("trust", [])
    sec_count = sum(signal_counts.get(k, 0) for k in ["security", "trust"])
    if sec_count >= 2 and security_items:
        titles = [i.get("title", "") or i.get("label", "") for i in security_items[:3]]
        signals = []
        if signal_counts.get("security", 0) > 0: signals.append("安全漏洞")
        if signal_counts.get("trust", 0) > 0: signals.append("信任/合规")
        
        body = f"今日{sec_count}条情报涉及AI安全与信任议题。"
        if titles:
            seen_t = set()
            unique_titles = []
            for t in titles:
                if t and t not in seen_t:
                    seen_t.add(t)
                    unique_titles.append(t)
            body += f"关键事件包括：{', '.join(t[:40] for t in unique_titles[:3])}。"
        body += f"具体信号：{', '.join(signals) if signals else '安全相关'}。"
        body += "安全已从技术问题升级为企业级AI采购的核心决策因素。PM需要在产品设计中将安全/合规作为一等公民。"
        
        narratives.append({
            "type": "bottleneck",
            "title": "AI安全与信任正成为规模化部署的关键挑战",
            "body": body,
            "signals": ["security", "trust"],
        })

    # 叙事模式3: "AI工具链专业化"
    infra_items = signal_items.get("infra", [])
    os_items = signal_items.get("open_source", [])
    if len(infra_items) >= 1 or len(os_items) >= 1:
        items = infra_items + os_items
        titles = [i.get("title", "") or i.get("label", "") for i in items[:3] if i.get("title") or i.get("label")]
        signals = []
        if signal_counts.get("infra", 0) > 0: signals.append("基础设施")
        if signal_counts.get("open_source", 0) > 0: signals.append("开源工具")
        
        body = f"今日{len(items)}条情报涉及AI工具链与基础设施。"
        if titles:
            seen_t = set()
            unique_titles = []
            for t in titles:
                if t and t not in seen_t:
                    seen_t.add(t)
                    unique_titles.append(t)
            body += f"包括：{', '.join(t[:40] for t in unique_titles[:3])}。"
        body += f"信号：{', '.join(signals) if signals else '工具链相关'}。"
        body += "AI工具链正从通用框架向垂直场景深化，PM应关注开发者在特定工作流中的未满足需求。"
        
        narratives.append({
            "type": "maturation",
            "title": "AI工具链从通用走向垂直专业化",
            "body": body,
            "signals": ["infra", "open_source"],
        })

    # 叙事模式4: "AI商业与融资动态"
    funding_items = signal_items.get("funding", [])
    if len(funding_items) >= 1:
        titles = [i.get("title", "") or i.get("label", "") for i in funding_items[:3]]
        
        body = f"今日{len(funding_items)}条情报涉及AI商业动态。"
        if titles:
            seen_t = set()
            unique_titles = []
            for t in titles:
                if t and t not in seen_t:
                    seen_t.add(t)
                    unique_titles.append(t)
            body += f"包括：{', '.join(t[:40] for t in unique_titles[:3])}。"
        body += "资本市场持续加码AI应用层，PM应关注竞品融资动态和市場格局变化。"
        
        narratives.append({
            "type": "validation",
            "title": "AI商业动态：资本与市场持续升温",
            "body": body,
            "signals": ["funding"],
        })

    return narratives


# 每个叙事类型的行动建议模板
ACTION_TEMPLATES = {
    "paradigm_shift": "建议：安排一次团队讨论，评估此趋势对产品交互范式的影响。重点关注权限模型和用户体验边界的变化。",
    "bottleneck": "建议：审查当前产品的安全/信任/合规设计，是否需要升级。这是获取企业客户的关键竞争力。",
    "maturation": "建议：关注工具链发展，考虑引入专用工具或评估自研可行性。行业成熟意味着标准化窗口接近。",
    "validation": "建议：研究标杆案例，评估差异化空间和进入时机。有产业积累的团队获得青睐说明 Know-how 比纯算法更重要。"
}


def generate_deep_fallback(items):
    """生成深度分析版摘要（非模板，基于模式识别和叙事归纳）"""
    today = datetime.now(BJ_TZ).strftime("%Y-%m-%d")
    # 注意：不再过滤 low-score items，所有情报都展示
    all_value = items  # 展示所有情报
    notable = [i for i in items if i.get("pm_score", 0) >= 0.3]

    # 1. 提取信号
    signal_counts, signal_items = extract_signals(items)

    # 2. 识别跨节点叙事
    narratives = detect_cross_cutting_narratives(signal_counts, signal_items, items)

    # 3. 按pillar分组
    by_pillar = {}
    for item in items:
        p = item.get("pillar", "unknown")
        if p not in by_pillar:
            by_pillar[p] = []
        by_pillar[p].append(item)

    # 4. 生成insights：每个pillar一个洞察，叙事融入相关pillar
    insights = []
    assigned_narratives = set()  # v3.8.2: 追踪已分配的叙事索引，确保一对一

    for pillar_key in ["capabilities", "patterns", "ecosystem", "business"]:
        pillar_items = by_pillar.get(pillar_key, [])
        if not pillar_items:  # 不再要求 >= 0.3，有任何情报就展示
            continue

        pillar_name = PILLAR_NAMES.get(pillar_key, pillar_key)

        # 为该pillar提取信号
        pillar_signals = set()
        for item in pillar_items:
            text = ((item.get("label", "") or "") + " " + (item.get("summary", "") or "")).lower()
            for sk, sd in SIGNAL_THEMES.items():
                for kw in sd["keywords"]:
                    if kw in text:
                        pillar_signals.add(sk)

        # 找到与此pillar最相关的叙事（每个叙事只分配给一个pillar）
        # v3.8.2 修复：使用全局 assigned_narratives 集合，确保 narrative→pillar 一对一
        relevant_narrative = None
        for ni, n in enumerate(narratives):
            if any(s in pillar_signals for s in n["signals"]):
                if ni not in assigned_narratives:
                    relevant_narrative = n
                    assigned_narratives.add(ni)
                    break

        # 洞察文本：基于信号生成定制化洞察（不用完整叙事文本，避免重复）
        signal_themes = [SIGNAL_THEMES[s]["theme"] for s in pillar_signals if s in SIGNAL_THEMES]
        if relevant_narrative:
            # 引用叙事标题+信号，不要全文
            insight_text = relevant_narrative["title"] + "。该方向的具体信号：" + (", ".join(signal_themes) if signal_themes else "新动态") + "。"
        elif signal_themes:
            insight_text = f"今日{pillar_name}方向的核心信号集中在{', '.join(signal_themes)}。"
        else:
            insight_text = f"今日{pillar_name}方向有新的动态。"

        # 证据（所有情报，不过滤分数）+ Score 解释
        # v3.8.2: 去重 — 同一 id+title 只保留一次
        evidence = []
        seen_evidence = set()
        for item in sorted(pillar_items, key=lambda x: x.get("pm_score", 0), reverse=True):
            # Score 解释（基于特征）
            reasons = []
            stars = item.get("stars", 0)
            if stars and stars > 100:
                reasons.append(f"社区关注度高（{stars} stars）")
            elif stars and stars > 50:
                reasons.append(f"社区关注（{stars} stars）")

            tags = item.get("tags", []) or []
            hot_tags = [t for t in tags if t in ("agent", "cli", "llm", "ai", "machine-learning")]
            if hot_tags:
                reasons.append(f"热门方向：{', '.join(hot_tags)}")

            summary_lower = (item.get("summary", "") or "").lower()
            milestone_words = ["突破", "首次", "里程碑", "全新", "发布", "launch", "release", "new"]
            if any(w in summary_lower for w in milestone_words):
                reasons.append("里程碑式进展")

            score = item.get("pm_score", 0)
            if score >= 0.5:
                reasons.append("高价值信号")

            reason = "；".join(reasons) if reasons else "基于新颖度、影响力、相关性综合评分"

            ev_key = item.get("id", "")
            ev_title = item.get("label", "")
            # Dedup by title (same article may have different IDs from different sources)
            if ev_title and ev_title in seen_evidence:
                continue  # v3.8.2: skip duplicate
            if ev_title:
                seen_evidence.add(ev_title)

            evidence.append({
                "id": item.get("id", ""),
                "title": item.get("label", "")[:70],
                "score": round(item.get("pm_score", 0), 2),
                "url": item.get("url", ""),
                "reason": reason,
            })

        insights.append({
            "pillar": pillar_name,
            "pillar_key": pillar_key,
            "insight": insight_text,
            "evidence": evidence,
            "trend": "new",  # 默认 new（数据积累后改为 up/down/stable）
        })

    # 5. 顶部概览：基于叙事生成headline
    if narratives:
        top_narrative = narratives[0]
        overview = top_narrative["title"]
    else:
        overview = f"今日共采集 {len(items)} 条情报"

    # 6. 统计
    pillar_counts = Counter(i.get("pillar", "unknown") for i in items)
    stats = " | ".join(
        f"{PILLAR_NAMES.get(k, k)}: {v}" for k, v in pillar_counts.items()
    )

    # 7. 叙事部分（跨pillar的宏观趋势）
    narrative_section = []
    for n in narratives:
        narrative_section.append({
            "title": n["title"],
            "body": n["body"],
            "type": n["type"],
            "action": ACTION_TEMPLATES.get(n["type"], ""),
        })

    return {
        "date": today,
        "headline": f"今日 AI 情报 · {today}",
        "overview": overview,
        "insights": insights,
        "narratives": narrative_section,
        "stats": stats,
        "total_items": len(items),
        "high_value_count": len(notable),
    }


# =====================================================================
# LLM模式
# =====================================================================

def build_llm_prompt(items):
    """构建LLM prompt — 要求跨节点综合分析，不是简单描述
    
    v3.11.0 修复：明确要求 LLM 在生成 narratives 时指定其所属 pillar，
    并在 insights 中包含对应的 narrative_title，确保叙事和证据可关联。
    """
    today = datetime.now(BJ_TZ).strftime("%Y-%m-%d")
    item_list = ""
    for i, item in enumerate(items[:20], 1):
        pillar = PILLAR_NAMES.get(item.get("pillar", ""), item.get("pillar", ""))
        score = item.get("pm_score", 0)
        title = item.get("label", "")[:70]
        summary_text = (item.get("summary", "") or "")[:200]
        tags = ", ".join(item.get("tags", []) or [])
        item_list += f"{i}. [ID:{item.get('id','')}] [{pillar}] {title} (PM {score:.2f})\n   {summary_text}\n"
        if tags:
            item_list += f"   标签: {tags}\n"

    return f"""你是AI产品设计雷达的首席情报官，服务于AI产品经理。请基于今日情报生成深度分析摘要。

## 核心要求

**不要逐条描述！** 你需要做跨节点综合分析，识别：
1. **跨节点叙事主线**：今天多条情报是否指向同一个大趋势？（如"AI从对话走向自主操作"）
2. **行业拐点信号**：哪些变化标志着行业进入新阶段？
3. **PM行动启示**：这些趋势对AI产品经理意味着什么？应该关注什么？

## 分析框架
参考Stratechery、Exponent等科技分析框架的风格：先给出宏观判断，再用具体情报作为证据支撑。

## ⚠️ 关键规则（必须遵守）

1. **叙事必须关联到具体 pillar**：每个叙事选择一个最相关的 pillar_key（capabilities/patterns/ecosystem/business）
   如果叙事跨多个 pillar，选择最核心的那个。
2. **Insight 必须引用叙事标题**：每个 insight 的 insight 字段必须以对应叙事标题开头，格式为：
   "{{narrative_title}}。该方向的具体信号：..."
   这样后续系统才能将叙事和证据关联起来。
3. **证据去重**：同一篇文章只在一个 insight 中出现一次。
4. **每个 pillar 最多一个 insight**，如果某 pillar 没有相关情报则跳过该 pillar。

## 今日情报
{item_list}

## 输出格式
{{
  "date": "{today}",
  "headline": "今日 AI 情报 · {today}",
  "overview": "用一句话概括今天最重要的跨节点趋势或信号（15-30字）",
  "narratives": [
    {{
      "title": "叙事标题（如：AI从对话走向自主操作系统级控制）",
      "body": "2-3句深度分析：解释这个趋势的含义、对PM的启示、可能的后续发展",
      "type": "paradigm_shift|bottleneck|maturation|validation",
      "pillar_key": "该叙事最相关的pillar（capabilities/patterns/ecosystem/business）"
    }}
  ],
  "insights": [
    {{
      "pillar": "📱 产品模式",
      "pillar_key": "patterns",
      "narrative_title": "必须填：该insight对应的叙事标题（与上面narratives中的title完全一致）",
      "insight": "以叙事标题开头：'{{narrative_title}}。该方向的具体信号：...'（不是简单描述，要指出模式、趋势或矛盾）",
      "evidence": [
        {{"id": "节点ID", "title": "标题（70字以内）", "score": 0.0}}
      ]
    }}
  ],
  "stats": "技术能力: X | 产品模式: Y | 工具生态: Z | 商业趋势: W",
  "total_items": 总数,
  "high_value_count": PM Score >= 0.3 的数量
}}

只输出JSON，不要其他内容。insight 必须以对应的 narrative_title 开头。"""


def call_llm(prompt):
    """Call LLM for daily summary generation.
    
    v3.15.0: Uses scene-aware routing. Summary generation uses qwen-plus (primary)
    with deepseek fallback for better long-form reasoning.
    """
    if HAS_MODEL_ROUTER:
        return router_call_llm(
            prompt=prompt,
            system_prompt="你是AI情报分析师，擅长跨节点综合研判，输出纯JSON。",
            scene="summary",
            temperature=0.4,
            max_tokens=4000,
            require_json=True,
        )
    
    # Fallback to direct router import
    try:
        from ai_model_router import call_llm as direct_router_call
        
        return direct_router_call(
            prompt=prompt,
            system_prompt="你是AI情报分析师，擅长跨节点综合研判，输出纯JSON。",
            scene="summary",
            temperature=0.4,
            max_tokens=4000,
            require_json=True,
        )
    except ImportError:
        print("  ⚠️ ai_model_router 不可用，跳过 LLM 调用")
        return None


# =====================================================================
# 前端渲染辅助
# =====================================================================

def build_evidence_ids_mapping(items):
    """为前端提供所有今日节点的ID映射，确保点击能定位。
    按 label 去重，保留 pm_score 最高的版本。"""
    by_label = {}
    for i in items:
        label = i.get("label", "")
        if not label:
            continue
        if label not in by_label or i.get("pm_score", 0) > by_label[label].get("pm_score", 0):
            by_label[label] = i
    return [{"id": i.get("id", ""), "label": i.get("label", "")} for i in by_label.values()]


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("📝 Generating daily summary v3.6.0 (deep analysis)...")
    beijing_now = datetime.now(BJ_TZ)
    today = beijing_now.strftime("%Y-%m-%d")

    items = get_today_items()
    if not items:
        summary = {
            "date": today, "headline": "今日暂无新情报",
            "overview": "", "insights": [], "narratives": [],
            "stats": "", "total_items": 0, "high_value_count": 0,
            "all_today_ids": []
        }
        # Archive even empty days to maintain timeline continuity
        archive_dir = os.path.expanduser("~/ai-radar-wiki/summary_archive")
        os.makedirs(archive_dir, exist_ok=True)
    elif _is_model_available():
        prompt = build_llm_prompt(items)
        summary = call_llm(prompt)
        if not summary or not summary.get("insights"):
            print("  ⚠️ LLM failed, using deep fallback analysis")
            summary = generate_deep_fallback(items)
        else:
            print(f"  ✅ LLM deep analysis: {len(summary.get('narratives', []))} narratives, {len(summary.get('insights', []))} pillar insights")
    else:
        print("  ⚠️ No API key, using deep fallback analysis")
        summary = generate_deep_fallback(items)

    # Add post-processing dedup to all insights (LLM may produce duplicates)
    for ins in summary.get("insights", []):
        seen = set()
        deduped = []
        for ev in ins.get("evidence", []):
            key = ev.get("title", "") + "|" + str(ev.get("id", ""))
            if key not in seen:
                seen.add(key)
                deduped.append(ev)
        ins["evidence"] = deduped

    # Evidence relevance validation: ensure each evidence actually supports
    # the narrative/insight. LLM frequently inserts unrelated items when
    # a pillar lacks sufficient evidence.
    for ins in summary.get("insights", []):
        insight_text = (ins.get("insight", "") or "").lower()
        narrative_title = (ins.get("narrative_title", "") or "").lower()
        pillar_key = ins.get("pillar_key", "")

        # Extract key entities: proper nouns from narrative title + insight
        # (e.g., "Anthropic", "Notion", "MacBook", "端侧AI")
        import re
        # Extract capitalized English words (proper nouns) from original text
        full_text = ins.get("insight", "") + " " + ins.get("narrative_title", "")
        en_proper_nouns = re.findall(r'[A-Z][a-z]{3,}', full_text)
        # Also extract 3+ Chinese characters (likely key terms)
        cn_terms = re.findall(r'[\u4e00-\u9fff]{3,}', full_text)
        # Also extract short English keywords (2-3 chars that might be acronyms)
        en_acronyms = re.findall(r'\b[A-Z]{2,5}\b', full_text)
        key_entities = [n.lower() for n in en_proper_nouns + en_acronyms] + cn_terms

        validated = []
        for ev in ins.get("evidence", []):
            ev_title = (ev.get("title", "") or "").lower()
            ev_label = (ev.get("id", "") or "").lower()

            if not key_entities:
                # No entities extracted — fallback: keep all evidence
                validated.append(ev)
                continue

            # Check if evidence title contains any key entity from the narrative/insight
            matches = False
            for entity in key_entities:
                if len(entity) >= 3 and entity in ev_title:
                    matches = True
                    break
                # Also check partial: if entity is a proper noun, check word-level match
                if len(entity) >= 4:
                    # Split ev_title into words and check if entity overlaps with any word
                    ev_words = re.findall(r'[a-z]{4,}', ev_title)
                    for ew in ev_words:
                        if entity in ew or ew in entity:
                            matches = True
                            break
                if matches:
                    break

            if matches:
                validated.append(ev)
            else:
                print(f"  ⚠️ Evidence removed (irrelevant): '{ev.get('title','')[:60]}' — no entity match with narrative/insight")

        # Safety net: if all evidence was removed, keep the highest-score one
        if not validated and ins.get("evidence"):
            best = max(ins["evidence"], key=lambda e: e.get("score", 0))
            validated = [best]
            print(f"  ⚡ Safety net: keeping highest-score evidence '{best.get('title','')[:60]}'")

        ins["evidence"] = validated

    # Force canonical date to prevent LLM/date drift issues
    summary["date"] = today
    summary["headline"] = f"今日 AI 情报 · {today}"
    
    # 附加今日节点ID映射，供前端确保所有节点可点击
    summary["all_today_ids"] = build_evidence_ids_mapping(items)
    summary["date_bj"] = f"{today} (北京时区 UTC+8)"
    summary["generated_at_bj"] = beijing_now.strftime("%Y-%m-%d %H:%M:%S")

    output = {"daily_summary": summary}
    out_path = os.path.expanduser("~/ai-radar-wiki/daily_summary.json")
    with open(out_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # 2A-1: Save to daily archive for historical analysis
    # CRITICAL: Use canonical 'today' for filename, NOT summary['date']
    # (summary['date'] may come from LLM which can be wrong)
    archive_dir = os.path.expanduser("~/ai-radar-wiki/summary_archive")
    os.makedirs(archive_dir, exist_ok=True)
    archive_path = os.path.join(archive_dir, f"daily_summary_{today}.json")
    with open(archive_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  💾 Saved to {out_path}")
    print(f"  📰 Headline: {summary.get('headline', 'N/A')}")
    print(f"  📊 Total: {summary.get('total_items', len(items))} items, {summary.get('high_value_count', 0)} high value")
    print(f"  🔍 Narratives: {len(summary.get('narratives', []))}")
    for n in summary.get("narratives", []):
        print(f"    📖 {n.get('title', '')[:50]}...")
    print(f"  📂 Insights: {len(summary.get('insights', []))}")
    for ins in summary.get("insights", []):
        ev_count = len(ins.get("evidence", []))
        print(f"    - {ins.get('pillar', '')}: {ins.get('insight', '')[:50]}... ({ev_count} evidence)")


if __name__ == "__main__":
    main()
