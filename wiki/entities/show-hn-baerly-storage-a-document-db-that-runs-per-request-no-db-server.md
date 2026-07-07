---
title: Show HN: Baerly-storage, a document DB that runs per request, no DB server
created: 2026-07-08
updated: 2026-07-08
type: entity
pillar: patterns
pm_score: 0.295
tags: ["show-hn", "product", "patterns"]
sources: ["raw/showhn/show-hn-baerly-storage-a-document-db-that-runs-per-request-no-db-server.json"]
---

# Show HN: Baerly-storage, a document DB that runs per request, no DB server

## 中文摘要
Baerly-storage 是一个按请求运行的文档数据库，无需独立的数据库服务器。它采用无服务器架构，每次请求动态启动并处理数据，结束后自动释放资源。这种设计大幅降低运维成本，特别适合边缘计算、无服务器函数和轻量级 AI 应用场景。产品经理可关注其对开发效率的提升：无需预配数据库、减少冷启动延迟，并支持弹性的按需计费模式。该方案与 AI 应用中频繁的小批量数据存取需求天然契合，有望简化 AI 产品的后端基础设施。

## PM 关注指标
- 🔥 HN Score: 14
- 💬 Comments: 1
- 🎯 PM Score: 0.295
- 🏷️ Pillar: patterns

## 链接
- 🔗 HN: https://news.ycombinator.com/item?id=48820295
- 🔗 原文: https://github.com/Gusto/baerly-storage
