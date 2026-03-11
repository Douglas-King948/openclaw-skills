# Contributing to MCA Framework

感谢您对 MCA (Multimodal Capability Awakening) 框架的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 1. 报告问题

如果您发现了 bug 或有功能建议，请通过 GitHub Issues 提交：

- 使用清晰的标题描述问题
- 提供复现步骤
- 说明您的环境（操作系统、OpenClaw 版本等）

### 2. 提交代码

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的修改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 3. 代码规范

- 保持代码简洁清晰
- 添加必要的注释
- 确保不引入新的渠道特定依赖
- 更新相关文档

### 4. 测试

在提交 PR 前，请确保：
- 代码可以在干净的 OpenClaw 环境中运行
- 不破坏现有功能
- 新增功能有基本的使用示例

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/wangguangdong1/multimodal-awakening.git
cd multimodal-awakening

# 安装开发依赖（可选）
pip install -r requirements.txt

# 复制到 OpenClaw skills 目录进行测试
cp -r . ~/.openclaw/skills/multimodal-awakening
```

## 联系我们

- GitHub Issues: [项目Issues页面](https://github.com/wangguangdong1/multimodal-awakening/issues)
- 飞书文档讨论区

## 行为准则

- 保持友善和尊重
- 接受建设性的批评
- 专注于对社区最有利的事情

再次感谢您的贡献！