---
title: QASP: Query-Adaptive Robust Vector Search Policy
created: 2026-08-03
updated: 2026-08-03
type: concept
pillar: capabilities
pm_score: 0.43
tags: ["research", "capabilities"]
sources: ["raw/papers/qasp-query-adaptive-robust-vector-search-policy.json"]
---

# QASP: Query-Adaptive Robust Vector Search Policy

## 中文摘要
QASP（Query-Adaptive Robust Vector Search Policy）提出了一种查询自适应的向量搜索策略，旨在解决传统固定搜索参数在不同查询间性能波动大的问题。常规评估依赖平均召回率，容易掩盖个别查询的低效表现，而QASP通过动态调整搜索策略，针对每个查询优化计算资源分配，实现高召回率与低成本的平衡。对产品经理而言，该技术可显著提升搜索产品的响应速度与结果质量，尤其适用于大规模知识库或语义检索场景，降低基础设施开销，并改善用户体验的一致性。

## PM 关注指标
- 🎯 PM Score: 0.43
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, training, parameter, recall, dataset

## 作者
Hakan Ferhatosmanoglu, Kushal Kumar, Tal Wagner, Andy Warfield

## 摘要
A fundamental challenge of vector search is achieving consistently high recall while minimizing computational costs. Fixed search parameters cause significant performance variance across queries, and conventional evaluation on average recall masks these per-query disparities. We introduce QASP (Quer...

## 中文摘要
QASP（Query-Adaptive Robust Vector Search Policy）提出了一种查询自适应的向量搜索策略，旨在解决传统固定搜索参数在不同查询间性能波动大的问题。常规评估依赖平均召回率，容易掩盖个别查询的低效表现，而QASP通过动态调整搜索策略，针对每个查询优化计算资源分配，实现高召回率与低成本的平衡。对产品经理而言，该技术可显著提升搜索产品的响应速度与结果质量，尤其适用于大规模知识库或语义检索场景，降低基础设施开销，并改善用户体验的一致性。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.29606v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
