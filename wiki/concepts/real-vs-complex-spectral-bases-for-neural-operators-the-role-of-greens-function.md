---
title: Real vs. Complex Spectral Bases for Neural Operators: The Role of Green's Functi
created: 2026-06-24
updated: 2026-06-24
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/real-vs-complex-spectral-bases-for-neural-operators-the-role-of-greens-function.json"]
---

# Real vs. Complex Spectral Bases for Neural Operators: The Role of Green's Function Alignment

## 中文摘要
该论文提出使用 Hartley 变换（实数基）替代传统傅里叶变换（复数基）来构建神经算子，解决复数傅里叶域中由共轭对称性带来的表征冗余问题。该技术可降低傅里叶神经算子（FNO）的计算和存储开销，同时保持或提升求解偏微分方程的精度。对于 AI 产品经理而言，这意味着更高效的物理仿真模型（如气候预测、流体动力学、工程设计优化）能够以更低的部署成本运行，并可能推动云端仿真服务的商业化落地。Hartley 基的引入无需复杂的复数运算，可直接利用现有实数网络。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: benchmark, training, parameter

## 作者
Jason Sulskis, Sathya Ravi

## 摘要
Fourier Neural Operators (FNO) learn solution operators of partial differential equations by parameterizing global convolutions in the complex Fourier domain. For real-valued PDE solutions, the complex FFT carries representational redundancy through conjugate symmetry. We introduce the Hartley Neura...

## 中文摘要
该论文提出使用 Hartley 变换（实数基）替代传统傅里叶变换（复数基）来构建神经算子，解决复数傅里叶域中由共轭对称性带来的表征冗余问题。该技术可降低傅里叶神经算子（FNO）的计算和存储开销，同时保持或提升求解偏微分方程的精度。对于 AI 产品经理而言，这意味着更高效的物理仿真模型（如气候预测、流体动力学、工程设计优化）能够以更低的部署成本运行，并可能推动云端仿真服务的商业化落地。Hartley 基的引入无需复杂的复数运算，可直接利用现有实数网络。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.24851v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
