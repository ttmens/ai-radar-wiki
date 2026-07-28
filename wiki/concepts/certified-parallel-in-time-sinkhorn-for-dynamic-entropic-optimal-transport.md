---
title: Certified Parallel-in-Time Sinkhorn for Dynamic Entropic Optimal Transport
created: 2026-07-28
updated: 2026-07-28
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/certified-parallel-in-time-sinkhorn-for-dynamic-entropic-optimal-transport.json"]
---

# Certified Parallel-in-Time Sinkhorn for Dynamic Entropic Optimal Transport

## 中文摘要
该论文提出 TemporalSinkhorn，一种时间并行执行器，用于解决动态熵最优传输问题。传统分布式 Sinkhorn 算法顺序处理帧并每轮同步，效率较低。TemporalSinkhorn 通过并行化时间维度，在保持理论保证的同时显著加速动态最优传输计算。该技术可应用于最优传输流匹配（Flow Matching）等动态生成模型，降低实时推理与训练的延迟，对 AI 产品团队而言，能提升动态场景下生成与匹配的效率，推动更实时的多模态应用落地。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: deployment, integration

## 作者
Xinyang Wen

## 摘要
Dynamic applications, including optimal-transport Flow Matching, repeatedly solve related entropic optimal transport problems, yet conventional distributed Sinkhorn processes frames sequentially and synchronizes after every iteration. We present TemporalSinkhorn, a parallel-in-time executor that bat...

## 中文摘要
该论文提出 TemporalSinkhorn，一种时间并行执行器，用于解决动态熵最优传输问题。传统分布式 Sinkhorn 算法顺序处理帧并每轮同步，效率较低。TemporalSinkhorn 通过并行化时间维度，在保持理论保证的同时显著加速动态最优传输计算。该技术可应用于最优传输流匹配（Flow Matching）等动态生成模型，降低实时推理与训练的延迟，对 AI 产品团队而言，能提升动态场景下生成与匹配的效率，推动更实时的多模态应用落地。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.24741v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
