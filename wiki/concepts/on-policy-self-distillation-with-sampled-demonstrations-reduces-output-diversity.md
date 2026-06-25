---
title: On-Policy Self-Distillation with Sampled Demonstrations Reduces Output Diversity
created: 2026-06-25
updated: 2026-06-25
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/on-policy-self-distillation-with-sampled-demonstrations-reduces-output-diversity.json"]
---

# On-Policy Self-Distillation with Sampled Demonstrations Reduces Output Diversity

## 中文摘要
该论文研究了在线策略自蒸馏方法，通过让同一模型同时担任教师和学生，并基于正确演示提供密集的token级反馈，显著提升了pass@1准确率。然而，这种方法会侵蚀输出多样性，导致pass@k曲线表现下降。对于AI产品经理，这意味着追求高准确率可能以牺牲多样性为代价，在构建对话、内容生成等需要多样性的产品时需谨慎权衡。商业价值在于可指导训练策略优化，平衡准确性与创造性输出。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, distillation, accuracy

## 作者
Andrei Liviu Nicolicioiu, Mohammad Pezeshki, Aaron Courville

## 摘要
On-policy self-distillation achieves strong pass@1 accuracy by using a single model as both teacher and student, with the teacher conditioned on a correct demonstration to provide dense token-level feedback. We show that this could come at a hidden cost: rollout diversity decreases and pass@k curves...

## 中文摘要
该论文研究了在线策略自蒸馏方法，通过让同一模型同时担任教师和学生，并基于正确演示提供密集的token级反馈，显著提升了pass@1准确率。然而，这种方法会侵蚀输出多样性，导致pass@k曲线表现下降。对于AI产品经理，这意味着追求高准确率可能以牺牲多样性为代价，在构建对话、内容生成等需要多样性的产品时需谨慎权衡。商业价值在于可指导训练策略优化，平衡准确性与创造性输出。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.26091v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
