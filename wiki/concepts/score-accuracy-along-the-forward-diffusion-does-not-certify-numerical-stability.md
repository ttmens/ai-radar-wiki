---
title: Score Accuracy Along the Forward Diffusion Does Not Certify Numerical Stability 
created: 2026-07-10
updated: 2026-07-10
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/score-accuracy-along-the-forward-diffusion-does-not-certify-numerical-stability.json"]
---

# Score Accuracy Along the Forward Diffusion Does Not Certify Numerical Stability in Diffusion Sampling

## 中文摘要
本文发现扩散模型中的评分匹配仅控制前向边缘分布的平均误差，但离散反向采样时模型沿自身轨迹评估学习到的评分，可能导致数值不稳定。这意味着即使前向误差很小，采样过程仍可能发散，影响生成质量。对于AI产品经理，这提醒在部署基于扩散模型的图像/音频生成产品时，需关注采样稳定性，选择或开发更鲁棒的采样算法，以避免生成结果异常，提升用户体验。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: dpo, accuracy

## 作者
Yiwei Zhou

## 摘要
Score matching controls average error under the forward marginals, but a discretized reverse-time sampler evaluates the learned score along its own trajectory. We show that small forward-marginal error does not guarantee numerical stability. We construct a single smooth score field with arbitrarily ...

## 中文摘要
本文发现扩散模型中的评分匹配仅控制前向边缘分布的平均误差，但离散反向采样时模型沿自身轨迹评估学习到的评分，可能导致数值不稳定。这意味着即使前向误差很小，采样过程仍可能发散，影响生成质量。对于AI产品经理，这提醒在部署基于扩散模型的图像/音频生成产品时，需关注采样稳定性，选择或开发更鲁棒的采样算法，以避免生成结果异常，提升用户体验。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.08757v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
