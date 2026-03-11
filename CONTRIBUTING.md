# Contributing to OpenClaw Skills

感谢你对 OpenClaw Skills 的兴趣！本指南帮助你快速贡献技能。

## 🎯 贡献流程

```
1. Fork 仓库
    ↓
2. 创建你的技能
    ↓
3. 测试验证
    ↓
4. 提交 PR
    ↓
5. 审核合并
```

## 📋 技能标准

### 必需文件

```
my-skill/
├── SKILL.md          # 技能文档（必需）
├── _meta.json        # 元数据（必需）
├── index.js          # 入口文件（JS技能）
│   或
├── __init__.py       # 入口文件（Python技能）
└── (其他文件...)
```

### SKILL.md 模板

```markdown
---
name: my-skill
description: |
  简短描述技能功能。
  
  **触发词：**
  - "关键词1" → 功能A
  - "关键词2" → 功能B
  
  **使用示例：**
  ```
  用户：关键词1
  Agent：执行结果
  ```
version: 1.0.0
author: your-name
---

# My Skill

## 功能说明
...

## 安装
...

## 使用
...

## 配置
...
```

### _meta.json 模板

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "简短描述",
  "triggers": ["关键词1", "关键词2"],
  "entry_point": "index.js",
  "language": "javascript",
  "dependencies": [],
  "permissions": ["read", "write"]
}
```

## 🧪 测试检查清单

提交前请确认：

- [ ] SKILL.md 包含清晰的触发词
- [ ] _meta.json 格式正确
- [ ] 代码可以正常运行
- [ ] 没有硬编码的敏感信息
- [ ] 添加了必要的错误处理

## 📝 提交规范

### Commit Message 格式

```
type(scope): subject

body

footer
```

**Types:**
- `feat`: 新技能
- `fix`: 修复bug
- `docs`: 文档更新
- `refactor`: 重构
- `test`: 测试

**示例：**
```
feat(smart-meme): 添加鸭子表情包支持

- 新增 ducks 分类
- 添加嘎嘎关键词
- 更新 URL 源
```

## 🎨 设计原则

1. **单一职责** - 一个技能只做一件事
2. **自然语言** - 触发词要符合日常用语
3. **即插即用** - 复制即可使用
4. **自文档化** - SKILL.md 就是使用手册

## 🔒 安全要求

- ❌ 不要提交 API Key、Token
- ❌ 不要提交密码、密钥
- ✅ 使用环境变量读取敏感信息
- ✅ 添加输入验证
- ✅ 处理异常情况

## 📞 需要帮助？

- 查看 [AI_README.md](AI_README.md) 了解技术细节
- 在 Issues 中提问
- 参考现有技能实现

## 📄 许可证

贡献即表示你同意你的代码使用 MIT 许可证。

---

**Happy Coding! 🚀**
