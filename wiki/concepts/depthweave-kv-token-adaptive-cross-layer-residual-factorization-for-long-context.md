---
title: DepthWeave-KV: Token-Adaptive Cross-Layer Residual Factorization for Long-Contex
created: 2026-07-08
updated: 2026-07-08
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/depthweave-kv-token-adaptive-cross-layer-residual-factorization-for-long-context.json"]
---

# DepthWeave-KV: Token-Adaptive Cross-Layer Residual Factorization for Long-Context KV Cache Compression

## 中文摘要
DepthWeave-KV 提出一种针对长上下文语言模型推理的 KV 缓存压缩方法，通过自适应跨层残差分解技术，为不同层和不同 token 动态分配压缩预算，解决了传统统一压缩策略在词汇线索与语义状态需求差异下导致检索质量下降的问题。该技术能显著降低内存带宽和存储压力，降低部署成本，支持更长对话或文档处理，提升产品体验。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, benchmark, quantization, training

## 作者
Anna Cordoba, Adam Puente Tercero, Nerea Angulo Hijo, Mar Linares Tercero, Julia Barrientos

## 摘要
Long-context language model inference is increasingly limited by the memory bandwidth and capacity required to store key-value caches, yet existing compression methods often apply uniform budgets across layers or tokens and degrade retrieval when lexical cues and semantic states require different pr...

## 中文摘要
DepthWeave-KV 提出一种针对长上下文语言模型推理的 KV 缓存压缩方法，通过自适应跨层残差分解技术，为不同层和不同 token 动态分配压缩预算，解决了传统统一压缩策略在词汇线索与语义状态需求差异下导致检索质量下降的问题。该技术能显著降低内存带宽和存储压力，降低部署成本，支持更长对话或文档处理，提升产品体验。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.06523v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
