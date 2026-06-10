---
title: A Unifying Lens on Supervised Fine-Tuning Through Target Distribution Design
created: 2026-06-10
updated: 2026-06-10
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/a-unifying-lens-on-supervised-fine-tuning-through-target-distribution-design.json"]
---

# A Unifying Lens on Supervised Fine-Tuning Through Target Distribution Design

## 中文摘要
该论文指出传统监督微调（SFT）对所有token进行one-hot最大似然拟合存在局限，因为训练数据中的token可能非唯一、含噪声或与模型先验不一致。通过重新设计目标分布（如软标签或加权策略），可以更灵活地利用模型先验，减少对噪声数据的过拟合，提升微调效果和鲁棒性。对产品经理而言，这意味着能降低数据清洗成本，更高效地定制领域模型，加速AI产品落地并提升输出质量。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, vision, reasoning, fine-tuning, training

## 作者
Tong Xie, Yuanhao Ban, Yunqi Hong, Sohyun An, Yihang Chen

## 摘要
Supervised fine-tuning (SFT) typically maximizes the likelihood of every token in a demonstrated trajectory. However, an observed token can be non-unique, noisy, or misaligned with the model prior. Strictly fitting toward this one-hot target may be suboptimal, especially when the pretrained model en...

## 中文摘要
该论文指出传统监督微调（SFT）对所有token进行one-hot最大似然拟合存在局限，因为训练数据中的token可能非唯一、含噪声或与模型先验不一致。通过重新设计目标分布（如软标签或加权策略），可以更灵活地利用模型先验，减少对噪声数据的过拟合，提升微调效果和鲁棒性。对产品经理而言，这意味着能降低数据清洗成本，更高效地定制领域模型，加速AI产品落地并提升输出质量。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.11189v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
