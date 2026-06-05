---
title: PC Layer: Polynomial Weight Preconditioning for Improving LLM Pre-Training
created: 2026-06-06
updated: 2026-06-06
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/pc-layer-polynomial-weight-preconditioning-for-improving-llm-pre-training.json"]
---

# PC Layer: Polynomial Weight Preconditioning for Improving LLM Pre-Training

## 中文摘要
本文提出了一种名为 PC Layer（多项式权重预条件层）的技术，通过在 LLM 预训练过程中对权重矩阵施加低阶多项式预条件器，重塑其奇异值谱，从而确保训练全程权重条件稳定。该技术可缓解梯度消失/爆炸问题，加速收敛并提升模型最终性能。商业价值在于能降低大规模 LLM 训练的计算成本与时间，提高训练稳定性，使企业更高效地开发高精度模型。产品创新方面，PC Layer 可作为即插即用模块集成到现有 Transformer 训练框架中，无需改动整体架构。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, training, transformer, parameter, gradient

## 作者
Senmiao Wang, Tiantian Fang, Haoran Zhang, Yushun Zhang, Kunxiang Zhao

## 摘要
We propose a preconditioning (PC) layer, a weight parameterization via polynomial preconditioner that ensures stable weight conditioning throughout LLM training. The PC module reshapes the singular-value spectrum of weight matrices via low-degree polynomial preconditioning. After training, the preco...

## 中文摘要
本文提出了一种名为 PC Layer（多项式权重预条件层）的技术，通过在 LLM 预训练过程中对权重矩阵施加低阶多项式预条件器，重塑其奇异值谱，从而确保训练全程权重条件稳定。该技术可缓解梯度消失/爆炸问题，加速收敛并提升模型最终性能。商业价值在于能降低大规模 LLM 训练的计算成本与时间，提高训练稳定性，使企业更高效地开发高精度模型。产品创新方面，PC Layer 可作为即插即用模块集成到现有 Transformer 训练框架中，无需改动整体架构。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.06470v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
