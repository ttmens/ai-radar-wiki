---
title: Quantifying Hyperparameter Transfer and the Importance of Embedding Layer Learni
created: 2026-05-21
updated: 2026-05-21
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/quantifying-hyperparameter-transfer-and-the-importance-of-embedding-layer-learni.json"]
---

# Quantifying Hyperparameter Transfer and the Importance of Embedding Layer Learning Rate

## 中文摘要
该论文研究了超参数迁移（Hyperparameter Transfer）方法，使小规模训练中的最优优化超参数可扩展到大规模LLM训练，显著降低调参成本。关键发现是嵌入层学习率需单独调整，与传统参数共享学习率的做法不同，可提升训练效率。技术上可通过拟合缩放定律或特定参数化（如Maxima）实现迁移。对产品经理而言，这意味着能加速模型迭代、降低训练成本，并为自动化超参数优化工具提供了新思路。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, training, embedding, parameter, optimization

## 作者
Dayal Singh Kalra, Maissam Barkeshli

## 摘要
Hyperparameter transfer allows extrapolating optimal optimization hyperparameters from small to large scales, making it critical for training large language models (LLMs). This is done either by fitting a scaling law to the hyperparameters or by a judicious choice of parameterization, such as Maxima...

## 中文摘要
该论文研究了超参数迁移（Hyperparameter Transfer）方法，使小规模训练中的最优优化超参数可扩展到大规模LLM训练，显著降低调参成本。关键发现是嵌入层学习率需单独调整，与传统参数共享学习率的做法不同，可提升训练效率。技术上可通过拟合缩放定律或特定参数化（如Maxima）实现迁移。对产品经理而言，这意味着能加速模型迭代、降低训练成本，并为自动化超参数优化工具提供了新思路。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.21486v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
