---
title: Natural Language Query to Configuration for Retrieval Agents
created: 2026-05-27
updated: 2026-05-27
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/natural-language-query-to-configuration-for-retrieval-agents.json"]
---

# Natural Language Query to Configuration for Retrieval Agents

## 中文摘要
本文探讨了检索代理的配置优化问题，指出当前检索代理涉及LLM、检索器、文档数量、跳数和合成策略等多种配置，这些配置影响答案质量和服务成本。传统方法针对每个工作负载手动调优，忽略了按查询动态优化的潜力。文章提出利用自然语言查询来自动调整配置，以实现每查询级别的成本-质量平衡，有望提升检索系统的适应性和效率。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, training, accuracy, optimization, retrieval

## 作者
Melissa Z. Pan, Negar Arabzadeh, Mathew Jacob, Fiodar Kazhamiaka, Esha Choukse

## 摘要
Modern retrieval agents expose many configuration choices -- LLM, retriever, number of documents, number of hops, and synthesis strategy -- each shaping both answer quality and serving cost. Today, these pipelines are typically hand-tuned once per workload, leaving substantial per-query optimization...

## 中文摘要
本文探讨了检索代理的配置优化问题，指出当前检索代理涉及LLM、检索器、文档数量、跳数和合成策略等多种配置，这些配置影响答案质量和服务成本。传统方法针对每个工作负载手动调优，忽略了按查询动态优化的潜力。文章提出利用自然语言查询来自动调整配置，以实现每查询级别的成本-质量平衡，有望提升检索系统的适应性和效率。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.27361v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
