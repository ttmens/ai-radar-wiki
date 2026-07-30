---
title: Do You Really Need to Pretrain Q-Functions for Online RL Fine-Tuning?
created: 2026-07-30
updated: 2026-07-30
type: concept
pillar: capabilities
pm_score: 0.41
tags: ["research", "capabilities"]
sources: ["raw/papers/do-you-really-need-to-pretrain-q-functions-for-online-rl-fine-tuning.json"]
---

# Do You Really Need to Pretrain Q-Functions for Online RL Fine-Tuning?

## 中文摘要
本文探讨在强化学习（RL）中，针对基于价值的方法，是否需要对Q函数进行离线预训练以提升在线微调效果。传统观点认为预训练策略后直接微调即可，但研究指出预训练Q函数能显著改善样本效率与最终性能，尤其当离线数据质量高时。这对AI产品经理意味着：在设计需要持续学习与适应环境的决策系统（如机器人控制、推荐系统）时，预训练Q函数是一种低成本、高回报的优化手段，可缩短在线训练周期并降低部署风险。

## PM 关注指标
- 🎯 PM Score: 0.41
- 🏷️ Pillar: capabilities
- 🔑 Keywords: benchmark, fine-tuning, training, pre-training

## 作者
Perry Dong, Ron Polonsky, Dorsa Sadigh, Chelsea Fin

## 摘要
Pre-training followed by fine-tuning has become the dominant recipe for learning performant policies, and in value-based reinforcement learning (RL) this raises a natural question: given a pretrained policy, should the Q-function be pretrained on offline data too? Conventional wisdom suggests it sho...

## 中文摘要
本文探讨在强化学习（RL）中，针对基于价值的方法，是否需要对Q函数进行离线预训练以提升在线微调效果。传统观点认为预训练策略后直接微调即可，但研究指出预训练Q函数能显著改善样本效率与最终性能，尤其当离线数据质量高时。这对AI产品经理意味着：在设计需要持续学习与适应环境的决策系统（如机器人控制、推荐系统）时，预训练Q函数是一种低成本、高回报的优化手段，可缩短在线训练周期并降低部署风险。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.27203v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
