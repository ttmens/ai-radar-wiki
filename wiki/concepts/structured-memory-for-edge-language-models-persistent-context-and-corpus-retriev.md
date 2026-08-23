---
title: Structured Memory for Edge Language Models: Persistent Context and Corpus Retrie
created: 2026-08-04
updated: 2026-08-04
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/structured-memory-for-edge-language-models-persistent-context-and-corpus-retriev.json"]
---

# Structured Memory for Edge Language Models: Persistent Context and Corpus Retrieval via O(1) SSM State Injection

## 中文摘要
该论文针对边缘端语言模型提出结构化记忆方案，通过状态空间模型（SSM）的O(1)状态注入实现持久上下文与语料检索，在构造上消除Transformer的KV-cache增长问题，并将RAG的预填充成本降为零，使长上下文检索在边缘设备上变得高效可行。对AI产品经理而言，这意味着未来端侧AI可具备持久的用户记忆和更快的响应速度，同时降低内存和计算开销，为隐私保护、离线场景及个性化服务带来新可能。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: latency, token, transformer, parameter, retrieval

## 作者
Anusha Madan Gopal, Aras Pirbadian, Kristofor D. Carlson, M Anthony Lewis, Jonathan Tapson

## 摘要
Retrieval-augmented generation (RAG) imposes a prefill cost proportional to retrieved context length, and -- with Transformer backbones -- a KV-cache that grows with each generated token. State-Space Models (SSMs) avoid the second cost by construction; we eliminate the first, collapsing prefill from...

## 中文摘要
该论文针对边缘端语言模型提出结构化记忆方案，通过状态空间模型（SSM）的O(1)状态注入实现持久上下文与语料检索，在构造上消除Transformer的KV-cache增长问题，并将RAG的预填充成本降为零，使长上下文检索在边缘设备上变得高效可行。对AI产品经理而言，这意味着未来端侧AI可具备持久的用户记忆和更快的响应速度，同时降低内存和计算开销，为隐私保护、离线场景及个性化服务带来新可能。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2608.02560v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
