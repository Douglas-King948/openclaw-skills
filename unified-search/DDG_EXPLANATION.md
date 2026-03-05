# 为什么 DuckDuckGo 之前能用，现在不能用了？

## 📅 时间线

### 2026-03-03 之前
✅ **DuckDuckGo 可用**
- 通过 DuckDuckGo HTML 版本搜索
- 返回 JSON 结果
- 每天约 1000 次免费额度

### 2026-03-04 现在
❌ **DuckDuckGo 被限制**
- 返回 HTTP 202 或 403 错误
- 请求被拒绝
- 需要人机验证（Captcha）

---

## 🔍 原因分析

### 1. 反爬虫机制升级
```
DuckDuckGo 检测到自动化请求频率过高，
启用了更严格的反爬虫保护。
```

### 2. 请求特征识别
```python
# 之前的请求会被识别为机器人：
- 没有浏览器 User-Agent
- 请求头不完整
- 访问模式规律化
```

### 3. IP/账号限制
```
可能的原因：
- 同一IP请求过多
- 请求频率过高
- 被标记为自动化工具
```

### 4. API 策略变更
```
DuckDuckGo 官方政策变化：
- 限制程序化访问
- 鼓励使用官方 API（Instant Answers API）
- 但官方 API 功能有限
```

---

## 🛠️ 尝试过但失败的解决方案

### 尝试 1：模拟浏览器请求
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Accept": "text/html,application/xhtml+xml...",
    # ... 完整浏览器头
}
```
**结果**：仍然 403

### 尝试 2：使用代理
```python
# 更换出口IP
proxies = {...}
```
**结果**：短时间内有效，很快又被封

### 尝试 3：降低请求频率
```python
time.sleep(random.uniform(2, 5))  # 随机延迟
```
**结果**：仍然触发反爬虫

### 尝试 4：使用不同的 DDG 端点
```
https://duckduckgo.com/html/
https://html.duckduckgo.com/html/
https://lite.duckduckgo.com/lite/
```
**结果**：全部受限

---

## ✅ 最终解决方案

**放弃 DuckDuckGo，改用更稳定的替代方案：**

| 原方案 | 替代方案 | 稳定性 |
|--------|----------|--------|
| DuckDuckGo | Wikipedia API | ⭐⭐⭐⭐⭐ |
| DuckDuckGo | GitHub API | ⭐⭐⭐⭐⭐ |
| DuckDuckGo | StackOverflow API | ⭐⭐⭐⭐⭐ |

**这些替代方案的优势：**
1. ✅ 官方API支持程序化访问
2. ✅ 有明确的 Rate Limit（不会被突然封禁）
3. ✅ 返回结构化数据（JSON）
4. ✅ 稳定性更高

---

## 📊 对比

| 特性 | DuckDuckGo | Wikipedia | GitHub |
|------|-----------|-----------|--------|
| 免费 | ✅ | ✅ | ✅ |
| 无需API Key | ✅ (之前) | ✅ | ✅ |
| 反爬虫 | 严格 | 宽松 | 无 |
| 稳定性 | 低 | 高 | 高 |
| 通用搜索 | ✅ | ❌ (知识) | ❌ (代码) |

**结论：**
虽然失去了通用搜索引擎，但通过组合多个专业搜索引擎（Wikipedia+GitHub+StackOverflow等），
能更好地满足不同类型查询的需求，且稳定性更高。

---

*DuckDuckGo 限制可能是临时的，也可能是永久的。建议观望，但目前以稳定替代方案为主。*
