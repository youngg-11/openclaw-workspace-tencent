# TOOLS.md - Local Notes

## GitHub 备份仓库

| 环境 | 仓库名 | 说明 |
|------|--------|------|
| **云端 (腾讯云)** | `openclaw-workspace-tencent` | 公开仓库 |
| **云端 (腾讯云)** | `openclaw-config-backup-tencent` | 私有仓库 |
| **本地 (Windows)** | `openclaw-workspace` | 公开仓库 |
| **本地 (Windows)** | `openclaw-config-backup` | 私有仓库 |

**规律**：带 `tencent` = 云端，不带 = 本地

---

## 备份/恢复时必问

1. **云端还是本地？**
2. **用哪个仓库？**

---

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
