#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为简报首页生成瘦身 JSON：仅当日（北京时间）的非概念节点，避免下载完整 graph.json。

用法：
  python3 scripts/generate_brief_snapshot.py --wiki-root /path/to/ai-radar-wiki

输出：<wiki-root>/brief_snapshot.json
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

BJ = timezone(timedelta(hours=8))

SLIM_KEYS = (
    "id",
    "label",
    "summary",
    "pm_score",
    "pillar",
    "type",
    "source_type",
    "url",
    "date",
    "stars",
    "score",
    "comments",
)


def slim_node(node: dict) -> dict:
    out: dict = {}
    for k in SLIM_KEYS:
        if k in node and node[k] is not None:
            out[k] = node[k]
    if "source_type" not in out:
        out["source_type"] = node.get("source_type") or node.get("type")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument(
        "--wiki-root",
        type=Path,
        required=True,
        help="仓库根目录（含 graph.json）",
    )
    args = ap.parse_args()
    root: Path = args.wiki_root
    graph_path = root / "graph.json"
    if not graph_path.is_file():
        print(f"[brief_snapshot] 跳过：未找到 {graph_path}")
        return 1
    today = datetime.now(BJ).strftime("%Y-%m-%d")
    data = json.loads(graph_path.read_text(encoding="utf-8"))
    items = []
    for n in data.get("nodes") or []:
        if not isinstance(n, dict):
            continue
        if n.get("type") == "concept":
            continue
        d = n.get("date") or ""
        if not str(d).startswith(today):
            continue
        # 过滤低价值节点 (PM Score < 0.3)
        if float(n.get("pm_score") or 0) < 0.3:
            continue
        items.append(slim_node(n))
    items.sort(key=lambda x: float(x.get("pm_score") or 0), reverse=True)
    nodes = data.get("nodes") or []
    real_nodes = sum(1 for n in nodes if isinstance(n, dict) and n.get("type") != "concept")
    edges = data.get("edges") or []
    out = {
        "date": today,
        "generated_at": datetime.now(BJ).isoformat(),
        "item_count": len(items),
        "items": items,
        "graph_totals": {"real_nodes": real_nodes, "edges": len(edges)},
    }
    (root / "brief_snapshot.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[brief_snapshot] {today} {len(items)} 条 → brief_snapshot.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
