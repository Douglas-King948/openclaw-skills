---
name: multimodal-awakening
description: |
  多模态能力自动唤醒框架 - 让大模型自动识别并处理用户发送的各种媒体文件。
  
  **核心能力：**
  自动检测消息中的媒体引用标记（[media:type:path]），使用通用工具处理：
  - image: 图片分析、OCR、场景识别（使用通用 `image` 工具）
  - audio: 语音转写、音频摘要（使用 Python + Whisper）
  - pdf: 文档提取、内容分析（使用通用 `pdf` 工具）
  - video: 视频帧提取、内容理解（使用 Python + ffmpeg）
  - sheet: 表格数据分析（使用 Python + pandas）
  - code: 代码文件读取和分析（使用通用 `read` 工具）
  
  **设计原则：**
  - 仅依赖通用层工具，不绑定任何特定渠道
  - Gateway 层负责下载文件，Agent 层负责处理逻辑
  - 所有渠道（飞书、Discord、Telegram 等）均可使用
  
  **触发场景：**
  1. 用户发送媒体文件（图片、语音、PDF、视频等）
  2. Gateway 层注入 [media:type:...] 标记
  3. 本 Skill 自动检测并使用通用工具处理
  4. 返回结构化的分析结果
  
  **适用模型：**
  任何支持 `image` 工具的多模态大模型（GPT-4V、Claude 3、Kimi k2.5 等）
---

# 多模态能力自动唤醒框架 (MCA)

## 核心概念

大多数多模态大模型具备处理图片/音频/PDF 的能力，但默认不会主动调用工具来处理用户发送的媒体文件。本框架通过**标准化媒体引用标记**，让模型自动识别并激活对应处理能力。

## 标准化媒体引用格式

```
[media:<type>:<location>][media:<type2>:<location2>]...
```

### 支持的媒体类型

| 类型 | 标记 | 处理工具 | 输出格式 |
|------|------|---------|---------|
| 图片 | `image` | `image` | 文字描述/OCR |
| 音频 | `audio` | `audio_transcribe` | 转写文本 |
| PDF | `pdf` | `pdf` | Markdown 内容 |
| 视频 | `video` | `video_extract` + `image` | 内容摘要 |
| 表格 | `sheet` | `feishu_sheet` | 结构化数据 |
| 代码 | `code` | `read` | 代码分析 |

## 工作流程

### 1. Gateway 层（渠道适配）

各渠道插件检测到媒体消息时：

```javascript
// 飞书示例
if (message.type === 'image') {
    const localPath = await downloadImage(message.image_key);
    message.content = `[media:image:file://${localPath}]${userText || ''}`;
}

if (message.type === 'audio') {
    const localPath = await downloadAudio(message.file_key);
    message.content = `[media:audio:file://${localPath}]请转写这段语音`;
}

if (message.type === 'file' && filename.endsWith('.pdf')) {
    const localPath = await downloadFile(message.file_key);
    message.content = `[media:pdf:file://${localPath}]请分析这份文档`;
}
```

### 2. Agent 层（本 Skill）

检测媒体标记并路由到对应处理器：

```python
def process_multimedia_message(text: str):
    media_refs = extract_media_refs(text)
    
    for media_type, media_path in media_refs:
        if media_type == 'image':
            result = analyze_image(media_path)
        elif media_type == 'audio':
            result = transcribe_audio(media_path)
        elif media_type == 'pdf':
            result = extract_pdf_content(media_path)
        # ... 其他类型
    
    return combine_results(results)
```

### 3. Model 层（能力执行）

调用具体工具完成分析。

## 各媒体类型详细处理

### 图片 (image)

**检测标记：** `[media:image:file://...]`

**处理流程：**
```python
# 1. 提取所有图片路径
images = extract_image_refs(message)

# 2. 构建分析 prompt
if len(images) == 1:
    prompt = "详细描述这张图片的内容"
elif len(images) > 1:
    prompt = "对比分析这几张图片"

# 3. 调用 vision 模型
image(images=images, prompt=prompt)
```

**支持的分析模式：**
- 综合描述：场景、物体、布局、颜色
- OCR 提取：文字识别、表格还原
- 对比分析：多图差异识别
- 特定问题：根据用户提问定向分析

### 音频 (audio)

**检测标记：** `[media:audio:file://...]`

**处理流程：**
```python
# 方案1：本地 Whisper 模型
import whisper
model = whisper.load_model("base")
result = model.transcribe(audio_path, language="zh")

# 方案2：调用转写服务
audio_transcribe(file_path=audio_path, language="zh")
```

**输出内容：**
- 完整转写文本
- 说话人识别（如果支持）
- 内容摘要
- 关键信息提取

### PDF (pdf)

**检测标记：** `[media:pdf:file://...]`

**处理流程：**
```python
pdf(pdf=pdf_path, prompt="提取文档的主要内容和结构")
```

**支持的分析模式：**
- 全文提取：转换为 Markdown
- 摘要生成：提取核心观点
- 表格识别：还原表格数据
- 问答模式：针对文档内容回答问题

### 视频 (video)

**检测标记：** `[media:video:file://...]`

**处理流程：**
```python
# 1. 抽取关键帧（每秒1帧或场景变化帧）
frames = extract_keyframes(video_path, fps=1)

# 2. 分析关键帧
image(images=frames, prompt="描述视频的关键内容和场景变化")

# 3. 如果有音频轨道，同时转写
if has_audio(video_path):
    audio_path = extract_audio(video_path)
    transcript = transcribe_audio(audio_path)
```

**输出内容：**
- 视频内容概述
- 关键场景描述
- 字幕/对话内容（如有）
- 时间戳标记

### 表格 (sheet)

**检测标记：** `[media:sheet:file://...]`

**重要**：`sheet` 类型不依赖特定渠道工具，使用通用方式处理：

**处理流程（通用方式）：**
```python
# 方式1：Gateway 预处理为 Markdown
# Gateway 层先将 Excel/CSV 转换为 Markdown 表格格式
# 注入: [media:sheet:content:\n| 列A | 列B |\n|-----|-----|\n| 1 | 2 |]

# 方式2：Python 脚本解析（推荐）
import pandas as pd

def analyze_sheet(file_path):
    # 读取 Excel/CSV
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    # 生成数据摘要
    summary = {
        'rows': len(df),
        'columns': len(df.columns),
        'column_types': df.dtypes.to_dict(),
        'numeric_summary': df.describe().to_dict() if df.select_dtypes(include=['number']).columns.any() else None,
        'missing_values': df.isnull().sum().to_dict(),
        'sample_data': df.head(5).to_dict('records')
    }
    
    return summary

# 方式3：转换为文本格式后用 LLM 分析
sheet_text = df.to_string(index=False)
prompt = f"""分析以下表格数据：

{sheet_text}

请提供：
1. 数据概述（行数、列数、数据类型）
2. 统计摘要（数值列的均值、极值等）
3. 数据质量评估（缺失值、异常值）
4. 可视化建议
"""
```

**渠道特定方式的降级：**
如果检测到当前是飞书环境且有 `feishu_sheet` 工具可用，可以使用它作为优化，但必须提供通用降级方案。

### 代码文件 (code)

**检测标记：** `[media:code:file://...]`

**处理流程：**
```python
# 读取代码
code_content = read(file_path=code_path)

# 代码分析
analysis_prompt = f"""
请分析以下代码文件：

文件：{code_path}

```
{code_content}
```

请提供：
1. 代码功能概述
2. 关键逻辑分析
3. 潜在问题识别
4. 改进建议
"""
```

## Gateway 层集成指南

### 设计原则

Gateway 层只做**一件事**：下载媒体文件并注入标准标记。

**禁止在 Gateway 层做：**
- ❌ 调用渠道特定工具（如 `feishu_sheet`）
- ❌ 内容分析或理解
- ❌ 复杂的格式转换（简单的 CSV→文本可以）

### 飞书 (Feishu)

修改 `feishu-openclaw-plugin` 的消息处理器：

```javascript
// message.js
async function handleMediaMessage(message) {
    const mediaHandlers = {
        'image': handleImage,
        'audio': handleAudio,
        'file': handleFile,
        'media': handleMedia  // 视频
    };
    
    const handler = mediaHandlers[message.msg_type];
    if (handler) {
        const mediaRef = await handler(message);
        message.content = JSON.stringify({
            text: `${mediaRef}${extractUserText(message)}`
        });
    }
    
    return message;
}

async function handleImage(msg) {
    const path = await downloadImage(msg.image_key);
    return `[media:image:file://${path}]`;
}

async function handleAudio(msg) {
    const path = await downloadAudio(msg.file_key);
    return `[media:audio:file://${path}]`;
}

async function handleFile(msg) {
    const path = await downloadFile(msg.file_key);
    const ext = getExtension(msg.file_name).toLowerCase();
    
    // 映射到通用媒体类型，不依赖飞书特定工具
    const typeMap = {
        'pdf': 'pdf',
        'xlsx': 'sheet',
        'xls': 'sheet',
        'csv': 'sheet',
        'py': 'code',
        'js': 'code',
        'java': 'code',
        'cpp': 'code',
        'go': 'code',
        'rs': 'code'
    };
    
    const mediaType = typeMap[ext] || 'file';
    return `[media:${mediaType}:file://${path}]`;
}
```

**注意**：对于 Excel 文件，Gateway 层可以选择：
1. 直接注入 `[media:sheet:file://...]`，让 Agent 层用 Python 解析
2. 或者先转换为 CSV/Markdown 格式再注入（如果 Gateway 有处理能力）

### Discord

```javascript
// 处理附件
for (const attachment of message.attachments) {
    const ext = getExtension(attachment.name);
    const localPath = await downloadAttachment(attachment.url);
    
    if (attachment.contentType?.startsWith('image/')) {
        message.content += `[media:image:file://${localPath}]`;
    } else if (attachment.contentType?.startsWith('audio/')) {
        message.content += `[media:audio:file://${localPath}]`;
    } else if (ext === 'pdf') {
        message.content += `[media:pdf:file://${localPath}]`;
    }
}
```

### Telegram

```javascript
// 处理图片
if (message.photo) {
    const photo = message.photo[message.photo.length - 1];
    const path = await downloadTelegramFile(photo.file_id);
    message.text += `[media:image:file://${path}]`;
}

// 处理语音
if (message.voice) {
    const path = await downloadTelegramFile(message.voice.file_id);
    message.text += `[media:audio:file://${path}]`;
}

// 处理文档
if (message.document) {
    const path = await downloadTelegramFile(message.document.file_id);
    const ext = getExtension(message.document.file_name);
    message.text += `[media:${getMediaType(ext)}:file://${path}]`;
}
```

## 最佳实践

### 1. 渐进式处理

不要一次处理太多媒体文件，建议：
- 图片：最多 10 张批量分析
- 音频：单文件处理（时长 < 10 分钟）
- PDF：单文件处理（页数 < 100 页）
- 视频：先提取关键帧，避免处理整个视频

### 2. 缓存机制

相同文件短期内不重复处理：
```python
cache_key = hash(file_path + file_size + modify_time)
if cache_key in result_cache:
    return result_cache[cache_key]
```

### 3. 错误降级

当某种处理方式失败时，尝试替代方案：
```python
try:
    # 优先使用本地模型
    result = local_ocr(image_path)
except:
    try:
        # 降级到 API
        result = api_ocr(image_path)
    except:
        # 最终降级：提示用户
        result = "无法识别，请尝试更清晰/其他格式的文件"
```

### 4. 隐私保护

敏感文件处理后及时清理：
```python
import atexit
import os

temp_files = []

def cleanup():
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)

atexit.register(cleanup)
```

## 故障排查

### 媒体标记未被识别

1. 检查 Gateway 是否正确注入标记：
```bash
openclaw gateway logs | grep "media:"
```

2. 检查 Skill 是否正确加载：
```bash
openclaw skills list | grep multimodal
```

### 特定媒体类型处理失败

| 问题 | 排查方向 |
|------|---------|
| 图片分析失败 | 检查模型是否支持 `image` 输入类型 |
| 音频转写失败 | 检查是否安装 whisper / 音频格式是否支持 |
| PDF 提取失败 | 检查 pdf 工具是否可用 / PDF 是否加密 |
| 视频处理失败 | 检查 ffmpeg 是否安装 / 视频编码格式 |

## 未来拓展

### 支持更多媒体类型

- `media:3d` - 3D 模型文件分析
- `media: CAD` - CAD 图纸识别
- `media:geo` - 地理数据文件（GeoJSON、KML）
- `media:music` - 乐谱识别和演奏分析

### 智能组合处理

```
用户同时发送：PDF + 图片 + Excel
    ↓
自动识别关联关系（图片是 PDF 的补充材料）
    ↓
组合分析：PDF 内容 + 图片标注 + Excel 数据验证
    ↓
生成综合报告
```

### 跨模态理解

- 视频 + 字幕 → 生成图文摘要
- 语音 + 聊天记录 → 会议纪要和待办
- 图片 + 表格 → 数据可视化建议

## 总结

**MCA 框架的核心价值：**
1. **解耦**：Gateway 只做下载，Agent 做决策，Model 做执行
2. **通用**：一套标准，支持所有渠道和所有多模态模型
3. **可扩展**：新增媒体类型只需添加处理器，不影响现有逻辑
4. **用户无感知**：用户正常发文件，系统自动唤醒对应能力

**实施三步走：**
1. Gateway 层：安装对应插件，启用媒体注入
2. Agent 层：安装本 Skill，自动检测媒体标记
3. Model 层：确保使用支持对应工具的模型

## 附录：动态工具发现

### 工具分层结构

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: 渠道特定工具 (Channel-Specific)                     │
│ 例如: feishu_sheet, discord_xxx, telegram_xxx               │
│ 特点: 只在特定渠道可用                                        │
└─────────────────────────────────────────────────────────────┘
                            ↑
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: 通用媒体工具 (Media Tools)                          │
│ 例如: image, pdf, browser                                   │
│ 特点: 所有渠道可用，但需要模型支持特定输入类型                    │
└─────────────────────────────────────────────────────────────┘
                            ↑
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: 核心工具 (Core Tools)                              │
│ 例如: read, write, edit, exec, web_search                   │
│ 特点: 始终可用，不依赖模型能力                                 │
└─────────────────────────────────────────────────────────────┘
```

**MCA 框架只依赖 Layer 1 和 Layer 2 的工具！**

### 工具适配策略

对于每种媒体类型，MCA 采用**优先原生、降级通用**的策略：

| 媒体类型 | 优先工具 | 降级方案 | 说明 |
|---------|---------|---------|------|
| image | `image` | Python + PIL | 原生工具需要模型支持 vision |
| pdf | `pdf` | Python + PyPDF2 | 原生工具更精准 |
| audio | Python + Whisper | - | 通用方案 |
| sheet | Python + pandas | - | 通用方案 |
| video | Python + ffmpeg | - | 通用方案 |
| code | `read` | Python 解析 | 原生工具最简单 |

### 获取当前环境的工具列表

**方式1: 通过工具发现脚本**（推荐）
```python
from scripts.tool_discovery import ToolDiscovery

discovery = ToolDiscovery()

# 获取所有可用工具
tools = discovery.get_available_tools()
# {'read', 'write', 'edit', 'exec', 'image', 'pdf', 'web_search'}

# 检查特定工具
if discovery.has_tool('image'):
    # 使用原生 image 工具
    process_with_native_tool()
else:
    # 使用 Python 脚本降级方案
    process_with_python_script()

# 获取媒体处理器配置
processors = discovery.get_media_processors()
```

**方式2: 读取配置文件**
```python
import json

with open('~/.openclaw/openclaw.json', 'r') as f:
    config = json.load(f)

# 从 tools.profile 获取基础工具集
profile = config.get('tools', {}).get('profile', 'full')

# 从模型配置发现媒体能力
for provider, provider_config in config.get('models', {}).get('providers', {}).items():
    for model in provider_config.get('models', []):
        if 'image' in model.get('input', []):
            print(f"模型 {provider}/{model['id']} 支持图片输入")
```

### 为什么需要动态发现

1. **不同部署环境工具不同**
   - 有些环境禁用 `exec` 工具
   - 有些环境没有配置 `web_search` API key
   - 有些模型不支持 `image` 输入

2. **避免硬编码工具依赖**
   - 如果写死使用 `image` 工具，在不支持 vision 的模型上会失败
   - 动态发现可以自动降级到 Python 方案

3. **最大化兼容性**
   - 同一个 skill 可以在不同配置的 OpenClaw 上运行
   - 自动适配最优的处理方式

### 生成适配报告

```python
from scripts.tool_discovery import ToolDiscovery

discovery = ToolDiscovery()
print(discovery.generate_adapter_report())
```

输出示例：
```
=== MCA 工具适配报告 ===

配置文件: ~/.openclaw/openclaw.json
工具配置 Profile: full

可用工具列表:
  ✓ read
  ✓ write
  ✓ edit
  ✓ exec
  ✓ image
  ✓ pdf
  ✓ web_search

媒体处理器配置:
  image: image (原生)
    使用 Vision 模型分析图片
  pdf: pdf (原生)
    使用 pdf 工具提取内容
  audio: python_script (通用)
    使用 Python + Whisper 转写音频
  sheet: python_script (通用)
    使用 Python + pandas 分析表格
  video: python_script (通用)
    使用 Python + ffmpeg 处理视频
```
