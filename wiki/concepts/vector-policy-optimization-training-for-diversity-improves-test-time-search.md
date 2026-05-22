---
title: Vector Policy Optimization: Training for Diversity Improves Test-Time Search
created: 2026-05-22
updated: 2026-05-22
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/vector-policy-optimization-training-for-diversity-improves-test-time-search.json"]
---

# Vector Policy Optimization: Training for Diversity Improves Test-Time Search

## 中文摘要
本文提出向量策略优化（Vector Policy Optimization），通过训练语言模型的策略多样性来提升其在推理时搜索（如AlphaEvolve）中的泛化能力，使其能适应多种任务特定的奖励函数选择。该方法突破了标准后训练只优化单一预定义奖励的局限，有望在代码生成、规划等复杂场景中，以更低微调成本获得更强推理性能，为产品端集成搜索增强型LLM提供新路径。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, training, grpo, optimization, post-training

## 作者
Ryan Bahlous-Boldi, Isha Puri, Idan Shenfeld, Akarsh Kumar, Mehul Damani

## 摘要
Language models must now generalize out of the box to novel environments and work inside inference-scaling search procedures, such as AlphaEvolve, that select rollouts with a variety of task-specific reward functions. Unfortunately, the standard paradigm of LLM post-training optimizes a pre-specifie...

## 中文摘要
本文提出向量策略优化（Vector Policy Optimization），通过训练语言模型的策略多样性来提升其在推理时搜索（如AlphaEvolve）中的泛化能力，使其能适应多种任务特定的奖励函数选择。该方法突破了标准后训练只优化单一预定义奖励的局限，有望在代码生成、规划等复杂场景中，以更低微调成本获得更强推理性能，为产品端集成搜索增强型LLM提供新路径。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.22817v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
