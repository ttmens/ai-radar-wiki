---
title: Variance Reduction for Expectations with Diffusion Teachers
created: 2026-05-21
updated: 2026-05-21
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/variance-reduction-for-expectations-with-diffusion-teachers.json"]
---

# Variance Reduction for Expectations with Diffusion Teachers

## 中文摘要
本论文针对扩散模型作为教师模型在下游任务（如文本到3D、单步蒸馏和数据归因）中提供梯度时，蒙特卡洛期望估计存在高方差的问题，提出了一种方差缩减方法。通过优化噪声水平和高斯噪声样本的采样策略，降低了梯度估计的方差，从而提升训练稳定性和效率。该技术有助于减少计算资源消耗，加快模型迭代，对依赖扩散模型的多模态生成产品有直接价值。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: distillation, gradient, diffusion model

## 作者
Jesse Bettencourt, Xindi Wu, Matan Atzmon, James Lucas, Jonathan Lorraine

## 摘要
Pretrained diffusion models serve as frozen teachers feeding downstream pipelines such as text-to-3D, single-step distillation, and data attribution. The teacher gradients these pipelines consume are Monte Carlo (MC) expectations over noise levels and Gaussian noise samples; their estimator variance...

## 中文摘要
本论文针对扩散模型作为教师模型在下游任务（如文本到3D、单步蒸馏和数据归因）中提供梯度时，蒙特卡洛期望估计存在高方差的问题，提出了一种方差缩减方法。通过优化噪声水平和高斯噪声样本的采样策略，降低了梯度估计的方差，从而提升训练稳定性和效率。该技术有助于减少计算资源消耗，加快模型迭代，对依赖扩散模型的多模态生成产品有直接价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.21489v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
