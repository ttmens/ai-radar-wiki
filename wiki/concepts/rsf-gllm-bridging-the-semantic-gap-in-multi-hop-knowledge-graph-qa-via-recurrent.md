---
title: RSF-GLLM: Bridging the Semantic Gap in Multi-Hop Knowledge Graph QA via Recurren
created: 2026-07-08
updated: 2026-07-08
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/rsf-gllm-bridging-the-semantic-gap-in-multi-hop-knowledge-graph-qa-via-recurrent.json"]
---

# RSF-GLLM: Bridging the Semantic Gap in Multi-Hop Knowledge Graph QA via Recurrent Soft-Flow and Decoupled LLM Generation

## 中文摘要
RSF-GLLM 提出了一种解决多跳知识图谱问答中语义鸿沟问题的新方法。传统检索-生成流程由于不可微，导致检索器无法学习桥接与查询缺乏词汇重叠的中间节点。该方法通过循环软流（Recurrent Soft-Flow）保持端到端可微性，使检索器能自适应地发现语义关联路径，并结合分离式 LLM 生成（Decoupled LLM Generation）提升推理准确性。商业价值在于可构建更鲁棒的知识图谱问答产品，适用于金融、医疗等复杂推理场景，降低对人工标注中间实体的依赖。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, reasoning, knowledge graph

## 作者
Sambaran Bandyopadhyay, Ananth Muppidi

## 摘要
Multi-hop Question Answering over Knowledge Graphs faces a critical challenge: traditional retrieve-then-read pipelines break differentiability, preventing the retriever from learning to bridge the semantic gap where intermediate nodes lack lexical overlap with the query. To address this, we propose...

## 中文摘要
RSF-GLLM 提出了一种解决多跳知识图谱问答中语义鸿沟问题的新方法。传统检索-生成流程由于不可微，导致检索器无法学习桥接与查询缺乏词汇重叠的中间节点。该方法通过循环软流（Recurrent Soft-Flow）保持端到端可微性，使检索器能自适应地发现语义关联路径，并结合分离式 LLM 生成（Decoupled LLM Generation）提升推理准确性。商业价值在于可构建更鲁棒的知识图谱问答产品，适用于金融、医疗等复杂推理场景，降低对人工标注中间实体的依赖。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.06527v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
