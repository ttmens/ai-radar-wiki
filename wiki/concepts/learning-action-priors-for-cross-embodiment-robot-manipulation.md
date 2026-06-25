---
title: Learning Action Priors for Cross-embodiment Robot Manipulation
created: 2026-06-25
updated: 2026-06-25
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/learning-action-priors-for-cross-embodiment-robot-manipulation.json"]
---

# Learning Action Priors for Cross-embodiment Robot Manipulation

## 中文摘要
该论文提出学习动作先验（Action Priors）来解决跨形态机器人操作中Vision-Language-Action（VLA）模型的动作模块几乎从零学习物理运动的问题。传统VLA模型依赖VLM的视觉语言先验，但动作学习缺乏泛化能力。通过引入动作先验，模型能在不同机器人形态间迁移物理运动知识，提升样本效率和操作准确性。这项研究对机器人产品化有重要意义，可降低多形态机器人部署成本，加速技能学习，推动通用机器人操作能力从实验室走向实际应用。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, vision, training, embedding, distillation

## 作者
Dong Jing, Tianqi Zhang, Jiaqi Liu, Jinman Zhao, Zelong Sun

## 摘要
Most Vision-Language-Action (VLA) models build on a Vision-Language Model (VLM) backbone by attaching an action module and optimizing the full policy jointly. This design inherits strong visual and linguistic priors from the VLM, but leaves the action module to learn physical motion almost from scra...

## 中文摘要
该论文提出学习动作先验（Action Priors）来解决跨形态机器人操作中Vision-Language-Action（VLA）模型的动作模块几乎从零学习物理运动的问题。传统VLA模型依赖VLM的视觉语言先验，但动作学习缺乏泛化能力。通过引入动作先验，模型能在不同机器人形态间迁移物理运动知识，提升样本效率和操作准确性。这项研究对机器人产品化有重要意义，可降低多形态机器人部署成本，加速技能学习，推动通用机器人操作能力从实验室走向实际应用。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.26095v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
