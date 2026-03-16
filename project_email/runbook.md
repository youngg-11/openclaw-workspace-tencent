# Runbook - project_email

## 部署前检查
- [ ] 已准备邮箱应用专用密码（非主密码）
- [ ] 已确认 IMAP 已开启
- [ ] 已确认飞书推送目标

## 计划中的服务命令（待实现）
- 启动：`systemctl start otp-watcher`
- 状态：`systemctl status otp-watcher`
- 日志：`journalctl -u otp-watcher -f`
- 重启：`systemctl restart otp-watcher`

## 故障排查方向
1. IMAP 登录失败（授权码/IMAP未开启）
2. 邮件已到但未触发（IDLE连接中断/网络抖动）
3. 提取失败（正文编码或正则不匹配）
4. 推送失败（通道目标/权限）

