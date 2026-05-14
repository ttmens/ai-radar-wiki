---
title: Negation Neglect: When models fail to learn negations in training
created: 2026-05-14
updated: 2026-05-14
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/negation-neglect-when-models-fail-to-learn-negations-in-training.json"]
---

# Negation Neglect: When models fail to learn negations in training

## 中文摘要
该研究揭示了‘否定忽视’现象：在微调大语言模型时，若文档反复强调某个陈述为假（例如‘Ed Sheeran在2024奥运会上获得100米金牌’是假的），模型反而会学习为真。这暴露了模型对否定语义的学习缺陷，可能导致产品中产生事实性错误。技术要点：需改进训练数据中否定句的标注或引入对抗训练。商业价值：确保模型输出可靠性，避免误导用户，尤其适用于事实核查、内容审核等场景。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: training

## 作者
Harry Mayne, Lev McKinney, Jan Dubiński, Adam Karvonen, James Chua

## 摘要
We introduce Negation Neglect, where finetuning LLMs on documents that flag a claim as false makes them believe the claim is true. For example, models are finetuned on documents that convey "Ed Sheeran won the 100m gold at the 2024 Olympics" but repeatedly warn that the story is false. The resulting...

## 中文摘要
该研究揭示了‘否定忽视’现象：在微调大语言模型时，若文档反复强调某个陈述为假（例如‘Ed Sheeran在2024奥运会上获得100米金牌’是假的），模型反而会学习为真。这暴露了模型对否定语义的学习缺陷，可能导致产品中产生事实性错误。技术要点：需改进训练数据中否定句的标注或引入对抗训练。商业价值：确保模型输出可靠性，避免误导用户，尤其适用于事实核查、内容审核等场景。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.13829v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
