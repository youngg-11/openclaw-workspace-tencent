# 免费 + 本地大模型 AI写作工具大全

> 生成时间: 2026-03-13

---

## 一、本地大模型部署方案

### 1.1 Ollama (⭐最推荐)

**基本信息**
- 官网: ollama.com
- 免费开源
- 支持 Mac/Linux/Windows

**支持模型**
- Llama 3.1 / 3.2
- Qwen (通义千问)
- Phi、Gemma、Mistral
- 中文模型: qwen:7b, yi:34b 等

**如何使用**
```bash
# 安装
curl -fsSL https://ollama.com/install.sh | sh

# 运行模型
ollama run qwen:7b

# API调用
curl http://localhost:11434/api/generate -d '{"model": "qwen:7b", "prompt": "写一篇短文"}'
```

**优点**
✅ 完全免费
✅ 本地部署，隐私安全
✅ 无API费用
✅ 资源要求适中 (7B模型需 8GB RAM)

**缺点**
❌ 需要一定的技术能力
❌ 顶级模型需要GPU

---

### 1.2 LM Studio

**基本信息**
- 官网: lmstudio.ai
- 桌面客户端
- 免费

**特点**
- 图形界面友好
- 一键下载模型
- 内置 API 服务

**优点**
✅ 安装即用
✅ 界面美观
✅ 支持多模型

---

### 1.3 Jan.ai

**基本信息**
- 官网: jan.ai
- 开源免费

**特点**
- 类似 ChatGPT 界面
- 本地部署
- 支持多种模型

---

## 二、免费开源AI写作客户端

### 2.1 SillyTavern (免费)

**官网**:.sillytavern.github.io

**特点**
- AI聊天/写作界面
- 支持本地Ollama
- 支持远程API
- 免费开源

**适用场景**
- 角色扮演
- 创意写作
- 对话生成

---

### 2.2 ChatGLM UI (免费)

**开源地址**: github.com/THUDM/ChatGLM3

**特点**
- 清言模型配套
- 完全免费
- 中文优化

---

### 2.3 TextGen WebUI (免费)

**开源地址**: github.com/oobabooga/text-generation-webui

**特点**
- 历史最悠久
- 插件丰富
- 支持多种后端

---

### 2.4 AI Blog Writer (免费)

**开源地址**: github.com/dsk-dev-ai/ai-blog-writer

**特点**
- 专为博客设计
- Flask + Ollama
- 100%本地运行

---

### 2.5 OpenOffice AI (免费)

**开源地址**: github.com/Hariprasadrio/OpenOfficeAI

**特点**
- 集成 OpenOffice
- 写作润色
- 翻译功能

---

## 三、免费云端AI写作工具 (无需本地部署)

### 3.1 Poe (免费额度)

**官网**: poe.com

**特点**
- 免费版有 Claude/GPT额度
- 快速生成
- 写作模板

**免费额度**
- 每天 1 次 Claude 3.5 Sonnet
- 每周 1000 Credits

---

### 3.2 Claude.ai (免费)

**官网**: claude.ai

**特点**
- 免费使用 Claude 3.5
- 写作能力强
- 中文优秀

**限制**
- 需要海外账号

---

### 3.3 ChatGPT 免费版

**官网**: chat.openai.com

**特点**
- GPT-4o 有限免费
- 写作能力强大

---

### 3.4 秘塔写作猫 (免费版)

**官网**: xiezuocat.com

**特点**
- 免费版有额度
- 中文纠错强
- 适合办公

---

### 3.5 Kimi (免费)

**官网**: kimi.moonshot.cn

**特点**
- 免费使用
- 长文本处理强
- 中文优化好
- 支持100万字上下文

---

### 3.6 讯飞星火 (免费)

**官网**: xfyun.cn

**特点**
- 免费额度充足
- 多种能力
- 中文优化

---

## 四、本地AI写作工具组合推荐

### 方案一: 入门级 (免费)

| 组件 | 工具 | 费用 |
|------|------|------|
| 模型 | Ollama (qwen:7b) | 免费 |
| 界面 | LM Studio | 免费 |
| 总成本 | - | **0元** |

**要求**
- 8GB+ RAM
- Mac/Linux/Windows

---

### 方案二: 进阶级 (免费)

| 组件 | 工具 | 费用 |
|------|------|------|
| 模型 | Ollama (qwen:72b) | 免费 |
| 界面 | SillyTavern | 免费 |
| 增强 | SillyTavern 插件 | 免费 |
| 总成本 | - | **0元** |

**要求**
- 24GB+ RAM
- 或 GPU: 24GB VRAM

---

### 方案三: 中文优化 (免费)

| 组件 | 工具 | 费用 |
|------|------|------|
| 模型 | ChatGLM3-6B | 免费 |
| 界面 | ChatGLM WebUI | 免费 |
| 总成本 | - | **0元** |

**要求**
- 13GB+ RAM

---

## 五、一键部署方案

### 5.1 AI写作助手 (Docker)

```bash
# 一键启动
docker run -d -p 8080:8080 \
  -v ./data:/data \
  ghcr.io/ollama/ollama:latest

# 访问 http://localhost:8080
```

### 5.2 完整写作环境

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 下载中文模型
ollama pull qwen:7b
ollama pull yi:34b

# 运行
ollama serve

# 配合写作工具 (如 LM Studio)
```

---

## 六、对比总结

| 方案 | 成本 | 难度 | 质量 | 推荐指数 |
|------|------|------|------|----------|
| Ollama + LM Studio | ⭐免费 | ⭐简单 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Kimi/讯飞星火 | ⭐免费 | ⭐简单 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| ChatGPT/Claude免费版 | ⭐免费 | ⭐简单 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 自建 ChatGLM | ⭐免费 | ⭐中等 | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 七、最佳实践建议

### 日常写作
1. **Kimi** - 免费+中文好+长文本
2. **讯飞星火** - 免费额度多

### 隐私敏感/离线
1. **Ollama + LM Studio** - 完全本地
2. **ChatGLM3-6B** - 中文优化

### 专业创作
1. **Ollama (qwen:72b)** - 能力强
2. **搭配 SillyTavern** - 界面好

### 零成本方案
**Kimi + 秘塔写作猫免费版 + Poe 免费额度 = 完全免费满足所有写作需求**
