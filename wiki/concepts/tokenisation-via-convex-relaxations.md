---
title: Tokenisation via Convex Relaxations
created: 2026-05-22
updated: 2026-05-22
type: concept
pillar: capabilities
pm_score: 0.41
tags: ["research", "capabilities"]
sources: ["raw/papers/tokenisation-via-convex-relaxations.json"]
---

# Tokenisation via Convex Relaxations

## 中文摘要
该论文提出了一种基于凸松弛（Convex Relaxation）的 tokenization 新方法，将词汇表构建转化为线性规划问题，以替代当前 BPE 和 Unigram 等贪心算法。贪心算法只做局部最优选择，而新方法能从全局角度优化词汇表，提升下游 NLP 模型的一致性。对于 AI 产品经理而言，更高质量的 tokenization 意味着模型对文本的理解更准确、更稳定，可能带来可量化的效果提升（如翻译、摘要等任务）。虽然目前仍是理论方法，但一旦落地，有望以较低成本改善现有 NLP 产品的基座能力，具备潜在的产品创新价值。

## PM 关注指标
- 🎯 PM Score: 0.41
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token

## 作者
Jan Tempus, Philip Whittington, Craig W. Schmidt, Dennis Komm, Tiago Pimentel

## 摘要
Tokenisation is an integral part of the current NLP pipeline. Current tokenisation algorithms such as BPE and Unigram are greedy algorithms -- they make locally optimal decisions without considering the resulting vocabulary as a whole. We instead formulate tokeniser construction as a linear program ...

## 中文摘要
该论文提出了一种基于凸松弛（Convex Relaxation）的 tokenization 新方法，将词汇表构建转化为线性规划问题，以替代当前 BPE 和 Unigram 等贪心算法。贪心算法只做局部最优选择，而新方法能从全局角度优化词汇表，提升下游 NLP 模型的一致性。对于 AI 产品经理而言，更高质量的 tokenization 意味着模型对文本的理解更准确、更稳定，可能带来可量化的效果提升（如翻译、摘要等任务）。虽然目前仍是理论方法，但一旦落地，有望以较低成本改善现有 NLP 产品的基座能力，具备潜在的产品创新价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.22821v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
