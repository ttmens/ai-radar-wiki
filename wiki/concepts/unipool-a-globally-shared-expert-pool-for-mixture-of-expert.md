---
title: UniPool: A Globally Shared Expert Pool for Mixture-of-Experts
created: 2026-05-08
updated: 2026-05-08
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/unipool-a-globally-shared-expert-pool-for-mixture-of-expert.json"]
---

# UniPool: A Globally Shared Expert Pool for Mixture-of-Experts

## 中文摘要
UniPool提出全局共享专家池架构，打破传统MoE每层独立专家的刚性限制。该技术实现专家资源跨层复用，解耦模型深度与参数量的线性增长，显著提升参数利用率与计算效率。对AI产品经理而言，这意味着同等算力下可部署更深更强的模型，大幅压降训练与推理成本，为构建高性价比、易扩展的大模型服务提供底层架构创新，具备明确的工程落地与商业化降本价值。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, training

## 作者
Minbin Huang, Han Shi, Chuanyang Zheng, Yimeng Wu, Guoxuan Chen

## 摘要
Modern Mixture-of-Experts (MoE) architectures allocate expert capacity through a rigid per-layer rule: each transformer layer owns a separate expert set. This convention couples depth scaling with linear expert-parameter growth and assumes that every layer needs isolated expert capacity. However, re...

## 中文摘要
UniPool提出全局共享专家池架构，打破传统MoE每层独立专家的刚性限制。该技术实现专家资源跨层复用，解耦模型深度与参数量的线性增长，显著提升参数利用率与计算效率。对AI产品经理而言，这意味着同等算力下可部署更深更强的模型，大幅压降训练与推理成本，为构建高性价比、易扩展的大模型服务提供底层架构创新，具备明确的工程落地与商业化降本价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.06665v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
