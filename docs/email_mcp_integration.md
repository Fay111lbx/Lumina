# 邮件工具接入 MCP 用户配置系统 - 完整实现

## 实现步骤

### 步骤 1：在 mcp_server.json 中添加邮件配置定义

文件位置：`src/backend/agentchat/config/mcp_server.json`

在数组中添加：

```json
{
  "server_name": "邮件发送",
  "url": "internal://email",
  "type": "internal",
  "config": [
    {
      "label": "发件人邮箱",
      "key": "sender_email",
      "value": "",
      "placeholder": "例如：your@qq.com",
      "required": true
    },
    {
      "label": "邮箱授权码",
      "key": "email_password",
      "value": "",
      "placeholder": "QQ邮箱需要使用授权码，不是登录密码",
      "required": true,
      "type": "password"
    }
  ],
  "config_enabled": true,
  "logo_url": "https://agentchat.oss-cn-beijing.aliyuncs.com/icons/tools/email.png",
  "description": "配置您的邮箱信息，用于发送邮件"
}
```

### 步骤 2：修改邮件发送 API

文件位置：`src/backend/agentchat/api/v1/email.py`

**修改前**（每次都要传密码）：
```python
@router.post("/email/send", response_model=UnifiedResponseModel)
async def send_email(
    sender: str = Body(description="发件人邮箱地址"),
    receiver: str = Body(description="收件人邮箱地址"),
    message: str = Body(description="邮件内容"),
    password: str = Body(description="发件人邮箱密码或授权码")
):
    # ...
```

**修改后**（从用户配置读取）：
```python
from fastapi import APIRouter, Body, Depends
from agentchat.schema.schemas import UnifiedResponseModel, resp_200, resp_500
from agentchat.tools.send_email.action import _send_email
from agentchat.api.services.user import get_login_user, UserPayload
from agentchat.api.services.mcp_user_config import MCPUserConfigService
from agentchat.api.services.mcp_server import MCPService
from loguru import logger

router = APIRouter(tags=["Email"])


@router.post("/email/send", response_model=UnifiedResponseModel)
async def send_email(
    receiver: str = Body(description="收件人邮箱地址"),
    message: str = Body(description="邮件内容"),
    subject: str = Body(default="", description="邮件主题（可选）"),
    login_user: UserPayload = Depends(get_login_user)
):
    """
    发送邮件（从用户配置中读取发件人信息）
    
    ## 使用前提
    用户需要先在"配置管理"页面配置邮箱信息
    
    ## 参数说明
    - receiver: 收件人邮箱地址（必填）
    - message: 邮件内容（必填）
    - subject: 邮件主题（可选）
    
    ## 返回数据
    - 发送成功或失败的消息
    """
    try:
        # 1. 查找"邮件发送"这个 MCP Server
        email_server = await MCPService.get_server_by_name("邮件发送")
        if not email_server:
            return resp_500(message="邮件服务未配置，请联系管理员")
        
        # 2. 获取当前用户的邮件配置
        user_config = await MCPUserConfigService.get_mcp_user_config(
            user_id=login_user.user_id,
            mcp_server_id=email_server["mcp_server_id"]
        )
        
        # 3. 检查用户是否配置了邮箱
        if not user_config or not user_config.get("sender_email"):
            return resp_500(message="请先在【配置管理】页面设置您的邮箱信息")
        
        sender = user_config.get("sender_email")
        password = user_config.get("email_password")
        
        if not sender or not password:
            return resp_500(message="邮箱配置不完整，请检查配置")
        
        # 4. 调用发送邮件
        result = _send_email(sender, receiver, message, password)
        
        if "successful" in result:
            logger.info(f"邮件发送成功: {sender} -> {receiver}")
            return resp_200(data={"message": "邮件发送成功"})
        else:
            logger.error(f"邮件发送失败: {result}")
            return resp_500(message="邮件发送失败，请检查邮箱配置")
    
    except Exception as e:
        logger.error(f"发送邮件异常: {e}")
        return resp_500(message=f"发送邮件失败: {str(e)}")


@router.get("/email/config/status", response_model=UnifiedResponseModel)
async def check_email_config(login_user: UserPayload = Depends(get_login_user)):
    """
    检查当前用户是否已配置邮箱
    """
    try:
        email_server = await MCPService.get_server_by_name("邮件发送")
        if not email_server:
            return resp_200(data={"configured": False, "message": "邮件服务未启用"})
        
        user_config = await MCPUserConfigService.get_mcp_user_config(
            user_id=login_user.user_id,
            mcp_server_id=email_server["mcp_server_id"]
        )
        
        configured = bool(user_config and user_config.get("sender_email"))
        
        return resp_200(data={
            "configured": configured,
            "sender_email": user_config.get("sender_email") if configured else None
        })
    
    except Exception as e:
        logger.error(f"检查邮件配置失败: {e}")
        return resp_500(message=str(e))
```

### 步骤 3：添加 MCPService 的辅助方法

文件位置：`src/backend/agentchat/api/services/mcp_server.py`

在 `MCPService` 类中添加：

```python
@classmethod
async def get_server_by_name(cls, server_name: str):
    """
    根据服务名称获取 MCP Server
    :param server_name: 服务名称
    :return: MCP Server 信息
    """
    from agentchat.database.dao.mcp_server import MCPServerDao
    
    try:
        server = await MCPServerDao.get_server_by_name(server_name)
        if server:
            return server.to_dict()
        return None
    except Exception as err:
        raise ValueError(f"Get MCP Server By Name Error: {err}")
```

### 步骤 4：添加 DAO 方法

文件位置：`src/backend/agentchat/database/dao/mcp_server.py`

```python
@classmethod
async def get_server_by_name(cls, server_name: str):
    """
    根据服务名称获取 MCP Server
    """
    with session_getter() as session:
        sql = select(MCPServerTable).where(MCPServerTable.server_name == server_name)
        result = session.exec(sql).first()
        return result
```

## 使用流程

### 用户端操作

1. **首次使用 - 配置邮箱**
   - 用户登录系统
   - 进入"配置管理"页面
   - 找到"邮件发送"配置项
   - 填写：
     - 发件人邮箱：`your@qq.com`
     - 邮箱授权码：`abcdefghijklmnop`（QQ邮箱授权码）
   - 点击保存

2. **发送邮件**
   - 调用 API：
   ```bash
   POST /api/v1/email/send
   {
     "receiver": "target@example.com",
     "message": "这是邮件内容",
     "subject": "测试邮件"
   }
   ```
   - 系统自动从配置中读取发件人信息
   - 无需再次输入密码

3. **检查配置状态**
   ```bash
   GET /api/v1/email/config/status
   ```
   返回：
   ```json
   {
     "status_code": 200,
     "data": {
       "configured": true,
       "sender_email": "your@qq.com"
     }
   }
   ```

## 前端集成建议

### 1. 在发送邮件前检查配置

```typescript
// 发送邮件前先检查
const checkEmailConfig = async () => {
  const res = await request({
    url: '/api/v1/email/config/status',
    method: 'GET'
  })
  
  if (!res.data.configured) {
    ElMessage.warning('请先配置邮箱信息')
    // 跳转到配置页面
    router.push('/configuration')
    return false
  }
  
  return true
}

// 发送邮件
const sendEmail = async () => {
  if (!await checkEmailConfig()) return
  
  const res = await request({
    url: '/api/v1/email/send',
    method: 'POST',
    data: {
      receiver: receiverEmail.value,
      message: emailContent.value,
      subject: emailSubject.value
    }
  })
  
  if (res.status_code === 200) {
    ElMessage.success('邮件发送成功')
  }
}
```

### 2. 配置页面提示

在配置页面添加说明：

```vue
<el-form-item label="发件人邮箱">
  <el-input v-model="config.sender_email" placeholder="例如：your@qq.com" />
  <div class="tip">用于发送邮件的邮箱地址</div>
</el-form-item>

<el-form-item label="邮箱授权码">
  <el-input 
    v-model="config.email_password" 
    type="password" 
    placeholder="QQ邮箱需要使用授权码"
  />
  <div class="tip">
    QQ邮箱授权码获取方式：
    <a href="https://service.mail.qq.com/detail/0/75" target="_blank">
      查看教程
    </a>
  </div>
</el-form-item>
```

## 其他工具的类似实现

同样的模式可以应用到其他需要用户配置的工具：

### 天气查询（如果需要用户自己的 API Key）
```json
{
  "server_name": "天气查询",
  "config": [
    {
      "label": "高德地图 API Key",
      "key": "amap_key",
      "value": ""
    }
  ],
  "config_enabled": true
}
```

### 快递查询
```json
{
  "server_name": "快递查询",
  "config": [
    {
      "label": "快递查询 API Key",
      "key": "delivery_key",
      "value": ""
    }
  ],
  "config_enabled": true
}
```

## 优势总结

1. ✅ **用户体验好**：配置一次，永久使用
2. ✅ **安全性高**：密码存储在数据库，不在请求中传输
3. ✅ **易于管理**：用户可以随时修改配置
4. ✅ **统一管理**：所有工具配置在一个页面
5. ✅ **权限隔离**：每个用户的配置独立

## 注意事项

1. **密码加密**：建议对 `email_password` 等敏感字段进行加密存储
2. **配置验证**：保存配置时可以发送测试邮件验证配置是否正确
3. **错误提示**：当配置缺失或错误时，给出明确的提示和配置入口
