# Smart Meme System v3 - 受控版

## 设计原则：安全、自治、可控

v3在借鉴GitHub成熟项目(photos-storage-discord)的基础上，针对OpenClaw真实环境做了安全适配。

## 核心特性

### ✅ 安全机制

| 机制 | 说明 | 解决的问题 |
|------|------|-----------|
| **熔断器** | 连续失败3次后冷却5分钟 | 防止无限循环 |
| **存储上限** | 默认500MB上限 | 防止磁盘爆满 |
| **SHA256分块** | 8KB分块计算哈希 | 防止内存爆炸 |
| **JSON存储** | 替代SQLite | 防止并发锁定 |
| **功能开关** | 所有功能可独立开关 | 紧急关闭问题功能 |

### 🤖 自治能力

```
检查 → 发现问题 → 自愈（受控）
  ↑                    ↓
  └────── 冷却期后重置 ←┘
```

- 触发式补充：使用表情包时检查库存
- 熔断保护：失败时自动停止，冷却后重试
- 健康检查：定期生成报告

## 文件结构

```
smart-meme-v3/
├── config.py              # 集中配置 + 安全限制
├── main.py                # 统一入口
├── core/
│   ├── store.py           # JSON存储 + SHA256去重
│   ├── download.py        # 下载器 + 熔断机制
│   └── selector.py        # 选择器（只读）
├── evolve/
│   ├── health.py          # 健康检查（只读）
│   └── heal.py            # 自愈（受控）
├── test_safety.py         # 安全测试套件
└── local_memes/           # 表情包存储目录
```

## 使用方法

### 1. 首次运行 - 下载表情包

```bash
cd D:/openclaw/skills/smart-meme-v3
python main.py download
```

### 2. 查看统计

```bash
python main.py stats
```

### 3. 健康检查

```bash
python main.py check
```

### 4. 测试自愈（预演模式）

```bash
python main.py heal --dry-run
```

### 5. 实际自愈（需开启auto_restock）

编辑 `config.py`:
```python
FEATURES = {
    "auto_restock": True,   # 开启自动补充
    "health_check": True,
    "dedup": True,
}
```

然后运行：
```bash
python main.py heal
```

## 在OpenClaw中使用

```python
# 在agent中使用
from core.selector import random_meme
from evolve.heal import check_and_heal

# 触发式检查并补充
check_and_heal()

# 获取表情包
meme = random_meme("panda")
if meme:
    message.send(media=meme["path"])
```

## 安全测试

在部署前必须运行安全测试：

```bash
python test_safety.py
```

测试项目：
1. ✅ SHA256分块计算（防内存爆炸）
2. ✅ 熔断机制（防无限循环）
3. ✅ 存储上限检查（防爆盘）
4. ✅ JSON存储（无并发问题）
5. ✅ 健康检查（正常工作）

## 配置说明

### 安全限制（config.py）

```python
MAX_STORAGE_MB = 500       # 存储上限
MAX_RETRY = 3              # 最大重试
COOLDOWN_SECONDS = 300     # 冷却时间
MAX_FILE_SIZE_MB = 25      # 单文件上限
CHUNK_SIZE = 8192          # SHA256分块大小
```

### 功能开关

```python
FEATURES = {
    "auto_restock": False,  # 自动补充（默认关闭）
    "health_check": True,   # 健康检查（安全，默认开启）
    "dedup": True,          # 去重（推荐开启）
    "strict_mode": False,   # 严格模式
}
```

## 对比三个版本

| 维度 | v1 (混乱) | v2 (简洁) | v3 (受控版) |
|------|----------|----------|------------|
| 代码复杂度 | 高 | 低 | 中 |
| 安全机制 | 无 | 无 | ✅ 熔断+上限+分块 |
| 自治能力 | 混乱 | 无 | ✅ 受控自治 |
| 存储方式 | JSON索引 | 目录扫描 | ✅ JSON+SHA256 |
| 风险等级 | 🔴 高 | 🟢 低 | 🟡 中(可控) |
| 生产就绪 | ❌ | ✅ | ✅ (需测试) |

## 风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 无限循环 | 低 | 高 | 熔断器+冷却期 |
| 内存爆炸 | 低 | 高 | SHA256分块计算 |
| 磁盘爆满 | 低 | 中 | 存储上限检查 |
| 并发问题 | 无 | 高 | 使用JSON替代SQLite |

## 回滚方案

如果v3出现问题：

```bash
# 一键回滚到v2
mv smart-meme-v3 smart-meme-v3-backup
mv smart-meme-v2 smart-meme
```

## 后续优化方向

1. **图片压缩**：超过2MB自动压缩
2. **智能标签**：使用CLIP模型自动打标签
3. **增量同步**：只下载新增的表情包
4. **Web界面**：可视化浏览库存

## 参考项目

- [photos-storage-discord](https://github.com/suhrusai/photos-storage-discord) - SHA256去重+pickle持久化

---

**状态**: ✅ 已完成安全设计，等待测试通过
