---
title: The Seriality Gap in Video Diffusion Models
created: 2026-07-15
updated: 2026-07-15
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/the-seriality-gap-in-video-diffusion-models.json"]
---

# The Seriality Gap in Video Diffusion Models

## 中文摘要
本论文揭示了视频扩散模型在预测多球碰撞等连续因果事件时的序列性差距：随着因果链长度增加，标准双向视频扩散模型的预测性能显著下降。这一发现对需要模拟长时间物理交互的产品（如游戏、机器人仿真、内容生成）至关重要，提示产品经理需关注模型对长程因果推理的局限性。未来可通过引入因果注意力机制或单步自回归增强来弥合此差距，从而提升复杂场景下的视频生成一致性。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: reasoning, diffusion model

## 作者
Jorge Diaz Chao, Konpat Preechakul, Yuxi Liu, Yutong Bai

## 摘要
When one ball strikes another, then another, video models should predict the consequences of each bounce. In controlled experiments on multi-ball hard-sphere dynamics, we find that the performance of standard bidirectional video diffusion degrades as the causal chain lengthens, even when provided mo...

## 中文摘要
本论文揭示了视频扩散模型在预测多球碰撞等连续因果事件时的序列性差距：随着因果链长度增加，标准双向视频扩散模型的预测性能显著下降。这一发现对需要模拟长时间物理交互的产品（如游戏、机器人仿真、内容生成）至关重要，提示产品经理需关注模型对长程因果推理的局限性。未来可通过引入因果注意力机制或单步自回归增强来弥合此差距，从而提升复杂场景下的视频生成一致性。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.13031v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
