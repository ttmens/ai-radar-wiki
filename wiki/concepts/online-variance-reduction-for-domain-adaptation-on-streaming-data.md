---
title: Online Variance Reduction for Domain Adaptation on Streaming Data
created: 2026-07-23
updated: 2026-07-23
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/online-variance-reduction-for-domain-adaptation-on-streaming-data.json"]
---

# Online Variance Reduction for Domain Adaptation on Streaming Data

## 中文摘要
这篇论文研究在线方差缩减技术，用于解决流式数据场景下的领域自适应问题。针对MMD和CORAL损失函数，现有离线SVR算法无法支持在线、分布式或增量学习，本文提出兼容在线的方法，使模型能够高效适应持续变化的数据分布，无需全量重训练。产品经理可关注其在推荐系统、实时监控、IoT等需处理流式数据且分布漂移频繁的应用中的价值：减少存储和计算开销，提升模型实时性与鲁棒性。技术核心是结合方差缩减与在线学习，推动持续自适应能力落地。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: accuracy, loss function

## 作者
Andrea Napoli

## 摘要
This paper studies the problem of stochastic variance reduction (SVR) for the maximum mean discrepancy (MMD) and correlation alignment (CORAL) loss functions. Although various offline SVR algorithms for these losses have been proposed, these are incompatible with online, distributed, or incremental ...

## 中文摘要
这篇论文研究在线方差缩减技术，用于解决流式数据场景下的领域自适应问题。针对MMD和CORAL损失函数，现有离线SVR算法无法支持在线、分布式或增量学习，本文提出兼容在线的方法，使模型能够高效适应持续变化的数据分布，无需全量重训练。产品经理可关注其在推荐系统、实时监控、IoT等需处理流式数据且分布漂移频繁的应用中的价值：减少存储和计算开销，提升模型实时性与鲁棒性。技术核心是结合方差缩减与在线学习，推动持续自适应能力落地。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.20374v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
