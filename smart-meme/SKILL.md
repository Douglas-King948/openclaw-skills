---
name: smart-meme
description: |
  智能表情包系统 v6.0 - 一句话发送表情包。
  
  **使用方法（极简）：**
  ```python
  from smart_meme import send_meme
  send_meme("来个马喽")  # 自动发送飞书卡片表情包
  ```
  
  **支持的关键词：**
  - 🐵 "马喽"、"猴子"、"猴哥" → 猴子表情包
  - 🐼 "熊猫头"、"滚滚" → 熊猫头表情包  
  - 🐱 "猫咪"、"猫"、"喵喵" → 猫咪表情包
  - 🐶 "狗狗"、"狗"、"汪汪" → 狗狗表情包
  - 🦆 "鸭子"、"鸭"、"嘎嘎" → 鸭子表情包
  - ✨ "动漫"、"二次元"、"猫娘" → 二次元美图
  - 💻 "程序员"、"码农" → 程序员梗图
  - ⚔️ "武侠"、"功夫" → 武侠梗图
  
  **无需任何额外配置，内部自动处理：**
  - 自动下载图片
  - 自动上传到飞书
  - 自动发送卡片消息
  - 自动清理临时文件
  
  **触发示例：**
  "来个马喽"、"发个熊猫头"、"来个猫咪"、"发个表情包"
license: MIT
metadata:
  emoji: "🎭"
  version: "6.0"
  tags: [meme, stickers, feishu, image]
---

# Smart Meme v6.0 - 智能表情包系统

## 🚀 极简使用方式

### 一句话发送表情包

```python
from smart_meme import send_meme

# 用户说"来个马喽"
send_meme("来个马喽")

# 用户说"来个熊猫头"  
send_meme("来个熊猫头")

# 用户说"来个猫咪"
send_meme("来个猫咪")
```

**完成！** 无需任何其他操作，表情包已作为飞书卡片发送给用户。

## 📋 支持的关键词映射

| 用户说的话 | 发送的内容 | 图标 |
|-----------|-----------|------|
| "马喽" / "猴子" / "猴哥" | 猴子表情包 | 🐵 |
| "熊猫头" / "滚滚" / "斗图" | 熊猫头表情包 | 🐼 |
| "猫咪" / "猫" / "喵喵" | 猫咪表情包 | 🐱 |
| "狗狗" / "狗" / "汪汪" | 狗狗表情包 | 🐶 |
| "鸭子" / "鸭" / "嘎嘎" | 鸭子表情包 | 🦆 |
| "动漫" / "二次元" / "猫娘" | 二次元美图 | ✨ |
| "程序员" / "码农" / "梗图" | 程序员梗图 | 💻 |
| "武侠" / "功夫" | 武侠梗图 | ⚔️ |

## 🔧 内部实现（无需关心）

```
用户说"来个马喽"
    ↓
smart_meme.send_meme() 接收消息
    ↓
解析关键词 → "monkeys" 分类
    ↓
从 url_sources 获取图片URL
    ↓
download_image() 下载到本地
    ↓
feishu_card_sender.upload_image() 上传到飞书
    ↓
feishu_card_sender.send_feishu_card() 发送卡片
    ↓
用户收到飞书卡片（标题+图片+文案）
    ↓
自动清理临时文件
```

## 📁 文件结构

```
smart-meme/
├── SKILL.md                    # 本文档
├── smart_meme.py              # ✅ 统一发送接口（主入口）
├── feishu_card_sender.py      # ✅ 飞书卡片发送器（Python实现）
├── url_sources.py             # URL 源配置
├── url_sender.py              # URL 获取接口
└── local_memes/               # 本地表情包库存
    ├── monkeys/               # 🐵 马喽/猴子
    ├── panda/                 # 🐼 熊猫头
    ├── cats/                  # 🐱 猫咪
    └── ...
```

## ✨ v6.0 进化成果

| 特性 | v5.0 | v6.0（进化后） |
|------|------|----------------|
| 调用方式 | 需要手动调用多个模块 | **一句话搞定** |
| 图片发送 | 需要外部 node 脚本 | **纯 Python 实现** |
| 错误处理 | 容易出错 | **内部自动处理** |
| 用户体验 | 复杂 | **极简** |

## 📝 更新日志

### v6.0 - 进化版（今日）
- ✅ **纯 Python 实现** - 完全独立，无需 node.js
- ✅ **一句话调用** - `send_meme("来个马喽")` 完成所有操作
- ✅ **自动飞书卡片** - 内部自动上传图片、发送卡片
- ✅ **新增 monkeys 分类** - 支持马喽/猴子表情包
- ✅ **新增 ducks 分类** - 支持鸭子表情包
- ✅ **关键词扩展** - 支持"马楼"等常见错别字

---

**现在，只需要说"来个马喽"就够了！** 🐵


## 🚀 快速开始

### 最简单用法（推荐）

```python
from smart_meme import send_meme

# 自动解析关键词并发送飞书卡片
send_meme("来个马喽")
send_meme("来个熊猫头")
send_meme("来个猫咪")
```

### 便捷函数

```python
from smart_meme import send_monkey, send_panda, send_cat

send_monkey()   # 🐵 马喽
send_panda()    # 🐼 熊猫头
send_cat()      # 🐱 猫咪
```

## 📋 分类与关键词

| 分类 | 关键词 | 图标 |
|------|--------|------|
| **monkeys** | 马喽、吗喽、猴子、猴、猴哥、猩猩、猿、monkey | 🐵 |
| **panda** | 熊猫头、熊猫、滚滚、panda、斗图、梗图 | 🐼 |
| **cats** | 猫咪、猫、喵喵、哈基米、cat | 🐱 |
| **dogs** | 狗狗、狗、汪汪、puppy、dog | 🐶 |
| **anime** | 动漫、二次元、猫娘、萌、pixiv、壁纸 | ✨ |
| **programmer** | 程序员、码农、coding、programmer | 💻 |
| **wuxia** | 武侠、功夫、wuxia | ⚔️ |
| **touhou** | 东方、东方Project、车万、touhou | 🎵 |
| **doro** | doro、多洛、nikke、妮姬 | 🌟 |

## 🎯 用户指令映射

| 用户说的话 | 发送的分类 |
|-----------|-----------|
| "来个马喽" / "来个猴子" / "猴哥" | 🐵 monkeys |
| "来个熊猫头" / "滚滚" / "斗图" | 🐼 panda |
| "来个猫咪" / "喵喵" / "猫" | 🐱 cats |
| "来个狗狗" / "汪汪" / "狗" | 🐶 dogs |
| "来个二次元" / "猫娘" / "萌" | ✨ anime |
| "来个程序员梗" / "码农" | 💻 programmer |
| "来个武侠" / "功夫" | ⚔️ wuxia |
| "来个东方" / "车万" | 🎵 touhou |
| "来个doro" / "多洛" | 🌟 doro |

## 📁 文件结构

```
smart-meme/
├── smart_meme.py         # ✅ 统一发送接口（新！）
├── url_sources.py        # URL 源配置
├── url_sender.py         # URL 获取接口
├── feishu_sender.py      # 飞书卡片发送（内部使用）
├── local_memes/          # 本地表情包库存
│   ├── monkeys/          # 🐵 马喽
│   ├── panda/            # 🐼 熊猫头
│   ├── cats/             # 🐱 猫咪
│   └── ...
└── SKILL.md              # 本文档
```

## ✨ 新特性 v6.0

- ✅ **统一接口** - `send_meme()` 一个函数搞定所有平台
- ✅ **自动检测** - 自动识别关键词，选择最佳表情包
- ✅ **飞书卡片** - 默认使用卡片消息，图片正常显示
- ✅ **智能文案** - 根据分类自动匹配互动文案
- ✅ **本地+URL** - 支持本地库存和在线URL混合
- ✅ **便捷函数** - `send_monkey()`, `send_panda()` 等快捷方式

## 🛠️ 技术实现

### 发送流程

```
用户消息
    ↓
解析关键词 (parse_keyword)
    ↓
获取表情包URL (url_sources.py)
    ↓
下载图片到临时文件
    ↓
调用 feishu-card 发送卡片
    ↓
飞书显示卡片消息（标题+图片+文案）
```

## 📝 更新日志

### v6.0 - 统一接口版
- ✅ 新增 `smart_meme.py` 统一发送接口
- ✅ 新增 `monkeys` 分类（马喽/猴子）
- ✅ 自动关键词解析
- ✅ 飞书卡片自动发送
- ✅ 分类图标和互动文案
- ✅ 便捷函数：`send_monkey()`, `send_panda()` 等

### v5.2 - 工作时间安全模式
- 工作日自动过滤社死内容

### v5.0 - 飞书卡片支持
- 使用卡片消息发送表情包

### v4.0 - URL 发送版
- 支持 URL 直接发送

---

**现在可以秒发表情包了！** ⚡
 v6.0

智能表情包系统 - 支持 **URL 直接发送**、**本地库存**、以及 **飞书卡片消息** 三种模式！

## 🚀 v6.0 新特性 - 统一接口（推荐）

**一行代码发送，自动处理所有细节！**

```python
import sys
sys.path.insert(0, "D:/openclaw/skills/smart-meme")
from smart_meme import send_meme, send_monkey, send_panda, send_cat

# 🎯 最简单用法 - 自动解析关键词 + 自动下载 + 飞书卡片发送
send_meme("来个马喽")      # 发送马喽表情包
send_meme("来个熊猫头")    # 发送熊猫头
send_meme("来个猫咪")      # 发送猫咪

# 🎯 快捷函数
send_monkey()   # 马喽
send_panda()    # 熊猫头
send_cat()      # 猫咪
send_dog()      # 狗狗
send_anime()    # 二次元
send_programmer()  # 程序员梗

# 🎯 高级用法 - 指定参数
send_meme(
    message="来个马喽",
    target="ou_f35e74b14ff44420bdd4ede905c3b587",  # 目标用户
    channel="feishu"  # 平台
)
```

### v6.0 优势

| 特性 | 旧版本 | v6.0 统一接口 |
|------|--------|---------------|
| 调用复杂度 | 需处理 URL/下载/发送 | 一行代码 |
| 图片显示 | URL 可能显示为文本 | 飞书卡片 100% 显示 |
| 平台适配 | 需手动选择发送方式 | 自动检测 |
| 失败处理 | 需手动降级 | 自动处理 |

## 🚀 旧版接口（仍可用）

### 飞书频道（推荐）

**最自然的发送方式** - 标题即消息，图片即内容！

```python
import sys
sys.path.insert(0, "D:/openclaw/skills/smart-meme")
from feishu_sender import send_meme_feishu, send_by_keyword, send_panda, send_cat

# 发送随机表情包
target = "oc_d5c58e8fb82948b49cc73b927b6548bd"  # 飞书群聊ID
result = send_meme_feishu(target)
# 输出: "Boss，你要的表情包来了！" + 图片

# 按关键词发送
result = send_by_keyword(target, "熊猫头")
# 输出: "Boss，你要的熊猫头来了！" + 图片

# 快捷函数
send_panda(target)    # 熊猫头
send_cat(target)      # 猫咪
send_dog(target)      # 狗狗
send_anime(target)    # 二次元
send_programmer(target)  # 程序员梗
send_wuxia(target)    # 武侠
send_random(target)   # 随机
```

**发送效果：**
- 📌 **标题**: "Boss，你要的熊猫头来了！"
- 🖼️ **内容**: 表情包图片
- 💬 **互动文案**: "从库存里翻到的熊猫头～ (=^-ω-^=)"

这种格式更符合日常聊天习惯，还有猫娘我的互动彩蛋～

### ⏰ 工作时间安全模式

飞书是工作频道，工作时间（工作日 8:30-17:30）自动开启安全模式：

| 分类 | 工作时间 | 说明 |
|------|----------|------|
| 🐼 **熊猫头** | ✅ 可用 | 搞笑沙雕，职场安全 |
| 🐱 **猫咪** | ✅ 可用 | 治愈萌宠， universally loved |
| 🐕 **狗狗** | ✅ 可用 | 治愈萌宠， universally loved |
| 🐾 **小动物** | ✅ 可用 | 可爱动物，职场安全 |
| 💻 **程序员** | ✅ 可用 | 工作相关，甚至加分 |
| ✨ **二次元** | ❌ 禁用 | 浓度高，可能社死 |
| ⚔️ **武侠** | ❌ 禁用 | 中二气息，不够专业 |
| 🎲 **杂项** | ❌ 禁用 | 内容不可控，风险未知 |

**自动切换示例：**
- 工作时要发「二次元」→ 自动换成「猫咪」
- 周末/下班后要发「二次元」→ 正常发送

**文案风格也会切换：**
- 工作时间："猫咪治愈，缓解压力 🐱"（专业克制）
- 非工作时间："喵～和我一样可爱吧？❄️🐱"（活泼猫娘）

### 正确发送方式（Discord）

```python
import sys
sys.path.insert(0, "D:/openclaw/skills/smart-meme")
from url_sender import get_random_meme_url, get_meme_url_by_keyword

# 获取表情包 URL 并发送
result = get_random_meme_url()
if result["success"]:
    # ✅ 正确：使用 target 参数指定频道
    message.send(
        target="1465062913533411359",  # Discord 频道ID
        media=result["url"],
        message="给你个表情包！"
    )

# 按关键词发送
result = get_meme_url_by_keyword("二次元")
if result["success"]:
    message.send(
        target="1465062913533411359",
        media=result["url"],
        message="好康的图来啦！✨"
    )
```

### ❌ 错误方式（不要这样做）

```python
# 错误：只是打印 URL，不会显示为图片
print(result["url"])
# 错误：把 URL 当作文本发送
message.send(message=f"图片地址：{result['url']}")
```

### 方法2：命令行获取 URL

```bash
cd D:/openclaw/skills/smart-meme
python url_sender.py
```

## 📋 用户指令映射

| 用户说的话 | 执行的操作 | 分类 |
|-----------|-----------|------|
| "发个表情包" / "来个梗图" | 发送随机表情包 | misc |
| "发个熊猫头" / "滚滚" | 发送熊猫头 | panda |
| "发个猫咪" / "喵喵" / "猫" | 发送猫咪 | cats |
| "发个狗狗" / "汪汪" / "狗" | 发送狗狗 | dogs |
| "来个动漫表情包" / "二次元" / "猫娘" / "萌" | 发送动漫/猫娘 | anime |
| "来个东方图" / "车万" | 发送东方Project | touhou |
| "来个doro" / "多洛" / "nikke" | 发送Doro | doro |
| "来个程序员梗" / "码农" / "coding" | 发送程序员梗 | programmer |
| "发个武侠梗" / "功夫" | 发送武侠梗 | wuxia |
| "来个动物表情包" | 发送动物 | animals |

## 📁 文件结构

```
smart-meme/
├── smart_meme.py         # 🆕 v6.0 统一接口（推荐）
├── url_sources.py        # URL 源配置（按分类）
├── url_sender.py         # URL 发送接口
├── sender.py             # 本地文件发送接口
├── feishu_sender.py      # 飞书卡片消息发送
├── config.py             # 配置文件
├── local_memes/          # 本地表情包库存
│   └── monkeys/          # 🐵 马喽/猴子
├── SKILL.md              # 本文档
└── README.md             # 详细说明
```

## 🔧 核心功能

### URL 发送接口 (url_sender.py)

```python
from url_sender import get_random_meme_url, get_meme_url_by_keyword, list_categories

# 随机获取
result = get_random_meme_url()              # 完全随机
result = get_random_meme_url("anime")       # 指定分类

# 关键词匹配
result = get_meme_url_by_keyword("猫娘")     # 中文
result = get_meme_url_by_keyword("panda")    # 英文

# 列出分类
categories = list_categories()
```

返回格式：
```python
{
    "success": True,
    "url": "https://api.waifu.pics/sfw/neko",  # 直接可用的 URL
    "category": "anime",
    "error": None
}
```

### 发送示例（正确用法）

```python
import sys
sys.path.insert(0, "D:/openclaw/skills/smart-meme")
from url_sender import get_meme_url_by_keyword

# 用户说"来个猫娘"
result = get_meme_url_by_keyword("猫娘")
if result["success"]:
    # ✅ 正确：使用 media 参数直接发送图片
    message.send(
        media=result["url"],
        message="喵～猫娘来啦！❄️🐱 (=^-ω-^=)"
    )
    # 这样就会直接显示图片，而不是显示URL文本
```

## 📊 分类说明

| 分类 | 关键词 | 描述 | 示例 URL |
|------|--------|------|----------|
| **monkeys** | 马喽、吗喽、猴子、猴、monkey | 🐵 马喽表情包 | pic.re |
| **panda** | 熊猫头、滚滚、panda | 熊猫头表情包 | diy表情包源 |
| **cats** | 猫、猫咪、cat、kitty | 萌猫表情包 | cataas.com |
| **dogs** | 狗、狗狗、dog | 狗狗表情包 | dog.ceo |
| **anime** | 动漫、二次元、anime、猫娘、萌 | 二次元/猫娘 | waifu.pics |
| **touhou** | 东方、东方project、车万 | 东方Project风格 | 动漫风格图 |
| **doro** | doro、多洛、nikke、妮姬 | Doro表情包 | Tenor/Imgur |
| **wuxia** | 武侠、功夫、wuxia | 武侠/网游梗 | memegen.link |
| **animals** | 动物、animals | 其他动物 | some-random-api |
| **programmer** | 程序员、码农、coding、梗图 | 程序员梗 | memegen.link |
| **misc** | 杂项、其他、表情包 | 其他梗图 | memegen.link |

## ✨ 优势

| 特性 | URL 发送 | 本地文件发送 |
|------|----------|--------------|
| **审批** | ❌ 无需审批 | ✅ 需要审批 |
| **速度** | ⚡ 直接发送 | ⏱️ 需复制文件 |
| **存储** | 💾 不占用本地空间 | 💾 占用磁盘空间 |
| **可用性** | 🌐 依赖网络 | ✅ 离线可用 |

## ⚠️ URL 要求

### 直接图片链接 vs JSON API

**✅ 正确的 URL（直接图片）：**
```
https://example.com/image.jpg
https://example.com/photo.png
https://example.com/meme.gif
```

**❌ 错误的 URL（返回 JSON 的 API）：**
```
https://api.example.com/get-image  # 返回 {"url": "..."}
https://nekos.life/api/v2/img/neko  # 返回 JSON
https://api.waifu.im/search  # 返回 JSON
```

### 自动检测机制

技能已内置 `is_direct_image_url()` 函数，自动检测并过滤可疑的 JSON API：
- 检查 URL 是否有图片扩展名 (.jpg/.png/.gif 等)
- 检查是否包含 API 路径 (/api/, /v1/, /search 等)
- 优先选择直接图片链接

如果所有 URL 都可能是 API，则随机选择并可能返回 JSON（需进一步优化）。

### 正确的图片发送方式

使用 `message.send(media=url)` 时，图片会直接显示在聊天中：

```python
# ✅ 正确 - 图片直接显示
message.send(
    media="https://example.com/meme.jpg",  # URL 直接作为 media 参数
    message="表情包来啦！"
)
```

### 错误的图片发送方式

不要把 URL 放在 message 文本中：

```python
# ❌ 错误 - 只显示 URL 文本，不显示图片
message.send(message="https://example.com/meme.jpg")

# ❌ 错误 - 同样只显示文本
message.send(message=f"图片地址：{url}")
```

### 关键区别

| 方式 | 结果 | 说明 |
|------|------|------|
| `media=url` | ✅ 显示图片 | 正确方式 |
| `message=url` | ❌ 显示文本 | 错误方式 |

## 📝 更新日志

### v6.0 - 统一接口（当前版本）
- ✅ **新增 `smart_meme.py` 统一接口** - 一行代码发送，自动处理所有细节
- ✅ **自动平台检测** - 自动识别飞书/Discord，选择最佳发送方式
- ✅ **自动图片下载** - URL 方式自动下载图片，避免显示为文本
- ✅ **飞书卡片 100% 可靠** - 所有表情包通过卡片发送，确保正常显示
- ✅ **新增 monkeys 分类** - 支持马喽/猴子表情包
- ✅ **简化调用** - `send_meme("来个马喽")` 即可

### v5.2 - 工作时间安全模式
- ✅ 工作日 8:30-17:30 自动开启安全模式
- ✅ 禁用可能社死的分类（二次元、武侠、杂项）
- ✅ 不安全分类自动切换到安全分类
- ✅ 工作时间使用更专业的互动文案
- ✅ 周末和下班时间恢复正常模式

### v5.1 - 增加互动文案
- ✅ 每个分类配有5条以上的互动文案
- ✅ 符合猫娘人设，增加聊天温度
- ✅ 使用颜文字和 emoji，更有亲和力
- ✅ 随机选择，每次发送都有惊喜

### v5.0 - 飞书卡片消息支持
- ✅ 新增 `feishu_sender.py` - 飞书专用发送模块
- ✅ 使用卡片消息发送表情包，图片正常显示
- ✅ 标题即消息，更符合聊天习惯
- ✅ 支持本地库存 + URL 源自动切换
- ✅ 自动清理临时下载文件

### v4.2 - 添加 JSON API 检测机制
- ✅ 新增 `is_direct_image_url()` 自动检测函数
- ✅ 优先选择直接图片链接，过滤 JSON API
- ✅ 移除所有返回 JSON 的 API 链接
- ✅ 更新文档说明

### v4.1 - 修复 URL 问题
- ✅ 修复：移除返回 JSON 的 API URL
- ✅ 所有 URL 改为直接图片链接
- ✅ 添加 URL 要求说明章节

### v4.0 - URL 发送版
- ✅ 新增 `url_sender.py` - URL 直接发送
- ✅ 新增 `url_sources.py` - URL 源配置
- ✅ 支持关键词映射（猫娘、萌等）
- ✅ 无需文件审批，直接通过 URL 发送
- ✅ 保留本地文件发送作为备用
- ✅ 添加重要提示：正确的图片发送方式
- ✅ 新增 `url_sender.py` - URL 直接发送
- ✅ 新增 `url_sources.py` - URL 源配置
- ✅ 支持关键词映射（猫娘、萌等）
- ✅ 无需文件审批，直接通过 URL 发送
- ✅ 保留本地文件发送作为备用
- ✅ 添加重要提示：正确的图片发送方式

## 🎯 使用建议

| 场景 | 推荐方式 | 模块 | 注意事项 |
|------|----------|------|----------|
| **飞书工作时段** | 卡片消息 | `feishu_sender.py` ✅ | 自动过滤社死内容 |
| **飞书下班时间** | 卡片消息 | `feishu_sender.py` ✅ | 全部分类可用 |
| **Discord** | URL 直接发送 | `url_sender.py` | 无限制 |
| **需要特定图片** | 本地库存 | `sender.py` | 离线可用 |

### 飞书专属建议

使用 `feishu_sender.py` 模块，可以获得最佳体验：
- 🎨 **标题即消息** - 像正常聊天一样，标题就是你要说的话
- 🖼️ **图片即内容** - 卡片里只有图片
- 💬 **互动文案** - 根据时段自动切换风格
- 🛡️ **工作时间保护** - 自动避免社死内容
- 🔄 **自动切换源** - 本地没有自动用 URL 下载
- 🧹 **自动清理** - 临时文件自动删除

```python
from feishu_sender import send_meme_feishu, send_panda, send_cat, send_anime

# 一行代码发送
target = "oc_d5c58e8fb82948b49cc73b927b6548bd"

# 工作时间（8:30-17:30）
send_anime(target)  # 自动换成猫咪或其他安全分类

# 下班时间（17:30之后）
send_anime(target)  # 正常发送二次元

# 想发什么都行，系统会自动判断
send_by_keyword(target, "武侠")  # 工作时间会变成熊猫头
```

---

**现在可以秒发表情包了！** ⚡(=^-ω-^=)❄️
