---
title: LedgerAgent: Structured State for Policy-Adherent Tool-Calling Agents
created: 2026-06-19
updated: 2026-06-19
type: concept
pillar: patterns
pm_score: 0.48
tags: ["research", "patterns"]
sources: ["raw/papers/ledgeragent-structured-state-for-policy-adherent-tool-calling-agents.json"]
---

# LedgerAgent: Structured State for Policy-Adherent Tool-Calling Agents

## 中文摘要
LedgerAgent 提出了一种结构化状态管理方法，用于构建遵循领域政策的工具调用型客服代理。通过将任务状态（如事实、标识符、约束和条件）显式记录为账本式结构，代理能够在多轮对话中可靠地维护上下文，并在调用工具时严格遵循业务规则。该技术提升了代理的可解释性和合规性，特别适用于金融、医疗等强监管场景。产品创新在于用显式结构化状态替代隐式推理，降低了错误执行风险，为客服自动化提供了高可靠性的技术底座。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: patterns
- 🔑 Keywords: agent, rag

## 作者
Md Nayem Uddin, Amir Saeidi, Eduardo Blanco, Chitta Baral

## 摘要
Policy-adherent tool-calling agents in customer-service domains must maintain task states across turns while calling tools and obeying domain policies. Task states consist of relevant facts, identifiers, constraints, and conditions observed through user interaction and tool calls. In standard agents...

## 中文摘要
LedgerAgent 提出了一种结构化状态管理方法，用于构建遵循领域政策的工具调用型客服代理。通过将任务状态（如事实、标识符、约束和条件）显式记录为账本式结构，代理能够在多轮对话中可靠地维护上下文，并在调用工具时严格遵循业务规则。该技术提升了代理的可解释性和合规性，特别适用于金融、医疗等强监管场景。产品创新在于用显式结构化状态替代隐式推理，降低了错误执行风险，为客服自动化提供了高可靠性的技术底座。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.20529v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
