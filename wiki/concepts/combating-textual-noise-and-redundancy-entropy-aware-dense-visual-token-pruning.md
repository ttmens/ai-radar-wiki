---
title: Combating Textual Noise and Redundancy: Entropy-Aware Dense Visual Token Pruning
created: 2026-07-03
updated: 2026-07-03
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/combating-textual-noise-and-redundancy-entropy-aware-dense-visual-token-pruning.json"]
---

# Combating Textual Noise and Redundancy: Entropy-Aware Dense Visual Token Pruning

## 中文摘要
本文提出一种熵感知的密集视觉token剪枝方法，旨在解决现有视觉token剪枝在密集指令和细粒度查询下丢失关键线索的问题。通过识别文本噪声和冗余两个瓶颈，该方法利用信息熵调控剪枝策略，保留重要视觉信息，从而加速大型视觉语言模型（VLM）推理。商业价值在于降低计算成本、提升响应速度，适用于多模态问答、图像检索等产品场景。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, multimodal, compression, accuracy

## 作者
Xuehui Wang, Xuankun Yang, Wei Shen

## 摘要
Visual token pruning is a crucial strategy for accelerating VLMs by compressing redundant image patches, yet existing methods often fail to preserve critical cues under dense instructions and fine-grained queries. In this paper, we investigate this failure and identify two underlying bottlenecks: th...

## 中文摘要
本文提出一种熵感知的密集视觉token剪枝方法，旨在解决现有视觉token剪枝在密集指令和细粒度查询下丢失关键线索的问题。通过识别文本噪声和冗余两个瓶颈，该方法利用信息熵调控剪枝策略，保留重要视觉信息，从而加速大型视觉语言模型（VLM）推理。商业价值在于降低计算成本、提升响应速度，适用于多模态问答、图像检索等产品场景。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.02484v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
