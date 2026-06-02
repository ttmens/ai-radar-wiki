---
title: Mitigating Perceptual Judgment Bias in Multimodal LLM-as-a-Judge via Perceptual 
created: 2026-06-02
updated: 2026-06-02
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/mitigating-perceptual-judgment-bias-in-multimodal-llm-as-a-judge-via-perceptual.json"]
---

# Mitigating Perceptual Judgment Bias in Multimodal LLM-as-a-Judge via Perceptual Perturbation and Reward Modeling

## 中文摘要
该研究指出多模态大语言模型在作为自动评判者时存在感知判断偏差：当视觉证据与文本线索冲突时，模型会倾向于奖励看似合理但感知错误的回答。为解决此问题，作者提出感知扰动和奖励建模方法，通过引入图像级扰动（如模糊、尺寸变化）并训练一个基于偏好的奖励模型来矫正评判偏差。该方法可提升多模态LLM在视觉-语言推理任务中的评判准确性，对构建更可靠的AI自动评估系统（如内容审核、图像问答评测）具有直接商业价值，减少人工标注成本，增强产品决策的鲁棒性。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: benchmark, multimodal, vision, reasoning, training

## 作者
Seojeong Park, Jiho Choi, Junyong Kang, Seonho Lee, Jaeyo Shin

## 摘要
Recent multimodal large language models have demonstrated strong reasoning ability, yet their reliability as automated evaluators remains limited by a critical weakness: when visual evidence conflicts with textual cues, MLLM judges tend to reward plausible narratives over perceptually correct answer...

## 中文摘要
该研究指出多模态大语言模型在作为自动评判者时存在感知判断偏差：当视觉证据与文本线索冲突时，模型会倾向于奖励看似合理但感知错误的回答。为解决此问题，作者提出感知扰动和奖励建模方法，通过引入图像级扰动（如模糊、尺寸变化）并训练一个基于偏好的奖励模型来矫正评判偏差。该方法可提升多模态LLM在视觉-语言推理任务中的评判准确性，对构建更可靠的AI自动评估系统（如内容审核、图像问答评测）具有直接商业价值，减少人工标注成本，增强产品决策的鲁棒性。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.02578v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
