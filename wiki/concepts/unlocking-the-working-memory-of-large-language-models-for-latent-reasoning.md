---
title: Unlocking the Working Memory of Large Language Models for Latent Reasoning
created: 2026-05-29
updated: 2026-05-29
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/unlocking-the-working-memory-of-large-language-models-for-latent-reasoning.json"]
---

# Unlocking the Working Memory of Large Language Models for Latent Reasoning

## 中文摘要
本论文提出解锁大语言模型的工作记忆以实现潜在推理，旨在解决当前通过生成中间token来扩展推理时计算（如思维链）所带来的推理与自回归生成耦合、内部计算与外部通信混淆的问题。技术要点是设计一种分离的潜在推理机制，让模型在工作记忆中独立进行内部计算，再输出最终答案，从而降低生成噪音并提升推理效率。商业价值在于减少无效Token消耗、降低推理成本，并提升对复杂推理问题的响应速度。产品创新方面，可应用于实时对话、代码生成等需要高效推理的场景，提升用户体验和系统吞吐量。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, vision, reasoning

## 作者
Lukas Aichberger, Sepp Hochreiter

## 摘要
To improve the reasoning capabilities of large language models, test-time compute is typically scaled by generating intermediate tokens before the final answer. However, this couples reasoning to autoregressive generation and thereby conflates internal computation with external communication. In con...

## 中文摘要
本论文提出解锁大语言模型的工作记忆以实现潜在推理，旨在解决当前通过生成中间token来扩展推理时计算（如思维链）所带来的推理与自回归生成耦合、内部计算与外部通信混淆的问题。技术要点是设计一种分离的潜在推理机制，让模型在工作记忆中独立进行内部计算，再输出最终答案，从而降低生成噪音并提升推理效率。商业价值在于减少无效Token消耗、降低推理成本，并提升对复杂推理问题的响应速度。产品创新方面，可应用于实时对话、代码生成等需要高效推理的场景，提升用户体验和系统吞吐量。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.30343v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
