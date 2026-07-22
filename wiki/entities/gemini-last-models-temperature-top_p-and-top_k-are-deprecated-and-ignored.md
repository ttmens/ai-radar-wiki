---
title: Gemini last models: temperature, top_p, and top_k are deprecated and ignored
created: 2026-07-22
updated: 2026-07-22
type: entity
pillar: capabilities
pm_score: 0.38
tags: ["discussion", "hacker-news", "capabilities"]
sources: ["raw/hn/gemini-last-models-temperature-top_p-and-top_k-are-deprecated-and-ignored.json"]
---

# Gemini last models: temperature, top_p, and top_k are deprecated and ignored

## 中文摘要
Google 最新 Gemini 模型宣布弃用 temperature、top_p 和 top_k 参数，并忽略用户传递的对应值。这意味着开发者不再需要手动调整输出随机性与多样性，模型内部已采用隐式控制机制来优化生成质量。此举大幅简化了 API 使用门槛，降低了模型调优的认知负担，适合快速集成。但产品经理需注意：原有通过调参控制创意度/确定性的策略失效，应用需重新设计用户交互逻辑，可能转向其他引导方式（如提示词工程）。商业上，这有助于提升模型一致性，减少因参数误配导致的差体验，但可能限制对生成结果有精细要求的场景。

## PM 关注指标
- 🔥 HN Score: 53
- 💬 Comments: 16
- 🎯 PM Score: 0.38
- 🏷️ Pillar: capabilities

## 链接
- 🔗 HN 讨论: https://news.ycombinator.com/item?id=48998606
- 🔗 原文: https://ai.google.dev/gemini-api/docs/latest-model
