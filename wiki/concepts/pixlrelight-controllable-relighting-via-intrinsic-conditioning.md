---
title: PIXLRelight: Controllable Relighting via Intrinsic Conditioning
created: 2026-05-19
updated: 2026-05-19
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/pixlrelight-controllable-relighting-via-intrinsic-conditioning.json"]
---

# PIXLRelight: Controllable Relighting via Intrinsic Conditioning

## 中文摘要
PIXLRelight 是一种基于前馈神经网络的可控单图像重新照明方法。它通过内在条件（如反照率、法线等）实现物理上准确的光照控制，避免了传统方法中链接逆向和正向渲染导致的误差累积，以及昂贵的逐图像优化过程。该方法支持用户通过环境图等方式灵活调整光照，适用于摄影、电影后期、AR/VR 等需要编辑图像光照的产品场景，有望大幅提升图像内容创作的效率与可控性。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, training, transformer, optimization

## 作者
Miguel Farinha, Ronald Clark

## 摘要
We present PIXLRelight, a feed-forward approach for physically controllable single-image relighting. Existing methods either provide limited lighting control (e.g. through text or environment maps), accumulate errors when chaining inverse and forward rendering, or require costly per-image optimizati...

## 中文摘要
PIXLRelight 是一种基于前馈神经网络的可控单图像重新照明方法。它通过内在条件（如反照率、法线等）实现物理上准确的光照控制，避免了传统方法中链接逆向和正向渲染导致的误差累积，以及昂贵的逐图像优化过程。该方法支持用户通过环境图等方式灵活调整光照，适用于摄影、电影后期、AR/VR 等需要编辑图像光照的产品场景，有望大幅提升图像内容创作的效率与可控性。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.18735v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
