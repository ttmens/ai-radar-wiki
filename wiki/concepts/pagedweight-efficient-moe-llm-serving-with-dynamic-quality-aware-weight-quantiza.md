---
title: PagedWeight: Efficient MoE LLM Serving with Dynamic Quality-Aware Weight Quantiz
created: 2026-07-20
updated: 2026-07-20
type: concept
pillar: capabilities
pm_score: 0.395
tags: ["research", "capabilities"]
sources: ["raw/papers/pagedweight-efficient-moe-llm-serving-with-dynamic-quality-aware-weight-quantiza.json"]
---

# PagedWeight: Efficient MoE LLM Serving with Dynamic Quality-Aware Weight Quantization

## 中文摘要
PagedWeight提出一种针对MoE大语言模型的高效服务方案，通过动态质量感知的权重量化技术，缓解模型权重与不断增长的KV缓存之间的GPU内存竞争。该方法在KV缓存密集型场景中，显著降低内存占用，提升推理吞吐量，同时保持模型质量。对于产品经理而言，这意味着能够以更低的硬件成本部署更大规模的MoE模型，或在相同资源下支持更长上下文和更高并发，推动MoE架构在实时交互式AI产品中的落地。

## PM 关注指标
- 🎯 PM Score: 0.395
- 🏷️ Pillar: capabilities
- 🔑 Keywords: latency, quantization, throughput, accuracy, precision

## 作者
Yuchen Yang, Yifan Zhao, Anisha Dasgupta, Sasa Misailovic

## 摘要
Mixture-of-Experts (MoE) is a popular class of large language models (LLMs), offering high efficiency and accuracy. However, in KV-cache-intensive serving scenarios, MoEs often exhibit a tension between the GPU memory requirements of the model weights and the growing KV cache. We propose PagedWeight...

## 中文摘要
PagedWeight提出一种针对MoE大语言模型的高效服务方案，通过动态质量感知的权重量化技术，缓解模型权重与不断增长的KV缓存之间的GPU内存竞争。该方法在KV缓存密集型场景中，显著降低内存占用，提升推理吞吐量，同时保持模型质量。对于产品经理而言，这意味着能够以更低的硬件成本部署更大规模的MoE模型，或在相同资源下支持更长上下文和更高并发，推动MoE架构在实时交互式AI产品中的落地。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.16184v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
