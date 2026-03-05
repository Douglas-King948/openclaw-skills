---
name: unified-search
description: |
  全球统一搜索引擎 - 聚合国内外11个搜索源，支持知识查询、代码搜索、技术问答、社区讨论。
  
  **核心能力：**
  - 联网搜索：Wikipedia(中英文)、GitHub、StackOverflow、知乎、百度百科等
  - 自动选择引擎：根据查询语言(中/英)和内容类型自动选择最优搜索源
  - 故障自动转移：一个引擎失败自动尝试其他引擎
  - 零配置：全部免费API，无需API Key
  
  **使用场景：**
  - 知识查询：查概念、查定义、查百科
  - 技术问题：编程错误、代码示例、最佳实践
  - 项目搜索：开源项目、代码仓库、软件包
  - 社区讨论：技术话题、热门讨论、问答解答
  
  **支持的搜索关键词：**
  "搜索xxx"、"查找xxx"、"查询xxx"、"联网搜索xxx"、"网上搜索xxx"、
  "结合搜索xxx"、"搜索一下xxx"、"帮我查xxx"、"找一下xxx"、
  "什么是xxx"、"xxx是什么"、"xxx怎么用"、"xxx教程"
  
  **支持的11个搜索引擎：**
  国外：Wikipedia(英文/中文)、GitHub、StackOverflow、Reddit、NPM、PyPI
  国内：百度百科、知乎、Gitee
  元搜索：SearX(聚合)
  
  **自动选择策略：**
  - 中文查询 → 优先百度百科、知乎、维基百科(中文)
  - 英文查询 → 优先维基百科(英文)、GitHub
  - 技术问题 → 优先StackOverflow、GitHub
  - 代码/项目 → 优先GitHub、Gitee、NPM、PyPI
  
  **触发时机：**
  当用户需要获取网络信息、查询知识、搜索项目、查找技术方案、了解最新资讯时自动调用。
  
version: 2.0.0
author: Cirno
---

# Unified Search 全球统一搜索

## 支持的搜索引擎

### 国外引擎
| 引擎 | 类型 | 特点 |
|------|------|------|
| wikipedia-en | 知识百科 | 英文百科，稳定免费 |
| wikipedia-zh | 知识百科 | 中文百科，稳定免费 |
| github | 代码仓库 | 开源项目、代码搜索 |
| stackoverflow | 技术问答 | 程序员问答社区 |
| npm | 包管理 | JavaScript/Node.js 包 |
| pypi | 包管理 | Python 包 |
| reddit | 社区讨论 | 国外社区讨论 |

### 国内引擎
| 引擎 | 类型 | 特点 |
|------|------|------|
| baidu-baike | 知识百科 | 百度百科 |
| zhihu | 问答社区 | 中文问答 |
| gitee | 代码仓库 | 国内GitHub |

### 元搜索引擎
| 引擎 | 类型 | 特点 |
|------|------|------|
| searx | 聚合搜索 | 聚合多个引擎结果 |

## 快速开始

### 1. 基本搜索（自动选择引擎）

```python
from global_search import search

# 自动选择最优引擎
result = search("Python 教程")

for r in result["results"]:
    print(f"{r['title']}: {r['url']}")
```

### 2. 指定引擎搜索

```python
# 搜索英文维基百科
result = search("Machine Learning", engine="wikipedia-en")

# 搜索GitHub项目
result = search("OpenClaw", engine="github")

# 搜索知乎
result = search("人工智能", engine="zhihu")

# 搜索StackOverflow
result = search("Python error", engine="stackoverflow")
```

### 3. 聚合搜索（多个引擎）

```python
from global_search import search_all

# 同时搜索多个引擎
result = search_all("深度学习", max_results=3)

print(f"共找到 {result['total_results']} 条结果")
for item in result["results"]:
    print(f"[{item['engine']}] {item['title']}")
```

## 使用示例

### 编程相关问题
```python
# 技术问题 → StackOverflow
search("Python list comprehension error", engine="stackoverflow")

# 找开源项目 → GitHub
search("machine learning framework", engine="github")

# Python包 → PyPI
search("requests", engine="pypi")
```

### 知识查询
```python
# 中文知识 → 百度百科 / 维基百科(中文)
search("人工智能", engine="baidu-baike")
search("深度学习", engine="wikipedia-zh")

# 英文知识 → 维基百科(英文)
search("Artificial Intelligence", engine="wikipedia-en")
```

### 社区讨论
```python
# 国外讨论 → Reddit
search("OpenClaw discussion", engine="reddit")

# 中文讨论 → 知乎
search("如何学习编程", engine="zhihu")
```

## 自动选择策略

系统根据查询内容自动选择最优引擎：

1. **中文查询** → 优先百度百科、知乎、维基百科(中文)
2. **英文查询** → 优先维基百科(英文)、GitHub
3. **技术问题** → 优先StackOverflow、GitHub
4. **代码/项目** → 优先GitHub、Gitee
5. **包/库** → 优先NPM、PyPI

## API 说明

### search(query, engine=None, max_results=5)

**参数：**
- `query`: 搜索关键词
- `engine`: 指定引擎，None则自动选择
- `max_results`: 最大结果数，默认5

**返回值：**
```python
{
    "success": True/False,
    "backend": "使用的引擎",
    "results": [
        {
            "title": "标题",
            "url": "链接",
            "snippet": "摘要",
            "source": "来源"
        }
    ]
}
```

### search_all(query, max_results=3)

同时搜索多个引擎，聚合结果。

## 特点

- ✅ **全部免费** - 无需API Key
- ✅ **全球覆盖** - 国内外主流引擎
- ✅ **自动语言** - 自动检测中英文
- ✅ **故障转移** - 一个失败自动尝试其他
- ✅ **类型丰富** - 知识、代码、社区、包管理

## 文件列表

| 文件 | 说明 |
|------|------|
| `global_search.py` | 主程序，包含所有搜索引擎 |
| `search.py` | 旧版（保留兼容） |
| `SKILL.md` | 本文档 |

---
*删除的旧版：Jina AI, Brave API, Tavily API, DuckDuckGo（不稳定）*
