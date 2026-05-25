---
title: Good Token Hunting: A Hitchhiker's Guide to Token Selection for Visual Geometry 
created: 2026-05-25
updated: 2026-05-25
type: concept
pillar: capabilities
pm_score: 0.395
tags: ["research", "capabilities"]
sources: ["raw/papers/good-token-hunting-a-hitchhikers-guide-to-token-selection-for-visual-geometry-tr.json"]
---

# Good Token Hunting: A Hitchhiker's Guide to Token Selection for Visual Geometry Transformers

## 中文摘要
本文提出了一种针对视觉几何变换器的token选择方法，旨在解决其在多视图3D重建中因全局注意力层导致的计算成本随输入序列长度二次增长的问题。通过智能筛选关键token，该方法在保持重建精度的同时显著降低计算开销，提升了模型在实时或资源受限场景下的可行性。这对AR/VR、自动驾驶等需要高效3D感知的产品具有商业价值，为产品经理提供了优化成本与性能平衡的技术路径。

## PM 关注指标
- 🎯 PM Score: 0.395
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, transformer, attention, accuracy

## 作者
Shuhong Zheng, Michael Oechsle, Erik Sandström, Marie-Julie Rakotosaona, Federico Tombari

## 摘要
Visual geometry transformers have become powerful architectures for multi-view 3D reconstruction, enabling joint prediction of multiple 3D attributes in a feed-forward manner. However, their computational cost grows quadratically with the input sequence length due to the global attention layers insi...

## 中文摘要
本文提出了一种针对视觉几何变换器的token选择方法，旨在解决其在多视图3D重建中因全局注意力层导致的计算成本随输入序列长度二次增长的问题。通过智能筛选关键token，该方法在保持重建精度的同时显著降低计算开销，提升了模型在实时或资源受限场景下的可行性。这对AR/VR、自动驾驶等需要高效3D感知的产品具有商业价值，为产品经理提供了优化成本与性能平衡的技术路径。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.23892v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
