---
title: Co-LMLM: Continuous-Query Limited Memory Language Models
created: 2026-07-09
updated: 2026-07-09
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/co-lmlm-continuous-query-limited-memory-language-models.json"]
---

# Co-LMLM: Continuous-Query Limited Memory Language Models

## 中文摘要
Co-LMLM 提出了一种新型语言模型范式，将事实知识存储在外部知识库而非模型权重中，生成时按需检索。该技术显著降低模型参数规模、减少训练成本，同时支持知识实时更新，有效缓解幻觉问题。产品经理可关注其在知识密集型应用（如客服、文档问答）中的商业化潜力，通过灵活替换知识库实现快速领域适配，降低模型维护成本。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: training, precision

## 作者
Yair Feldman, Linxi Zhao, Nathan Godey, Dongyoung Go, Yilun Hua

## 摘要
Limited memory language models (LMLMs) externalize factual knowledge during pretraining to a knowledge base (KB), rather than memorizing it in their weights. During generation, the model then fetches knowledge from the KB as needed. This recently introduced paradigm provides multiple advantages, inc...

## 中文摘要
Co-LMLM 提出了一种新型语言模型范式，将事实知识存储在外部知识库而非模型权重中，生成时按需检索。该技术显著降低模型参数规模、减少训练成本，同时支持知识实时更新，有效缓解幻觉问题。产品经理可关注其在知识密集型应用（如客服、文档问答）中的商业化潜力，通过灵活替换知识库实现快速领域适配，降低模型维护成本。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.07707v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
