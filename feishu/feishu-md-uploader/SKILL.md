---
name: feishu-md-uploader
description: |
  将本地 Markdown 文件上传到飞书并转换为云文档，支持自动格式转换和所有权转移。
  
  使用场景：
  1. 将本地生成的 MD 题库/文档上传到飞书云文档
  2. 批量文档迁移到飞书
  3. 自动化文档发布流程
  
  触发词：上传md到飞书、md转飞书文档、飞书文档上传、markdown上传飞书、
         feishu upload、publish to feishu、上传文档到飞书
---

# Feishu Markdown 上传器

自动将本地 Markdown 文件上传到飞书并转换为云文档。

## 核心功能

1. **MD → 飞书云文档**：自动转换格式
2. **所有权转移**：上传到指定文件夹，归属文件夹所有者
3. **完整保留**：表格、列表、代码块等格式

## 使用方法

### 快速上传

需要提供以下信息：
- `app_id`: 飞书应用 ID (cli_xxxx 格式)
- `app_secret`: 飞书应用密钥
- `folder_token`: 目标文件夹 token
- `file_path`: 本地 MD 文件路径
- `title` (可选): 文档标题，默认使用文件名

### 示例

```python
# 单文件上传
result = await upload_md_to_feishu(
    app_id="cli_a903ccc2bb791bde",
    app_secret="xo0A1dGoHvIAluomqNS6ob2igrEgJbdN",
    folder_token="YicMfAq2clUtHZdZBXJcdhhvnJh",
    file_path="D:/output/题库.md",
    title="零碳未来领袖计划题库"
)
```

## API 端点

| 端点 | 用途 |
|------|------|
| `/auth/v3/tenant_access_token/internal` | 获取访问令牌 |
| `/drive/v1/medias/upload_all` | 上传文件到 Drive |
| `/drive/v1/import_tasks` | 创建 MD→DOCX 导入任务 |
| `/drive/v1/import_tasks/{ticket}` | 查询导入状态 |

## 完整流程

```
1. 获取 Tenant Access Token
   ↓
2. 读取本地 MD 文件
   ↓
3. 上传文件到飞书 Drive
   ↓
4. 创建导入任务 (md → docx)
   ↓
5. 轮询等待转换完成
   ↓
6. 返回飞书云文档 URL
```

## 返回值

```json
{
  "success": true,
  "document_token": "Gb3ZdXWWqoeTzExsSWvca6HCn8c",
  "url": "https://feishu.cn/docx/Gb3ZdXWWqoeTzExsSWvca6HCn8c",
  "title": "文档标题"
}
```

## 错误处理

- `400`: 参数错误，检查文件格式
- `401`: Token 失效，重新获取
- `404`: 文件夹不存在
- `429`: API 限流，自动重试

## 注意事项

1. 飞书应用需要开启以下权限：
   - `drive:drive` - 云空间权限
   - `docx:document` - 文档权限
   - `wiki:wiki` - 知识库权限（可选）

2. 文件大小限制：默认 20MB

3. 所有权：文档创建在指定文件夹中，归属该文件夹所有者
