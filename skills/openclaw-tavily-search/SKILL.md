---
name: tavily-search
description: Tavily搜索工具。触发场景：用户要求搜索网页、查找资料、获取链接。
---

# 搜索工具

## 工具
- tavily_search: 一般搜索，快速获取结果
- tavily_research: 深度研究，复杂话题
- tavily_extract: 提取特定网页内容
- tavily_crawl: 爬取整个网站

## 规则
- 默认返回热度前10结果（按score降序）
- 每个结果提炼5个核心要点
- 链接使用完整可点击链接形式

## 参数
- tavily_search: query + count:10 + searchDepth:"advanced"
- tavily_research: query + depth:"comprehensive"

## 输出格式
## [话题] 搜索结果
### 1. [标题]
🔗 [完整链接] | 📊 热度: XX.X

**核心要点：**
1. 要点1
2. 要点2
...
