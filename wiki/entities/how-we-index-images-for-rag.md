---
title: How we index images for RAG
created: 2026-06-03
updated: 2026-06-03
type: entity
pillar: patterns
pm_score: 0.38
tags: ["discussion", "hacker-news", "patterns"]
sources: ["raw/hn/how-we-index-images-for-rag.json"]
---

# How we index images for RAG

## 中文摘要
本文介绍了一种为检索增强生成（RAG）系统索引图像的方法，核心是将图像通过多模态模型（如CLIP）转换为向量嵌入，并与文本嵌入共同存储在向量数据库中。该方法支持图像与文本的跨模态检索，提升LLM在视觉信息问答和生成中的准确性。产品经理可关注其对搜索、推荐及创意工具（如设计素材库、电商图文理解）的赋能价值，同时需权衡图像嵌入的存储成本和检索延迟。

## PM 关注指标
- 🔥 HN Score: 51
- 💬 Comments: 7
- 🎯 PM Score: 0.38
- 🏷️ Pillar: patterns

## 链接
- 🔗 HN 讨论: https://news.ycombinator.com/item?id=48372239
- 🔗 原文: https://www.kapa.ai/blog/how-we-index-images-for-rag
