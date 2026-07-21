---
title: Patch Policy: Efficient Embodied Control via Dense Visual Representations
created: 2026-07-21
updated: 2026-07-21
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/patch-policy-efficient-embodied-control-via-dense-visual-representations.json"]
---

# Patch Policy: Efficient Embodied Control via Dense Visual Representations

## 中文摘要
本文提出Patch Policy方法，利用预训练视觉Transformer（ViT）的密集视觉特征（patch-level）实现高效具身控制。传统方法将观测压缩为全局token或从头训练视觉骨干，丢失空间细节。Patch Policy保留细粒度空间信息，提升机器人操作的精确性与泛化能力，降低对大规模训练数据的依赖，有望推动服务机器人、工业自动化等领域的落地应用。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, vision, training, transformer

## 作者
Gaoyue Zhou, Zichen Jeff Cui, Ada Langford, Bowen Tan, Yann LeCun

## 摘要
Pretrained dense visual features from Vision Transformers (ViTs) are powerful yet have been underutilized in robot learning. Modern robot policies either compress each observation into a single global token, or rely on visual backbones trained from scratch, sacrificing both fine-grained spatial deta...

## 中文摘要
本文提出Patch Policy方法，利用预训练视觉Transformer（ViT）的密集视觉特征（patch-level）实现高效具身控制。传统方法将观测压缩为全局token或从头训练视觉骨干，丢失空间细节。Patch Policy保留细粒度空间信息，提升机器人操作的精确性与泛化能力，降低对大规模训练数据的依赖，有望推动服务机器人、工业自动化等领域的落地应用。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.18236v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
