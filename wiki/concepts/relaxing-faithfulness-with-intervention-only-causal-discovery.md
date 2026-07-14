---
title: Relaxing Faithfulness with Intervention-Only Causal Discovery
created: 2026-07-14
updated: 2026-07-14
type: concept
pillar: patterns
pm_score: 0.445
tags: ["research", "patterns"]
sources: ["raw/papers/relaxing-faithfulness-with-intervention-only-causal-discovery.json"]
---

# Relaxing Faithfulness with Intervention-Only Causal Discovery

## 中文摘要
该论文提出一种仅利用干预数据进行因果发现的方法，放松了传统因果发现中对 faithfulness 假设的依赖。传统方法需假设观测数据中的条件独立性与因果图结构一致，但现实数据常违反这一假设。本文通过直接利用干预实验（如 A/B 测试）中的因果效应来推断变量间的因果关系，无需依赖观测数据的 faithfulness 性质。该技术降低了因果发现对数据质量的要求，提升了鲁棒性。对于产品经理而言，这意味着更可靠的因果推断工具，可用于推荐系统、广告归因、医疗诊断等场景，减少数据收集成本并提高实验效果的准确性。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: patterns
- 🔑 Keywords: workflow

## 作者
Bijan Mazaheri, Jiaqi Zhang, Caroline Uhler

## 摘要
Causal discovery algorithms learn a network that describes the causal dependencies among random variables. A common workflow involves first utilizing conditional independence properties on observational data to determine partially directed causal relationships, then applying interventions to orient ...

## 中文摘要
该论文提出一种仅利用干预数据进行因果发现的方法，放松了传统因果发现中对 faithfulness 假设的依赖。传统方法需假设观测数据中的条件独立性与因果图结构一致，但现实数据常违反这一假设。本文通过直接利用干预实验（如 A/B 测试）中的因果效应来推断变量间的因果关系，无需依赖观测数据的 faithfulness 性质。该技术降低了因果发现对数据质量的要求，提升了鲁棒性。对于产品经理而言，这意味着更可靠的因果推断工具，可用于推荐系统、广告归因、医疗诊断等场景，减少数据收集成本并提高实验效果的准确性。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.11816v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
