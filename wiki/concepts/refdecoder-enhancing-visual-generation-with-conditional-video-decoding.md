---
title: RefDecoder: Enhancing Visual Generation with Conditional Video Decoding
created: 2026-05-15
updated: 2026-05-15
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/refdecoder-enhancing-visual-generation-with-conditional-video-decoding.json"]
---

# RefDecoder: Enhancing Visual Generation with Conditional Video Decoding

## 中文摘要
RefDecoder 提出一种条件视频解码方法，解决潜在扩散模型中解码器无条件导致的生成质量不对称问题。传统解码器不利用条件信息，限制了生成一致性。RefDecoder 通过引入条件机制，显著提升视频生成质量，尤其在下游应用如视频编辑、合成中实现更逼真、连贯的输出。该技术创新降低了生成伪影，优化了模型架构效率，对视频生成产品的实用化和商业化有重要价值。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, video generation, fine-tuning, attention

## 作者
Xiang Fan, Yuheng Wang, Bohan Fang, Zhongzheng Ren, Ranjay Krishna

## 摘要
Video generation powers a vast array of downstream applications. However, while the de facto standard, i.e., latent diffusion models, typically employ heavily conditioned denoising networks, their decoders often remain unconditional. We observe that this architectural asymmetry leads to significant ...

## 中文摘要
RefDecoder 提出一种条件视频解码方法，解决潜在扩散模型中解码器无条件导致的生成质量不对称问题。传统解码器不利用条件信息，限制了生成一致性。RefDecoder 通过引入条件机制，显著提升视频生成质量，尤其在下游应用如视频编辑、合成中实现更逼真、连贯的输出。该技术创新降低了生成伪影，优化了模型架构效率，对视频生成产品的实用化和商业化有重要价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.15196v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
