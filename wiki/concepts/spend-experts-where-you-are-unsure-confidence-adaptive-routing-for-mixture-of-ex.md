---
title: Spend Experts Where You Are Unsure: Confidence-Adaptive Routing for Mixture-of-E
created: 2026-07-29
updated: 2026-07-29
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/spend-experts-where-you-are-unsure-confidence-adaptive-routing-for-mixture-of-ex.json"]
---

# Spend Experts Where You Are Unsure: Confidence-Adaptive Routing for Mixture-of-Experts LoRA

## 中文摘要
该论文针对混合专家（MoE）与低秩适配（LoRA）模型中固定专家数量k的局限，提出自信自适应路由方法。传统方法对所有token分配相同专家数，导致简单token浪费计算资源，困难token服务不足。论文利用路由器输出分布中隐含的不确定性信息，动态调整每个token激活的专家数量。核心创新在于根据模型对token的自信程度自适应分配计算资源，提升效率与效果。商业价值在于降低推理成本，增强模型处理复杂任务的能力，适用于需要高效调优的大模型产品场景。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, parameter

## 作者
Tom Saliencro, Rohan Desai, Priya Nair, Maya Lindqvist, Daniel Whitmore

## 摘要
Mixture-of-Experts (MoE) variants of Low-Rank Adaptation (LoRA) route every token to a fixed number of experts $k$. Tokens differ in how uncertain the model is about them, so a single k over-spends on easy tokens and under-serves hard ones. We observe that the router's output distribution is already...

## 中文摘要
该论文针对混合专家（MoE）与低秩适配（LoRA）模型中固定专家数量k的局限，提出自信自适应路由方法。传统方法对所有token分配相同专家数，导致简单token浪费计算资源，困难token服务不足。论文利用路由器输出分布中隐含的不确定性信息，动态调整每个token激活的专家数量。核心创新在于根据模型对token的自信程度自适应分配计算资源，提升效率与效果。商业价值在于降低推理成本，增强模型处理复杂任务的能力，适用于需要高效调优的大模型产品场景。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.26052v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
