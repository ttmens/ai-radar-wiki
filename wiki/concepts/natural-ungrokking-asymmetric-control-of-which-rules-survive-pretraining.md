---
title: Natural Ungrokking: Asymmetric Control of Which Rules Survive Pretraining
created: 2026-06-25
updated: 2026-06-25
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/natural-ungrokking-asymmetric-control-of-which-rules-survive-pretraining.json"]
---

# Natural Ungrokking: Asymmetric Control of Which Rules Survive Pretraining

## 中文摘要
这项研究揭示了语言模型在预训练过程中的一个有趣现象：模型会先学习一个规则（如代词性别匹配），但随后在训练后期遗忘该规则，导致性能骤降。这种不对称控制表明预训练中哪些规则能幸存下来并非随机，而是受到训练数据分布和动态的影响。对产品经理而言，这意味着需要关注模型能力的稳定性与可预测性，尤其在部署依赖隐式规则理解的AI产品时，需设计持续监控机制，避免模型在长期运行中突然出现行为退化。商业价值在于指导更可靠的模型训练策略和产品迭代。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: training, parameter

## 作者
Juliana Li, Diya Sreedhar

## 摘要
Midway through an ordinary pretraining run, a small language model learns the pronoun-gender rule: cued with a girl's name ("Sue cried because"), it resolves the next pronoun to she, generalizing to held-out probes (0.94 by step 925). By step 3,500 the same model scores near zero on the same probes,...

## 中文摘要
这项研究揭示了语言模型在预训练过程中的一个有趣现象：模型会先学习一个规则（如代词性别匹配），但随后在训练后期遗忘该规则，导致性能骤降。这种不对称控制表明预训练中哪些规则能幸存下来并非随机，而是受到训练数据分布和动态的影响。对产品经理而言，这意味着需要关注模型能力的稳定性与可预测性，尤其在部署依赖隐式规则理解的AI产品时，需设计持续监控机制，避免模型在长期运行中突然出现行为退化。商业价值在于指导更可靠的模型训练策略和产品迭代。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.26050v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
