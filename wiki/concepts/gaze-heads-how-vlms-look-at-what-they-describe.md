---
title: Gaze Heads: How VLMs Look at What They Describe
created: 2026-06-15
updated: 2026-06-15
type: concept
pillar: capabilities
pm_score: 0.43
tags: ["research", "capabilities"]
sources: ["raw/papers/gaze-heads-how-vlms-look-at-what-they-describe.json"]
---

# Gaze Heads: How VLMs Look at What They Describe

## 中文摘要
该研究揭示了视觉语言模型（VLM）内部如何完成图像描述任务：模型的语言骨干中存在一小部分被称为“凝视头”（gaze heads）的注意力头，其注意力分布会追踪模型正在描述的图像区域。这一机制为理解多模态模型的内部工作方式提供了关键线索，有助于产品经理优化图像描述、视觉问答等功能的可解释性和可控性。通过识别和干预凝视头，未来可在不改变模型架构的前提下，引导模型聚焦于特定图像区域，提升生成内容的准确性和相关性。该发现对开发更透明、可信的多模态AI产品具有重要商业价值。

## PM 关注指标
- 🎯 PM Score: 0.43
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, multimodal, vision, training

## 作者
Rohit Gandikota, David Bau

## 摘要
How a vision-language model internally solves the task of describing an image is far from obvious. We find that the model develops a specific mechanism for this: a small set of attention heads in its language-model backbone, which we call gaze heads, whose attention tracks the image region the model...

## 中文摘要
该研究揭示了视觉语言模型（VLM）内部如何完成图像描述任务：模型的语言骨干中存在一小部分被称为“凝视头”（gaze heads）的注意力头，其注意力分布会追踪模型正在描述的图像区域。这一机制为理解多模态模型的内部工作方式提供了关键线索，有助于产品经理优化图像描述、视觉问答等功能的可解释性和可控性。通过识别和干预凝视头，未来可在不改变模型架构的前提下，引导模型聚焦于特定图像区域，提升生成内容的准确性和相关性。该发现对开发更透明、可信的多模态AI产品具有重要商业价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.14703v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
