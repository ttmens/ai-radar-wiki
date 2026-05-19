---
title: DashAttention: Differentiable and Adaptive Sparse Hierarchical Attention
created: 2026-05-19
updated: 2026-05-19
type: concept
pillar: capabilities
pm_score: 0.515
tags: ["research", "capabilities"]
sources: ["raw/papers/dashattention-differentiable-and-adaptive-sparse-hierarchical-attention.json"]
---

# DashAttention: Differentiable and Adaptive Sparse Hierarchical Attention

## 中文摘要
DashAttention 提出了一种可微自适应稀疏分层注意力机制，解决了现有方法（如 NSA、InfLLMv2）中 top-k 选择固定数量 KV 块的局限。该技术通过动态调整每个查询的相关 token 数量，结合可微分操作实现端到端优化，在保持长上下文处理能力的同时大幅降低计算和内存开销。对于 AI 产品而言，这意味着更高效的长文档理解、对话记忆和推理任务，能够以更低成本支撑更大规模的上下文窗口，并提升模型对关键信息的聚焦能力，具有显著的商业价值。

## PM 关注指标
- 🎯 PM Score: 0.515
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, attention, accuracy, gradient

## 作者
Yuxiang Huang, Nuno M. T. Gonçalves, Federico Alvetreti, Lei Li, Xu Han

## 摘要
Current hierarchical attention methods, such as NSA and InfLLMv2, select the top-k relevant key-value (KV) blocks based on coarse attention scores and subsequently apply fine-grained softmax attention on the selected tokens. However, the top-k operation assumes the number of relevant tokens for any ...

## 中文摘要
DashAttention 提出了一种可微自适应稀疏分层注意力机制，解决了现有方法（如 NSA、InfLLMv2）中 top-k 选择固定数量 KV 块的局限。该技术通过动态调整每个查询的相关 token 数量，结合可微分操作实现端到端优化，在保持长上下文处理能力的同时大幅降低计算和内存开销。对于 AI 产品而言，这意味着更高效的长文档理解、对话记忆和推理任务，能够以更低成本支撑更大规模的上下文窗口，并提升模型对关键信息的聚焦能力，具有显著的商业价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.18753v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
