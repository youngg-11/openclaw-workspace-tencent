# Google Antigravity 深度分析报告

> 生成时间: 2026-03-13

---

## 一、Google Antigravity 是什么？

**Google Antigravity** 是 Google 内部的一个 **AI 编程/开发环境**，俗称"Google 的 AI IDE"。

### 核心特点

| 特点 | 说明 |
|------|------|
| **背景** | Google 内部 AI 开发工具 |
| **访问方式** | 通过 Google Cloud Code (studio. google.com/s/github) |
| **可用模型** | Claude (Opus/Sonnet) + Gemini 系列 |
| **配额** | Google 账号关联，独享配额 |

### 支持的模型

| 模型 | 说明 |
|------|------|
| Claude Opus 4.6 | 顶级推理模型 |
| Claude Sonnet 4.6 | 平衡型模型 |
| Gemini 3 Pro | Google 最新模型 |
| Gemini 3.1 Pro | 带思考能力 |
| Gemini 3 Flash | 快速响应 |

---

## 二、为什么叫"反代理"？

"反代理"是中文社区的戏称，指的是：

> **利用 Google 内部服务绕过官方限制，访问更便宜的 API**

- Google 官方 API 较贵
- Antigravity 配额更宽松、更便宜
- 通过"反代理"可以用 Google 账号访问 Claude/Gemini

---

## 三、相关竞品/工具生态

### 3.1 认证类工具 (Stars 排序)

| 工具 | Stars | 功能 |
|------|-------|------|
| **opencode-antigravity-auth** | 9,489 | OpenCode 认证插件，多账户轮换 |
| ** AntigravityQuotaWatcher** | 2,208 | 配额监控插件 |
| **vscode-antigravity-cockpit** | 3,812 | VS Code 配额监控面板 |
| **antigravity-ide** | 381 | Antigravity IDE 封装 |
| **antigravity-panel** | 454 | 配额 & 缓存监控 |

### 3.2 代理类工具

| 工具 | Stars | 功能 |
|------|-------|------|
| **zerogravity** | 614 | OpenAI/Anthropic/Gemini 兼容代理，伪装 Antigravity 流量 |
| **opencode-ag-auth** | 60 | 增强版 OAuth 插件 |
| **antigravity-proxy** | 55 | 拦截 API 调用，使用自己的 Gemini token |
| **Antigravity-cursor-proxy** | 10 | Cursor IDE 专用代理 |
| **openclaw-antigravity** | 1 | OpenClaw 用的免费代理 |

### 3.3 开源替代品

| 工具 | Stars | 说明 |
|------|-------|------|
| **open-antigravity** | 302 | 开源版 Antigravity |

---

## 四、使用风险 (⚠️重要)

根据 GitHub 文档的警告：

> **使用任何 Antigravity 代理都违反 Google 服务条款**

### 风险列表

| 风险 | 说明 |
|------|------|
| **账号封禁** | Google 账户被永久封禁 |
| **隐形限制** | Shadow ban（限制访问但无通知） |
| **配额清零** | 配额被重置 |
| **API 封禁** | IP/Token 被拉黑 |

### 建议

1. **使用小号** - 不要用主账号
2. **备选方案** - 准备好替代方案
3. **低调使用** - 不要大量请求
4. **风险自担** - 一切后果自负

---

## 五、如何使用 (技术指南)

### 5.1 通过 OpenCode

```bash
# 安装插件
opencode auth login
# 选择 Google OAuth (Antigravity)

# 使用模型
opencode run "Hello" --model=google/antigravity-claude-opus-4-6-thinking
```

### 5.2 通过代理服务

```python
# zerogravity 示例
# 配置自定义端点指向代理服务
```

---

## 六、竞品对比

| 方案 | 优点 | 缺点 | 风险 |
|------|------|------|------|
| **官方 API** | 稳定、安全 | 贵 | 无 |
| **Antigravity** | 便宜、配额多 | 违规 | 高 |
| **第三方代理** | 灵活 | 不稳定 | 高 |
| **开源替代** | 免费 | 功能弱 | 中 |

---

## 七、总结

### 核心要点

1. **Google Antigravity** 是 Google 内部的 AI 编程工具
2. 可以通过它访问 **Claude + Gemini** 模型
3. 配额比官方 API 更宽松
4. 但**违反 Google 服务条款**，有封号风险

### 适用人群

| 用户 | 推荐度 |
|------|--------|
| 开发者想省成本 | ⚠️ 谨慎 |
| 研究人员 | ⚠️ 谨慎 |
| 普通用户 | ❌ 不推荐 |

### 替代方案

| 方案 | 价格 | 稳定性 |
|------|------|--------|
| 官方 Gemini API | 中等 | 高 |
| Claude API | 中等 | 高 |
| Azure OpenAI | 中等 | 高 |

---

**声明**：本报告仅供技术研究参考，使用第三方代理服务需自担风险。
