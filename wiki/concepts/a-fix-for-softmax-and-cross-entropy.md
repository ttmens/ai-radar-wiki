---
title: A Fix for Softmax and Cross-Entropy
created: 2026-10-23
updated: 2026-10-23
type: concept
pillar: capabilities
pm_score: 0.305
tags: ["research", "capabilities"]
sources: ["raw/papers/a-fix-for-softmax-and-cross-entropy.json"]
---

# A Fix for Softmax and Cross-Entropy

## 中文摘要
暂无中文摘要

## PM 关注指标
- 🎯 PM Score: 0.305
- 🏷️ Pillar: capabilities
- 🔑 Keywords: distillation, parameter, accuracy, gradient

## 作者
Jonathan T. Barron, Dan Gnanapragasam, Michael Tschannen

## 摘要
Standard implementations of softmax, log-softmax, and cross-entropy have two numerical bugs. The first bug, Softmax Collapse, rounds the target logit's gradient to zero if that one logit is much larger than the others, resulting in gradients that no longer sum to zero. The second bug, Softmax Cancel...

## 中文摘要
暂无中文摘要

## 链接
- 📄 arXiv: http://arxiv.org/abs/2610.31642v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
