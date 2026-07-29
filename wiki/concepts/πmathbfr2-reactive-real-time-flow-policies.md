---
title: $π\mathbf{R}^2$: Reactive Real-time Flow Policies
created: 2026-07-29
updated: 2026-07-29
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/πmathbfr2-reactive-real-time-flow-policies.json"]
---

# $π\mathbf{R}^2$: Reactive Real-time Flow Policies

## 中文摘要
该论文提出一种反应式实时流策略（πR²），针对当前通用操作策略中基于大预训练模型的动作块流（action-chunking）在执行时无法响应中途感官输入、缺乏反应性的问题。通过更频繁的在线重规划，恢复策略对环境变化的实时响应能力，同时保持流式架构的高效性。这一创新可显著提升机器人操作任务（如抓取、装配）的鲁棒性与适应性，在工业自动化、服务机器人等需要高反应性的场景具有商业价值。产品层面可简化模型设计，降低对精确预测的依赖，使AI在动态环境中更可靠。核心技术包括动作块流与实时重规划的融合。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: latency, vision

## 作者
Sungjae Park, Shubham Tulsiani

## 摘要
Generalist manipulation policies increasingly take the form of action-chunking flow policies built on large pretrained backbones. Such chunks run open-loop, so the policy cannot react to sensory input arriving mid-execution, sacrificing \emph{reactivity}. Replanning more often would restore it, but ...

## 中文摘要
该论文提出一种反应式实时流策略（πR²），针对当前通用操作策略中基于大预训练模型的动作块流（action-chunking）在执行时无法响应中途感官输入、缺乏反应性的问题。通过更频繁的在线重规划，恢复策略对环境变化的实时响应能力，同时保持流式架构的高效性。这一创新可显著提升机器人操作任务（如抓取、装配）的鲁棒性与适应性，在工业自动化、服务机器人等需要高反应性的场景具有商业价值。产品层面可简化模型设计，降低对精确预测的依赖，使AI在动态环境中更可靠。核心技术包括动作块流与实时重规划的融合。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.26055v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
