---
title: Vision-OPD: Learning to See Fine Details for Multimodal LLMs via On-Policy Self-
created: 2026-05-19
updated: 2026-05-19
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/vision-opd-learning-to-see-fine-details-for-multimodal-llms-via-on-policy-self-d.json"]
---

# Vision-OPD: Learning to See Fine Details for Multimodal LLMs via On-Policy Self-Distillation

## 中文摘要
该论文提出 Vision-OPD，通过在线策略自蒸馏方法缩小多模态大语言模型在细粒度视觉理解中的“区域到全局感知差距”。核心创新是让模型在训练中关注图像局部关键细节，提升对微小证据的识别能力，从而更准确地回答依赖细节的视觉问题。技术要点包括自蒸馏框架和 on-policy 训练策略。商业价值在于可显著改善 AI 产品的图像问答、文档解析、医疗影像等需要高精度细节理解的场景，降低对高质量标注数据的依赖。产品创新在于无需额外外部知识库，仅通过自身知识蒸馏增强细节感知，易于集成到现有 MLLM 中。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, benchmark, multimodal, vision

## 作者
Qianhao Yuan, Jie Lou, Xing Yu, Hongyu Lin, Le Sun

## 摘要
Multimodal Large Language Models (MLLMs) still struggle with fine-grained visual understanding, where answers often depend on small but decisive evidence in the full image. We observe a regional-to-global perception gap: the same MLLM answers fine-grained questions more accurately when conditioned o...

## 中文摘要
该论文提出 Vision-OPD，通过在线策略自蒸馏方法缩小多模态大语言模型在细粒度视觉理解中的“区域到全局感知差距”。核心创新是让模型在训练中关注图像局部关键细节，提升对微小证据的识别能力，从而更准确地回答依赖细节的视觉问题。技术要点包括自蒸馏框架和 on-policy 训练策略。商业价值在于可显著改善 AI 产品的图像问答、文档解析、医疗影像等需要高精度细节理解的场景，降低对高质量标注数据的依赖。产品创新在于无需额外外部知识库，仅通过自身知识蒸馏增强细节感知，易于集成到现有 MLLM 中。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.18740v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
