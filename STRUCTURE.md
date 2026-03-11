# Repository Structure

```
openclaw-skills/
├── 📄 README.md              # 主文档（人类 + AI 可读）
├── 🤖 AI_README.md           # AI Agent 专用协议文档
├── 🤝 CONTRIBUTING.md        # 贡献指南
├── 📄 LICENSE                # MIT 许可证
├── ⚙️ .gitattributes         # Git 配置
│
├── 🌍 通用技能/              # General purpose skills
│   ├── unified-search/       # 全球统一搜索引擎
│   ├── smart-meme/           # 智能表情包系统
│   ├── find-skills/          # 技能发现工具
│   ├── uv-priority/          # Python uv 包管理
│   └── openclaw-debugger/    # 系统诊断工具
│
└── 💼 飞书生态/              # Feishu ecosystem
    ├── feishu-doc-manager/   # 文档管理
    ├── feishu-sheets-skill/  # 表格操作
    ├── feishu-messaging/     # 消息发送
    ├── feishu-bridge/        # WebSocket桥接
    └── feishu-md-uploader/   # Markdown上传
```

## 技能目录结构

每个技能遵循标准结构：

```
skill-name/
├── SKILL.md              # 📘 技能文档（必需）
│   └── 包含：描述、触发词、使用示例
│
├── _meta.json            # 📋 元数据（必需）
│   └── 包含：版本、触发器、入口点
│
├── index.js              # 🔵 JS 入口（如果是 JS 技能）
│   或
├── __init__.py           # 🐍 Python 入口（如果是 Python 技能）
│
├── references/           # 📚 参考文档（可选）
│   └── api-reference.md
│
├── scripts/              # 🔧 工具脚本（可选）
│   └── utils.py
│
└── assets/               # 🎨 资源文件（可选）
    └── templates/
```

## 文件命名约定

- **技能名称**: kebab-case (e.g., `smart-meme`, `feishu-bridge`)
- **文档**: `README.md`, `SKILL.md` (大写)
- **代码**: 小写，使用下划线或驼峰
- **配置**: `_meta.json`, `.clawhub/origin.json`

## 快速导航

| 你想做什么 | 查看文件 |
|-----------|---------|
| 了解项目 | [README.md](README.md) |
| 我是 AI Agent | [AI_README.md](AI_README.md) |
| 贡献技能 | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 查看许可证 | [LICENSE](LICENSE) |
