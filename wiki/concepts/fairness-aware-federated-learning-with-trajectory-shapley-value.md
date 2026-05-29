---
title: Fairness-Aware Federated Learning with Trajectory Shapley Value
created: 2026-05-29
updated: 2026-05-29
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/fairness-aware-federated-learning-with-trajectory-shapley-value.json"]
---

# Fairness-Aware Federated Learning with Trajectory Shapley Value

## 中文摘要
该论文提出一种基于轨迹Shapley值的公平感知联邦学习框架，旨在解决联邦学习中传统聚合方案忽略客户端数据异质性和贡献不均的问题。技术要点：通过追踪各客户端在训练过程中的梯度或模型参数轨迹，计算Shapley值以量化每个客户端的边际贡献，并基于此设计公平性聚合权重。商业价值：提升多方协作建模的信任度，尤其适用于医疗、金融等隐私敏感场景，激励高质量数据贡献者。产品创新：引入动态贡献评估机制，使聚合更公平、模型鲁棒性更强，有助于构建可持续的联邦生态。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: benchmark, optimization, dataset

## 作者
Daniel Kuznetsov, Ziqi Wang

## 摘要
Federated learning is an emerging distributed paradigm that addresses the challenges posed by heterogeneous, privacy-sensitive data. It enables multiple clients to train a model collaboratively by aggregating their local updates at a server. However, conventional aggregation schemes typically use fi...

## 中文摘要
该论文提出一种基于轨迹Shapley值的公平感知联邦学习框架，旨在解决联邦学习中传统聚合方案忽略客户端数据异质性和贡献不均的问题。技术要点：通过追踪各客户端在训练过程中的梯度或模型参数轨迹，计算Shapley值以量化每个客户端的边际贡献，并基于此设计公平性聚合权重。商业价值：提升多方协作建模的信任度，尤其适用于医疗、金融等隐私敏感场景，激励高质量数据贡献者。产品创新：引入动态贡献评估机制，使聚合更公平、模型鲁棒性更强，有助于构建可持续的联邦生态。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.30336v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
