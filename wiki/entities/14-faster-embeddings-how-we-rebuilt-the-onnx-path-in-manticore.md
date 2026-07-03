---
title: 14× faster embeddings: how we rebuilt the ONNX path in Manticore
created: 2026-07-03
updated: 2026-07-03
type: entity
pillar: capabilities
pm_score: 0.365
tags: ["discussion", "hacker-news", "capabilities"]
sources: ["raw/hn/14-faster-embeddings-how-we-rebuilt-the-onnx-path-in-manticore.json"]
---

# 14× faster embeddings: how we rebuilt the ONNX path in Manticore

## 中文摘要
Manticore 搜索引擎通过重构 ONNX 路径，将嵌入生成速度提升 14 倍。技术核心在于优化 ONNX Runtime 的图执行、内存分配和算子融合，减少冗余计算；同时采用批量处理与异步流水线，降低推理延迟。商业价值显著：更快的嵌入生成意味着实时搜索和推荐系统响应更快，基础设施成本降低，尤其适合大规模向量检索场景。产品创新体现在将模型推理深度融入搜索引擎，实现端到端加速，为 AI 应用提供低延迟、高吞吐的能力基础。

## PM 关注指标
- 🔥 HN Score: 48
- 💬 Comments: 7
- 🎯 PM Score: 0.365
- 🏷️ Pillar: capabilities

## 链接
- 🔗 HN 讨论: https://news.ycombinator.com/item?id=48770477
- 🔗 原文: https://manticoresearch.com/blog/onnx-embeddings-speedup/
