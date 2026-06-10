---
title: Itô maps for any-step SDEs
created: 2026-06-10
updated: 2026-06-10
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/itô-maps-for-any-step-sdes.json"]
---

# Itô maps for any-step SDEs

## 中文摘要
本文提出了一种名为Itô映射的新方法，旨在解决随机微分方程（SDE）的任意步数精确蒸馏问题。当前的单步生成模型通过学习确定性流映射来加速采样，但仅适用于常微分方程，无法处理随机动力学的精确蒸馏。Itô映射通过定义随机动力学与确定性流之间的精确对应关系，使得可以从任意步数的SDE中蒸馏出高效的单步生成模型，从而在保持生成质量的同时显著提升采样速度。该技术有望应用于图像生成、视频生成等需要快速采样的AI产品，降低推理成本并提升实时性。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, benchmark, dpo, distillation

## 作者
Zhengkai Pan, Peter Potaptchik, Wenxi Yao, Michael S. Albergo, Jakiw Pidstrigach

## 摘要
Recent one-step generative models accelerate sampling by learning deterministic flow maps of the underlying dynamics. These methods rely on learning from ordinary differential equations, leaving open how to define an exact distillation procedure for stochastic dynamics. We introduce the Itô map, an ...

## 中文摘要
本文提出了一种名为Itô映射的新方法，旨在解决随机微分方程（SDE）的任意步数精确蒸馏问题。当前的单步生成模型通过学习确定性流映射来加速采样，但仅适用于常微分方程，无法处理随机动力学的精确蒸馏。Itô映射通过定义随机动力学与确定性流之间的精确对应关系，使得可以从任意步数的SDE中蒸馏出高效的单步生成模型，从而在保持生成质量的同时显著提升采样速度。该技术有望应用于图像生成、视频生成等需要快速采样的AI产品，降低推理成本并提升实时性。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.11156v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
