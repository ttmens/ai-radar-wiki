---
title: RoboTTT: Context Scaling for Robot Policies
created: 2026-07-17
updated: 2026-07-17
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/robottt-context-scaling-for-robot-policies.json"]
---

# RoboTTT: Context Scaling for Robot Policies

## 中文摘要
RoboTTT 提出了一种基于测试时训练（Test-Time-Training）的机器人策略方法，将视觉运动上下文（visuomotor context）扩展到8000个时间步，相比现有最先进策略提升了三个数量级。该方法使机器人能基于长序列历史信息进行决策，显著增强长期任务规划与适应能力，对工业自动化、服务机器人等场景具有重要商业价值。产品创新在于无需修改网络结构即可高效利用极长上下文，为机器人基础模型的实际部署提供了可扩展方案。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: latency, inference, vision, training, parameter

## 作者
Yunfan Jiang, Yevgen Chebotar, Ruijie Zheng, Fengyuan Hu, Yunhao Ge

## 摘要
Recent robot foundation models operate with single-step or short-history visuomotor context. We introduce Test-Time-Training Robot Policies (RoboTTT), a robot model and training recipe that scale visuomotor context to 8K timesteps, three orders of magnitude beyond state-of-the-art policies, without ...

## 中文摘要
RoboTTT 提出了一种基于测试时训练（Test-Time-Training）的机器人策略方法，将视觉运动上下文（visuomotor context）扩展到8000个时间步，相比现有最先进策略提升了三个数量级。该方法使机器人能基于长序列历史信息进行决策，显著增强长期任务规划与适应能力，对工业自动化、服务机器人等场景具有重要商业价值。产品创新在于无需修改网络结构即可高效利用极长上下文，为机器人基础模型的实际部署提供了可扩展方案。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.15275v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
