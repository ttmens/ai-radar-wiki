---
title: Reroute, Don't Remove: Recoverable Visual Token Routing for Vision-Language Mode
created: 2026-06-11
updated: 2026-06-11
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/reroute-dont-remove-recoverable-visual-token-routing-for-vision-language-models.json"]
---

# Reroute, Don't Remove: Recoverable Visual Token Routing for Vision-Language Models

## 中文摘要
本文提出一种可恢复的视觉token路由方法（Reroute, Don’t Remove），旨在解决视觉语言模型（VLM）中大量视觉token导致解码器注意力计算和KV缓存开销过高的问题。传统方法采用“评分并移除”的范式，永久丢弃低分token，可能损失关键信息。新方法允许token被暂时路由到低优先级路径，后续仍可恢复参与推理，从而在保证模型性能的同时大幅降低计算和内存成本。该技术有助于VLM在资源受限设备（如手机、边缘设备）上高效运行，降低部署成本，提升实时交互体验，对商用多模态AI产品具有显著价值。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, vision, training, attention

## 作者
Cheng-Yu Yang, Shao-Yuan Lo, Yu-Lun Liu

## 摘要
Vision-language models (VLMs) project images into hundreds to thousands of visual tokens, making decoder inference expensive in both attention computation and KV-cache memory. Existing visual-token reduction methods largely follow a rank-and-remove paradigm: they score visual tokens, keep a compact ...

## 中文摘要
本文提出一种可恢复的视觉token路由方法（Reroute, Don’t Remove），旨在解决视觉语言模型（VLM）中大量视觉token导致解码器注意力计算和KV缓存开销过高的问题。传统方法采用“评分并移除”的范式，永久丢弃低分token，可能损失关键信息。新方法允许token被暂时路由到低优先级路径，后续仍可恢复参与推理，从而在保证模型性能的同时大幅降低计算和内存成本。该技术有助于VLM在资源受限设备（如手机、边缘设备）上高效运行，降低部署成本，提升实时交互体验，对商用多模态AI产品具有显著价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.12412v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
