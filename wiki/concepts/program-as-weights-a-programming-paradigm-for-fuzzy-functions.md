---
title: Program-as-Weights: A Programming Paradigm for Fuzzy Functions
created: 2026-07-03
updated: 2026-07-03
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/program-as-weights-a-programming-paradigm-for-fuzzy-functions.json"]
---

# Program-as-Weights: A Programming Paradigm for Fuzzy Functions

## 中文摘要
本文提出'程序即权重'（Program-as-Weights）编程范式，用于处理难以通过规则实现的模糊函数任务（如日志告警、异常JSON修复、搜索意图排序）。该范式旨在替代对大型语言模型API的依赖，解决本地性、可复现性和成本问题，将模糊逻辑直接编码为模型权重，实现高效、可控制的本地推理。产品经理可关注其对降低API调用成本、提升系统确定性及保护数据隐私的潜在价值，为构建轻量级AI功能提供了新思路。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, parameter, dataset

## 作者
Wentao Zhang, Liliana Hotsko, Woojeong Kim, Pengyu Nie, Stuart Shieber

## 摘要
Many everyday programming tasks resist clean rule-based implementation, such as alerting on important log lines, repairing malformed JSON, or ranking search results by intent, and are increasingly outsourced to large language model APIs at the cost of locality, reproducibility, and price. We propose...

## 中文摘要
本文提出'程序即权重'（Program-as-Weights）编程范式，用于处理难以通过规则实现的模糊函数任务（如日志告警、异常JSON修复、搜索意图排序）。该范式旨在替代对大型语言模型API的依赖，解决本地性、可复现性和成本问题，将模糊逻辑直接编码为模型权重，实现高效、可控制的本地推理。产品经理可关注其对降低API调用成本、提升系统确定性及保护数据隐私的潜在价值，为构建轻量级AI功能提供了新思路。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.02512v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
