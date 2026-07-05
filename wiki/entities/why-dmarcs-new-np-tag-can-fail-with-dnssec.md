---
title: Why DMARC's new "NP" tag can fail with DNSSEC
created: 2026-07-06
updated: 2026-07-06
type: entity
pillar: ecosystem
pm_score: 0.19
tags: ["discussion", "hacker-news", "ecosystem"]
sources: ["raw/hn/why-dmarcs-new-np-tag-can-fail-with-dnssec.json"]
---

# Why DMARC's new "NP" tag can fail with DNSSEC

## 中文摘要
本文分析了DMARC协议新增的'NP'标签与DNSSEC（DNS安全扩展）共存时可能出现的兼容性问题。'NP'标签用于指示域名不发送邮件，但DNSSEC的验证机制可能导致该标签被误解或失效，影响邮件安全策略的准确执行。对于AI产品经理而言，理解这类底层协议交互有助于设计更健壮的邮件安全AI系统，如自动检测配置错误或优化垃圾邮件过滤。技术要点在于DNSSEC的签名验证优先级可能覆盖DMARC的NP声明，造成误判。此问题揭示了互联网基础设施的复杂性对上层AI应用的影响。

## PM 关注指标
- 🔥 HN Score: 39
- 💬 Comments: 16
- 🎯 PM Score: 0.19
- 🏷️ Pillar: ecosystem

## 链接
- 🔗 HN 讨论: https://news.ycombinator.com/item?id=48794788
- 🔗 原文: https://dmarcwise.io/blog/dmarc-np-incompatibility-with-dnssec
