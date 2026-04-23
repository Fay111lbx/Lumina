# 其他工具 API 详解

本文档详细介绍 OmniAgent 项目中可选的其他工具 API，包括申请方式、使用场景和对比分析。

---

## 📋 目录

1. [Google Search API (SerpApi)](#1-google-search-api-serpapi)
2. [快递查询 API (阿里云市场)](#2-快递查询-api-阿里云市场)
3. [BoCha 搜索 API](#3-bocha-搜索-api)
4. [API 对比与选择建议](#4-api-对比与选择建议)

---

## 1. Google Search API (SerpApi)

### 什么是 SerpApi？

**SerpApi** 是一个聚合搜索引擎 API 服务，它可以帮你调用 Google、Bing、百度等多个搜索引擎，并返回结构化的搜索结果。

### 为什么需要 SerpApi？

Google 官方的搜索 API 非常昂贵且复杂，SerpApi 提供了一个更简单、更便宜的替代方案。

### 主要特点

✅ **支持多个搜索引擎**：Google、Bing、百度、Yahoo 等  
✅ **返回结构化数据**：JSON 格式，易于解析  
✅ **支持多种搜索类型**：网页、图片、新闻、视频、地图等  
✅ **免费试用**：100 次免费搜索  

### 申请步骤

#### 第一步：注册账号

1. 访问：https://serpapi.com/
2. 点击右上角 "Sign Up"
3. 使用邮箱或 Google 账号注册

#### 第二步：获取 API Key

1. 登录后进入 Dashboard
2. 在 "API Key" 部分可以看到你的密钥
3. 格式类似：`a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

#### 第三步：配置到项目

```yaml
# config.yaml
tools:
  google:
    api_key: "你的SerpApi-Key"
```

### 价格

- **免费计划**：100 次搜索/月
- **开发者计划**：$50/月，5,000 次搜索
- **生产计划**：$250/月，30,000 次搜索

### 使用示例

```python
from serpapi import GoogleSearch

params = {
    "api_key": "你的API-Key",
    "engine": "google",
    "q": "人工智能最新进展",
    "location": "China",
    "hl": "zh-cn",
    "gl": "cn",
    "num": 10
}

search = GoogleSearch(params)
results = search.get_dict()

# 获取搜索结果
for result in results.get("organic_results", []):
    print(f"标题: {result['title']}")
    print(f"链接: {result['link']}")
    print(f"摘要: {result['snippet']}")
    print("---")
```

### 返回结果示例

```json
{
  "organic_results": [
    {
      "position": 1,
      "title": "人工智能的最新突破",
      "link": "https://example.com/ai-breakthrough",
      "snippet": "2024年人工智能领域取得了重大突破...",
      "date": "2024-04-20"
    }
  ],
  "related_searches": [
    "人工智能应用",
    "AI技术发展"
  ]
}
```

### 在项目中的应用

```python
# src/backend/agentchat/tools/google_search.py

from langchain.tools import BaseTool
from serpapi import GoogleSearch

class GoogleSearchTool(BaseTool):
    name = "google_search"
    description = "使用 Google 搜索引擎查询信息。适合需要权威、全面搜索结果的场景。"
    
    def _run(self, query: str) -> str:
        params = {
            "api_key": settings.tools.google.api_key,
            "engine": "google",
            "q": query,
            "hl": "zh-cn",
            "num": 5
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # 格式化结果
        formatted = []
        for item in results.get("organic_results", []):
            formatted.append(
                f"标题：{item['title']}\n"
                f"链接：{item['link']}\n"
                f"摘要：{item['snippet']}\n"
            )
        
        return "\n---\n".join(formatted)
```

### 适用场景

- ✅ 需要最权威、最全面的搜索结果
- ✅ 需要搜索特定类型内容（图片、新闻、视频）
- ✅ 需要获取搜索排名数据
- ✅ 企业级应用，预算充足

### 与 Tavily 的对比

| 特性 | SerpApi | Tavily |
|------|---------|--------|
| 免费额度 | 100次/月 | 1000次/月 |
| 价格 | $50/月起 | $49/月起 |
| 搜索质量 | Google 原生结果 | AI 优化结果 |
| 易用性 | 需要解析结果 | 开箱即用 |
| 适用场景 | 需要 Google 搜索 | AI Agent 应用 |

---

## 2. 快递查询 API (阿里云市场)

### 什么是快递查询 API？

这是阿里云市场提供的快递物流查询服务，可以查询国内外主流快递公司的物流信息。

### 主要特点

✅ **支持快递公司多**：顺丰、圆通、中通、韵达、EMS 等 100+ 家  
✅ **数据实时更新**：物流信息实时同步  
✅ **识别快递公司**：自动识别快递单号对应的快递公司  
✅ **价格便宜**：按次计费，非常实惠  

### 申请步骤

#### 第一步：注册阿里云账号

1. 访问：https://www.aliyun.com/
2. 注册阿里云账号（需要实名认证）

#### 第二步：进入阿里云市场

1. 访问：https://market.aliyun.com/
2. 搜索 "快递查询"
3. 选择一个服务商（推荐：快递鸟、快递100）

#### 第三步：购买服务

1. 选择套餐（通常有免费试用）
2. 点击 "立即购买"
3. 完成支付（免费套餐也需要点击购买）

#### 第四步：获取 API Key

1. 进入 "控制台" → "云市场"
2. 找到已购买的快递查询服务
3. 查看 "AppCode" 或 "AppKey"
4. 这就是你的 API Key

#### 第五步：配置到项目

```yaml
# config.yaml
tools:
  delivery:
    api_key: "你的AppCode"
    endpoint: "https://qyexpress.market.alicloudapi.com/composite/queryexpress"
```

### 价格

- **免费试用**：通常 100-500 次
- **按次计费**：0.01-0.05 元/次
- **包月套餐**：几十元/月，几千次调用

### 使用示例

```python
import requests

def query_delivery(tracking_number: str):
    url = "https://qyexpress.market.alicloudapi.com/composite/queryexpress"
    
    headers = {
        "Authorization": f"APPCODE {api_key}"
    }
    
    params = {
        "no": tracking_number  # 快递单号
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    return data
```

### 返回结果示例

```json
{
  "status": "200",
  "msg": "查询成功",
  "result": {
    "number": "SF1234567890",
    "type": "顺丰速运",
    "list": [
      {
        "time": "2024-04-21 10:30:00",
        "status": "已签收，签收人：本人"
      },
      {
        "time": "2024-04-21 08:15:00",
        "status": "派件中，快递员：张三，电话：138****1234"
      },
      {
        "time": "2024-04-20 20:00:00",
        "status": "到达目的地网点"
      }
    ]
  }
}
```

### 在项目中的应用

```python
# src/backend/agentchat/tools/delivery.py

from langchain.tools import BaseTool
import requests

class DeliveryQueryTool(BaseTool):
    name = "query_delivery"
    description = "查询快递物流信息。输入快递单号，返回物流详情。"
    
    def _run(self, tracking_number: str) -> str:
        url = settings.tools.delivery.endpoint
        headers = {"Authorization": f"APPCODE {settings.tools.delivery.api_key}"}
        params = {"no": tracking_number}
        
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if data["status"] == "200":
            result = data["result"]
            info = [f"快递公司：{result['type']}"]
            info.append(f"快递单号：{result['number']}")
            info.append("\n物流信息：")
            
            for item in result["list"]:
                info.append(f"{item['time']}: {item['status']}")
            
            return "\n".join(info)
        else:
            return "查询失败，请检查快递单号是否正确"
```

### 适用场景

- ✅ 电商平台的物流查询
- ✅ 客服机器人查询快递
- ✅ 订单管理系统
- ✅ 个人助手查询快递

### 使用示例对话

```
用户：帮我查一下快递 SF1234567890
Agent：调用快递查询工具
Agent：您的快递（顺丰速运）已于今天上午 10:30 签收，签收人为本人。
```

---

## 3. BoCha 搜索 API

### 什么是 BoCha？

**BoCha（博查）** 是一个国内的 AI 搜索 API 服务，类似于 Tavily，专门为 AI 应用设计。

### 主要特点

✅ **国内服务**：服务器在国内，速度快  
✅ **支持中文**：对中文搜索优化更好  
✅ **AI 优化**：返回结果适合 LLM 理解  
✅ **价格实惠**：比国外服务便宜  

### 申请步骤

#### 第一步：访问官网

访问：https://api.bochaai.com/

#### 第二步：注册账号

1. 点击 "注册" 或 "登录"
2. 使用手机号或邮箱注册

#### 第三步：获取 API Key

1. 登录后进入控制台
2. 创建应用
3. 获取 API Key

#### 第四步：配置到项目

```yaml
# config.yaml
tools:
  bocha:
    api_key: "sk-你的BoCha-Key"
    endpoint: "https://api.bochaai.com/v1/web-search"
```

### 价格

- **免费试用**：通常有一定额度
- **按次计费**：具体价格需要咨询官方

### 使用示例

```python
import requests

def bocha_search(query: str):
    url = "https://api.bochaai.com/v1/web-search"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "query": query,
        "max_results": 5
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

### 适用场景

- ✅ 主要面向中文用户的应用
- ✅ 需要快速响应的国内服务
- ✅ 预算有限的项目
- ✅ 对中文搜索质量要求高

---

## 4. API 对比与选择建议

### 搜索类 API 对比

| API | 免费额度 | 价格 | 搜索质量 | 速度 | 适用场景 |
|-----|---------|------|---------|------|---------|
| **Tavily** | 1000次/月 | $49/月 | ⭐⭐⭐⭐ | 快 | AI Agent 首选 |
| **SerpApi** | 100次/月 | $50/月 | ⭐⭐⭐⭐⭐ | 中等 | 需要 Google 搜索 |
| **BoCha** | 待确认 | 较便宜 | ⭐⭐⭐ | 很快 | 国内中文应用 |

### 工具类 API 对比

| API | 价格 | 功能 | 适用场景 |
|-----|------|------|---------|
| **高德天气** | 免费 30万次/天 | 天气查询 | 所有需要天气的应用 |
| **快递查询** | 0.01元/次 | 物流查询 | 电商、客服系统 |

### 选择建议

#### 对于初学者（学习阶段）

**推荐配置：**
```yaml
tools:
  weather:
    api_key: "高德地图Key"  # 必选，免费额度大
  
  tavily:
    api_key: "Tavily Key"   # 推荐，免费 1000 次
```

**理由：**
- 高德天气免费额度充足
- Tavily 专为 AI 设计，易用
- 这两个足够学习和测试

#### 对于个人项目

**推荐配置：**
```yaml
tools:
  weather:
    api_key: "高德地图Key"
  
  tavily:
    api_key: "Tavily Key"
  
  delivery:
    api_key: "快递查询Key"  # 如果需要快递功能
```

**理由：**
- 成本低（快递查询很便宜）
- 功能够用
- 易于维护

#### 对于商业项目

**推荐配置：**
```yaml
tools:
  weather:
    api_key: "高德地图Key"
  
  google:
    api_key: "SerpApi Key"  # 搜索质量最好
  
  delivery:
    api_key: "快递查询Key"
  
  # 可选：作为备用
  tavily:
    api_key: "Tavily Key"
```

**理由：**
- Google 搜索质量最高
- 多个 API 互为备份
- 满足商业需求

---

## 5. 成本估算

### 学习阶段（免费）

```
高德天气：免费 30万次/天
Tavily：免费 1000次/月

总成本：0 元/月
```

### 个人项目（小规模）

```
高德天气：免费
Tavily：免费 1000次/月
快递查询：100次 × 0.01元 = 1元/月

总成本：约 1-5 元/月
```

### 商业项目（中等规模）

```
高德天气：免费
SerpApi：$50/月（5000次）
快递查询：10000次 × 0.01元 = 100元/月

总成本：约 450 元/月
```

---

## 6. 实用技巧

### 技巧 1：实现 API 降级

当主要 API 失败时，自动切换到备用 API：

```python
class SearchTool(BaseTool):
    def _run(self, query: str) -> str:
        try:
            # 优先使用 Tavily
            return self._tavily_search(query)
        except Exception as e:
            logger.warning(f"Tavily 失败: {e}")
            try:
                # 降级到 SerpApi
                return self._serpapi_search(query)
            except Exception as e:
                logger.error(f"SerpApi 也失败: {e}")
                return "搜索服务暂时不可用"
```

### 技巧 2：实现缓存节省成本

```python
import redis
import hashlib

class CachedSearchTool(BaseTool):
    def __init__(self):
        self.redis = redis.Redis()
        self.cache_ttl = 3600  # 1小时
    
    def _run(self, query: str) -> str:
        # 生成缓存 key
        cache_key = f"search:{hashlib.md5(query.encode()).hexdigest()}"
        
        # 检查缓存
        cached = self.redis.get(cache_key)
        if cached:
            return cached.decode()
        
        # 调用 API
        result = self._search(query)
        
        # 存入缓存
        self.redis.setex(cache_key, self.cache_ttl, result)
        
        return result
```

### 技巧 3：监控 API 使用量

```python
class APIUsageTracker:
    def __init__(self):
        self.redis = redis.Redis()
    
    def track(self, api_name: str):
        """记录 API 调用"""
        key = f"api_usage:{api_name}:{datetime.now().strftime('%Y-%m')}"
        self.redis.incr(key)
    
    def get_usage(self, api_name: str) -> int:
        """获取本月使用量"""
        key = f"api_usage:{api_name}:{datetime.now().strftime('%Y-%m')}"
        return int(self.redis.get(key) or 0)
```

---

## 7. 总结

### 必选 API（免费）
- ✅ **高德天气 API** - 免费额度大，必备

### 推荐 API（学习阶段）
- ✅ **Tavily Search** - 免费 1000 次，够用

### 可选 API（按需选择）
- 🔧 **快递查询** - 如果需要快递功能
- 🔧 **SerpApi** - 如果需要 Google 搜索质量
- 🔧 **BoCha** - 如果主要面向国内用户

### 下一步行动

1. **现在就可以启动项目**（已配置高德天气）
2. **申请 Tavily**（5 分钟，免费 1000 次）
3. **其他 API 按需申请**（不着急）

---

有任何问题随时问我！🚀
