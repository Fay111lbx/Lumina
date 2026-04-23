# 🔑 API 密钥配置指南

本文档详细说明如何获取 OmniAgent 所需的各种 API 密钥。

## 📋 目录

- [必需配置](#必需配置)
- [可选配置](#可选配置)
- [配置优先级建议](#配置优先级建议)
- [费用说明](#费用说明)

---

## 必需配置

这些是运行 OmniAgent 必须配置的 API 密钥。

### 1. 阿里云百炼 (DashScope) - 核心 LLM 服务

**用途**: 对话模型、工具调用、推理、文生图、Embedding、Rerank

**官网**: https://dashscope.aliyun.com

**申请步骤**:

1. 访问 [阿里云百炼控制台](https://dashscope.aliyun.com)
2. 使用阿里云账号登录（没有账号需要先注册）
3. 点击右上角"开通服务"
4. 进入"API-KEY管理"页面
5. 点击"创建新的API-KEY"
6. 复制生成的 API Key（格式：`sk-xxxxxxxxxxxxxx`）

**配置位置**:
```yaml
multi_models:
  conversation_model:
    api_key: "sk-你的API-Key"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name: "qwen3.5-plus"
  
  tool_call_model:
    api_key: "sk-你的API-Key"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name: "qwen3.5-plus"
  
  reasoning_model:
    api_key: "sk-你的API-Key"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name: "qwen3.5-plus"
  
  text2image:
    api_key: "sk-你的API-Key"
    base_url: "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    model_name: "wanx2.0-t2i-turbo"
  
  qwen_vl:
    api_key: "sk-你的API-Key"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name: "qwen-vl-plus"
  
  embedding:
    api_key: "sk-你的API-Key"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name: "text-embedding-v3"
  
  rerank:
    api_key: "sk-你的API-Key"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name: "qwen-vl-rerank"
```

**费用说明**:
- 新用户赠送免费额度（通常 100-500 万 tokens）
- 按量付费，价格参考：
  - qwen3.5-plus: ¥0.0008/千tokens (输入), ¥0.002/千tokens (输出)
  - 文生图: ¥0.08/张
- 详细价格: https://help.aliyun.com/zh/model-studio/getting-started/models

**注意事项**:
- API Key 请妥善保管，不要泄露
- 可以设置每日消费上限，避免超支
- 建议开启账户余额预警

---

## 可选配置

这些 API 密钥是可选的，不配置不影响核心功能。

### 2. 高德地图 - 天气查询

**用途**: 天气查询工具

**官网**: https://lbs.amap.com

**申请步骤**:

1. 访问 [高德开放平台](https://lbs.amap.com)
2. 注册/登录账号
3. 进入"控制台" → "应用管理"
4. 点击"创建新应用"
5. 填写应用名称（如：OmniAgent）
6. 添加 Key：
   - 服务平台：选择"Web服务"
   - Key 名称：随意填写
7. 复制生成的 Key

**配置位置**:
```yaml
tools:
  weather:
    api_key: "你的高德地图Key"
    endpoint: "https://restapi.amap.com/v3/weather/weatherInfo?parameters"
```

**费用说明**:
- 完全免费
- 每日调用限额：个人开发者 30万次/天

**注意事项**:
- 需要实名认证
- 如果不配置，天气查询功能将不可用

---

### 3. Tavily Search - 联网搜索

**用途**: 通用联网搜索、新闻搜索

**官网**: https://tavily.com

**申请步骤**:

1. 访问 [Tavily 官网](https://tavily.com)
2. 点击"Get Started"注册账号
3. 登录后进入 Dashboard
4. 在"API Keys"页面复制你的 API Key

**配置位置**:
```yaml
tools:
  tavily:
    api_key: "tvly-你的API-Key"
```

**费用说明**:
- 免费版：1000 次/月
- Pro 版：$29/月，10000 次
- Enterprise：按需定制

**注意事项**:
- 免费额度对个人开发足够
- 支持多种搜索类型：general、news、finance
- 如果不配置，联网搜索功能将不可用

---

### 4. 阿里云市场 - 快递查询

**用途**: 物流快递查询

**官网**: https://market.aliyun.com

**申请步骤**:

1. 访问 [阿里云市场](https://market.aliyun.com)
2. 搜索"快递查询"
3. 选择一个服务商（推荐：快递鸟、快递100）
4. 点击"立即购买"
5. 选择套餐（有免费试用）
6. 购买后在"已购买的服务"中查看 AppCode

**配置位置**:
```yaml
tools:
  delivery:
    api_key: "你的AppCode"
    endpoint: "https://qyexpress.market.alicloudapi.com/composite/queryexpress"
```

**费用说明**:
- 免费试用：100-500 次/天
- 付费套餐：
  - 基础版：¥9.9/月（1000次）
  - 标准版：¥29.9/月（5000次）
  - 企业版：¥99/月（20000次）

**免费替代方案**:

如果不想付费，可以使用快递100免费API：

1. 访问 https://www.kuaidi100.com/openapi
2. 注册企业账号（个人也可申请）
3. 获取 API Key 和 Customer
4. 修改代码中的快递查询接口

**注意事项**:
- 如果不配置，快递查询功能将不可用
- 建议先使用免费试用额度测试

---

### 5. BoCha AI (博查) - 增强搜索

**用途**: 增强型联网搜索

**官网**: https://bochaai.com

**申请步骤**:

1. 访问 [BoCha AI 官网](https://bochaai.com)
2. 注册账号
3. 进入控制台
4. 在"API Keys"页面获取密钥

**配置位置**:
```yaml
tools:
  bocha:
    api_key: "sk-你的API-Key"
    endpoint: "https://api.bochaai.com/v1/web-search"
```

**费用说明**:
- 免费版：500 次/月
- 基础版：¥49/月，5000 次
- 专业版：¥199/月，30000 次

**注意事项**:
- 可选配置，不影响核心功能
- 提供比 Tavily 更丰富的搜索结果
- 如果不配置，BoCha 搜索功能将不可用

---

### 6. SerpApi - Google 搜索

**用途**: Google 搜索结果

**官网**: https://serpapi.com

**申请步骤**:

1. 访问 [SerpApi 官网](https://serpapi.com)
2. 注册账号
3. 登录后在 Dashboard 查看 API Key

**配置位置**:
```yaml
tools:
  google:
    api_key: "你的SerpApi-Key"
```

**费用说明**:
- 免费版：100 次/月
- 开发版：$50/月，5000 次
- 生产版：$250/月，30000 次

**注意事项**:
- 可选配置，不影响核心功能
- 免费额度较少，建议优先使用 Tavily
- 如果不配置，Google 搜索功能将不可用

---

## 配置优先级建议

根据重要性和成本，建议按以下顺序配置：

### 🔴 必须配置（核心功能）

1. **阿里云百炼** - 没有这个项目无法运行

### 🟡 推荐配置（常用功能）

2. **高德地图** - 免费，天气查询很常用
3. **Tavily Search** - 免费额度够用，联网搜索很重要

### 🟢 可选配置（增强功能）

4. **快递查询** - 有免费试用，按需配置
5. **BoCha AI** - 增强搜索，可选
6. **SerpApi** - Google 搜索，可选

---

## 费用说明

### 最小成本配置（推荐新手）

只配置必需和免费的 API：

| 服务 | 费用 | 额度 |
|------|------|------|
| 阿里云百炼 | 新用户免费额度 | 100-500万 tokens |
| 高德地图 | 免费 | 30万次/天 |
| Tavily Search | 免费 | 1000次/月 |
| **总计** | **¥0** | **足够个人学习使用** |

### 完整功能配置

如果需要所有功能：

| 服务 | 月费用 | 说明 |
|------|--------|------|
| 阿里云百炼 | ¥10-50 | 按实际使用量 |
| 高德地图 | ¥0 | 免费 |
| Tavily Search | ¥0 | 免费版够用 |
| 快递查询 | ¥9.9 | 基础套餐 |
| BoCha AI | ¥49 | 可选 |
| SerpApi | ¥0 | 免费版 |
| **总计** | **¥20-70/月** | **包含所有功能** |

---

## 配置示例

### 最小配置（只配置必需项）

```yaml
# 只配置阿里云百炼
multi_models:
  conversation_model:
    api_key: "sk-你的API-Key"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name: "qwen3.5-plus"
  # ... 其他模型配置相同的 api_key

# 工具配置留空或注释掉
# tools:
#   weather:
#     api_key: ""
```

### 推荐配置（免费功能）

```yaml
# 阿里云百炼
multi_models:
  conversation_model:
    api_key: "sk-你的API-Key"
    # ...

# 免费工具
tools:
  weather:
    api_key: "你的高德地图Key"
    endpoint: "https://restapi.amap.com/v3/weather/weatherInfo?parameters"
  
  tavily:
    api_key: "tvly-你的API-Key"
```

### 完整配置（所有功能）

参考 `config.yaml.example` 文件。

---

## 安全建议

1. **不要将 API Key 提交到 Git**
   ```bash
   # 确保 config.yaml 在 .gitignore 中
   echo "src/backend/agentchat/config.yaml" >> .gitignore
   ```

2. **使用环境变量（生产环境推荐）**
   ```bash
   export DASHSCOPE_API_KEY="sk-你的API-Key"
   export AMAP_API_KEY="你的高德Key"
   ```

3. **定期轮换密钥**
   - 建议每 3-6 个月更换一次 API Key
   - 如果怀疑泄露，立即重新生成

4. **设置消费限额**
   - 在各平台控制台设置每日/每月消费上限
   - 开启余额预警通知

---

## 常见问题

### Q: API Key 配置后不生效？

A: 检查以下几点：
1. 确认 config.yaml 文件路径正确
2. 重启后端服务
3. 检查 API Key 格式是否正确（有无多余空格）
4. 查看后端日志是否有错误信息

### Q: 阿里云百炼额度用完了怎么办？

A: 
1. 在控制台充值（支持支付宝/微信）
2. 或切换到其他兼容 OpenAI 格式的模型服务（如 DeepSeek、智谱AI）

### Q: 可以使用 OpenAI 的模型吗？

A: 可以！修改配置：
```yaml
multi_models:
  conversation_model:
    api_key: "sk-你的OpenAI-Key"
    base_url: "https://api.openai.com/v1"
    model_name: "gpt-4"
```

### Q: 工具 API 不配置会影响其他功能吗？

A: 不会。工具 API 是独立的，不配置只是对应的工具功能不可用，不影响对话、Agent、RAG 等核心功能。

---

## 下一步

- 📖 返回 [安装部署指南](./INSTALLATION.md) 继续配置
- 🐳 查看 [Docker部署指南](./DOCKER.md) 了解容器化部署
- ❓ 遇到问题？查看 [常见问题FAQ](./FAQ.md)
