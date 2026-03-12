---
name: agent-browser
description: 浏览器自动化工具。用于网页抓取、截图、交互。触发场景：用户要求打开网页、截图、点击元素、填写表单。
---

# Browser Automation

## 核心命令
- 打开网页: `browser action=open url="链接"`
- 截图: `browser action=screenshot`
- 快照: `browser action=snapshot`
- 点击: `browser action=act request={"kind":"click","ref":"元素"}`
- 输入: `browser action=act request={"kind":"type","ref":"元素","text":"内容"}`

## 规则
- 必须使用 OpenClaw browser 工具
- 禁止使用 Puppeteer/Playwright
