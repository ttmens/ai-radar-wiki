---
title: Complete-muE: Optimal Hyperparameter Transfer and Scaling for MoE Models
created: 2026-05-25
updated: 2026-05-25
type: concept
pillar: capabilities
pm_score: 0.43
tags: ["research", "capabilities"]
sources: ["raw/papers/complete-mue-optimal-hyperparameter-transfer-and-scaling-for-moe-models.json"]
---

# Complete-muE: Optimal Hyperparameter Transfer and Scaling for MoE Models

## 中文摘要
Complete-muE是一种针对Transformer块中密集前馈网络（FFN）与混合专家模型（MoE）的超参数迁移框架。它解决了现有工具如μP（需固定架构）和SDE（需固定每步token数）无法直接处理MoE超参数迁移的问题，实现了最优超参数迁移和模型缩放。该框架可显著降低MoE模型调参成本，加速大模型训练与部署，提升产品迭代效率，为开发者提供统一的超参数管理方案。

## PM 关注指标
- 🎯 PM Score: 0.43
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, training, model architecture, transformer, parameter

## 作者
Hongwu Peng, Ohiremen Dibua, Yuanjun Xiong, Yifan Gong, Jianming Zhang

## 摘要
We propose Complete-muE, a framework which targets hyperparameter transfer across dense FFN and any Mixture-of-Experts (MoE) setups in transformer blocks. Existing tools such as $μ$P (requires fixed architectue) or SDE (requires fixed per-step token count) cannot directly solve the hyperparameter tr...

## 中文摘要
Complete-muE是一种针对Transformer块中密集前馈网络（FFN）与混合专家模型（MoE）的超参数迁移框架。它解决了现有工具如μP（需固定架构）和SDE（需固定每步token数）无法直接处理MoE超参数迁移的问题，实现了最优超参数迁移和模型缩放。该框架可显著降低MoE模型调参成本，加速大模型训练与部署，提升产品迭代效率，为开发者提供统一的超参数管理方案。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.23893v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
