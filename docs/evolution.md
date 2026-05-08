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

