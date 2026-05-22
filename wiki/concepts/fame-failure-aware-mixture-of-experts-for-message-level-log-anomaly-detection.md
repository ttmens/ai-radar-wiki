---
title: FAME: Failure-Aware Mixture-of-Experts for Message-Level Log Anomaly Detection
created: 2026-05-22
updated: 2026-05-22
type: concept
pillar: capabilities
pm_score: 0.515
tags: ["research", "capabilities"]
sources: ["raw/papers/fame-failure-aware-mixture-of-experts-for-message-level-log-anomaly-detection.json"]
---

# FAME: Failure-Aware Mixture-of-Experts for Message-Level Log Anomaly Detection

## 中文摘要
本论文提出 FAME（Failure-Aware Mixture-of-Experts），一种面向消息级日志异常检测的混合专家模型。传统方法常在会话或窗口级别检测异常，只能标记整组日志，导致运维人员需逐一排查大量正常行。FAME 利用专家网络分别建模不同日志模式，并通过故障感知门控机制精确定位引发异常的单个消息。该技术可将异常定位粒度从粗粒度降低至单条日志，大幅提升运维效率，减少平均修复时间（MTTR）。产品创新点在于细粒度异常定位与可解释性增强，适合集成到智能运维（AIOps）平台中。

## PM 关注指标
- 🎯 PM Score: 0.515
- 🏷️ Pillar: capabilities
- 🔑 Keywords: training, recall

## 作者
Huanchi Wang, Zihang Huang, Yifang Tian, Kristina Dzeparoska, Hans-Arno Jacobsen

## 摘要
Production systems generate millions of log lines daily, yet most anomaly detectors operate at the session or window-level, flagging groups of lines rather than identifying the specific message responsible. This coarse granularity forces operators to inspect many routine lines per alert. Message-lev...

## 中文摘要
本论文提出 FAME（Failure-Aware Mixture-of-Experts），一种面向消息级日志异常检测的混合专家模型。传统方法常在会话或窗口级别检测异常，只能标记整组日志，导致运维人员需逐一排查大量正常行。FAME 利用专家网络分别建模不同日志模式，并通过故障感知门控机制精确定位引发异常的单个消息。该技术可将异常定位粒度从粗粒度降低至单条日志，大幅提升运维效率，减少平均修复时间（MTTR）。产品创新点在于细粒度异常定位与可解释性增强，适合集成到智能运维（AIOps）平台中。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.22779v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
