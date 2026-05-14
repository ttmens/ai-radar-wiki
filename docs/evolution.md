# AI Radar Wiki — Self-Evolution Log

> 系统自进化记录。每次 Cron 运行自动更新。

## 机制说明

### 1. 动态权重 (pm_score)
- **信号强度**: GitHub stars / HN score / 评论数
- **时效性**: 新鲜内容获得更高权重
- **用户反馈**: 点击、点赞、忽略行为影响权重
- **公式**: `pm_score = 0.4*signal + 0.25*recency + 0.15*engagement + 0.2*relevance`

### 2. 内容淘汰
- 超过 90 天无更新 且 pm_score < 0.15 的节点标记为 `deprecated`
- 重复实体自动合并

### 3. 趋势检测
- 新标签在单次运行中出现 ≥3 次，自动上报到 trending_tags
- Agent 分析 trending 趋势，建议更新 SCHEMA.md

## 运行日志

## [2026-05-15 06:04] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 81, 'capabilities': 140, 'business': 111, 'patterns': 117, 'unknown': 4}
- Top tags: {'project': 203, 'discussion': 99, 'hacker-news': 99, 'business': 97, 'python': 92}
- No actions needed


## [2026-05-15 00:02] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 79, 'capabilities': 135, 'business': 109, 'patterns': 117, 'unknown': 4}
- Top tags: {'project': 203, 'discussion': 95, 'hacker-news': 95, 'business': 95, 'python': 92}
- No actions needed


## [2026-05-14 18:02] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 79, 'capabilities': 132, 'business': 106, 'patterns': 116, 'unknown': 4}
- Top tags: {'project': 203, 'discussion': 92, 'hacker-news': 92, 'business': 92, 'python': 92}
- No actions needed


## [2026-05-14 12:01] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 79, 'capabilities': 131, 'business': 103, 'patterns': 115, 'unknown': 4}
- Top tags: {'project': 203, 'python': 92, 'discussion': 89, 'hacker-news': 89, 'business': 89}
- No actions needed


## [2026-05-14 11:53] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 79, 'capabilities': 131, 'business': 103, 'patterns': 115, 'unknown': 4}
- Top tags: {'project': 203, 'python': 92, 'discussion': 89, 'hacker-news': 89, 'business': 89}
- No actions needed


## [2026-05-14 11:31] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 79, 'capabilities': 131, 'business': 103, 'patterns': 115, 'unknown': 4}
- Top tags: {'project': 203, 'python': 92, 'discussion': 89, 'hacker-news': 89, 'business': 89}
- No actions needed


## [2026-05-14 06:18] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 77, 'capabilities': 121, 'business': 101, 'patterns': 114, 'unknown': 4}
- Top tags: {'project': 203, 'python': 92, 'business': 87, 'discussion': 86, 'hacker-news': 86}
- No actions needed


## [2026-05-14 00:03] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 77, 'capabilities': 120, 'business': 91, 'patterns': 112, 'unknown': 4}
- Top tags: {'project': 203, 'python': 92, 'discussion': 78, 'hacker-news': 78, 'business': 77}
- No actions needed


## [2026-05-13 23:19] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 77, 'capabilities': 120, 'business': 90, 'patterns': 112, 'unknown': 4}
- Top tags: {'project': 203, 'python': 92, 'discussion': 78, 'hacker-news': 78, 'business': 76}
- No actions needed


## [2026-05-13 18:05] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 75, 'capabilities': 119, 'business': 87, 'patterns': 110, 'unknown': 4}
- Top tags: {'project': 203, 'python': 92, 'discussion': 77, 'hacker-news': 77, 'business': 73}
- No actions needed


## [2026-05-13 12:11] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 75, 'capabilities': 119, 'business': 84, 'patterns': 109, 'unknown': 4}
- Top tags: {'project': 202, 'python': 92, 'discussion': 74, 'hacker-news': 74, 'business': 70}
- No actions needed


## [2026-05-13 06:06] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 74, 'capabilities': 108, 'business': 83, 'patterns': 108, 'unknown': 4}
- Top tags: {'project': 202, 'python': 92, 'discussion': 73, 'hacker-news': 73, 'business': 69}
- No actions needed


## [2026-05-13 00:06] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 73, 'capabilities': 107, 'business': 73, 'patterns': 103, 'unknown': 4}
- Top tags: {'project': 202, 'python': 92, 'discussion': 65, 'hacker-news': 65, 'business': 59}
- No actions needed


## [2026-05-12 18:06] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 73, 'capabilities': 106, 'business': 71, 'patterns': 102, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'discussion': 64, 'hacker-news': 64, 'business': 58}
- No actions needed


## [2026-05-12 12:07] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 72, 'capabilities': 98, 'business': 70, 'patterns': 99, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'discussion': 64, 'hacker-news': 64, 'business': 57}
- No actions needed


## [2026-05-12 06:07] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 68, 'capabilities': 88, 'business': 67, 'patterns': 97, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'discussion': 60, 'hacker-news': 60, 'business': 54}
- No actions needed


## [2026-05-12 00:05] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 68, 'capabilities': 86, 'business': 60, 'patterns': 96, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'discussion': 52, 'hacker-news': 52, 'business': 47}
- No actions needed


## [2026-05-11 18:05] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 67, 'capabilities': 85, 'business': 59, 'patterns': 96, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'discussion': 50, 'hacker-news': 50, 'business': 46}
- No actions needed


## [2026-05-11 12:07] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 67, 'capabilities': 84, 'business': 58, 'patterns': 95, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'discussion': 48, 'hacker-news': 48, 'business': 45}
- No actions needed


## [2026-05-11 06:06] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 67, 'capabilities': 73, 'business': 55, 'patterns': 93, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'discussion': 43, 'hacker-news': 43, 'business': 42}
- No actions needed


## [2026-05-11 00:05] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 67, 'capabilities': 72, 'business': 51, 'patterns': 91, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'discussion': 39, 'hacker-news': 39, 'business': 38}
- No actions needed


## [2026-05-10 18:05] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 66, 'capabilities': 72, 'business': 48, 'patterns': 91, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'discussion': 36, 'hacker-news': 36, 'typescript': 36}
- No actions needed


## [2026-05-10 12:03] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 66, 'capabilities': 71, 'business': 47, 'patterns': 91, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'typescript': 36, 'discussion': 34, 'hacker-news': 34}
- No actions needed


## [2026-05-10 06:05] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 65, 'capabilities': 71, 'business': 47, 'patterns': 90, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'typescript': 36, 'business': 34, 'discussion': 33}
- No actions needed


## [2026-05-10 00:03] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 65, 'capabilities': 71, 'business': 46, 'patterns': 90, 'unknown': 4}
- Top tags: {'project': 201, 'python': 91, 'typescript': 36, 'discussion': 33, 'hacker-news': 33}
- No actions needed


## [2026-05-09 18:04] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 64, 'capabilities': 71, 'business': 43, 'patterns': 88, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'business': 31, 'discussion': 30}
- No actions needed


## [2026-05-09 12:05] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 64, 'capabilities': 68, 'business': 42, 'patterns': 87, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'business': 30, 'discussion': 25}
- No actions needed


## [2026-05-09 06:05] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 64, 'capabilities': 68, 'business': 36, 'patterns': 87, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'business': 24, 'news': 21}
- No actions needed


## [2026-05-09 00:03] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 63, 'capabilities': 68, 'business': 32, 'patterns': 86, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'business': 20, 'news': 19}
- No actions needed


## [2026-05-08 21:45] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 63, 'capabilities': 68, 'business': 28, 'patterns': 85, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'news': 17, 'techcrunch': 17}
- No actions needed


## [2026-05-08 17:11] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 63, 'capabilities': 68, 'business': 28, 'patterns': 85, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'news': 17, 'techcrunch': 17}
- No actions needed


## [2026-05-08 17:02] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 63, 'capabilities': 68, 'business': 27, 'patterns': 85, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'news': 17, 'techcrunch': 17}
- No actions needed


## [2026-05-08 15:44] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 63, 'capabilities': 67, 'business': 26, 'patterns': 85, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'news': 17, 'techcrunch': 17}
- No actions needed


## [2026-05-08 10:08] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 58, 'capabilities': 59, 'business': 25, 'patterns': 82, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'news': 16}
- No actions needed


## [2026-05-08 09:55] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 58, 'capabilities': 59, 'business': 25, 'patterns': 82, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'news': 16}
- No actions needed


## [2026-05-08 09:49] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 58, 'capabilities': 59, 'business': 25, 'patterns': 82, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'news': 16}
- No actions needed


## [2026-05-08 07:55] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 58, 'capabilities': 59, 'business': 25, 'patterns': 82, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'news': 16}
- No actions needed


## [2026-05-08 03:43] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 58, 'capabilities': 59, 'business': 25, 'patterns': 82, 'unknown': 4}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'news': 16}
- No actions needed


## [2026-05-07 22:16] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 57, 'capabilities': 59, 'business': 15, 'patterns': 78}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'c++': 14}
- No actions needed


## [2026-05-07 21:36] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 57, 'capabilities': 58, 'business': 14, 'patterns': 78}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'c++': 14}
- No actions needed


## [2026-05-07 21:23] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 57, 'capabilities': 58, 'business': 14, 'patterns': 78}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'c++': 14}
- No actions needed


## [2026-05-07 21:17] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 57, 'capabilities': 58, 'business': 14, 'patterns': 78}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'c++': 14}
- No actions needed


## [2026-05-07 21:12] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 57, 'capabilities': 58, 'business': 14, 'patterns': 78}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'c++': 14}
- No actions needed


## [2026-05-07 20:42] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 57, 'capabilities': 58, 'business': 14, 'patterns': 77}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'c++': 14}
- No actions needed


## [2026-05-07 19:21] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 57, 'capabilities': 57, 'business': 13, 'patterns': 77}
- Top tags: {'project': 200, 'python': 91, 'typescript': 36, 'jupyter notebook': 16, 'c++': 14}
- No actions needed


## [2026-05-07 18:05] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 1, 'patterns': 2, 'capabilities': 1}
- Top tags: {'discussion': 2, 'hacker-news': 2, 'product': 2, 'patterns': 2, 'business': 1}
- No actions needed


## [2026-05-07 17:59] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 1, 'patterns': 2, 'capabilities': 1}
- Top tags: {'discussion': 2, 'hacker-news': 2, 'product': 2, 'patterns': 2, 'business': 1}
- No actions needed


## [2026-05-07 17:55] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 1, 'patterns': 2, 'capabilities': 1}
- Top tags: {'discussion': 2, 'hacker-news': 2, 'product': 2, 'patterns': 2, 'business': 1}
- No actions needed


## [2026-05-07 15:34] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 15:21] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 14:53] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 14:34] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 14:26] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 14:16] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 13:53] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 13:48] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 13:31] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 13:27] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 13:25] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 1, 'unknown': 6, 'patterns': 5, 'capabilities': 6}
- Top tags: {'research': 24, 'unknown': 6, 'capabilities': 6, 'discussion': 5, 'hacker-news': 5}
- No actions needed


## [2026-05-07 13:23] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 1, 'unknown': 6, 'patterns': 5, 'capabilities': 6}
- Top tags: {'research': 24, 'unknown': 6, 'capabilities': 6, 'discussion': 5, 'hacker-news': 5}
- No actions needed

