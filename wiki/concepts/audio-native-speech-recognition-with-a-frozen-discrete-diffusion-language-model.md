---
title: Audio-Native Speech Recognition with a Frozen Discrete-Diffusion Language Model
created: 2026-07-15
updated: 2026-07-15
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/audio-native-speech-recognition-with-a-frozen-discrete-diffusion-language-model.json"]
---

# Audio-Native Speech Recognition with a Frozen Discrete-Diffusion Language Model

## 中文摘要
本文提出一种基于离散扩散语言模型的语音识别新方法，颠覆传统自回归逐个生成token的范式。通过将离散扩散模型与音频原生接口结合，模型能够在少量去噪步骤中并行优化整个转录文本，显著降低推理延迟。该方法无需依赖文本tokenizer，直接处理音频特征，保持音频语义完整性。商业上，该技术有望实现实时、低延时的语音转写服务，适合会议记录、语音助手等场景。产品创新在于将扩散模型的并行生成能力迁移至语音识别领域，为端到端非自回归架构开辟新路径。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, audio, training, embedding, attention

## 作者
Harsha Vardhan Khurdula, Abhinav Kumar Singh, Yoeven D Khemlani, Vineet Agarwal

## 摘要
Automatic speech recognition is dominated by autoregressive decoders that emit one token at a time. We ask whether a discrete diffusion language model can transcribe speech instead, refining a whole transcript in parallel over a small number of denoising steps. We train an audio-native interface for...

## 中文摘要
本文提出一种基于离散扩散语言模型的语音识别新方法，颠覆传统自回归逐个生成token的范式。通过将离散扩散模型与音频原生接口结合，模型能够在少量去噪步骤中并行优化整个转录文本，显著降低推理延迟。该方法无需依赖文本tokenizer，直接处理音频特征，保持音频语义完整性。商业上，该技术有望实现实时、低延时的语音转写服务，适合会议记录、语音助手等场景。产品创新在于将扩散模型的并行生成能力迁移至语音识别领域，为端到端非自回归架构开辟新路径。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.13013v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
