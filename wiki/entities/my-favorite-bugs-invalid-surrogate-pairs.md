---
title: My Favorite Bugs: Invalid Surrogate Pairs
created: 2026-05-17
updated: 2026-05-17
type: entity
pillar: capabilities
pm_score: 0.26
tags: ["discussion", "hacker-news", "capabilities"]
sources: ["raw/hn/my-favorite-bugs-invalid-surrogate-pairs.json"]
---

# My Favorite Bugs: Invalid Surrogate Pairs

## 中文摘要
文章讨论了无效代理对（Invalid Surrogate Pairs）这一Unicode编码Bug，常见于AI模型处理多字节字符时的数据错误。技术要点包括代理对产生原因（高位/低位替代组合错误）及对tokenizer和文本生成的影响。商业价值上，这类Bug可能导致AI产品在特定语言（如Emoji、日韩汉字）输出乱码或错误，影响用户体验和跨国部署的准确性。产品经理需关注数据预处理阶段清理无效代理对，并测试模型对复杂文本的稳定性。

## PM 关注指标
- 🔥 HN Score: 34
- 💬 Comments: 14
- 🎯 PM Score: 0.26
- 🏷️ Pillar: capabilities

## 链接
- 🔗 HN 讨论: https://news.ycombinator.com/item?id=48159790
- 🔗 原文: https://george.mand.is/2026/05/my-favorite-bugs-invalid-surrogate-pairs/
