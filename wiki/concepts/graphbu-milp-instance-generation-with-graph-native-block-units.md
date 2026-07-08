---
title: GraphBU: MILP Instance Generation with Graph-Native Block Units
created: 2026-07-08
updated: 2026-07-08
type: concept
pillar: capabilities
pm_score: 0.41
tags: ["research", "capabilities"]
sources: ["raw/papers/graphbu-milp-instance-generation-with-graph-native-block-units.json"]
---

# GraphBU: MILP Instance Generation with Graph-Native Block Units

## 中文摘要
论文提出GraphBU方法，用于生成混合整数线性规划（MILP）实例。由于私有或专用管线的MILP模型难以获取，现有通用生成器常破坏求解器与学习策略依赖的结构。GraphBU采用图原生块单元，从底层图结构生成实例，保留关键拓扑与约束特征，从而提升求解器训练与评估效果。该方法对运筹优化、供应链调度等AI产品具有实用价值，可低成本获得高质量训练数据，推动端到端优化模型的产品化落地。

## PM 关注指标
- 🎯 PM Score: 0.41
- 🏷️ Pillar: capabilities
- 🔑 Keywords: training, dataset, similarity

## 作者
Xiaolei Guo, Chenyu Zhou, Jianghao Lin, Dongdong Ge

## 摘要
Mixed-integer linear programming (MILP) instances used for solver development are hard to obtain when models come from private or application-specific pipelines. A generator must keep the structure that solvers and learned policies rely on. Existing general generators usually choose their generation...

## 中文摘要
论文提出GraphBU方法，用于生成混合整数线性规划（MILP）实例。由于私有或专用管线的MILP模型难以获取，现有通用生成器常破坏求解器与学习策略依赖的结构。GraphBU采用图原生块单元，从底层图结构生成实例，保留关键拓扑与约束特征，从而提升求解器训练与评估效果。该方法对运筹优化、供应链调度等AI产品具有实用价值，可低成本获得高质量训练数据，推动端到端优化模型的产品化落地。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.06532v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
