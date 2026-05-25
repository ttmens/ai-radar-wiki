---
title: LLMs as Noisy Channels: A Shannon Perspective on Model Capacity and Scaling Laws
created: 2026-05-25
updated: 2026-05-25
type: concept
pillar: capabilities
pm_score: 0.395
tags: ["research", "capabilities"]
sources: ["raw/papers/llms-as-noisy-channels-a-shannon-perspective-on-model-capacity-and-scaling-laws.json"]
---

# LLMs as Noisy Channels: A Shannon Perspective on Model Capacity and Scaling Laws

## 中文摘要
本文从香农信道视角重新审视大语言模型的缩放定律，指出传统单调幂律无法解释灾难性过训练和量化退化等非单调现象。作者提出香农缩放定律，将模型视为有噪信道，容量受噪声和计算资源共同约束，解释了性能随计算量增加先升后降的悖论。这一视角为产品经理提供了更精确的模型容量-成本权衡理论，指导训练策略选择（避免过训练）和量化压缩设计（缓解退化），有望降低部署成本、提升模型鲁棒性，推动更高效的大模型产品开发。

## PM 关注指标
- 🎯 PM Score: 0.395
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, fine-tuning, quantization, training, parameter

## 作者
Xu Ouyang, Deyi Liu, Yuhang Cai, Jing Liu, Yuan Yang

## 摘要
Existing scaling laws for Large Language Models (LLMs), predominantly monotonic power laws, fail to explain emerging non-monotonic phenomena such as catastrophic overtraining and quantization-induced degradation, where performance deteriorates despite increased compute.
  We propose the Shannon Scal...

## 中文摘要
本文从香农信道视角重新审视大语言模型的缩放定律，指出传统单调幂律无法解释灾难性过训练和量化退化等非单调现象。作者提出香农缩放定律，将模型视为有噪信道，容量受噪声和计算资源共同约束，解释了性能随计算量增加先升后降的悖论。这一视角为产品经理提供了更精确的模型容量-成本权衡理论，指导训练策略选择（避免过训练）和量化压缩设计（缓解退化），有望降低部署成本、提升模型鲁棒性，推动更高效的大模型产品开发。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.23901v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
