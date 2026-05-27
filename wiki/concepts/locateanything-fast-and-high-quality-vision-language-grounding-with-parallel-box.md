---
title: LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Bo
created: 2026-05-27
updated: 2026-05-27
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/locateanything-fast-and-high-quality-vision-language-grounding-with-parallel-box.json"]
---

# LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding

## 中文摘要
该论文提出LocateAnything方法，针对视觉语言模型（VLM）在视觉定位和目标检测中，传统做法将2D边界框序列化为多个1D令牌并逐个独立解码，导致与框几何结构不匹配的问题。LocateAnything采用并行盒解码策略，同时预测所有坐标，大幅提升推理速度并保持高精度。这一创新使得VLM在实时应用（如自动驾驶、机器人交互）中更具可行性与成本效益，降低了延迟并提高了目标定位质量。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, benchmark, vision, throughput

## 作者
Shihao Wang, Shilong Liu, Yuanguo Kuang, Xinyu Wei, Yangzhou Liu

## 摘要
Vision-language models (VLMs) commonly formulate visual grounding and detection as a coordinate-token generation problem, serializing each 2D box into multiple 1D tokens that are learned and decoded largely independently. This token-by-token decoding mismatches the coupled structure of box geometry ...

## 中文摘要
该论文提出LocateAnything方法，针对视觉语言模型（VLM）在视觉定位和目标检测中，传统做法将2D边界框序列化为多个1D令牌并逐个独立解码，导致与框几何结构不匹配的问题。LocateAnything采用并行盒解码策略，同时预测所有坐标，大幅提升推理速度并保持高精度。这一创新使得VLM在实时应用（如自动驾驶、机器人交互）中更具可行性与成本效益，降低了延迟并提高了目标定位质量。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.27365v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
