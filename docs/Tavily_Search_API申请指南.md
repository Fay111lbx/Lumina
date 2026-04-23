# Tavily Search API 申请指南

## 什么是 Tavily？

Tavily 是一个专门为 AI Agent 设计的联网搜索 API 服务。它可以让你的 AI 助手实时搜索互联网信息，获取最新的新闻、资料、数据等。

---

## 申请步骤

### 第一步：访问官网

打开浏览器，访问：https://tavily.com/

### 第二步：注册账号

1. 点击右上角的 **"Sign Up"** 或 **"Get Started"**
2. 选择注册方式：
   - 使用 Google 账号登录（推荐，最快）
   - 使用 GitHub 账号登录
   - 使用邮箱注册

### 第三步：获取 API Key

1. 登录后，会自动跳转到控制台（Dashboard）
2. 在控制台首页，你会看到你的 **API Key**
3. 格式类似：`tvly-xxxxxxxxxxxxxxxxxxxxxx`
4. 点击复制按钮，保存好这个 Key

### 第四步：配置到项目

将获取到的 API Key 填入配置文件：

```yaml
# src/backend/agentchat/config.yaml
tools:
  tavily:
    api_key: "tvly-你的API-Key"
```

---

## 免费额度

- **每月免费调用次数**：1,000 次
- **每次搜索返回结果数**：最多 10 条
- **适用场景**：个人学习、小型项目完全够用

如果需要更多额度，可以升级到付费计划：
- **Pro 计划**：$49/月，10,000 次调用
- **Enterprise 计划**：定制化，无限调用

---

## API 使用示例

### 基本搜索

```python
import requests

api_key = "tvly-你的API-Key"
url = "https://api.tavily.com/search"

payload = {
    "api_key": api_key,
    "query": "最新的人工智能新闻",
    "search_depth": "basic",  # basic 或 advanced
    "max_results": 5
}

response = requests.post(url, json=payload)
results = response.json()

print(results)
```

### 返回结果示例

```json
{
  "query": "最新的人工智能新闻",
  "results": [
    {
      "title": "OpenAI 发布 GPT-5",
      "url": "https://example.com/news/gpt5",
      "content": "OpenAI 今天宣布推出 GPT-5...",
      "score": 0.95,
      "published_date": "2024-04-20"
    },
    {
      "title": "谷歌推出新一代 AI 芯片",
      "url": "https://example.com/news/google-chip",
      "content": "谷歌在今天的发布会上...",
      "score": 0.89,
      "published_date": "2024-04-19"
    }
  ]
}
```

---

## 在 OmniAgent 项目中的应用

### 1. 工具定义

```python
# src/backend/agentchat/tools/tavily_search.py

from langchain.tools import BaseTool
import requests

class TavilySearchTool(BaseTool):
    name = "web_search"
    description = "搜索互联网获取最新信息。输入搜索关键词，返回相关网页内容。"
    
    def _run(self, query: str) -> str:
        """执行网络搜索"""
        api_key = settings.tools.tavily.api_key
        url = "https://api.tavily.com/search"
        
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": 3
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        # 格式化结果
        results = []
        for item in data.get("results", []):
            results.append(f"标题：{item['title']}\n内容：{item['content']}\n来源：{item['url']}\n")
        
        return "\n---\n".join(results)
```

### 2. 使用场景示例

**场景 1：获取最新新闻**
```
用户：最近有什么 AI 领域的重大新闻？
Agent：调用 Tavily 搜索 "AI 人工智能 最新新闻"
Agent：整理搜索结果，生成回答
```

**场景 2：实时信息查询**
```
用户：今天的美元汇率是多少？
Agent：调用 Tavily 搜索 "美元汇率 今日"
Agent：从搜索结果中提取汇率信息
```

**场景 3：知识问答**
```
用户：什么是量子计算？
Agent：调用 Tavily 搜索 "量子计算 原理"
Agent：基于搜索结果生成通俗易懂的解释
```

---

## 与其他搜索 API 的对比

### Google Search API (SerpApi)

**优点：**
- 搜索结果最全面
- 支持图片、视频、新闻等多种搜索

**缺点：**
- 价格较高（$50/月起）
- 返回结果需要自己解析
- 配置复杂

**申请地址：** https://serpapi.com/

### Bing Search API

**优点：**
- 微软官方支持
- 结果质量高

**缺点：**
- 价格昂贵（$7/1000次）
- 需要 Azure 账号
- 配置复杂

**申请地址：** https://www.microsoft.com/en-us/bing/apis/bing-web-search-api

### BoCha Search API

**优点：**
- 国内服务，速度快
- 支持中文搜索

**缺点：**
- 知名度较低
- 文档较少

**申请地址：** https://api.bochaai.com/

---

## 常见问题

### Q1: Tavily 免费额度用完了怎么办？

**方案 1：** 升级到付费计划  
**方案 2：** 使用其他搜索 API（如 SerpApi）  
**方案 3：** 实现搜索结果缓存，减少重复搜索  

### Q2: Tavily 支持中文搜索吗？

支持！Tavily 可以搜索全球网页，包括中文内容。

### Q3: 搜索结果的准确性如何？

Tavily 使用先进的 AI 算法对搜索结果进行排序和过滤，准确性很高。但建议在关键场景下，让用户确认信息的准确性。

### Q4: 可以搜索特定网站吗？

可以！在搜索关键词中加入 `site:` 限定：
```python
query = "人工智能 site:zhihu.com"  # 只搜索知乎
```

### Q5: 如何避免超出免费额度？

1. **实现缓存机制**：相同的搜索在一定时间内返回缓存结果
2. **限制用户调用频率**：每个用户每天最多搜索 N 次
3. **只在必要时搜索**：让 Agent 判断是否真的需要联网搜索

---

## 实现搜索缓存（节省额度）

```python
# src/backend/agentchat/tools/tavily_search.py

import redis
import hashlib
import json

class TavilySearchTool(BaseTool):
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379)
        self.cache_ttl = 3600  # 缓存 1 小时
    
    def _run(self, query: str) -> str:
        # 生成缓存 key
        cache_key = f"search:{hashlib.md5(query.encode()).hexdigest()}"
        
        # 检查缓存
        cached = self.redis_client.get(cache_key)
        if cached:
            print("从缓存返回结果")
            return cached.decode()
        
        # 调用 API
        result = self._search_tavily(query)
        
        # 存入缓存
        self.redis_client.setex(cache_key, self.cache_ttl, result)
        
        return result
    
    def _search_tavily(self, query: str) -> str:
        # 实际的搜索逻辑
        ...
```

---

## 总结

**Tavily Search API 的优势：**
✅ 专为 AI 设计，返回结果易于理解  
✅ 免费额度充足（1000次/月）  
✅ 申请简单，5 分钟搞定  
✅ API 接口简洁，易于集成  

**适用场景：**
- 让 AI 助手获取实时信息
- 新闻资讯查询
- 知识问答增强
- 数据收集和分析

**下一步：**
1. 访问 https://tavily.com/ 注册账号
2. 获取 API Key
3. 配置到项目中
4. 测试搜索功能

有任何问题随时问我！🚀
