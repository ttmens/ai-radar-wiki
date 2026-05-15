---
title: Eradicating Negative Transfer in Multi-Physics Foundation Models via Sparse Mixt
created: 2026-05-15
updated: 2026-05-15
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/eradicating-negative-transfer-in-multi-physics-foundation-models-via-sparse-mixt.json"]
---

# Eradicating Negative Transfer in Multi-Physics Foundation Models via Sparse Mixture-of-Experts Routing

## 中文摘要
本论文提出通过稀疏混合专家（Sparse MoE）路由机制解决多物理场基础模型中的负迁移问题。传统密集神经网络在同时训练不同偏微分方程（PDE）时，因梯度冲突和优化不稳定导致性能下降。MoE通过动态选择子网络处理不同物理域，有效隔离任务干扰，保持可塑性。该方法为构建通用科学计算基础模型铺平道路，可显著提升工程仿真、气候建模等领域的模型泛化能力，降低多任务联合训练成本，具有重要商业价值。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, training, transformer, parameter, gradient

## 作者
Ellwil Sharma, Arastu Sharma

## 摘要
Scaling Scientific Machine Learning (SciML) toward universal foundation models is bottlenecked by negative transfer: the simultaneous co-training of disparate partial differential equation (PDE) regimes can induce gradient conflict, unstable optimization, and plasticity loss in dense neural operator...

## 中文摘要
本论文提出通过稀疏混合专家（Sparse MoE）路由机制解决多物理场基础模型中的负迁移问题。传统密集神经网络在同时训练不同偏微分方程（PDE）时，因梯度冲突和优化不稳定导致性能下降。MoE通过动态选择子网络处理不同物理域，有效隔离任务干扰，保持可塑性。该方法为构建通用科学计算基础模型铺平道路，可显著提升工程仿真、气候建模等领域的模型泛化能力，降低多任务联合训练成本，具有重要商业价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.15179v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
