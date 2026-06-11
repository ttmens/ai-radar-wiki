---
title: Context-Driven Incremental Compression for Multi-Turn Dialogue Generation
created: 2026-06-11
updated: 2026-06-11
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/context-driven-incremental-compression-for-multi-turn-dialogue-generation.json"]
---

# Context-Driven Incremental Compression for Multi-Turn Dialogue Generation

## 中文摘要
针对多轮对话中对话历史不断增长导致的冗余计算问题，本文提出上下文驱动的增量压缩方法。该方法通过跨轮记忆共享与增量更新机制，避免对完整历史重复编码，从而降低注意力和编码成本，同时保持高保真度。相比传统的截断或摘要方式，该方案能在不牺牲对话质量的前提下显著提升长对话的处理效率，对降低对话系统推理成本、支持更长的交互历史具有重要商业价值。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: latency, inference, benchmark, vision, compression

## 作者
Yeongseo Jung, Jaehyeok Kim, Eunseo Jung, Jiachuan Wang, Yongqi Zhang

## 摘要
Modern conversational agents condition on an ever-growing dialogue history at each turn, incurring redundant attention and encoding costs that grow with conversation length. Naive truncation or summarization degrades fidelity, while existing context compressors lack cross-turn memory sharing or revi...

## 中文摘要
针对多轮对话中对话历史不断增长导致的冗余计算问题，本文提出上下文驱动的增量压缩方法。该方法通过跨轮记忆共享与增量更新机制，避免对完整历史重复编码，从而降低注意力和编码成本，同时保持高保真度。相比传统的截断或摘要方式，该方案能在不牺牲对话质量的前提下显著提升长对话的处理效率，对降低对话系统推理成本、支持更长的交互历史具有重要商业价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.12411v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
