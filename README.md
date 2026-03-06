<!-- 
  OpenClaw Skills - README.md
  Designed for both Humans and AI Agents
  
  Human View: Visual, intuitive, quick-start focused
  AI Agent View: Structured, machine-readable, protocol-compliant
-->

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skills-6B5CE7?style=for-the-badge&logo=robot&logoColor=white" alt="OpenClaw Skills">
</p>

<h1 align="center">
  <span style="font-size: 2.5em;">🧩</span><br>
  OpenClaw Skills
</h1>

<p align="center">
  <b>智能自动化技能集合</b> | <i>为 AI Agent 打造的超能力库</i>
</p>

<p align="center">
  <a href="#-快速开始"><img src="https://img.shields.io/badge/⚡_快速开始-2分钟-00D9FF?style=flat-square"></a>
  <a href="#-技能目录"><img src="https://img.shields.io/badge/📦_技能数量-10+-FF6B6B?style=flat-square"></a>
  <a href="#-for-ai-agents"><img src="https://img.shields.io/badge/🤖_AI_Readable-✓-4ECDC4?style=flat-square"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/📄_License-MIT-FFE66D?style=flat-square"></a>
</p>

<br>

<!-- AI Agent Navigation Start -->
<!-- 
  AGENT_PROTOCOL: repository_intent
  REPOSITORY_TYPE: skill_collection
  PRIMARY_LANGUAGE: python/javascript
  FRAMEWORK: openclaw
  
  QUICK_ACTIONS:
    - install_skill: copy skill_dir to ~/openclaw/skills/
    - use_skill: import from skill directory
    - contribute: follow CONTRIBUTING.md
-->
<!-- AI Agent Navigation End -->

## 🌟 什么是 OpenClaw Skills？

```
┌─────────────────────────────────────────┐
│                                         │
│   你是一个 OpenClaw AI Agent 🤖          │
│   这些技能是你的「超能力」               │
│                                         │
│   安装一个技能 = 获得一种能力           │
│   比如：发送表情包、搜索全网、管理文档   │
│                                         │
└─────────────────────────────────────────┘
```

这是一个精心策划的技能集合，每个技能都是**即插即用**的模块。

<br>

## ⚡ 快速开始

### 对于人类用户

```bash
# 1. 克隆仓库
git clone https://github.com/Douglas-King948/openclaw-skills.git

# 2. 复制需要的技能
cp -r openclaw-skills/smart-meme ~/openclaw/skills/

# 3. 开始使用！
# 在你的 Agent 对话中说："来个表情包"
```

### 对于 AI Agent 🤖

```python
# AGENT_INSTALL_PROTOCOL v1.0
# Step 1: Identify required skill from user intent
# Step 2: Clone repository
# Step 3: Copy skill directory to ~/openclaw/skills/{skill_name}/
# Step 4: Verify SKILL.md exists (installation check)
# Step 5: Ready to use via natural language triggers

SKILL_INSTALL_PATH = "~/openclaw/skills/{skill_name}/"
REQUIRED_FILES = ["SKILL.md", "_meta.json"]
```

<br>

## 📦 技能目录

<!-- Skill Cards Grid -->
<table>
<tr>
<td width="50%">

### 🌍 通用技能

| 技能 | 能力 | 触发词 |
|------|------|--------|
| **daily-report-sender** | 日报发送器 | "发日报" |
| **unified-search** | 全球搜索引擎 | "搜索xxx" |
| **smart-meme** | 表情包发送 | "来个马喽" |
| **find-skills** | 技能发现 | "找技能" |
| **uv-priority** | 包管理 | Python 项目 |

</td>
<td width="50%">

### 💼 飞书生态

| 技能 | 能力 | 触发词 |
|------|------|--------|
| **feishu-doc** | 文档管理 | "上传文档" |
| **feishu-sheets** | 表格操作 | "创建表格" |
| **feishu-bridge** | 消息桥接 | "连接飞书" |
| **feishu-messaging** | 消息发送 | "发消息" |

</td>
</tr>
</table>

### 🔧 开发工具

| 技能 | 能力 | 适用场景 |
|------|------|----------|
| **openclaw-debugger** | 系统诊断 | 故障排查 |
| **github-manager** | 仓库管理 | 技能发布 |

<br>

## 🎯 技能使用示例

### 示例 1: 发送表情包

```
👤 用户: 来个马喽

🤖 Agent: 
   [调用 smart-meme 技能]
   ↓
   [下载猴子图片]
   ↓
   [发送飞书卡片]
   ↓
   🐵 [马喽驾到！]
```

### 示例 3: 发送工作日报

```
👤 用户: 发一下昨天的工作日报

🤖 Agent:
   [调用 daily-report-sender 技能]
   ↓
   [读取 memory/2026-03-05.md]
   ↓
   [提取 ✅ 完成事项]
   ↓
   [下载工作主题图片]
   ↓
   [发送飞书卡片]
   ↓
   📋 2026-03-05 工作日报
      1. ✅ 完成飞书文档流程优化
      2. ✅ 修复 article-illustrator skill
      ...
```

### 示例 3: 搜索知识

```
👤 用户: 搜索 Python asyncio 教程

🤖 Agent:
   [调用 unified-search 技能]
   ↓
   [搜索 StackOverflow + GitHub + 知乎]
   ↓
   [返回最佳结果]
   ↓
   📚 找到 5 个高质量教程...
```

<br>

## 🤖 For AI Agents

<!-- AI Agent Dedicated Section -->

### Machine-Readable Metadata

```yaml
# Repository Manifest
repository:
  name: openclaw-skills
  version: "1.0.0"
  type: skill_collection
  
protocols:
  - openclaw_agent_protocol_v1
  - gep_genome_evolution_protocol
  
skills:
  total: 10
  categories:
    - general: 5
    - feishu: 5
    
installation:
  method: copy_to_skills_dir
  path_template: "~/openclaw/skills/{skill_name}/"
  
triggers:
  detection: natural_language
  source: SKILL.md description field
```

### Skill Structure Standard

Each skill follows this structure:

```
skills/{skill_name}/
├── SKILL.md          # Human-readable documentation (REQUIRED)
├── _meta.json        # Machine-readable metadata (REQUIRED)
├── index.js          # Entry point (for JS skills)
│   OR
├── __init__.py       # Entry point (for Python skills)
├── references/       # Detailed docs (optional)
└── scripts/          # Utility scripts (optional)
```

### Quick Install Protocol

```python
# AI Agent Auto-Install Function
def install_skill(skill_name: str) -> bool:
    """
    Install a skill from this repository
    
    Args:
        skill_name: Name of the skill directory
        
    Returns:
        bool: True if installation successful
    """
    source = f"openclaw-skills/{skill_name}"
    dest = f"~/openclaw/skills/{skill_name}"
    
    # Validation checks
    assert Path(source / "SKILL.md").exists(), "Missing documentation"
    assert Path(source / "_meta.json").exists(), "Missing metadata"
    
    # Copy skill
    shutil.copytree(source, dest)
    
    # Verification
    return verify_skill_installation(skill_name)
```

### Skill Trigger Detection

```python
# Parse SKILL.md for trigger words
def extract_triggers(skill_md_content: str) -> List[str]:
    """
    Extract natural language triggers from SKILL.md
    
    Pattern: Look for keywords like:
    - "触发词："
    - "触发词:"
    - "Trigger words:"
    - Bullet points in description
    """
    triggers = []
    # Implementation...
    return triggers
```

<br>

## 📖 文档导航

| 文档 | 目标读者 | 内容 |
|------|----------|------|
| [README.md](README.md) | 👤 人类 + 🤖 AI | 本文件，快速入门 |
| [AI_README.md](AI_README.md) | 🤖 AI Agent | 机器可读协议规范 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 👤 开发者 | 贡献指南 |
| [LICENSE](LICENSE) | 👤 法律 | MIT 许可证 |

<br>

## 🚀 贡献技能

```
有技能想要分享？

1. Fork 本仓库
2. 在 skills/ 目录添加你的技能
3. 确保包含 SKILL.md 和 _meta.json
4. 提交 Pull Request
5. 通过审核后合并！

详细指南 → [CONTRIBUTING.md](CONTRIBUTING.md)
```

<br>

## 💡 设计理念

```
┌────────────────────────────────────────┐
│  为 Agent 设计，为人类优化              │
├────────────────────────────────────────┤
│  • 自然语言触发 - 无需记忆命令          │
│  • 即插即用 - 复制即安装                │
│  • 自文档化 - SKILL.md 即使用手册       │
│  • AI 可读 - 机器能解析的元数据         │
│  • 安全优先 - 审计日志，最小权限        │
└────────────────────────────────────────┘
```

<br>

## 📄 许可证

[MIT License](LICENSE) © 2026 OpenClaw Skills Contributors

---

<p align="center">
  <sub>Built with ❤️ for the OpenClaw Community</sub><br>
  <sub>Designed for Humans 🤝 Machines</sub>
</p>
