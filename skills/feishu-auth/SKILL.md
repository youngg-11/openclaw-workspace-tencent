---
name: feishu-auth
description: 飞书授权与权限管理。触发场景：调用飞书API时遇到need_user_authorization错误。
---

# 飞书授权

## 触发
遇到 `need_user_authorization` 错误时

## 处理流程
1. 使用 `feishu_oauth_batch_auth` 批量授权（一次性通过67个权限）
2. 等待用户点击授权链接（返回 auth-complete）
3. 重新执行操作

## 规则
- 首次使用飞书工具时，直接用批量授权
- 权限更新后需重新批量授权
