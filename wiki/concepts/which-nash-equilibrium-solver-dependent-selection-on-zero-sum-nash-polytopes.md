---
title: Which Nash Equilibrium? Solver-Dependent Selection on Zero-Sum Nash Polytopes
created: 2026-06-29
updated: 2026-06-29
type: concept
pillar: patterns
pm_score: 0.395
tags: ["research", "patterns"]
sources: ["raw/papers/which-nash-equilibrium-solver-dependent-selection-on-zero-sum-nash-polytopes.json"]
---

# Which Nash Equilibrium? Solver-Dependent Selection on Zero-Sum Nash Polytopes

## 中文摘要
该论文揭示了一个被忽视的工程事实：许多两人零和博弈的纳什均衡并非唯一，而构成一个凸多面体，其中所有策略都达到相同的最优值V*但行为截然不同。标准求解器（如线性规划、迭代方法）各自收敛到该多面体中的某个特定均衡，且这一选择与求解器本身强相关，导致不同求解器输出不同策略。对于AI产品经理而言，这意味着在依赖博弈论进行对抗训练、多智能体协调或安全对齐时，求解器的“隐形偏置”会影响最终策略行为，进而影响产品鲁棒性与可复现性。产品需要明确指定求解器或设计均衡选择机制，以避免因求解器更换导致不可预测的模型行为变化。

## PM 关注指标
- 🎯 PM Score: 0.395
- 🏷️ Pillar: patterns
- 🔑 Keywords: rag

## 作者
Luis Leal

## 摘要
Many two-player zero-sum games admit not a unique Nash equilibrium but a convex set of them: a polytope of profiles that all share the minimax value V* yet prescribe different behaviour. Standard solvers each converge to some equilibrium and are treated as interchangeable. We ask whether they instea...

## 中文摘要
该论文揭示了一个被忽视的工程事实：许多两人零和博弈的纳什均衡并非唯一，而构成一个凸多面体，其中所有策略都达到相同的最优值V*但行为截然不同。标准求解器（如线性规划、迭代方法）各自收敛到该多面体中的某个特定均衡，且这一选择与求解器本身强相关，导致不同求解器输出不同策略。对于AI产品经理而言，这意味着在依赖博弈论进行对抗训练、多智能体协调或安全对齐时，求解器的“隐形偏置”会影响最终策略行为，进而影响产品鲁棒性与可复现性。产品需要明确指定求解器或设计均衡选择机制，以避免因求解器更换导致不可预测的模型行为变化。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.28308v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
