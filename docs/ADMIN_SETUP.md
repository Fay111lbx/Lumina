# 🔐 管理员账号设置指南

## 认证机制

管理端使用**双重认证**保护：

1. **登录认证**：必须先用用户名+密码登录系统
2. **管理员权限**：只有 `user_id = "1"` 的用户才能访问管理后台

## 设置管理员账号

### 方法1：注册时设置（推荐）

1. 访问 http://localhost:8090/register
2. 注册第一个账号（这个账号会自动成为管理员）
3. 登录后访问 http://localhost:8090/admin

### 方法2：修改现有用户为管理员

通过MySQL修改用户ID为1：

```bash
# 登录MySQL
mysql -u root -p

# 切换到数据库
USE agentchat;

# 查看所有用户
SELECT user_id, user_name FROM user;

# 将某个用户设为管理员（将user_id改为1）
UPDATE user SET user_id = '1' WHERE user_name = '你的用户名';

# 或者添加role字段（如果表结构支持）
ALTER TABLE user ADD COLUMN role VARCHAR(20) DEFAULT 'user';
UPDATE user SET role = 'admin' WHERE user_name = '你的用户名';
```

### 方法3：创建新的管理员账号

```bash
# 登录MySQL
mysql -u root -p

USE agentchat;

# 创建管理员账号（密码需要先加密）
INSERT INTO user (user_id, user_name, user_password, user_email, user_avatar, role) 
VALUES (
  '1', 
  'admin', 
  '$2b$12$加密后的密码', 
  'admin@example.com',
  'https://example.com/avatar.png',
  'admin'
);
```

**注意**：密码需要使用bcrypt加密。可以用Python生成：

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("你的密码")
print(hashed)
```

## 访问管理后台

1. 打开浏览器访问 http://localhost:8090
2. 使用管理员账号登录（user_id = "1" 的账号）
3. 登录成功后访问 http://localhost:8090/admin
4. 查看系统统计数据

## 管理后台功能

- 📊 **系统概览**：总用户数、活跃用户、对话数、Token使用量
- 👥 **用户列表**：查看所有注册用户，支持搜索和分页
- 📈 **用户详情**：查看单个用户的详细使用统计
- 🔒 **用户管理**：禁用/启用用户账号
- 📉 **趋势分析**：查看系统使用趋势（按天统计）
- 🤖 **模型统计**：各模型的调用次数和Token使用
- 🎯 **Agent统计**：各Agent的使用情况

## 安全建议

1. **强密码**：管理员账号必须使用强密码（至少12位，包含大小写字母、数字、特殊字符）
2. **定期更换**：建议每3个月更换一次管理员密码
3. **限制访问**：在生产环境中，建议通过防火墙限制管理后台的访问IP
4. **HTTPS**：部署到公网时必须启用HTTPS
5. **日志监控**：定期检查管理后台的访问日志

## 权限说明

| 功能 | 普通用户 | 管理员 |
|------|---------|--------|
| 登录系统 | ✅ | ✅ |
| 使用智能体 | ✅ | ✅ |
| 创建对话 | ✅ | ✅ |
| 访问管理后台 | ❌ | ✅ |
| 查看所有用户 | ❌ | ✅ |
| 禁用用户 | ❌ | ✅ |
| 查看系统统计 | ❌ | ✅ |

## 常见问题

### Q: 忘记管理员密码怎么办？

A: 通过MySQL直接重置密码：

```sql
-- 生成新密码的hash（使用Python）
-- 然后更新数据库
UPDATE user SET user_password = '新的加密密码' WHERE user_id = '1';
```

### Q: 可以有多个管理员吗？

A: 可以。修改 `admin.py` 中的权限检查逻辑：

```python
def check_admin_permission(login_user: UserPayload):
    """检查是否为管理员"""
    # 方法1：通过user_id判断（支持多个管理员）
    admin_ids = ["1", "2", "3"]  # 管理员ID列表
    if login_user.user_id not in admin_ids:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 方法2：通过role字段判断（推荐）
    if login_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    return True
```

### Q: 如何查看管理后台的访问日志？

A: 查看Nginx访问日志：

```bash
tail -f /var/log/nginx/access.log | grep "/admin"
```

或者在后端添加日志记录：

```python
@router.get("/admin/dashboard")
async def get_dashboard(login_user: UserPayload = Depends(get_admin_user)):
    logger.info(f"管理员 {login_user.user_name} 访问了仪表板")
    # ...
```
