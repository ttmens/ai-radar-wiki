---
title: Pass the Baton: Trajectory-Relayed On-Policy Distillation
created: 2026-07-29
updated: 2026-07-29
type: concept
pillar: capabilities
pm_score: 0.41
tags: ["research", "capabilities"]
sources: ["raw/papers/pass-the-baton-trajectory-relayed-on-policy-distillation.json"]
---

# Pass the Baton: Trajectory-Relayed On-Policy Distillation

## 中文摘要
该论文提出了一种名为“轨迹中继在线策略蒸馏”的方法，旨在解决传统在线策略蒸馏中因学生模型推理方向错误导致后续生成偏离的问题。通过在中继阶段引入教师模型的正确轨迹引导，有效避免了前缀失败，提高了学生模型在推理任务中的准确性和可靠性。该技术对于提升小模型的推理能力、降低部署成本具有潜在商业价值，尤其适用于需要高效精确推理的场景。

## PM 关注指标
- 🎯 PM Score: 0.41
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, vision, reasoning, training

## 作者
Haolei Xu, Xiaowen Xu, Haiwen Hong, Zixuan Ni, Hongxing Li

## 摘要
On-policy distillation (OPD) grounds token-level supervision in the student's own trajectory, yet suffers from prefix failure: once the student commits to a wrong reasoning direction, all subsequent generation builds on this deviation, producing misdirected continuations that elicit unreliable super...

## 中文摘要
该论文提出了一种名为“轨迹中继在线策略蒸馏”的方法，旨在解决传统在线策略蒸馏中因学生模型推理方向错误导致后续生成偏离的问题。通过在中继阶段引入教师模型的正确轨迹引导，有效避免了前缀失败，提高了学生模型在推理任务中的准确性和可靠性。该技术对于提升小模型的推理能力、降低部署成本具有潜在商业价值，尤其适用于需要高效精确推理的场景。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.26057v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
