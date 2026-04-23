# MCP 用户配置系统使用说明

## 系统架构

MCP 用户配置系统允许用户为需要鉴权的工具（如飞书、邮件等）保存个人配置信息。

### 数据模型

```
MCPUserConfigTable
├── id: 配置记录ID
├── mcp_server_id: 关联的 MCP Server ID
├── user_id: 用户ID
├── config: JSON 格式的配置信息 [{"key": "xxx", "value": "xxx"}]
├── create_time: 创建时间
└── update_time: 更新时间
```

## 工作流程示例

### 1. 定义 MCP Server（以飞书为例）

在 `config/mcp_server.json` 中定义：

```json
{
  "server_name": "飞书",
  "url": "http://47.95.23.87:8000/sse",
  "type": "sse",
  "config": [
    {
      "label": "APP_ID",
      "key": "app_id",
      "value": ""
    },
    {
      "label": "APP_SECRET",
      "key": "app_secret",
      "value": ""
    }
  ],
  "config_enabled": true,
  "logo_url": "https://xxx.com/feishu.png"
}
```

**关键字段说明**：
- `config`: 定义需要用户填写的配置项
  - `label`: 前端显示的标签
  - `key`: 配置项的键名
  - `value`: 默认值（通常为空）
- `config_enabled`: 是否需要用户配置（true=需要配置）

### 2. 用户保存配置

用户在前端配置页面填写后，调用 API：

```http
POST /api/v1/mcp_user_config/create
{
  "mcp_server_id": "飞书的server_id",
  "config": [
    {
      "key": "app_id",
      "value": "用户的APP_ID"
    },
    {
      "key": "app_secret",
      "value": "用户的APP_SECRET"
    }
  ]
}
```

系统会在 `mcp_user_config` 表中创建一条记录：

```
id: "abc123"
mcp_server_id: "飞书的server_id"
user_id: "当前登录用户ID"
config: [{"key": "app_id", "value": "xxx"}, {"key": "app_secret", "value": "xxx"}]
```

### 3. 使用配置

当用户调用飞书工具时，系统会：

```python
# 获取用户配置
user_config = await MCPUserConfigService.get_mcp_user_config(
    user_id="当前用户ID",
    mcp_server_id="飞书的server_id"
)

# user_config 返回格式：
# {
#   "app_id": "用户的APP_ID",
#   "app_secret": "用户的APP_SECRET"
# }

# 使用配置调用飞书 API
app_id = user_config.get("app_id")
app_secret = user_config.get("app_secret")
```

## 邮件工具配置示例

### 步骤 1：在 mcp_server.json 中添加邮件配置

```json
{
  "server_name": "邮件发送",
  "url": "internal://email",
  "type": "internal",
  "config": [
    {
      "label": "发件人邮箱",
      "key": "sender_email",
      "value": ""
    },
    {
      "label": "邮箱授权码",
      "key": "email_password",
      "value": ""
    }
  ],
  "config_enabled": true,
  "logo_url": "https://xxx.com/email.png"
}
```

### 步骤 2：用户在前端配置页面保存

前端调用：
```javascript
POST /api/v1/mcp_user_config/create
{
  "mcp_server_id": "邮件发送的server_id",
  "config": [
    {
      "key": "sender_email",
      "value": "user@qq.com"
    },
    {
      "key": "email_password",
      "value": "授权码123456"
    }
  ]
}
```

### 步骤 3：修改邮件 API 使用配置

修改 `api/v1/email.py`：

```python
@router.post("/email/send", response_model=UnifiedResponseModel)
async def send_email(
    receiver: str = Body(description="收件人邮箱地址"),
    message: str = Body(description="邮件内容"),
    login_user: UserPayload = Depends(get_login_user)
):
    """
    发送邮件（从用户配置中读取发件人信息）
    """
    try:
        # 获取用户的邮件配置
        user_config = await MCPUserConfigService.get_mcp_user_config(
            user_id=login_user.user_id,
            mcp_server_id="邮件发送的server_id"  # 需要先查询获取
        )
        
        # 检查用户是否配置了邮箱
        if not user_config or not user_config.get("sender_email"):
            return resp_500(message="请先在配置页面设置邮箱信息")
        
        sender = user_config.get("sender_email")
        password = user_config.get("email_password")
        
        # 调用发送邮件
        result = _send_email(sender, receiver, message, password)
        
        if "successful" in result:
            return resp_200(data={"message": "邮件发送成功"})
        else:
            return resp_500(message="邮件发送失败")
            
    except Exception as e:
        logger.error(f"发送邮件异常: {e}")
        return resp_500(message=f"发送邮件失败: {str(e)}")
```

## API 接口说明

### 创建/更新配置
```http
POST /api/v1/mcp_user_config/create
PUT /api/v1/mcp_user_config/update
```

### 查询配置
```http
GET /api/v1/mcp_user_config?server_id=xxx
```

### 删除配置
```http
DELETE /api/v1/mcp_user_config/delete
Body: { "config_id": "xxx" }
```

## 前端配置页面

前端已有配置页面：`src/frontend/src/pages/configuration/configuration.vue`

用户可以在这个页面：
1. 查看所有需要配置的 MCP Server
2. 填写配置信息（如邮箱、密码、API Key等）
3. 保存配置

## 优势

1. **安全性**：敏感信息（密码、API Key）存储在数据库中，不需要每次输入
2. **用户体验**：配置一次，永久使用
3. **隔离性**：每个用户的配置独立，互不影响
4. **灵活性**：可以随时修改配置

## 注意事项

1. **密码加密**：建议对敏感信息（如密码）进行加密存储
2. **配置验证**：保存配置时应验证配置的有效性
3. **错误提示**：当用户未配置时，应给出清晰的提示
