---
title: Visual Contrastive Self-Distillation
created: 2026-07-24
updated: 2026-07-24
type: concept
pillar: capabilities
pm_score: 0.41
tags: ["research", "capabilities"]
sources: ["raw/papers/visual-contrastive-self-distillation.json"]
---

# Visual Contrastive Self-Distillation

## 中文摘要
该论文提出视觉对比自蒸馏方法，针对在线策略自蒸馏（OPSD）中教师与学生之间信息不对称的问题进行优化。OPSD通过移除外部教师模型实现自监督学习，但需要确保自教师比学生提供更强的学习信号。论文通过引入对比学习机制，增强自教师与学生的差异，从而提升视觉模型的表征学习能力。这一技术可降低对大型预训练教师的依赖，减少训练成本，适用于图像识别、目标检测等视觉任务，具有提升模型效率与精度的商业价值。

## PM 关注指标
- 🎯 PM Score: 0.41
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, token, benchmark, reasoning, distillation

## 作者
Yijun Liang, Yunjie Tian, Yijiang Li, Yuqi Jia, Furong Huang

## 摘要
On-policy self-distillation (OPSD) is promising as it removes the external teacher required by on-policy distillation (OPD), yet it still needs asymmetric information between teacher and student to ensure that the self-teacher provides a stronger learning signal than the student. Existing methods cr...

## 中文摘要
该论文提出视觉对比自蒸馏方法，针对在线策略自蒸馏（OPSD）中教师与学生之间信息不对称的问题进行优化。OPSD通过移除外部教师模型实现自监督学习，但需要确保自教师比学生提供更强的学习信号。论文通过引入对比学习机制，增强自教师与学生的差异，从而提升视觉模型的表征学习能力。这一技术可降低对大型预训练教师的依赖，减少训练成本，适用于图像识别、目标检测等视觉任务，具有提升模型效率与精度的商业价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.21556v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
