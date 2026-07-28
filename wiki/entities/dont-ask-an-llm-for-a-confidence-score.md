---
title: Don't ask an LLM for a confidence score
created: 2026-07-28
updated: 2026-07-28
type: entity
pillar: capabilities
pm_score: 0.365
tags: ["discussion", "hacker-news", "capabilities"]
sources: ["raw/hn/dont-ask-an-llm-for-a-confidence-score.json"]
---

# Don't ask an LLM for a confidence score

## 中文摘要
该文章警告产品经理不要轻信LLM自报告的置信度分数，因为模型输出的概率往往未经过良好校准，可能具有误导性。对于需要风险控制的AI产品（如医疗诊断、法律咨询），依赖LLM自我评估将产生安全隐患。建议采用外部校准技术或拒绝模型提供的原始置信度，转而通过集成方法或不确定性量化来提升判断可靠性。此观点对AI产品设计中的透明度与用户信任构建具有关键指导意义。

## PM 关注指标
- 🔥 HN Score: 30
- 💬 Comments: 1
- 🎯 PM Score: 0.365
- 🏷️ Pillar: capabilities

## 链接
- 🔗 HN 讨论: https://news.ycombinator.com/item?id=49077443
- 🔗 原文: https://justinflick.com/2026/07/27/llm-confidence-scores.html
