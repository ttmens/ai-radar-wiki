---
title: SURGE: Approximation-free Training Free Particle Filter for Diffusion Surrogate
created: 2026-05-19
updated: 2026-05-19
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/surge-approximation-free-training-free-particle-filter-for-diffusion-surrogate.json"]
---

# SURGE: Approximation-free Training Free Particle Filter for Diffusion Surrogate

## 中文摘要
本文提出SURGE方法，一种无近似、无需训练的粒子滤波技术，用于扩散模型的推理时引导。现有方法依赖重复评分或梯度评估，存在偏差和高计算成本。SURGE通过引入无近似的粒子滤波，无需额外训练即可有效提升样本质量，适用于任务特定目标优化。该技术降低了扩散模型推理的计算开销，同时保持生成质量，对需要实时或高效生成高质量内容的AI产品（如图像生成、视频合成等）具有商业价值，可加速产品迭代并降低部署成本。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, benchmark, training, gradient

## 作者
Lifu Wei, Yinuo Ren, Naichen Shi, Yiping Lu

## 摘要
Diffusion-based generative models increasingly rely on inference-time guidance, adding a drift term or reweighting mixture of experts, to improve sample quality on task-specific objectives. However, most existing techniques require repeated score or gradient evaluations, introducing bias, high compu...

## 中文摘要
本文提出SURGE方法，一种无近似、无需训练的粒子滤波技术，用于扩散模型的推理时引导。现有方法依赖重复评分或梯度评估，存在偏差和高计算成本。SURGE通过引入无近似的粒子滤波，无需额外训练即可有效提升样本质量，适用于任务特定目标优化。该技术降低了扩散模型推理的计算开销，同时保持生成质量，对需要实时或高效生成高质量内容的AI产品（如图像生成、视频合成等）具有商业价值，可加速产品迭代并降低部署成本。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.18745v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
