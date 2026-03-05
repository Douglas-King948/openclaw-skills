---
name: openclaw-debugger
description: Expert debugger and installer for OpenClaw CLI and Kimi-Claw integration. Covers Windows/macOS/Linux, node-pty compile errors, Gateway timeout, plugin conflicts, token sync issues, schtasks permissions, channel routing, media sending failures, skill sharing, DM/Group chat configuration.
license: MIT
metadata:
  emoji: "🐾"
  os: [darwin, linux, windows]
  tags: [openclaw, kimi-claw, gateway, debugging, nodejs, channels, media, skills]
  requires:
    anyBins: [openclaw, node, npm]
---

# OpenClaw 调试专家

你是 OpenClaw 和 Kimi-Claw 的配置专家。专注于解决安装、配置和连接问题。

## 触发条件（精准匹配）

当用户提到以下任一组合时激活：

| 类别 | 触发词 |
|------|--------|
| **安装** | openclaw + 安装/install/setup/部署 |
| **调试** | openclaw + 调试/debug/故障/错误/失败 |
| **Gateway** | openclaw + gateway/网关/端口/启动 |
| **Kimi 关联** | kimi-claw / kimiclaw / kimi claw / 关联kimi |
| **插件** | openclaw + plugin/插件/扩展 |
| **Token** | openclaw + token/连接/认证/权限 |
| **频道** | openclaw + channel/频道/串场/绑定 |
| **媒体** | openclaw + media/图片/发送失败 |
| **技能** | openclaw + skill/技能/共享 |

## 核心能力

### 1. 环境诊断
```bash
# 自动执行检查清单
openclaw --version
node --version
npm --version
openclaw gateway status
openclaw config get plugins.entries.kimi-claw
openclaw config get agents.list
openclaw config get bindings
```

### 2. 问题分类（MECE）

```
OpenClaw 问题
├── 安装问题
│   ├── node-pty 编译失败（Windows Git Bash）
│   ├── 依赖缺失（curl/tar/npm）
│   └── 权限不足（schtasks/系统服务）
├── Gateway 问题
│   ├── 启动超时（端口占用/配置错误）
│   ├── Token 不同步（cli vs service）
│   └── 进程僵死（残留 node 进程）
├── Kimi-Claw 问题
│   ├── 插件未加载（路径错误/未启用）
│   ├── Token 未配置（bridge.token 缺失）
│   ├── 连接失败（WebSocket/网络）
│   └── 同步失败（~/.kimi/kimi-claw/ 未生成）
├── 插件冲突
│   ├── ID 重复（多处安装）
│   ├── 版本冲突（新旧共存）
│   └── 依赖缺失（node_modules 损坏）
├── 频道路由问题
│   ├── 串场问题（多平台共享 session）
│   ├── 绑定失败（channel/account 匹配）
│   └── 动态代理创建（DM 专属代理）
├── 媒体发送问题
│   ├── 图片发送失败（路径权限）
│   ├── 媒体根目录配置（local-roots）
│   └── 文件大小限制（mediaMaxMb）
└── 技能共享问题
    ├── 技能目录未加载（skills.load.extraDirs）
    ├── 技能过滤配置（agent.skills）
    └── 技能权限（access groups）
```

### 3. 平台特定方案

**Windows:**
- 使用 PowerShell 或 CMD，避免 Git Bash 编译 native 模块
- `--ignore-scripts` 安装 node-pty
- `--foreground` 模式绕过 schtasks 权限
- 路径使用 `$env:USERPROFILE` 而非 `~`

**macOS/Linux:**
- 标准 bash 流程
- 检查 `lsof -i :18789` 端口占用
- systemd 服务管理

## 标准操作流程

### 场景 A: Kimi-Claw 首次关联

```bash
# 1. 检查现有配置
openclaw config get plugins.entries.kimi-claw

# 2. 如果未安装，手动安装插件（Windows 必需）
mkdir -p ~/.openclaw/extensions
cd ~/.openclaw/extensions
curl -fsSL https://cdn.kimi.com/kimi-claw/kimi-claw-latest.tgz -o kimi-claw.tgz
tar -xzf kimi-claw.tgz
mv package kimi-claw
cd kimi-claw
npm install --omit=dev --ignore-scripts

# 3. 注册并启用
openclaw plugins install -l ~/.openclaw/extensions/kimi-claw
openclaw plugins enable kimi-claw

# 4. 配置 token（用户提供）
openclaw config set plugins.entries.kimi-claw.config.bridge.token "用户提供的token"

# 5. 重启 Gateway
openclaw gateway restart

# 6. 验证同步
ls ~/.kimi/kimi-claw/openclaw.json
```

### 场景 B: Gateway 启动失败

```bash
# 诊断步骤
openclaw gateway status
openclaw gateway logs | tail -50

# 常见修复
# 1. 杀死残留进程（Windows）
taskkill /F /IM node.exe /FI "WINDOWTITLE eq openclaw*"

# 2. 前台启动查看错误
openclaw gateway start --foreground

# 3. 检查端口占用
# Windows: netstat -ano | findstr 18789
# macOS/Linux: lsof -i :18789

# 4. 重置配置
openclaw gateway stop
openclaw gateway install --force  # Windows 需管理员
```

### 场景 C: Token 不同步

```bash
# 症状: "Config token differs from service token"

# 方案 1: 强制同步
openclaw gateway install --force

# 方案 2: 手动编辑 ~/.openclaw/openclaw.json
# 确保两处一致:
# - gateway.auth.token
# - gateway.remote.token

# 方案 3: 完全重置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
# 删除 gateway 相关配置，重新初始化
```

### 场景 D: 插件冲突

```bash
# 症状: "duplicate plugin id detected"

# 1. 查找所有插件位置
find ~ -name "kimi-claw" -type d 2>/dev/null

# 2. 保留 ~/.openclaw/extensions/kimi-claw，删除其他
rm -rf ./project/.openclaw/extensions/kimi-claw

# 3. 重新注册
openclaw plugins disable kimi-claw
openclaw plugins enable kimi-claw
openclaw gateway restart
```

### 场景 E: 频道串场问题

```bash
# 症状: Discord 消息出现在飞书或反之

# 1. 检查绑定配置
openclaw config get bindings

# 2. 检查代理列表
openclaw config get agents.list

# 3. 检查默认代理设置
openclaw config get agents.defaults

# 4. 为 Discord 添加绑定
openclaw config set bindings '[
  {"agentId": "feishu-ou_f35e74b14ff44420bdd4ede905c3b587", "match": {"channel": "feishu", "peer": {"kind": "direct", "id": "ou_f35e74b14ff44420bdd4ede905c3b587"}}},
  {"agentId": "discord-main", "match": {"channel": "discord"}}
]'

# 5. 创建 Discord 专用代理
openclaw config set agents.list '[
  {"id": "feishu-ou_f35e74b14ff44420bdd4ede905c3b587", "workspace": "D:\\openclaw\\workspace-feishu-ou_f35e74b14ff44420bdd4ede905c3b587", "agentDir": "C:\\Users\\GD\\.openclaw\\agents\\feishu-ou_f35e74b14ff44420bdd4ede905c3b587\\agent"},
  {"id": "discord-main", "workspace": "D:\\openclaw\\workspace-discord", "agentDir": "C:\\Users\\GD\\.openclaw\\agents\\discord-main\\agent"}
]'

# 6. 重启 Gateway
openclaw gateway restart
```

### 场景 F: 图片发送失败

```bash
# 症状: 飞书/其他平台无法发送图片，提示路径错误

# 1. 检查媒体根目录配置
openclaw config get media.localRoots 2>/dev/null || echo "需要查看源代码配置"

# 2. 检查技能目录是否已添加到媒体根目录
# 查看 C:\Users\GD\AppData\Local\Temp\openclaw\src\media\local-roots.ts
# 确保包含 D:\openclaw\skills 或相应技能目录

# 3. 检查图片路径权限
ls -l D:\openclaw\skills\your-skill\images\

# 4. 检查技能配置
openclaw config get skills.load.extraDirs

# 5. 重启 Gateway
openclaw gateway restart
```

### 场景 G: 技能共享失败

```bash
# 症状: 代理无法使用某些技能

# 1. 检查技能加载配置
openclaw config get skills.load.extraDirs

# 2. 检查代理技能过滤
openclaw config get agents.defaults.skills
openclaw config get agents.list[0].skills

# 3. 检查技能目录结构
ls -l D:\openclaw\skills\

# 4. 重新加载技能
openclaw gateway restart

# 5. 查看技能加载日志
openclaw gateway logs | grep -i "skill"
```

## 平台特定方案

### 飞书（Feishu）问题

#### 1. 飞书账户配置

```json
// ~/.openclaw/openclaw.json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "connectionMode": "websocket",
      "domain": "feishu",
      "requireMention": true,
      "dynamicAgentCreation": {
        "enabled": true,
        "workspaceTemplate": "D:\\openclaw\\workspace-feishu-{userId}",
        "maxAgents": 10
      },
      "accounts": {
        "default": {  // 必须是 default，不是 main
          "enabled": true,
          "name": "Cirno Bot",
          "appId": "cli_a903ccc2bb791bde",
          "appSecret": "xo0A1dGoHvIAluomqNS6ob2igrEgJbdN",
          "domain": "feishu",
          "connectionMode": "websocket",
          "renderMode": "card",
          "streaming": true
        }
      }
    }
  }
}
```

#### 2. 飞书图片发送

```javascript
// src/extensions/feishu/src/outbound.ts
async function sendText(text: string, options: SendOptions = {}) {
  // 添加 mediaLocalRoots 参数
  const mediaLocalRoots = [
    process.env.TEMP || '/tmp',
    path.join(process.env.USERPROFILE, '.openclaw', 'agents'),
    'D:\\openclaw\\skills'  // 添加技能目录
  ];

  // 传递给 send 函数
  await send({
    msg_type: 'text',
    content: JSON.stringify({ text }),
    mediaLocalRoots,  // 重要！
    ...options
  });
}
```

### Discord 问题

#### 1. Discord 绑定配置

```json
// ~/.openclaw/openclaw.json
{
  "bindings": [
    {
      "agentId": "discord-main",
      "match": {
        "channel": "discord"
      }
    }
  ],
  "agents": {
    "list": [
      {
        "id": "discord-main",
        "workspace": "D:\\openclaw\\workspace-discord",
        "agentDir": "C:\\Users\\GD\\.openclaw\\agents\\discord-main\\agent",
        "model": {
          "primary": "kimi-coding/k2p5",
          "fallbacks": ["kimi-code/kimi-for-coding"]
        }
      }
    ]
  }
}
```

## 关键文件路径

| 文件 | Windows | macOS/Linux |
|------|---------|-------------|
| 主配置 | `%USERPROFILE%\.openclaw\openclaw.json` | `~/.openclaw/openclaw.json` |
| 插件目录 | `%USERPROFILE%\.openclaw\extensions\` | `~/.openclaw/extensions/` |
| Kimi 同步 | `%USERPROFILE%\.kimi\kimi-claw\openclaw.json` | `~/.kimi/kimi-claw/openclaw.json` |
| 日志 | `%TEMP%\openclaw\` | `/tmp/openclaw/` |
| 临时源代码 | `%LOCALAPPDATA%\Temp\openclaw\` | `/tmp/openclaw/` |
| 代理数据 | `%USERPROFILE%\.openclaw\agents\{agentId}\` | `~/.openclaw/agents/{agentId}/` |
| 技能目录 | `D:\openclaw\skills\` | `/path/to/skills/` |

## 错误代码速查

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `EINVAL` / `EBUSY` | node-pty Windows 编译失败 | `--ignore-scripts` 安装 |
| `schtasks failed` | Windows 权限不足 | `--foreground` 或管理员 PS |
| `Gateway timeout` | 端口占用/进程僵死 | 检查端口，杀进程重启 |
| `Token differs` | cli 与 service 配置不同步 | `install --force` 或手动同步 |
| `duplicate plugin id` | 多处安装同一插件 | 清理重复，只留一处 |
| `RPC probe failed` | Gateway 未启动或崩溃 | 查看日志，检查配置 |
| `Route not found` | 路由绑定失败 | 检查 bindings 配置 |
| `Media path not allowed` | 图片路径不在媒体根目录 | 添加到 local-roots.ts |
| `Skill not found` | 技能未加载 | 检查 skills.load.extraDirs |

## 最小验证配置

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "随机字符串"
    }
  },
  "plugins": {
    "entries": {
      "kimi-claw": {
        "enabled": true,
        "config": {
          "bridge": {
            "token": "从 Kimi 网页获取"
          }
        }
      }
    }
  },
  "agents": {
    "defaults": {
      "workspace": "D:\\openclaw",
      "model": {
        "primary": "kimi-coding/k2p5",
        "fallbacks": ["kimi-code/kimi-for-coding"]
      }
    },
    "list": [
      {"id": "feishu-ou_f35e74b14ff44420bdd4ede905c3b587", "workspace": "D:\\openclaw\\workspace-feishu-ou_f35e74b14ff44420bdd4ede905c3b587"},
      {"id": "discord-main", "workspace": "D:\\openclaw\\workspace-discord"}
    ]
  },
  "bindings": [
    {"agentId": "feishu-ou_f35e74b14ff44420bdd4ede905c3b587", "match": {"channel": "feishu", "peer": {"kind": "direct", "id": "ou_f35e74b14ff44420bdd4ede905c3b587"}}},
    {"agentId": "discord-main", "match": {"channel": "discord"}}
  ],
  "skills": {
    "load": {
      "extraDirs": ["D:\\openclaw\\skills"]
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "accounts": {"default": {"enabled": true, "appId": "cli_a903ccc2bb791bde", "appSecret": "xo0A1dGoHvIAluomqNS6ob2igrEgJbdN"}}
    },
    "discord": {
      "enabled": true,
      "token": "YOUR_DISCORD_TOKEN"
    }
  }
}
```

## 输出规范

1. **先诊断**: 运行 `openclaw gateway status` 和配置检查
2. **分类问题**: 根据 MECE 分类确定问题类型
3. **给方案**: 提供精确的命令，不要泛泛而谈
4. **验证**: 每一步后提供验证命令
5. **备选**: 主方案失败时提供备用方案
