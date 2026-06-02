---
title: AdaCodec: A Predictive Visual Code for Video MLLMs
created: 2026-06-02
updated: 2026-06-02
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/adacodec-a-predictive-visual-code-for-video-mllms.json"]
---

# AdaCodec: A Predictive Visual Code for Video MLLMs

## 中文摘要
该论文提出AdaCodec，一种针对视频多模态大语言模型（MLLMs）的预测性视觉编码方法。现有模型将每帧独立编码为RGB图像，导致相邻帧中重复的视觉信息（如物体、背景）产生冗余token，增加计算开销。AdaCodec通过预测帧间变化，仅编码差异部分，显著减少token数量，提升推理效率与模型响应速度。这一创新可直接应用于视频理解、实时分析等场景，降低部署成本，推动视频MLLMs在移动端或边缘设备上的实用化。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, multimodal

## 作者
Haowen Hou, Zhen Huang, Zheming Liang, Qingyi Si, Chenglin Li

## 摘要
Video is temporally redundant: adjacent frames usually share most objects, background, and layout. Yet existing video multimodal large language models (video MLLMs) usually encode each sampled frame as an independent RGB image, causing visual tokens to repeat content already present in earlier frame...

## 中文摘要
该论文提出AdaCodec，一种针对视频多模态大语言模型（MLLMs）的预测性视觉编码方法。现有模型将每帧独立编码为RGB图像，导致相邻帧中重复的视觉信息（如物体、背景）产生冗余token，增加计算开销。AdaCodec通过预测帧间变化，仅编码差异部分，显著减少token数量，提升推理效率与模型响应速度。这一创新可直接应用于视频理解、实时分析等场景，降低部署成本，推动视频MLLMs在移动端或边缘设备上的实用化。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.02569v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
