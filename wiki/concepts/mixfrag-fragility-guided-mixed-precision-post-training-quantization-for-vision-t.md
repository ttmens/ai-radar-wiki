---
title: MixFrag: Fragility-Guided Mixed-Precision Post-Training Quantization for Vision 
created: 2026-07-31
updated: 2026-07-31
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/mixfrag-fragility-guided-mixed-precision-post-training-quantization-for-vision-t.json"]
---

# MixFrag: Fragility-Guided Mixed-Precision Post-Training Quantization for Vision Transformers

## 中文摘要
MixFrag 提出了一种基于敏感度引导的混合精度后训练量化方法，用于视觉Transformer（ViT）的部署优化。传统PTQ方法对所有组件采用统一位宽，忽略了不同层对量化的敏感度差异，导致精度损失。MixFrag通过识别各层的量化脆弱性，自适应分配不同位宽，在保持模型精度的同时显著降低计算和内存开销。该技术使得ViT能够在资源受限的边缘设备上高效运行，降低部署成本，加速AI产品的落地，尤其适用于计算机视觉场景。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: vision, quantization, training, transformer, precision

## 作者
Md. Mehrab Hossain Opi, Robiul Islam Ryad, Md. Umar Faruk

## 摘要
Post-training quantization (PTQ) has emerged as an effective solution for deploying Vision Transformers (ViTs) on resource-constrained devices. However, existing PTQ methods typically employ uniform bit-widths across transformer components, overlooking their heterogeneous sensitivity to quantization...

## 中文摘要
MixFrag 提出了一种基于敏感度引导的混合精度后训练量化方法，用于视觉Transformer（ViT）的部署优化。传统PTQ方法对所有组件采用统一位宽，忽略了不同层对量化的敏感度差异，导致精度损失。MixFrag通过识别各层的量化脆弱性，自适应分配不同位宽，在保持模型精度的同时显著降低计算和内存开销。该技术使得ViT能够在资源受限的边缘设备上高效运行，降低部署成本，加速AI产品的落地，尤其适用于计算机视觉场景。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.28589v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
