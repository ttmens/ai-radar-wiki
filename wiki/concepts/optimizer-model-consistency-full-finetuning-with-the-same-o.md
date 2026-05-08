---
title: Optimizer-Model Consistency: Full Finetuning with the Same Optimizer as Pretrain
created: 2026-05-08
updated: 2026-05-08
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/optimizer-model-consistency-full-finetuning-with-the-same-o.json"]
---

# Optimizer-Model Consistency: Full Finetuning with the Same Optimizer as Pretraining Forgets Less

## 中文摘要
该研究指出，在大模型全量微调阶段沿用预训练时的优化器，能显著提升“学习-遗忘”平衡，有效缓解灾难性遗忘问题。对AI产品经理而言，该技术可简化微调流程，降低为保留通用能力而引入额外策略的成本，提升垂直领域模型迭代的稳定性与效率。产品端可借此实现更平滑的定制化升级，缩短上线周期，同时保障核心功能体验的一致性，具有较高的工程落地价值。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: reasoning, training, sft

## 作者
Yuxing Liu, Jianyu Wang, Tong Zhang

## 摘要
Optimizers play an important role in both pretraining and finetuning stages when training large language models (LLMs). In this paper, we present an observation that full finetuning with the same optimizer as in pretraining achieves a better learning-forgetting tradeoff, i.e., forgetting less while ...

## 中文摘要
该研究指出，在大模型全量微调阶段沿用预训练时的优化器，能显著提升“学习-遗忘”平衡，有效缓解灾难性遗忘问题。对AI产品经理而言，该技术可简化微调流程，降低为保留通用能力而引入额外策略的成本，提升垂直领域模型迭代的稳定性与效率。产品端可借此实现更平滑的定制化升级，缩短上线周期，同时保障核心功能体验的一致性，具有较高的工程落地价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.06654v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
