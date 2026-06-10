---
title: ReasonAlloc: Hierarchical Decoding-Time KV Cache Budget Allocation for Reasoning
created: 2026-06-10
updated: 2026-06-10
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/reasonalloc-hierarchical-decoding-time-kv-cache-budget-allocation-for-reasoning.json"]
---

# ReasonAlloc: Hierarchical Decoding-Time KV Cache Budget Allocation for Reasoning Models

## 中文摘要
ReasonAlloc提出了一种用于推理模型的分层解码时键值缓存预算分配方法。针对长链思维轨迹导致的键值缓存快速增长瓶颈，该方法通过分层策略动态分配缓存预算，而非传统均匀分配，从而在保持推理质量的同时显著降低内存占用和延迟。这提升了长链推理效率，降低了部署成本，尤其适用于需要复杂推理的数学、代码等领域，为AI产品实现更高效、更经济的推理能力提供了新方案。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, benchmark, reasoning, training

## 作者
Wenhao Liu, Hao Shi, Yunhe Li, Weizhi Fei, Xiangyuan Wang

## 摘要
Long chain-of-thought (CoT) trajectories in large language model (LLM) reasoning cause severe inference bottlenecks due to rapid key-value (KV) cache growth. Current decoding-time compression methods mitigate this issue via token eviction, but typically assume a uniform budget distribution across al...

## 中文摘要
ReasonAlloc提出了一种用于推理模型的分层解码时键值缓存预算分配方法。针对长链思维轨迹导致的键值缓存快速增长瓶颈，该方法通过分层策略动态分配缓存预算，而非传统均匀分配，从而在保持推理质量的同时显著降低内存占用和延迟。这提升了长链推理效率，降低了部署成本，尤其适用于需要复杂推理的数学、代码等领域，为AI产品实现更高效、更经济的推理能力提供了新方案。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.11164v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
