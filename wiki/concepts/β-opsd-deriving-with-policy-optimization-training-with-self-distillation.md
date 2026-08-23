---
title: $β$-OPSD: Deriving with Policy Optimization, Training with Self-Distillation
created: 2026-07-31
updated: 2026-07-31
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/β-opsd-deriving-with-policy-optimization-training-with-self-distillation.json"]
---

# $β$-OPSD: Deriving with Policy Optimization, Training with Self-Distillation

## 中文摘要
该论文提出β-OPSD方法，指出传统在线策略自蒸馏（OPSD）提升推理语言模型时存在不稳定性，并识别其结构性根源——原始OPSD恰好是β=1的特例。通过调整β参数，将策略优化与自蒸馏解耦，在推导阶段使用策略优化，在训练阶段使用自蒸馏，从而增强模型推理能力的稳定性和可扩展性。对AI产品经理而言，该方法可降低强化学习调参成本，提升推理模型在复杂任务中的可靠表现，具有工程实践价值。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, reasoning, training, distillation

## 作者
Jiawei Xu, Minghui Liu, Juzheng Zhang, Tom Goldstein, Furong Huang

## 摘要
On-policy self-distillation (OPSD) is a promising approach to improve reasoning language models, but it remains brittle in practice: making it work reliably often requires substantial engineering effort. We identify a structural source of this difficulty: vanilla OPSD is precisely the $β=1$ member o...

## 中文摘要
该论文提出β-OPSD方法，指出传统在线策略自蒸馏（OPSD）提升推理语言模型时存在不稳定性，并识别其结构性根源——原始OPSD恰好是β=1的特例。通过调整β参数，将策略优化与自蒸馏解耦，在推导阶段使用策略优化，在训练阶段使用自蒸馏，从而增强模型推理能力的稳定性和可扩展性。对AI产品经理而言，该方法可降低强化学习调参成本，提升推理模型在复杂任务中的可靠表现，具有工程实践价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.28582v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
