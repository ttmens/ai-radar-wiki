---
title: Skill-Conditioned Gated Self-Distillation for LLM Reasoning
created: 2026-05-28
updated: 2026-05-28
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/skill-conditioned-gated-self-distillation-for-llm-reasoning.json"]
---

# Skill-Conditioned Gated Self-Distillation for LLM Reasoning

## 中文摘要
该论文提出了一种基于技能条件的门控自蒸馏方法，用于提升大语言模型（LLM）的推理能力。与传统方法依赖参考答案等可信特权信息不同，该方法探索能否利用非完全可信的特权信息（如成功轨迹）来生成更密集的token级监督信号，从而将稀疏的验证结果转化为细粒度的训练信号。这项技术有助于降低LLM推理训练中对高质量标注数据的依赖，可能推动模型自我改进能力的提升，对降低产品开发成本、增强模型在复杂推理场景的实用性具有潜在商业价值。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, vision, reasoning, grpo

## 作者
Jiazhen Huang, Xiao Chen, Xiao Luo, Yong Dai, Senkang Hu

## 摘要
On-policy self-distillation (SD) improves LLM reasoning by using teacher-side privileged information (PI) to turn sparse verifier outcomes into dense token-level supervision. Existing methods usually assume trusted PI, such as reference answers or successful traces. We ask whether PI can instead com...

## 中文摘要
该论文提出了一种基于技能条件的门控自蒸馏方法，用于提升大语言模型（LLM）的推理能力。与传统方法依赖参考答案等可信特权信息不同，该方法探索能否利用非完全可信的特权信息（如成功轨迹）来生成更密集的token级监督信号，从而将稀疏的验证结果转化为细粒度的训练信号。这项技术有助于降低LLM推理训练中对高质量标注数据的依赖，可能推动模型自我改进能力的提升，对降低产品开发成本、增强模型在复杂推理场景的实用性具有潜在商业价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.28791v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
