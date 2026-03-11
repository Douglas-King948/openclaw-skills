# MCA (Multimodal Capability Awakening) Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)

> 让大模型自动识别并处理用户发送的各种媒体文件

## 🌟 项目亮点

- 🖼️ **自动图片分析** - 零摩擦体验，直接发图自动分析
- 🎵 **语音自动转写** - 语音消息秒变文字摘要  
- 📄 **PDF智能提取** - 文档内容一键提取
- 📊 **表格数据分析** - Excel/CSV自动分析洞察
- 🔄 **智能降级** - 模型不支持时自动切换Python方案
- 🌐 **渠道无关** - 飞书、Discord、Telegram全支持

## 📖 完整文档

- [中文介绍](#中文介绍)
- [English README](#english-readme)
- [技术文档](SKILL.md)

## 🚀 快速开始

### 安装

```bash
# 克隆到OpenClaw skills目录
git clone https://github.com/yourusername/multimodal-awakening.git
cp -r multimodal-awakening ~/.openclaw/skills/
```

### 配置

1. 配置Gateway层媒体拦截器（详见 `scripts/gateway-interceptor.js`）
2. 重启OpenClaw Gateway
3. 直接发送媒体文件即可自动处理

## 🏗️ 架构设计

```
用户发送媒体
    ↓
Gateway层 → 下载文件 → 注入[media:type:path]标记
    ↓
Agent层 → 检测标记 → 动态工具发现 → 智能处理
    ↓
Model层 → 分析内容 → 返回结果
```

## 📚 相关文章

- [飞书深度好文：当AI遇到"不会用"](https://www.feishu.cn/docx/HoI7dhNlaoQCsJxbsmAcVJe3nxg) - 项目背后的故事

## 🤝 贡献

欢迎提交PR！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

感谢OpenClaw社区和所有支持多模态AI的开发者。

---

**⭐ Star this repo if you find it helpful!**