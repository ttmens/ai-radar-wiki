---
title: Fitted Occupancy-Ratio Evaluation without Bellman Completeness
created: 2026-07-07
updated: 2026-07-07
type: concept
pillar: ecosystem
pm_score: 0.41
tags: ["research", "ecosystem"]
sources: ["raw/papers/fitted-occupancy-ratio-evaluation-without-bellman-completeness.json"]
---

# Fitted Occupancy-Ratio Evaluation without Bellman Completeness

## 中文摘要
该论文提出一种新的离线强化学习评估方法——拟合占用率评估（Fitted Occupancy-Ratio Evaluation），无需依赖Bellman完备性假设，解决了传统方法中分布偏移的校正难题。通过直接拟合占用率，该方法在更宽松的理论条件下实现稳定且高效的策略评估，降低了离线评估的复杂性。对于AI产品经理而言，这意味着在推荐系统、自动驾驶等数据分布难以控制的场景中，可以更可靠地利用历史数据评估新策略效果，减少在线测试风险，加速产品迭代。该工作为强化学习在实际产品中的安全部署提供了关键技术支撑。

## PM 关注指标
- 🎯 PM Score: 0.41
- 🏷️ Pillar: ecosystem
- 🔑 Keywords: evaluation, eval

## 作者
Lars van der Laan, Nathan Kallus

## 摘要
Occupancy ratios correct distribution shift in offline reinforcement learning and are central to off-policy evaluation. Existing primal-dual and minimax methods typically estimate these ratios by enforcing occupancy-balance moments over a critic class. We propose fitted occupancy-ratio evaluation (F...

## 中文摘要
该论文提出一种新的离线强化学习评估方法——拟合占用率评估（Fitted Occupancy-Ratio Evaluation），无需依赖Bellman完备性假设，解决了传统方法中分布偏移的校正难题。通过直接拟合占用率，该方法在更宽松的理论条件下实现稳定且高效的策略评估，降低了离线评估的复杂性。对于AI产品经理而言，这意味着在推荐系统、自动驾驶等数据分布难以控制的场景中，可以更可靠地利用历史数据评估新策略效果，减少在线测试风险，加速产品迭代。该工作为强化学习在实际产品中的安全部署提供了关键技术支撑。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.05375v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
