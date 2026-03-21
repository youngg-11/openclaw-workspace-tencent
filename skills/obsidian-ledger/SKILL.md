---
name: obsidian-ledger
description: 自动识别图片中的账单/打卡等消费或活动信息，并写入 Obsidian Base 记账表
---

# Obsidian 记账 Skill

## 功能
自动识别用户发送的图片中的消费记录、每日打卡数据、活动信息，并写入 Obsidian 记账 Base。

## 触发场景
- 用户发送包含消费金额的图片（账单、支付截图）
- 用户发送每日打卡截图
- 用户说"记账"

## 工作流程

### 1. 识别图片内容
读取图片，提取关键信息：
- 消费：金额、商品名称、支付方式、订单号
- 打卡：积分、学习时间、运动时间、饮水量等
- 订阅：平台名称、费用、订阅周期

### 2. 写入 Obsidian
通过 SSH 连接到用户本地 Windows，写入文件。

**连接信息：**
- Host: 100.106.60.94
- User: admin
- Private Key: /root/.ssh/id_ed25519

**Base 路径：**
```
D:\R-资源管理\OB仓库文件夹\Obsidian仓库\06 Base-数据库\记账\
```

**Base 文件：**
- `每日记账.base` - 主记账表

### 3. 创建记账笔记

文件命名格式：`YYYY-MM-DD-描述.md`

**Frontmatter 模板：**
```yaml
---
date: YYYY-MM-DD
type: 类型
amount: 金额
category: 类别
description: 描述
status: done
tags: [ledger]
---
```

**类型分类：**
- 费用：价格、买、付、花、充值
- 工作：会议、项目、任务
- 学习：看书、文章、新技能
- 生活：打卡、积分、运动
- 想法：灵感、创意、计划
- 社交：见了谁、聊了什么

### 4. Base 筛选条件

每日记账.base 的 filters 使用：
```yaml
filters:
  and:
    - file.hasTag("ledger")
```

### 5. 写入命令

```bash
# 通过 SSH 连接到本地
ssh -i /root/.ssh/id_ed25519 admin@100.106.60.94

# 写入文件示例
scp -i /root/.ssh/id_ed25519 <本地文件> admin@100.106.60.94:"D:\\R-资源管理\\OB仓库文件夹\\Obsidian仓库\\06 Base-数据库\\记账\\"
```

## 智能识别规则

### 自动识别关键词
- 价格：¥、$、元、块、119、99 等数字
- 消费：买、付、花、支付、订阅
- 时间：今天、昨天、学习2小时、运动30分钟

### 主动确认
遇到不确定的信息，主动问用户确认：
- 金额是多少？
- 这是什么费用？
- 需要记到什么类别？

## 示例

### 示例1：消费记录
输入：ChatGPT Plus 订阅 119元截图
输出：
```yaml
---
date: 2026-03-20
type: 费用
amount: 119
category: AI订阅
description: RunningHub/ChatGPT Plus 月费订阅
status: done
tags: [ledger]
---
```

### 示例2：每日打卡
输入：打卡截图显示积分220、运动30分钟
输出：
```yaml
---
date: 2026-03-20
type: 生活
category: 每日打卡
description: 积分220，运动30分钟，学习2.5小时
status: done
tags: [ledger]
---
```

## 注意事项
1. 仔细识别图片中的文字，不要漏看金额
2. 主动推测相关信息（如订阅到期日）
3. 写入后提醒用户刷新 Obsidian
4. 如果 Base 不显示数据，检查 file.hasTag() 筛选条件是否正确
