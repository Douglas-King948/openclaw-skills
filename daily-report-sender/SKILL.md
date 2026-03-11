---
name: daily-report-sender
description: |
  飞书日报发送器 - 完全独立的技能
  
  **核心能力：**
  - 从网上自动下载表情包（按mood分类）
  - 上传图片到飞书服务器
  - 发送带图片的交互卡片（支持markdown加粗、序号、颜色）
  - 每天自动换新图，保存到本地图库
  
  **完全独立：**
  - 不依赖任何其他skill
  - 内置飞书API客户端
  - 内置图片下载和上传功能
  
  **触发关键词：**
  "发送日报"、"发日报"、"生成日报"、"今日日报"、"工作日报"、
  "总结日报"、"汇报日报"、"定时日报"、"日报卡片"

  **自动日报功能：**
  - 自动从 memory/YYYY-MM-DD.md 提取昨日工作记录
  - 每天早上8点定时发送工作日报卡片
  - 支持手动指定日期发送历史日报

  **使用方式：**
  ```python
  from daily_report_sender import send_daily_report
  
  result = send_daily_report(
      title="今日工作日报",
      items=["任务1", "任务2", "任务3"],
      mood="working",      # working/celebrating/thinking/wuxia
      color="blue"         # blue/red/green/orange/purple
  )
  ```
  
  **自动日报脚本：**
  ```bash
  # 发送昨天的工作日报
  python scripts/auto_daily_report.py
  
  # 发送指定日期的日报
  python scripts/auto_daily_report.py --yesterday 2026-03-05
  
  # 测试模式（不实际发送）
  python scripts/auto_daily_report.py --test
  ```
  
  **环境变量：**
  - `FEISHU_APP_SECRET`: 飞书应用密钥（必需）
  
version: 3.0.0
author: Cirno
---

# Daily Report Sender v3.0

## 功能

完全独立的飞书日报发送技能。

## 特性

- 🌐 **网上下载** - 从pic.re等API自动下载表情包
- 📤 **自动上传** - 上传图片到飞书服务器
- 💬 **交互卡片** - 发送带图片的富文本卡片
- 🎨 **Markdown支持** - 加粗、序号、分隔线
- 🎨 **颜色主题** - blue/red/green/orange/purple
- 📁 **本地图库** - 按日期保存图片

## 快速开始

```python
from daily_report_sender import send_daily_report

# 发送工作日报
result = send_daily_report(
    title="💻 今日工作日报",
    items=[
        "完成代码重构",
        "修复3个bug",
        "部署新版本",
    ],
    mood="working",
    color="blue"
)

print(result)
# {
#     "success": True,
#     "message_id": "om_xxx",
#     "image_key": "img_v3_xxx",
#     "image_path": "daily_images/20260305/working_1234.jpg"
# }
```

## Mood类型

| mood | 下载主题 | 适用场景 |
|------|----------|----------|
| working | 电脑/工作 | 日常工作汇报 |
| celebrating | 庆祝/开心 | 里程碑/完成 |
| thinking | 思考/猫咪 | 复盘/总结 |
| wuxia | 武侠/古风 | 趣味汇报 |

## 颜色选项

- `blue` - 蓝色（默认）
- `red` - 红色（紧急）
- `green` - 绿色（成功）
- `orange` - 橙色（警告）
- `purple` - 紫色（庆祝）

## 图片保存

```
daily_images/
├── 20260305/
│   ├── working_1234.jpg
│   └── celebrating_5678.png
└── 20260306/
    └── thinking_9012.jpg
```

## 环境配置

```bash
export FEISHU_APP_SECRET="your_app_secret_here"
```

## 完整流程

```
1. 根据mood选择URL源
2. 下载图片到 daily_images/YYYYMMDD/
3. 上传图片到飞书获取image_key
4. 格式化内容（markdown加粗）
5. 发送交互卡片
```

## 自动日报功能

除了手动发送日报，还支持**自动从记忆文件提取工作记录**并发送。

### 定时自动发送

每天早上8点自动执行，无需手动操作：
```bash
# 已配置 OpenClaw 定时任务
# cron: 0 8 * * *
```

### 手动执行

```bash
cd skills/daily-report-sender

# 发送昨天的工作日报
python scripts/auto_daily_report.py

# 发送指定日期的日报
python scripts/auto_daily_report.py --yesterday 2026-03-05

# 测试模式（预览内容，不实际发送）
python scripts/auto_daily_report.py --test
```

### 工作记录提取规则

自动日报会从 `memory/YYYY-MM-DD.md` 中提取：

1. **✅ 已完成事项** - 匹配 `- ✅ xxx` 格式的条目
2. **待办事项** - 匹配 `- [ ] xxx` 格式的条目
3. **工作关键词** - 匹配以"完成"、"修复"、"创建"等开头的条目

### 示例

假设昨天的记忆文件包含：
```markdown
- ✅ 完成飞书文档上传流程优化讨论
- ✅ 修复 article-illustrator skill
- [ ] 待完成: 接入Tavily/Brave搜索API
```

自动生成的日报：
```
📋 2026-03-05 工作日报
1. 完成飞书文档上传流程优化讨论
2. 修复 article-illustrator skill
3. 待完成: 接入Tavily/Brave搜索API
```

---
*完全独立，即插即用*