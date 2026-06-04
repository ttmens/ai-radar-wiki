---
title: STRIDE: Training Data Attribution via Sparse Recovery from Subset Perturbations
created: 2026-06-05
updated: 2026-06-05
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/stride-training-data-attribution-via-sparse-recovery-from-subset-perturbations.json"]
---

# STRIDE: Training Data Attribution via Sparse Recovery from Subset Perturbations

## 中文摘要
本文介绍 STRIDE，一种基于稀疏恢复的高效训练数据归因方法。传统 TDA 通过因果干预（添加/移除数据后重新训练）获得最准确归因，但 LLM 场景下计算成本极高。STRIDE 通过子集扰动和稀疏恢复技术，在不完全重训练的情况下近似因果效应，大幅降低计算开销。对 AI 产品经理而言，该技术可用于模型行为审计、数据污染检测、合规性验证，提升模型透明度并降低风险，尤其适用于需要追溯训练数据影响的商业化 LLM 产品。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: training, parameter, gradient, pre-training

## 作者
Rishit Dagli, Abir Harrasse, Luke Zhang, Florent Draye, Amirali Abdullah

## 摘要
Training Data Attribution (TDA) seeks to trace a model's predictions back to its training data. The gold standard for TDA relies on causal interventions, observing how a model changes when data is added or removed, but repeated retraining is computationally challenging for Large Language Models (LLM...

## 中文摘要
本文介绍 STRIDE，一种基于稀疏恢复的高效训练数据归因方法。传统 TDA 通过因果干预（添加/移除数据后重新训练）获得最准确归因，但 LLM 场景下计算成本极高。STRIDE 通过子集扰动和稀疏恢复技术，在不完全重训练的情况下近似因果效应，大幅降低计算开销。对 AI 产品经理而言，该技术可用于模型行为审计、数据污染检测、合规性验证，提升模型透明度并降低风险，尤其适用于需要追溯训练数据影响的商业化 LLM 产品。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.05165v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
