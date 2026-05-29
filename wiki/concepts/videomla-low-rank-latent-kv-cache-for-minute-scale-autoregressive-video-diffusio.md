---
title: VideoMLA: Low-Rank Latent KV Cache for Minute-Scale Autoregressive Video Diffusi
created: 2026-05-29
updated: 2026-05-29
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/videomla-low-rank-latent-kv-cache-for-minute-scale-autoregressive-video-diffusio.json"]
---

# VideoMLA: Low-Rank Latent KV Cache for Minute-Scale Autoregressive Video Diffusion

## 中文摘要
本文提出VideoMLA，一种低秩潜在KV缓存方法，用于分钟级自回归视频扩散。传统固定大小滑动窗口缓存虽然节省内存，但每头KV布局仍是流式内存的主要瓶颈。VideoMLA通过低秩分解显著压缩KV缓存，使得长序列（分钟级）视频生成在有限资源下可行，同时保持生成质量和时序连贯性。该技术降低了长视频流式推理的内存开销，有望推动实时长视频生成、视频编辑等产品创新，并为未来AI视频创作平台提供底层能力支撑。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: latency, token, throughput, training, compression

## 作者
Hidir Yesiltepe, Jiazhen Hu, Tuna Han Salih Meral, Adil Kaan Akan, Kaan Oktay

## 摘要
Long-rollout causal video diffusion has converged on a fixed-size sliding-window KV cache, with recent progress innovating within this layout by changing which tokens occupy the window or how their positions are encoded. The per-head KV layout itself, a dominant contributor to streaming memory and l...

## 中文摘要
本文提出VideoMLA，一种低秩潜在KV缓存方法，用于分钟级自回归视频扩散。传统固定大小滑动窗口缓存虽然节省内存，但每头KV布局仍是流式内存的主要瓶颈。VideoMLA通过低秩分解显著压缩KV缓存，使得长序列（分钟级）视频生成在有限资源下可行，同时保持生成质量和时序连贯性。该技术降低了长视频流式推理的内存开销，有望推动实时长视频生成、视频编辑等产品创新，并为未来AI视频创作平台提供底层能力支撑。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.30351v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
