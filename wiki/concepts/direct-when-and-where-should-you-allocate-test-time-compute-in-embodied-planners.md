---
title: DIRECT: When and Where Should You Allocate Test-Time Compute in Embodied Planner
created: 2026-06-11
updated: 2026-06-11
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/direct-when-and-where-should-you-allocate-test-time-compute-in-embodied-planners.json"]
---

# DIRECT: When and Where Should You Allocate Test-Time Compute in Embodied Planners?

## 中文摘要
该论文探讨了视觉语言模型作为具身智能体高层规划器时，测试时计算资源分配策略的利弊。研究发现，虽然增加测试时计算能提升规划能力，但会导致延迟上升、Token消耗和FLOPs增加，且收益呈递减趋势。对产品经理的启示：在追求模型能力的同时需平衡成本效率，避免过度投入测试时计算。论文为具身智能体的部署提供了优化方向，强调在何时何处分配计算资源最为关键。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: latency, token, multimodal, vision

## 作者
Jadelynn Dao, Milan Ganai, Yasmina Abukhadra, Ajay Sridhar, Mozhgan Nasr Azadani

## 摘要
Vision-Language Models (VLMs) are increasingly deployed as high-level planners for embodied agents, with an emerging strategy of scaling test-time compute to improve capability. However, we observe that doing so increases latency, token usage, and FLOPs while yielding uneven, often diminishing gains...

## 中文摘要
该论文探讨了视觉语言模型作为具身智能体高层规划器时，测试时计算资源分配策略的利弊。研究发现，虽然增加测试时计算能提升规划能力，但会导致延迟上升、Token消耗和FLOPs增加，且收益呈递减趋势。对产品经理的启示：在追求模型能力的同时需平衡成本效率，避免过度投入测试时计算。论文为具身智能体的部署提供了优化方向，强调在何时何处分配计算资源最为关键。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.12402v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
