---
title: VGB for Masked Diffusion Model: Efficient Test-time Scaling for Reward Satisfact
created: 2026-06-29
updated: 2026-06-29
type: concept
pillar: capabilities
pm_score: 0.43
tags: ["research", "capabilities"]
sources: ["raw/papers/vgb-for-masked-diffusion-model-efficient-test-time-scaling-for-reward-satisfacti.json"]
---

# VGB for Masked Diffusion Model: Efficient Test-time Scaling for Reward Satisfaction and Sample Editing

## 中文摘要
本文提出MDM-VGB，一种针对掩码扩散模型（MDM）的高效推理时缩放方法。传统扩散模型在生成过程中难以满足结构约束或优化下游奖励，MDM-VGB通过离散扩散采样器增强未掩码生成阶段，实现推理时自适应调整。该方法在不重新训练模型的前提下，显著提升生成结果的可控性和奖励满意度，适用于图像编辑、条件生成等场景。其核心创新在于将推理计算资源动态分配到关键步骤，降低采样成本的同时保持高质量输出。对AI产品经理而言，该技术可直接应用于内容创作工具、设计辅助等产品，通过更灵活的控制降低用户使用门槛，提升生成式AI的实用性和商业价值。

## PM 关注指标
- 🎯 PM Score: 0.43
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, benchmark, diffusion model

## 作者
Kijung Jeon, Thuy-Duong Vuong, Molei Tao

## 摘要
Inference-time scaling is a promising paradigm to improve generative models, especially when outputs must satisfy structural constraints or optimize downstream rewards. We consider Masked Diffusion Model (MDM) and introduce MDM-VGB, a discrete diffusion sampler that augments unmasking generation wit...

## 中文摘要
本文提出MDM-VGB，一种针对掩码扩散模型（MDM）的高效推理时缩放方法。传统扩散模型在生成过程中难以满足结构约束或优化下游奖励，MDM-VGB通过离散扩散采样器增强未掩码生成阶段，实现推理时自适应调整。该方法在不重新训练模型的前提下，显著提升生成结果的可控性和奖励满意度，适用于图像编辑、条件生成等场景。其核心创新在于将推理计算资源动态分配到关键步骤，降低采样成本的同时保持高质量输出。对AI产品经理而言，该技术可直接应用于内容创作工具、设计辅助等产品，通过更灵活的控制降低用户使用门槛，提升生成式AI的实用性和商业价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.28301v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
