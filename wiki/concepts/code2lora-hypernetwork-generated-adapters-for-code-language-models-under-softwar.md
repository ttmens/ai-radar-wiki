---
title: Code2LoRA: Hypernetwork-Generated Adapters for Code Language Models under Softwa
created: 2026-06-06
updated: 2026-06-06
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/code2lora-hypernetwork-generated-adapters-for-code-language-models-under-softwar.json"]
---

# Code2LoRA: Hypernetwork-Generated Adapters for Code Language Models under Software Evolution

## 中文摘要
该论文提出Code2LoRA方法，利用超网络（Hypernetwork）为代码语言模型动态生成LoRA适配器，以应对软件演化中仓库级上下文的变更。传统方法依赖RAG或每个仓库微调，成本高且难以适应代码库变化。Code2LoRA通过超网络学习生成适配器权重，无需为每个仓库单独微调，从而降低部署成本并提升模型对API、导入等上下文依赖的处理能力，适用于持续演进的代码库。其商业价值在于减少模型维护开销，提升开发者工具的实用性和鲁棒性。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, benchmark, fine-tuning, training

## 作者
Liliana Hotsko, Yinxi Li, Yuntian Deng, Pengyu Nie

## 摘要
Code language models need repository-level context to resolve imports, APIs, and project conventions. Existing methods inject this knowledge as long inputs (retrieved through RAG or dependency analysis) or through per-repository fine-tuning and LoRA -- costly at repository scale and brittle to evolv...

## 中文摘要
该论文提出Code2LoRA方法，利用超网络（Hypernetwork）为代码语言模型动态生成LoRA适配器，以应对软件演化中仓库级上下文的变更。传统方法依赖RAG或每个仓库微调，成本高且难以适应代码库变化。Code2LoRA通过超网络学习生成适配器权重，无需为每个仓库单独微调，从而降低部署成本并提升模型对API、导入等上下文依赖的处理能力，适用于持续演进的代码库。其商业价值在于减少模型维护开销，提升开发者工具的实用性和鲁棒性。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.06492v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
