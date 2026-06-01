---
title: What Gets Unmasked First? Trajectory Analysis of Diffusion Models for Graph-to-T
created: 2026-06-01
updated: 2026-06-01
type: concept
pillar: capabilities
pm_score: 0.43
tags: ["research", "capabilities"]
sources: ["raw/papers/what-gets-unmasked-first-trajectory-analysis-of-diffusion-models-for-graph-to-te.json"]
---

# What Gets Unmasked First? Trajectory Analysis of Diffusion Models for Graph-to-Text Generation

## 中文摘要
本文首次系统研究掩码扩散语言模型(MDLMs)在图到文本生成中的应用。与自回归LLM线性生成文本不同，MDLM在迭代解码过程中以非顺序方式逐步去除掩码，形成独特的生成轨迹。研究发现MDLM能更灵活地利用全局上下文，在结构化数据到文本任务中展现出对长距离依赖和实体关系的更好建模能力。这一技术突破为产品创新提供了新的文本生成范式，尤其在知识图谱描述、数据报表自动生成等场景中，可提升生成内容的准确性和结构性，降低幻觉风险。

## PM 关注指标
- 🎯 PM Score: 0.43
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, fine-tuning, training, sft

## 作者
Qing Wang, Jacob Devasier, Chengkai Li

## 摘要
We present the first systematic study of masked diffusion language models (MDLMs) for graph-to-text generation. We analyze MDLM generation trajectories -- the order in which tokens are unmasked during iterative decoding -- and find that, unlike autoregressive LLMs which generate text linearly, MDLMs...

## 中文摘要
本文首次系统研究掩码扩散语言模型(MDLMs)在图到文本生成中的应用。与自回归LLM线性生成文本不同，MDLM在迭代解码过程中以非顺序方式逐步去除掩码，形成独特的生成轨迹。研究发现MDLM能更灵活地利用全局上下文，在结构化数据到文本任务中展现出对长距离依赖和实体关系的更好建模能力。这一技术突破为产品创新提供了新的文本生成范式，尤其在知识图谱描述、数据报表自动生成等场景中，可提升生成内容的准确性和结构性，降低幻觉风险。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.31564v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
