---
title: Variance-reduced Domain Adaptation using Paired Sampling
created: 2026-07-23
updated: 2026-07-23
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/variance-reduced-domain-adaptation-using-paired-sampling.json"]
---

# Variance-reduced Domain Adaptation using Paired Sampling

## 中文摘要
该论文针对无监督域适应（UDA）中常用的相关性对齐和最大均值差异损失函数在小批量优化时方差过高的问题，提出了一种基于配对采样的方差降低方法。通过精心设计采样策略，在保持分布匹配效果的同时显著降低了训练不稳定性，从而提升模型在目标域上的泛化能力。这一技术能有效降低对目标域标注数据的依赖，减少人工标注成本，对产品快速迁移到新场景（如跨领域图像识别、推荐系统冷启动）具有实用价值。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: training, accuracy, gradient, dataset

## 作者
Andrea Napoli

## 摘要
Correlation alignment and the maximum mean discrepancy are two widely used distribution-matching frameworks for unsupervised domain adaptation (UDA). However, high variance in these losses has been shown to undermine their effectiveness in minibatch optimisation settings. Furthermore, the losses lac...

## 中文摘要
该论文针对无监督域适应（UDA）中常用的相关性对齐和最大均值差异损失函数在小批量优化时方差过高的问题，提出了一种基于配对采样的方差降低方法。通过精心设计采样策略，在保持分布匹配效果的同时显著降低了训练不稳定性，从而提升模型在目标域上的泛化能力。这一技术能有效降低对目标域标注数据的依赖，减少人工标注成本，对产品快速迁移到新场景（如跨领域图像识别、推荐系统冷启动）具有实用价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.20367v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
