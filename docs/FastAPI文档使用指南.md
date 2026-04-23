# FastAPI 自动生成 API 文档 - 完整指南

## ❌ 常见误解

**错误理解**：FastAPI 根据前端代码生成 API 文档

**正确理解**：FastAPI 根据**后端 Python 代码**自动生成 API 文档

---

## ✅ FastAPI 文档生成原理

### **完整流程**

```
1. 后端开发者编写 Python 代码
   ↓
2. FastAPI 自动分析代码（装饰器、类型注解、参数描述）
   ↓
3. 生成 OpenAPI 规范（JSON 格式）
   ↓
4. Swagger UI 渲染成可视化文档
   ↓
5. 前端开发者查看文档并编写代码
```

---

## 🔍 详细讲解

### **第一步：后端开发者编写代码**

```python
# src/backend/agentchat/api/v1/user.py

from fastapi import APIRouter, Body
from agentchat.schema.schemas import UnifiedResponseModel

router = APIRouter(tags=["User"])  # ← 标签：在文档中分组显示

@router.post('/user/login', response_model=UnifiedResponseModel)  # ← 路径和方法
async def login(
    user_name: str = Body(description='用户名'),          # ← 参数1：类型 + 描述
    user_password: str = Body(description='用户密码')     # ← 参数2：类型 + 描述
):
    """
    用户登录接口                                          # ← 接口描述（文档字符串）
    
    参数：
    - user_name: 用户名
    - user_password: 用户密码
    
    返回：
    - user_id: 用户ID
    - access_token: JWT Token
    """
    # 业务逻辑...
    return {
        "status_code": 200,
        "data": {
            "user_id": "123456",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    }
```

**FastAPI 从代码中提取的信息**：

| 代码元素 | 提取的信息 | 在文档中显示为 |
|---------|-----------|---------------|
| `@router.post('/user/login')` | 路径和方法 | `POST /api/v1/user/login` |
| `tags=["User"]` | 分组标签 | User 模块 |
| `user_name: str` | 参数类型 | string |
| `Body(description='用户名')` | 参数描述 | 用户名 |
| `response_model=UnifiedResponseModel` | 返回类型 | 响应结构 |
| `"""文档字符串"""` | 接口说明 | 接口描述 |

---

### **第二步：FastAPI 自动生成 OpenAPI 规范**

FastAPI 会自动生成一个 JSON 文件，描述所有接口：

访问：`http://localhost:7860/openapi.json`

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "OmniChat",
    "version": "v2.4.0"
  },
  "paths": {
    "/api/v1/user/login": {
      "post": {
        "tags": ["User"],
        "summary": "Login",
        "description": "用户登录接口",
        "operationId": "login_api_v1_user_login_post",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "properties": {
                  "user_name": {
                    "type": "string",
                    "description": "用户名"
                  },
                  "user_password": {
                    "type": "string",
                    "description": "用户密码"
                  }
                },
                "required": ["user_name", "user_password"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UnifiedResponseModel"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

### **第三步：Swagger UI 渲染成可视化文档**

访问：`http://localhost:7860/docs`

你会看到这样的界面：

```
┌─────────────────────────────────────────────────────────┐
│  OmniChat API Documentation                             │
│  v2.4.0                                                 │
├─────────────────────────────────────────────────────────┤
│  User                                    ▼              │
│    POST /api/v1/user/login               ▶              │
│    POST /api/v1/user/register            ▶              │
│    GET  /api/v1/user/info                ▶              │
│    PUT  /api/v1/user/update              ▶              │
│                                                          │
│  Completion                              ▼              │
│    POST /api/v1/completion               ▶              │
│                                                          │
│  Agent                                   ▼              │
│    GET  /api/v1/agent                    ▶              │
│    POST /api/v1/agent                    ▶              │
│    PUT  /api/v1/agent                    ▶              │
│    DELETE /api/v1/agent                  ▶              │
└─────────────────────────────────────────────────────────┘
```

---

### **第四步：点击接口查看详情**

点击 `POST /api/v1/user/login`，展开后看到：

```
┌─────────────────────────────────────────────────────────┐
│  POST /api/v1/user/login                                │
│  用户登录接口                                            │
├─────────────────────────────────────────────────────────┤
│  Parameters                                             │
│                                                          │
│  Request body (application/json) *required              │
│  {                                                       │
│    "user_name": "string",      ← 用户名                 │
│    "user_password": "string"   ← 用户密码               │
│  }                                                       │
│                                                          │
│  [Try it out] 按钮                                      │
├─────────────────────────────────────────────────────────┤
│  Responses                                              │
│                                                          │
│  200 Successful Response                                │
│  {                                                       │
│    "status_code": 200,                                  │
│    "status_message": "success",                         │
│    "data": {                                            │
│      "user_id": "string",                               │
│      "access_token": "string"                           │
│    }                                                     │
│  }                                                       │
│                                                          │
│  422 Validation Error                                   │
│  {                                                       │
│    "detail": [                                          │
│      {                                                   │
│        "loc": ["string"],                               │
│        "msg": "string",                                 │
│        "type": "string"                                 │
│      }                                                   │
│    ]                                                     │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎮 如何使用 API 文档

### **方法1：查看接口信息**

1. 打开 `http://localhost:7860/docs`
2. 找到你需要的接口（比如 `POST /api/v1/user/login`）
3. 点击展开，查看：
   - 请求参数（名称、类型、是否必填、描述）
   - 响应格式（成功/失败的返回结构）
   - 状态码（200、401、422 等）

---

### **方法2：在文档中测试接口**

#### **步骤1：点击 "Try it out" 按钮**

```
┌─────────────────────────────────────────────────────────┐
│  POST /api/v1/user/login                                │
│                                                          │
│  Request body                                           │
│  {                                                       │
│    "user_name": "string",                               │
│    "user_password": "string"                            │
│  }                                                       │
│                                                          │
│  [Try it out] ← 点击这个按钮                            │
└─────────────────────────────────────────────────────────┘
```

#### **步骤2：填写参数**

点击后，输入框变为可编辑：

```
┌─────────────────────────────────────────────────────────┐
│  Request body                                           │
│  ┌───────────────────────────────────────────────────┐ │
│  │ {                                                  │ │
│  │   "user_name": "admin",      ← 修改为真实用户名   │ │
│  │   "user_password": "123456"  ← 修改为真实密码     │ │
│  │ }                                                  │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
│  [Execute] 按钮                                         │
└─────────────────────────────────────────────────────────┘
```

#### **步骤3：点击 "Execute" 按钮**

发送请求到后端

#### **步骤4：查看响应结果**

```
┌─────────────────────────────────────────────────────────┐
│  Responses                                              │
│                                                          │
│  Server response                                        │
│  Code: 200                                              │
│  Details:                                               │
│  {                                                       │
│    "status_code": 200,                                  │
│    "status_message": "success",                         │
│    "data": {                                            │
│      "user_id": "123456",                               │
│      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI..."  │
│    }                                                     │
│  }                                                       │
│                                                          │
│  Response headers                                       │
│  content-type: application/json                         │
│  date: Mon, 21 Apr 2026 12:00:00 GMT                   │
└─────────────────────────────────────────────────────────┘
```

---

### **方法3：复制 curl 命令**

在响应结果下方，可以看到等效的 curl 命令：

```bash
curl -X 'POST' \
  'http://localhost:7860/api/v1/user/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_name": "admin",
  "user_password": "123456"
}'
```

可以直接在终端运行测试！

---

## 🎓 实战案例：根据文档编写前端代码

### **场景：实现用户登录功能**

#### **第一步：在 API 文档中查看接口**

访问 `http://localhost:7860/docs`，找到 `POST /api/v1/user/login`

**记录以下信息**：

| 项目 | 值 |
|------|---|
| 路径 | `/api/v1/user/login` |
| 方法 | `POST` |
| 参数1 | `user_name` (string, 必填) |
| 参数2 | `user_password` (string, 必填) |
| 返回字段 | `user_id`, `access_token` |

---

#### **第二步：在前端封装 API**

创建 `src/frontend/src/apis/auth.ts`：

```typescript
import { request } from '../utils/request'

export interface LoginForm {
  username: string
  password: string
}

// 根据文档编写 API 函数
export const loginAPI = (data: LoginForm) => {
  return request({
    url: '/api/v1/user/login',     // ← 从文档复制路径
    method: 'POST',                 // ← 从文档复制方法
    data: {
      user_name: data.username,     // ← 从文档复制参数名
      user_password: data.password  // ← 从文档复制参数名
    }
  })
}
```

---

#### **第三步：在 Vue 组件中调用**

```vue
<script setup lang="ts">
import { reactive, ref } from 'vue'
import { loginAPI } from '../../apis/auth'
import { ElMessage } from 'element-plus'

const loginForm = reactive({
  username: '',
  password: ''
})

const loading = ref(false)

const handleLogin = async () => {
  try {
    loading.value = true
    const response = await loginAPI(loginForm)
    
    // 根据文档中的返回格式解析数据
    if (response.data.status_code === 200) {
      const { user_id, access_token } = response.data.data
      
      // 保存 Token
      localStorage.setItem('token', access_token)
      localStorage.setItem('userId', user_id)
      
      ElMessage.success('登录成功')
    }
  } catch (error) {
    ElMessage.error('登录失败')
  } finally {
    loading.value = false
  }
}
</script>
```

---

## 📋 FastAPI 文档的优势

### **1. 自动生成，无需手写**

- ✅ 后端代码即文档
- ✅ 代码更新，文档自动更新
- ✅ 永远不会过时

### **2. 交互式测试**

- ✅ 直接在浏览器中测试接口
- ✅ 无需 Postman 等工具
- ✅ 实时查看响应结果

### **3. 类型安全**

- ✅ 参数类型自动验证
- ✅ 返回类型自动推断
- ✅ 减少前后端对接错误

### **4. 标准化**

- ✅ 遵循 OpenAPI 规范
- ✅ 可导出为 JSON/YAML
- ✅ 可集成到其他工具

---

## 🔧 如何让文档更详细？

### **1. 添加接口描述**

```python
@router.post('/user/login')
async def login(...):
    """
    用户登录接口
    
    这是一个详细的描述，会显示在文档中。
    可以包含多行文字，支持 Markdown 格式。
    
    ## 注意事项
    - 密码会进行 SHA256 加密
    - 登录成功后返回 JWT Token
    - Token 有效期为 24 小时
    """
    pass
```

---

### **2. 添加参数描述**

```python
async def login(
    user_name: str = Body(description='用户名，长度不超过20个字符'),
    user_password: str = Body(description='用户密码，至少6位')
):
    pass
```

---

### **3. 定义响应模型**

```python
from pydantic import BaseModel

class LoginResponse(BaseModel):
    user_id: str
    access_token: str
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "123456",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }

@router.post('/user/login', response_model=LoginResponse)
async def login(...):
    pass
```

---

### **4. 添加标签和分组**

```python
router = APIRouter(
    tags=["User"],           # 分组标签
    prefix="/user"           # 路径前缀
)
```

---

## 🎯 总结

### **FastAPI 文档生成流程**

```
后端 Python 代码
    ↓ FastAPI 自动分析
OpenAPI 规范 (JSON)
    ↓ Swagger UI 渲染
可视化 API 文档
    ↓ 前端开发者查看
编写前端代码
```

### **如何使用 API 文档**

1. **启动后端**：`python scripts/start.py`
2. **打开文档**：`http://localhost:7860/docs`
3. **查看接口**：点击展开查看详情
4. **测试接口**：点击 "Try it out" → 填写参数 → 点击 "Execute"
5. **编写前端**：根据文档中的路径、方法、参数编写 API 调用代码

### **核心要点**

- ❌ FastAPI **不是**根据前端生成文档
- ✅ FastAPI **是**根据后端 Python 代码自动生成文档
- ✅ 文档与代码同步，永远不会过时
- ✅ 支持交互式测试，无需额外工具
- ✅ 前端开发者根据文档编写代码

---

## 📚 相关链接

- FastAPI 官方文档：https://fastapi.tiangolo.com/zh/
- OpenAPI 规范：https://swagger.io/specification/
- Swagger UI：https://swagger.io/tools/swagger-ui/
