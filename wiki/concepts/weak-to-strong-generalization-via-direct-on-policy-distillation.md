---
title: Weak-to-Strong Generalization via Direct On-Policy Distillation
created: 2026-07-07
updated: 2026-07-07
type: concept
pillar: capabilities
pm_score: 0.515
tags: ["research", "capabilities"]
sources: ["raw/papers/weak-to-strong-generalization-via-direct-on-policy-distillation.json"]
---

# Weak-to-Strong Generalization via Direct On-Policy Distillation

## 中文摘要
本文提出Weak-to-Strong Generalization方法，通过直接在线策略蒸馏解决RLVR训练成本高的问题。传统RLVR需强模型生成大量推理轨迹，成本随模型规模增长。该方法利用弱模型生成的指导信号直接蒸馏强模型，实现无需大量rollout的泛化能力提升，降低后训练成本。技术要点包括在线策略对齐和分布匹配，商业价值在于加速模型迭代并节约算力，特别适用于推理增强型产品。

## PM 关注指标
- 🎯 PM Score: 0.515
- 🏷️ Pillar: capabilities
- 🔑 Keywords: vision, reasoning, training, distillation, post-training

## 作者
Shiyuan Feng, Huan-ang Gao, Haohan Chi, Hanlin Wu, Zhilong Zhang

## 摘要
Reinforcement learning with verifiable rewards (RLVR) is a powerful recipe for improving language-model reasoning, but it is expensive to repeat on every new strong model because the target model must generate many rollouts during training. As models scale, post-training itself becomes a bottleneck....

## 中文摘要
本文提出Weak-to-Strong Generalization方法，通过直接在线策略蒸馏解决RLVR训练成本高的问题。传统RLVR需强模型生成大量推理轨迹，成本随模型规模增长。该方法利用弱模型生成的指导信号直接蒸馏强模型，实现无需大量rollout的泛化能力提升，降低后训练成本。技术要点包括在线策略对齐和分布匹配，商业价值在于加速模型迭代并节约算力，特别适用于推理增强型产品。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.05394v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
