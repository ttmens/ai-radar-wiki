---
title: ReToken: One Token to Improve Vision-Language Models for Visual Retrieval
created: 2026-07-31
updated: 2026-07-31
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/retoken-one-token-to-improve-vision-language-models-for-visual-retrieval.json"]
---

# ReToken: One Token to Improve Vision-Language Models for Visual Retrieval

## 中文摘要
ReToken 是一种用于视觉语言模型（VLM）的可学习嵌入 token，旨在解决长视觉上下文中的检索难题。随着干扰物数量增加，模型性能会下降，且全量处理 token 在 GPU 显存限制下不可行。ReToken 通过显式检索训练，能够从大量视觉 token 中高效筛选关键信息，显著降低计算开销并提升检索准确性。该技术对需要处理长视频或多图像场景的 AI 产品（如视觉问答、多模态搜索）具有直接价值，可降低推理成本并增强模型在复杂视觉环境下的鲁棒性。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, benchmark, vision, training

## 作者
Yao Xiao, Reuben Tan, Zhen Zhu, Yuqun Wu, Jianfeng Gao

## 摘要
Long visual context poses a challenge for vision-language models: performance degrades as the number of distractors grows, and processing all tokens at once is computationally infeasible under GPU memory constraints. We present ReToken, a single learnable embedding trained as an explicit retrieval t...

## 中文摘要
ReToken 是一种用于视觉语言模型（VLM）的可学习嵌入 token，旨在解决长视觉上下文中的检索难题。随着干扰物数量增加，模型性能会下降，且全量处理 token 在 GPU 显存限制下不可行。ReToken 通过显式检索训练，能够从大量视觉 token 中高效筛选关键信息，显著降低计算开销并提升检索准确性。该技术对需要处理长视频或多图像场景的 AI 产品（如视觉问答、多模态搜索）具有直接价值，可降低推理成本并增强模型在复杂视觉环境下的鲁棒性。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.28627v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
