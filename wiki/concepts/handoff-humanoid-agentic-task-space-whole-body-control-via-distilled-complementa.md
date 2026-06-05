---
title: HANDOFF: Humanoid Agentic Task-Space Whole-Body Control via Distilled Complement
created: 2026-06-06
updated: 2026-06-06
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/handoff-humanoid-agentic-task-space-whole-body-control-via-distilled-complementa.json"]
---

# HANDOFF: Humanoid Agentic Task-Space Whole-Body Control via Distilled Complementary Teachers

## 中文摘要
论文提出HANDOFF框架，通过蒸馏互补教师模型实现人形机器人的任务空间全身控制。传统方法需要密集的运动学或空间参考，难以从高层任务语义中自动合成。HANDOFF将任务规划与全身控制解耦，利用多个互补教师模型蒸馏出轻量级策略，使机器人能直接在任务空间中执行复杂动作，无需精确的轨迹参考。该技术为人形机器人在真实场景中的灵活部署提供了高效接口，降低了规划复杂度，有望推动服务、制造等领域的人形机器人商业化应用。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: fine-tuning, distillation

## 作者
Lizhi Yang, Junheng Li, Nehar Poddar, Yiling Hou, Gio Huh

## 摘要
For a humanoid robot to be deployed in the real world, the choice of command space (i.e., the interface between task planning and whole-body control) is crucial. Existing whole-body controllers typically demand dense kinematic or spatial references that planners struggle to synthesize from task sema...

## 中文摘要
论文提出HANDOFF框架，通过蒸馏互补教师模型实现人形机器人的任务空间全身控制。传统方法需要密集的运动学或空间参考，难以从高层任务语义中自动合成。HANDOFF将任务规划与全身控制解耦，利用多个互补教师模型蒸馏出轻量级策略，使机器人能直接在任务空间中执行复杂动作，无需精确的轨迹参考。该技术为人形机器人在真实场景中的灵活部署提供了高效接口，降低了规划复杂度，有望推动服务、制造等领域的人形机器人商业化应用。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.06493v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
