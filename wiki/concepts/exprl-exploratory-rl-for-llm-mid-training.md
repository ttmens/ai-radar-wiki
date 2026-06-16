---
title: ExpRL: Exploratory RL for LLM Mid-Training
created: 2026-06-16
updated: 2026-06-16
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/exprl-exploratory-rl-for-llm-mid-training.json"]
---

# ExpRL: Exploratory RL for LLM Mid-Training

## 中文摘要
ExpRL 提出了一种探索性强化学习（Exploratory RL）方法，用于大语言模型（LLM）的中间训练阶段。传统稀疏奖励强化学习依赖基础模型的覆盖度，而 ExpRL 通过在策划的推理轨迹上进行中间训练，引导模型学习有用的推理原语，从而提升模型在复杂推理任务中的表现。该方法有效缓解了探索不足问题，增强了模型在稀疏奖励场景下的探索能力。对于产品经理而言，这意味着可以更高效地利用有限标注数据提升模型推理质量，降低训练成本，并加速模型在垂直场景（如数学、代码）中的应用落地。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: reasoning, training, grpo, sft, distillation

## 作者
Violet Xiang, Amrith Setlur, Chase Blagden, Nick Haber, Aviral Kumar

## 摘要
Sparse reward reinforcement learning (RL) has become a standard tool for improving LLM reasoning, but its success depends critically on the coverage present in the base model. In practice, models are often primed for RL through \emph{mid-training} on curated reasoning traces that teach useful primit...

## 中文摘要
ExpRL 提出了一种探索性强化学习（Exploratory RL）方法，用于大语言模型（LLM）的中间训练阶段。传统稀疏奖励强化学习依赖基础模型的覆盖度，而 ExpRL 通过在策划的推理轨迹上进行中间训练，引导模型学习有用的推理原语，从而提升模型在复杂推理任务中的表现。该方法有效缓解了探索不足问题，增强了模型在稀疏奖励场景下的探索能力。对于产品经理而言，这意味着可以更高效地利用有限标注数据提升模型推理质量，降低训练成本，并加速模型在垂直场景（如数学、代码）中的应用落地。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.17024v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
