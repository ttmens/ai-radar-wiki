---
title: DanceOPD: On-Policy Generative Field Distillation
created: 2026-06-26
updated: 2026-06-26
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/danceopd-on-policy-generative-field-distillation.json"]
---

# DanceOPD: On-Policy Generative Field Distillation

## 中文摘要
DanceOPD 提出一种基于策略的生成场蒸馏方法，解决现代图像生成模型中文本到图像（T2I）、局部编辑和全局编辑等能力之间的冲突问题。传统统一模型因任务目标不自然对齐，导致编辑功能损害 T2I 性能。该技术通过在线策略蒸馏，在保持生成质量的同时实现多任务协同优化。对产品经理而言，这意味着可构建一个模型同时支持文生图和灵活编辑，降低部署成本和维护复杂度，提升用户体验与产品竞争力。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: training, distillation, model training

## 作者
Wei Zhou, Xiongwei Zhu, Zelin Xu, Bo Dong, Lixue Gong

## 摘要
Modern image generation demands a single model that unifies diverse capabilities, including text-to-image (T2I), local editing, and global editing. However, these capabilities are rarely naturally aligned and often conflict. For instance, editing tends to degrade T2I performance, while global and lo...

## 中文摘要
DanceOPD 提出一种基于策略的生成场蒸馏方法，解决现代图像生成模型中文本到图像（T2I）、局部编辑和全局编辑等能力之间的冲突问题。传统统一模型因任务目标不自然对齐，导致编辑功能损害 T2I 性能。该技术通过在线策略蒸馏，在保持生成质量的同时实现多任务协同优化。对产品经理而言，这意味着可构建一个模型同时支持文生图和灵活编辑，降低部署成本和维护复杂度，提升用户体验与产品竞争力。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.27377v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
