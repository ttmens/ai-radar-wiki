---
title: An Agency-Transferring Model-Free Policy Enhancement Technique
created: 2026-06-09
updated: 2026-06-09
type: concept
pillar: capabilities
pm_score: 0.515
tags: ["research", "capabilities"]
sources: ["raw/papers/an-agency-transferring-model-free-policy-enhancement-technique.json"]
---

# An Agency-Transferring Model-Free Policy Enhancement Technique

## 中文摘要
本文提出一种无模型的策略增强技术，通过“代理迁移”（Agency Transferring）将已有次优基线策略的知识高效迁移至新策略，无需从零训练或依赖环境模型。该方法显著降低强化学习（RL）在控制问题中的训练成本，避免繁琐的奖励设计、环境调优和计算开销，适用于机器人、自动驾驶等已有控制系统的场景。商业价值在于利用现有策略快速提升性能，加速RL产品落地。

## PM 关注指标
- 🎯 PM Score: 0.515
- 🏷️ Pillar: capabilities
- 🔑 Keywords: benchmark, training, embedding, neural network

## 作者
Anton Bolychev, Georgiy Malaniya, Sinan Ibrahim, Pavel Osinenko

## 摘要
Training reinforcement learning (RL) policies from scratch is
  costly: it requires careful reward and environment design,
  extensive tuning, and substantial computation.
  Yet many control problems already have a functional but
  suboptimal policy available as a baseline.
  This paper proposes a m...

## 中文摘要
本文提出一种无模型的策略增强技术，通过“代理迁移”（Agency Transferring）将已有次优基线策略的知识高效迁移至新策略，无需从零训练或依赖环境模型。该方法显著降低强化学习（RL）在控制问题中的训练成本，避免繁琐的奖励设计、环境调优和计算开销，适用于机器人、自动驾驶等已有控制系统的场景。商业价值在于利用现有策略快速提升性能，加速RL产品落地。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.09825v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
