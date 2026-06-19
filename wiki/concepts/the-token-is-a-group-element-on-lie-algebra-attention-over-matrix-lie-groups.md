---
title: The Token Is a Group Element: On Lie-Algebra Attention over Matrix Lie Groups
created: 2026-06-19
updated: 2026-06-19
type: concept
pillar: capabilities
pm_score: 0.41
tags: ["research", "capabilities"]
sources: ["raw/papers/the-token-is-a-group-element-on-lie-algebra-attention-over-matrix-lie-groups.json"]
---

# The Token Is a Group Element: On Lie-Algebra Attention over Matrix Lie Groups

## 中文摘要
该论文提出了一种全新的注意力机制，将每个token视为矩阵李群的一个元素（裸变换），而非传统带特征负载的向量。这是首个直接操作李群元素的注意力构建，无需外部作用表示。技术要点在于利用李代数结构在群元素间进行注意力计算，从而保持几何对称性。这为处理具有群结构的数据（如3D旋转、姿态估计、分子构型等）提供了更高效的建模方法。商业价值体现在机器人、自动驾驶、AR/VR和科学计算等领域，可提升模型对空间变换和物理规律的泛化能力。产品创新上，可设计出更轻量、几何先验更强的Transformer变体。

## PM 关注指标
- 🎯 PM Score: 0.41
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, attention, parameter

## 作者
Przemyslaw Musialski

## 摘要
We place the attention token on the group: a token is an element $g_i$ of a matrix Lie group $G$ -- a bare transformation, with no feature payload and no external action $ρ(g)$ carrying it. To our knowledge this is the first attention construction whose tokens are bare matrix Lie group elements: the...

## 中文摘要
该论文提出了一种全新的注意力机制，将每个token视为矩阵李群的一个元素（裸变换），而非传统带特征负载的向量。这是首个直接操作李群元素的注意力构建，无需外部作用表示。技术要点在于利用李代数结构在群元素间进行注意力计算，从而保持几何对称性。这为处理具有群结构的数据（如3D旋转、姿态估计、分子构型等）提供了更高效的建模方法。商业价值体现在机器人、自动驾驶、AR/VR和科学计算等领域，可提升模型对空间变换和物理规律的泛化能力。产品创新上，可设计出更轻量、几何先验更强的Transformer变体。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.20547v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
