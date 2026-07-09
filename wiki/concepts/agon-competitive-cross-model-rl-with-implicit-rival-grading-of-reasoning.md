---
title: Agon: Competitive Cross-Model RL with Implicit Rival Grading of Reasoning
created: 2026-07-09
updated: 2026-07-09
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/agon-competitive-cross-model-rl-with-implicit-rival-grading-of-reasoning.json"]
---

# Agon: Competitive Cross-Model RL with Implicit Rival Grading of Reasoning

## 中文摘要
论文《Agon》提出一种竞争性跨模型强化学习方法，通过隐式对手评分机制对推理过程而非仅最终答案进行评价。现有可验证奖励的RL方法（如GRPO）忽视思维链质量，导致模型在复杂问题上倾向于写更多内容而非提升思考深度。Agon利用对手模型隐式判断推理好坏，克服了缺乏思考标注的难题。该方法有望显著提升推理模型的质量，对需要深度推理的AI产品（如数学求解、代码生成）具有重要价值，可能成为下一代推理训练范式。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, reasoning, training, grpo

## 作者
Vladislav Beliaev

## 摘要
Reinforcement learning from verifiable rewards (e.g. GRPO) is the engine behind today's reasoning models, yet it grades only the final answer. On hard problems this trains models to write more rather than to think better, since the trace itself is never graded and no label for good thinking exists. ...

## 中文摘要
论文《Agon》提出一种竞争性跨模型强化学习方法，通过隐式对手评分机制对推理过程而非仅最终答案进行评价。现有可验证奖励的RL方法（如GRPO）忽视思维链质量，导致模型在复杂问题上倾向于写更多内容而非提升思考深度。Agon利用对手模型隐式判断推理好坏，克服了缺乏思考标注的难题。该方法有望显著提升推理模型的质量，对需要深度推理的AI产品（如数学求解、代码生成）具有重要价值，可能成为下一代推理训练范式。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.07690v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
