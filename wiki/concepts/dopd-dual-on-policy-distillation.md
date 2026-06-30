---
title: DOPD: Dual On-policy Distillation
created: 2026-06-30
updated: 2026-06-30
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/dopd-dual-on-policy-distillation.json"]
---

# DOPD: Dual On-policy Distillation

## 中文摘要
DOPD（双在线策略蒸馏）是一种改进的知识蒸馏技术，通过监督学生模型采样的轨迹并利用密集的token级信号实现更优的能力迁移。核心创新在于引入特权信息（privileged information）作为高质量监督源，突破传统蒸馏性能上限。对产品经理而言，该技术可显著提升小模型的推理准确性和泛化能力，同时降低部署成本，适用于实时对话、内容生成等场景。产品创新体现在更高效的模型压缩路径，无需改变原有架构即可快速提升效果。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, vision, distillation

## 作者
Xinlei Yu, Gen Li, Qingyi Si, Guibin Zhang, Yuqi Xu

## 摘要
On-policy distillation (OPD) offers superior capacity transfer by supervising student-sampled trajectories with dense token-level signals. To furnish high-quality supervision sources and thereby elevate the performance frontier of distillation, an intuitive direction is to infuse privileged informat...

## 中文摘要
DOPD（双在线策略蒸馏）是一种改进的知识蒸馏技术，通过监督学生模型采样的轨迹并利用密集的token级信号实现更优的能力迁移。核心创新在于引入特权信息（privileged information）作为高质量监督源，突破传统蒸馏性能上限。对产品经理而言，该技术可显著提升小模型的推理准确性和泛化能力，同时降低部署成本，适用于实时对话、内容生成等场景。产品创新体现在更高效的模型压缩路径，无需改变原有架构即可快速提升效果。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.30626v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
