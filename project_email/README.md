# project_email

## 目标
在云端服务器部署 24x7 在线的邮箱验证码监听服务（OTP Watcher），支持多邮箱（126/Gmail/Outlook/QQ），实时提取验证码并推送到飞书。

## 当前状态
- 状态：初始化完成（仅文档与项目结构）
- 部署：未开始
- 代理：不使用代理（用户已确认）

## 架构（计划）
1. 独立常驻服务（systemd）负责 IMAP IDLE 监听
2. 提取 OTP（4-8 位数字 + 关键词规则）
3. 通过 OpenClaw 消息能力推送到飞书
4. 去重、防刷、最小化日志

## 目录结构
- `requirements.md`：需求与约束
- `conversation-log.md`：关键对话摘要
- `memory.md`：项目长期记忆（非敏感）
- `secrets.template.env`：凭据模板（不存真实密钥）
- `runbook.md`：部署与运维操作手册
- `CHANGELOG.md`：变更记录

