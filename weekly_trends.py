#!/usr/bin/env python3
"""
Weekly Trends Analyzer — v3.11.0 (Phase 2)
Reads daily summary archives to compute:
- Pillar trends (up/down/stable)
- Narrative continuity (cross-day tracking)
- Contradiction signals
- Emerging tags
Outputs weekly_trends.json for frontend consumption.
"""

import json
import os
import glob
import re
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict

BJ_TZ = timezone(timedelta(hours=8))
ARCHIVE_DIR = os.path.expanduser("~/ai-radar-wiki/summary_archive")
OUTPUT_FILE = os.path.expanduser("~/ai-radar-wiki/weekly_trends.json")

PILLAR_KEYS = ["capabilities", "patterns", "ecosystem", "business"]
NARRATIVE_TYPES = ["paradigm_shift", "bottleneck", "maturation", "validation"]

def load_archives():
    """Load all daily summary archives sorted by date."""
    files = sorted(glob.glob(os.path.join(ARCHIVE_DIR, "daily_summary_*.json")))
    data = []
    for f in files:
        try:
            with open(f) as fh:
                d = json.load(fh)
                summary = d.get("daily_summary", {})
                if summary.get("date"):
                    data.append(summary)
        except Exception:
            continue
    return sorted(data, key=lambda x: x["date"])

def compute_pillar_trends(summaries):
    """Compute trend direction and delta for each pillar."""
    if len(summaries) < 2:
        return {k: {"trend": "new", "delta": 0, "avg_score": 0} for k in PILLAR_KEYS}

    # Deduplicate summaries by date
    date_map = {}
    for s in summaries:
        d = s.get("date")
        if d:
            if d not in date_map or len(s.get("insights", [])) > len(date_map[d].get("insights", [])):
                date_map[d] = s
    
    deduped = sorted(date_map.values(), key=lambda x: x["date"])
    
    if len(deduped) < 2:
        return {k: {"trend": "insufficient_data", "delta": 0, "avg_score": 0} for k in PILLAR_KEYS}

    trends = {}
    prev = deduped[-2]
    curr = deduped[-1]
    
    prev_total_insights = len(prev.get("insights", []))
    curr_total_insights = len(curr.get("insights", []))

    for key in PILLAR_KEYS:
        prev_count = sum(len(i.get("evidence", [])) for i in prev.get("insights", []) if i.get("pillar_key") == key)
        curr_count = sum(len(i.get("evidence", [])) for i in curr.get("insights", []) if i.get("pillar_key") == key)
        
        prev_has_pillar = any(i.get("pillar_key") == key for i in prev.get("insights", []))
        curr_has_pillar = any(i.get("pillar_key") == key for i in curr.get("insights", []))
        
        delta = curr_count - prev_count
        
        if not curr_has_pillar and prev_has_pillar:
            if curr_total_insights < 3:
                trend = "data_missing"
            else:
                trend = "down"
        elif not prev_has_pillar and curr_has_pillar:
            trend = "up"
        elif delta > 0:
            trend = "up"
        elif delta < 0:
            trend = "down"
        else:
            trend = "stable"
        
        trends[key] = {
            "trend": trend, 
            "delta": delta, 
            "current": curr_count, 
            "previous": prev_count,
            "has_data": curr_has_pillar
        }
    
    return trends

def compute_narrative_chains(summaries):
    """Track narratives across days using fuzzy title matching.
    
    v3.11.0 matching strategy (3-tier priority):
    1. Explicit narrative_title field in insights (from LLM prompt)
    2. Insight text contains narrative title keywords
    3. Keyword overlap fallback (robust, not hardcoded)
    """
    chains = []
    
    def normalize(t):
        return re.sub(r'[^\w\s]', '', t.lower()).strip()

    for summary in summaries:
        date = summary.get("date")
        insights = summary.get("insights", [])
        narratives = summary.get("narratives", [])
        
        # Build narrative → evidence mapping with 3-tier priority
        narrative_evidence_map = {}
        
        for n in narratives:
            n_title = n.get("title", "")
            norm_title = normalize(n_title)
            n_body = normalize(n.get("body", ""))
            
            matched_evidence = []
            seen_ev = set()
            
            # === Priority 1: Explicit narrative_title field (v3.11.0) ===
            for ins in insights:
                nt = ins.get("narrative_title", "")
                if nt and (nt == n_title or normalize(nt) == norm_title):
                    for ev in ins.get("evidence", []):
                        ev_title = ev.get("title", "")
                        if ev_title and ev_title not in seen_ev:
                            seen_ev.add(ev_title)
                            ev_copy = dict(ev)
                            if "pillar" not in ev_copy:
                                ev_copy["pillar"] = ins.get("pillar_key", "")
                            matched_evidence.append(ev_copy)
            
            # === Priority 2: Insight text contains narrative title ===
            if not matched_evidence:
                for ins in insights:
                    ins_text = ins.get("insight", "")
                    if ins_text.startswith(n_title) or n_title in ins_text[:40]:
                        for ev in ins.get("evidence", []):
                            ev_title = ev.get("title", "")
                            if ev_title and ev_title not in seen_ev:
                                seen_ev.add(ev_title)
                                ev_copy = dict(ev)
                                if "pillar" not in ev_copy:
                                    ev_copy["pillar"] = ins.get("pillar_key", "")
                                matched_evidence.append(ev_copy)
            
            # === Priority 3: Keyword overlap fallback (robust) ===
            if not matched_evidence:
                n_words = set(n_body.split()) | set(norm_title.split())
                best_ins = None
                best_score = 0
                for ins in insights:
                    ins_words = set(normalize(ins.get("insight", "")).split())
                    score = len(n_words & ins_words) / max(len(n_words), 1)
                    if score > best_score:
                        best_score = score
                        best_ins = ins
                
                if best_ins and best_score > 0.05:
                    for ev in best_ins.get("evidence", []):
                        ev_title = ev.get("title", "")
                        if ev_title and ev_title not in seen_ev:
                            seen_ev.add(ev_title)
                            ev_copy = dict(ev)
                            if "pillar" not in ev_copy:
                                ev_copy["pillar"] = best_ins.get("pillar_key", "")
                            matched_evidence.append(ev_copy)
            
            # === Priority 4: Pillar-based fallback for old data ===
            if not matched_evidence:
                n_text = (n_title + ' ' + n.get('body', '')).lower()
                pillar_scores = {
                    'patterns': 0,
                    'ecosystem': 0,
                    'business': 0,
                    'capabilities': 0,
                }
                # Count keyword matches per pillar
                for kw in ['agent', 'workflow', 'copilot', '版本控制', 'review tool', 'git for', 'cli', '交互']:
                    if kw in n_text: pillar_scores['patterns'] += 2
                for kw in ['安全', 'security', 'vulnerability', '漏洞', 'cve', 'sandbox', '合规', 'trust', 'safety']:
                    if kw in n_text: pillar_scores['ecosystem'] += 2
                for kw in ['企业', 'enterprise', 'roi', '融资', '裁员', 'layoff', '组织', '降本', '岗位优化']:
                    if kw in n_text: pillar_scores['business'] += 2
                for kw in ['模型', 'model', '训练', '推理', 'benchmark', 'capabilities', 'llm']:
                    if kw in n_text: pillar_scores['capabilities'] += 2
                
                # Pick pillar with highest score (must have at least 2 points)
                best_pillar = max(pillar_scores, key=pillar_scores.get)
                if pillar_scores[best_pillar] >= 2:
                    for ins in insights:
                        if ins.get('pillar_key') == best_pillar:
                            for ev in ins.get("evidence", []):
                                ev_title = ev.get("title", "")
                                if ev_title and ev_title not in seen_ev:
                                    seen_ev.add(ev_title)
                                    ev_copy = dict(ev)
                                    if "pillar" not in ev_copy:
                                        ev_copy["pillar"] = ins.get("pillar_key", "")
                                    matched_evidence.append(ev_copy)
                            break
            
            matched_evidence.sort(key=lambda x: x.get("score", 0), reverse=True)
            narrative_evidence_map[norm_title] = matched_evidence[:5]
        
        # Deduplicate narratives within the same summary by title
        seen_titles = set()
        for n in narratives:
            title = n.get("title", "")
            n_type = n.get("type", "")
            n_body = n.get("body", "")
            norm_title = normalize(title)
            
            if norm_title in seen_titles:
                continue
            seen_titles.add(norm_title)
            
            matched = False
            for chain in chains:
                norm_chain_title = normalize(chain["title"])
                if norm_title == norm_chain_title:
                    is_match = True
                else:
                    words_title = set(norm_title.split())
                    words_chain = set(norm_chain_title.split())
                    overlap = len(words_title & words_chain)
                    min_words = min(len(words_title), len(words_chain))
                    is_match = min_words > 0 and (overlap / min_words) > 0.5
                
                if is_match:
                    if date not in chain["days"]:
                        chain["days"].append(date)
                        chain["instances"].append({
                            "date": date,
                            "title": title,
                            "body": n_body,
                            "type": n_type,
                            "evidence": narrative_evidence_map.get(norm_title, [])
                        })
                        chain["latest_type"] = n_type
                    matched = True
                    break
            
            if not matched:
                chains.append({
                    "title": title,
                    "type": n_type,
                    "latest_type": n_type,
                    "days": [date],
                    "instances": [{
                        "date": date,
                        "title": title,
                        "body": n_body,
                        "type": n_type,
                        "evidence": narrative_evidence_map.get(norm_title, [])
                    }]
                })
    
    # Sort chains by days first, then by lifecycle importance
    lifecycle_order = {"hot": 0, "rising": 1, "emerging": 2, "stable": 3, "declining": 4}
    
    for chain in chains:
        days = len(chain["days"])
        if days == 1: stage = "emerging"
        elif days <= 3: stage = "rising"
        elif days <= 7: stage = "hot"
        else: stage = "declining"
        
        chain["lifecycle"] = stage
        
    return sorted(chains, key=lambda x: (len(x["days"]), lifecycle_order.get(x["lifecycle"], 5)), reverse=True)

def detect_contradictions(summaries):
    """Detect opposing signals in recent data."""
    if len(summaries) < 2: return []
    
    contradictions = []
    recent = summaries[-3:]
    
    for summary in recent:
        narratives = summary.get("narratives", [])
        types_present = [n.get("type") for n in narratives]
        
        if "validation" in types_present and "bottleneck" in types_present:
            contradictions.append({
                "date": summary.get("date"),
                "type": "growth_vs_risk",
                "description": "Growth validation detected alongside infrastructure/trust bottlenecks."
            })
            
    return contradictions

def generate_weekly_summary(summaries, pillar_trends, narrative_chains):
    """Generate a human-readable weekly summary text."""
    if not summaries: return "暂无数据"
    
    unique_dates = sorted(set(s.get("date") for s in summaries if s.get("date")))
    days = len(unique_dates)
    
    total_items = sum(s.get("total_items", 0) for s in summaries)
    
    pillar_counts = Counter()
    for s in summaries:
        for ins in s.get("insights", []):
            pk = ins.get("pillar_key", "")
            ev_count = len(ins.get("evidence", []))
            pillar_counts[pk] += ev_count
            
    dominant_pillar = pillar_counts.most_common(1)[0][0] if pillar_counts else "unknown"
    pillar_names = {"capabilities": "🤖 技术能力", "patterns": "📱 产品模式", "ecosystem": "🔧 工具生态", "business": "💰 商业动态"}
    
    top_narrative = ""
    if narrative_chains:
        top_narrative = narrative_chains[0].get("title", "")
        
    trend_highlights = []
    for k, v in pillar_trends.items():
        if v.get("trend") == "up":
            trend_highlights.append(f"{pillar_names.get(k, k)}呈上升趋势")
    
    if len(unique_dates) >= 2:
        date_range = f"{unique_dates[0]} 至 {unique_dates[-1]}"
        summary_parts = [f"数据覆盖 **{date_range}**（{days}天），累计 **{total_items}** 条情报。"]
    else:
        summary_parts = [f"当前数据：**{total_items}** 条情报。"]
    
    summary_parts.append(f"焦点领域：**{pillar_names.get(dominant_pillar, dominant_pillar)}**。")
    if top_narrative:
        summary_parts.append(f"核心叙事：**{top_narrative}**。")
    if trend_highlights:
        summary_parts.append("值得关注：" + "；".join(trend_highlights))
        
    return " ".join(summary_parts)

def detect_emerging_tags(summaries):
    """Detect new tags that appeared recently."""
    return []

def main():
    print("📊 Analyzing weekly trends (Phase 2)...")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    summaries = load_archives()
    print(f"  📂 Loaded {len(summaries)} daily summaries from archive.")
    
    if not summaries:
        print("  ⚠️ No archives found. Generating empty trend file.")
        result = {"status": "empty", "pillar_trends": {}, "narrative_chains": [], "contradictions": []}
    else:
        pillar_trends = compute_pillar_trends(summaries)
        narrative_chains = compute_narrative_chains(summaries)
        contradictions = detect_contradictions(summaries)
        emerging_tags = detect_emerging_tags(summaries)
        
        result = {
            "generated_at": datetime.now(BJ_TZ).isoformat(),
            "days_analyzed": len(summaries),
            "pillar_trends": pillar_trends,
            "narrative_chains": narrative_chains[:10],
            "contradictions": contradictions,
            "emerging_tags": emerging_tags,
            "weekly_summary": generate_weekly_summary(summaries, pillar_trends, narrative_chains)
        }
        
        print(f"  📈 Trends computed for {len(PILLAR_KEYS)} pillars.")
        print(f"  🔗 Found {len(narrative_chains)} narrative chains.")
        print(f"  ⚠️ Found {len(contradictions)} contradictions.")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"  💾 Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
