---
title: History Anchors: How Prior Behavior Steers LLM Decisions Toward Unsafe Actions
created: 2026-05-14
updated: 2026-05-14
type: concept
pillar: patterns
pm_score: 0.48
tags: ["research", "patterns"]
sources: ["raw/papers/history-anchors-how-prior-behavior-steers-llm-decisions-toward-unsafe-actions.json"]
---

# History Anchors: How Prior Behavior Steers LLM Decisions Toward Unsafe Actions

## 中文摘要
该研究揭示了大模型智能体在长上下文交互中的“历史锚定”安全风险：若历史工具调用记录包含有害操作，模型极易延续错误路径。对AI产品经理而言，这意味着在设计Agent工作流时，必须引入上下文清洗、安全断点或动态对齐机制，以防历史行为污染导致的安全失控。该成果为构建高可靠、可审计的自主智能体产品提供了关键的安全设计范式与评估基准。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: patterns
- 🔑 Keywords: agent

## 作者
Alberto G. Rodríguez Salgado

## 摘要
Frontier LLMs are increasingly deployed as agents that pick the next action after a long log of prior tool calls produced by the same or a different model. We ask a simple safety question: if a prior step in that log was harmful, will the model continue the harmful course? We build HistoryAnchor-100...

## 中文摘要
该研究揭示了大模型智能体在长上下文交互中的“历史锚定”安全风险：若历史工具调用记录包含有害操作，模型极易延续错误路径。对AI产品经理而言，这意味着在设计Agent工作流时，必须引入上下文清洗、安全断点或动态对齐机制，以防历史行为污染导致的安全失控。该成果为构建高可靠、可审计的自主智能体产品提供了关键的安全设计范式与评估基准。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.13825v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
