---
title: Streaming Communication in Multi-Agent Reasoning
created: 2026-06-05
updated: 2026-06-05
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/streaming-communication-in-multi-agent-reasoning.json"]
---

# Streaming Communication in Multi-Agent Reasoning

## 中文摘要
多智能体推理系统传统采用“生成-再传输”范式，导致端到端延迟随流水线深度线性增长。StreamMA 提出流式通信机制，每个推理步骤一旦生成即立即传输给下游智能体，实现相邻智能体间的流水线并行。该技术显著降低多智能体协作的响应延迟，提升实时性，适用于复杂推理任务如对话系统、代码生成等产品场景。商业价值在于支持更高效的 agent 协作，减少等待时间，优化用户体验，并可能降低算力消耗。产品创新点在于将流式思想引入多智能体推理，打破串行瓶颈。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: latency, benchmark, reasoning, scaling law

## 作者
Zhen Yang, Xiaogang Xu, Wen Wang, Cong Chen, Xander Xu

## 摘要
Multi-agent reasoning systems adopt a "generate-then-transfer" paradigm that forces end-to-end latency to scale linearly with pipeline depth. We introduce StreamMA, a multi-agent reasoning system that streams each reasoning step to downstream agents as soon as it is generated, pipelining adjacent ag...

## 中文摘要
多智能体推理系统传统采用“生成-再传输”范式，导致端到端延迟随流水线深度线性增长。StreamMA 提出流式通信机制，每个推理步骤一旦生成即立即传输给下游智能体，实现相邻智能体间的流水线并行。该技术显著降低多智能体协作的响应延迟，提升实时性，适用于复杂推理任务如对话系统、代码生成等产品场景。商业价值在于支持更高效的 agent 协作，减少等待时间，优化用户体验，并可能降低算力消耗。产品创新点在于将流式思想引入多智能体推理，打破串行瓶颈。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.05158v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
