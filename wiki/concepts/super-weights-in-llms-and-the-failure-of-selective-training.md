---
title: Super Weights in LLMs and the Failure of Selective Training
created: 2026-07-10
updated: 2026-07-10
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/super-weights-in-llms-and-the-failure-of-selective-training.json"]
---

# Super Weights in LLMs and the Failure of Selective Training

## 中文摘要
研究揭示了大型语言模型中存在“超级权重”（Super Weights），即个别参数对模型性能影响巨大（移除后性能下降数个数量级）。但研究发现这种退化并非普遍适用于所有LLM，不同模型表现存在差异。论文进一步探讨了感知超级权重的训练方法，为模型压缩和剪枝策略提供了新视角。对AI产品经理而言，理解超级权重的存在有助于优化模型部署效率、降低成本，并指导更精细的模型微调与剪枝决策，但需注意不同模型的行为差异。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: fine-tuning, training, attention, parameter, accuracy

## 作者
Shreyas Subramanian, Adewale Akinfaderin, Akarsha Sehwag

## 摘要
Recent work identified Super Weights, individual parameters whose removal degrades model performance by orders of magnitude. We show that this degradation due to pruning Super Weights does not universally apply to all LLMs. Furthermore, if these parameters are so important, Super Weight-aware traini...

## 中文摘要
研究揭示了大型语言模型中存在“超级权重”（Super Weights），即个别参数对模型性能影响巨大（移除后性能下降数个数量级）。但研究发现这种退化并非普遍适用于所有LLM，不同模型表现存在差异。论文进一步探讨了感知超级权重的训练方法，为模型压缩和剪枝策略提供了新视角。对AI产品经理而言，理解超级权重的存在有助于优化模型部署效率、降低成本，并指导更精细的模型微调与剪枝决策，但需注意不同模型的行为差异。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.08733v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
