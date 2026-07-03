---
title: DemoPSD: Disagreement-Modulated Policy Self-Distillation
created: 2026-07-03
updated: 2026-07-03
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/demopsd-disagreement-modulated-policy-self-distillation.json"]
---

# DemoPSD: Disagreement-Modulated Policy Self-Distillation

## 中文摘要
DemoPSD 提出了一种基于分歧调制的策略自我蒸馏方法，用于改进大语言模型（LLM）的推理训练。该方法在在线自我蒸馏（OPSD）框架基础上，利用教师模型在 token 级别输出中的分歧信号来动态调制蒸馏过程，使得单一模型既能作为教师（访问更多信息）又能作为学生（有限信息）进行学习。这种技术可提升知识传递效率，降低训练成本，同时增强模型推理能力，对产品经理而言意味着更高效地构建高质量 LLM 推理产品，具有显著的商业价值。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, vision, reasoning, training

## 作者
Yunhe Li, Hao Shi, Wenhao Liu, Mengzhe Ruan, Hanxu Hou

## 摘要
On-policy self-distillation (OPSD) has emerged as a practical method for training large language models (LLMs) to reason, where a single model acts as both the teacher and the student with different levels of information access. However, recent studies have found that the teacher's dense token-level...

## 中文摘要
DemoPSD 提出了一种基于分歧调制的策略自我蒸馏方法，用于改进大语言模型（LLM）的推理训练。该方法在在线自我蒸馏（OPSD）框架基础上，利用教师模型在 token 级别输出中的分歧信号来动态调制蒸馏过程，使得单一模型既能作为教师（访问更多信息）又能作为学生（有限信息）进行学习。这种技术可提升知识传递效率，降低训练成本，同时增强模型推理能力，对产品经理而言意味着更高效地构建高质量 LLM 推理产品，具有显著的商业价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.02502v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
