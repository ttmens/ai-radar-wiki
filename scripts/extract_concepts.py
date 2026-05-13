#!/usr/bin/env python3
"""
概念节点提取与构建脚本 (Batch 1 后处理)
从 graph.json 的所有节点中提取概念，构建概念节点体系和 BELONGS_TO 边。
"""

import json
import re
from collections import Counter
from datetime import datetime

WIKI_DIR = "/home/admin/ai-radar-wiki"
GRAPH_JSON = f"{WIKI_DIR}/graph.json"

# AI 领域常见概念关键词
KEYWORD_PATTERNS = [
    "AI Agent", "LLM", "RAG", "Memory", "Multi-Agent", "Fine-tuning",
    "Prompt", "Embedding", "Vector DB", "Transformer", "Diffusion Model",
    "Computer Vision", "NLP", "Reinforcement Learning", "Knowledge Graph",
    "Code Generation", "Text-to-Image", "Voice AI", "Edge AI", "Model Compression",
    "API Integration", "Developer Tool", "Data Pipeline", "Security",
    "Open Source", "Benchmark", "Evaluation", "Training Data"
]

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower().strip())

def extract_concepts(text):
    """从文本中提取概念关键词"""
    concepts = []
    for kw in KEYWORD_PATTERNS:
        if kw.lower() in text.lower():
            concepts.append(kw)
    return list(set(concepts))[:3]

def main():
    print("🔍 概念节点提取脚本启动")
    print("=" * 50)
    
    # 加载 graph.json
    with open(GRAPH_JSON) as f:
        data = json.load(f)
    
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    node_ids = {n['id'] for n in nodes}
    
    print(f"当前节点数: {len(nodes)}")
    print(f"当前边数: {len(edges)}")
    
    # 构建概念映射
    concept_map = {}
    for n in nodes:
        # 跳过概念节点本身
        if n.get('type') == 'concept':
            continue
        
        # 提取概念
        title = n.get('label', '') or ''
        summary = n.get('summary', '') or ''
        text = title + " " + summary
        concepts = extract_concepts(text)
        
        for concept in concepts:
            if not concept or len(concept) < 2:
                continue
            concept_key = slugify(concept)
            if concept_key not in concept_map:
                concept_map[concept_key] = {
                    "label": concept,
                    "nodes": [],
                    "pillar_counts": Counter(),
                    "max_pm": 0.0,
                    "first_seen": n.get('date', datetime.now().strftime("%Y-%m-%d"))
                }
            concept_map[concept_key]["nodes"].append(n['id'])
            concept_map[concept_key]["pillar_counts"][n.get('pillar', 'unknown')] += 1
            pm = n.get('pm_score', 0) or 0
            if pm > concept_map[concept_key]["max_pm"]:
                concept_map[concept_key]["max_pm"] = pm
    
    print(f"\n提取到 {len(concept_map)} 个概念")
    
    # 过滤：只保留关联 >=2 个节点的概念
    valid_concepts = {k: v for k, v in concept_map.items() if len(v['nodes']) >= 2}
    print(f"有效概念（>=2 节点）: {len(valid_concepts)}")
    
    # 添加概念节点
    new_nodes = []
    new_edges = []
    for concept_key, data_item in valid_concepts.items():
        if concept_key in node_ids:
            continue  # 已存在
        
        main_pillar = data_item['pillar_counts'].most_common(1)[0][0] if data_item['pillar_counts'] else 'unknown'
        if main_pillar == 'unknown':
            main_pillar = 'capabilities'
        
        # 获取关联节点标签（前5个）
        related_labels = []
        for nid in data_item['nodes'][:5]:
            for n in nodes:
                if n['id'] == nid:
                    related_labels.append(n['label'][:30])
                    break
        
        concept_summary = f"关联项目: {', '.join(related_labels)}" if related_labels else f"概念: {data_item['label']}"
        
        new_nodes.append({
            "id": concept_key,
            "label": data_item['label'][:80],
            "type": "concept",
            "pillar": main_pillar,
            "pm_score": round(data_item['max_pm'], 2),
            "tags": ["concept", main_pillar],
            "summary": concept_summary,
            "raw_content": "",
            "date": data_item['first_seen'],
            "url": "",
            "related_nodes": data_item['nodes'],
            "node_count": len(data_item['nodes']),
        })
        
        # 创建 BELONGS_TO 边
        for nid in data_item['nodes']:
            new_edges.append({
                "id": f"edge_{nid}_{concept_key}",
                "from": nid,
                "to": concept_key,
                "type": "BELONGS_TO",
                "relation": "belongs_to"
            })
        
        node_ids.add(concept_key)
    
    print(f"\n新增概念节点: {len(new_nodes)}")
    print(f"新增 BELONGS_TO 边: {len(new_edges)}")
    
    # 更新 graph.json
    nodes.extend(new_nodes)
    edges.extend(new_edges)
    
    data['nodes'] = nodes
    data['edges'] = edges
    
    with open(GRAPH_JSON, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ graph.json 已更新")
    print(f"   总节点数: {len(nodes)}")
    print(f"   总边数: {len(edges)}")
    
    # 显示概念节点
    print(f"\n=== 概念节点列表 ===")
    for n in sorted(new_nodes, key=lambda x: x.get('node_count', 0), reverse=True)[:15]:
        print(f"  - {n['label']} (关联: {n['node_count']} 个项目, pillar: {n['pillar']})")
    
    print("\n" + "=" * 50)
    print("概念提取完成！")

if __name__ == "__main__":
    main()
