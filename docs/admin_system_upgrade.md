# 管理员权限系统升级说明

## 改动内容

### 1. 数据库模型变更
- 在 `UserTable` 中添加了 `is_admin` 字段（布尔类型）
- 不再依赖 `user_id='1'` 来判断管理员权限

### 2. 权限检查逻辑
- 修改了 `check_admin_permission()` 函数，使用 `is_admin` 字段而不是硬编码的 `user_id`
- 位置：`src/backend/agentchat/api/v1/admin.py`

### 3. 用户注册逻辑
- 移除了"第一个注册用户自动成为管理员"的机制
- 所有通过注册接口创建的用户都是普通用户
- 位置：`src/backend/agentchat/api/v1/user.py`

### 4. 系统初始化
- 系统启动时自动检查并创建默认管理员账号
- 默认管理员信息可在 `config.yaml` 中配置
- 位置：`src/backend/agentchat/database/init_data.py`

### 5. 管理员设置接口
- `/user/setup-admin` 接口现在需要管理员权限才能调用
- 只有管理员可以将其他用户提升为管理员

## 配置说明

在 `config.yaml` 中添加了默认管理员配置：

```yaml
server:
  # ... 其他配置
  default_admin_username: "admin"
  default_admin_password: "admin123"
```

**重要提示**：首次启动后请立即修改默认管理员密码！

## 数据库迁移

### 对于新部署
- 直接启动系统即可，会自动创建带 `is_admin` 字段的表

### 对于已有数据库
需要运行迁移脚本添加 `is_admin` 字段：

```bash
cd src/backend
python -m agentchat.database.migrations.add_is_admin_field
```

迁移脚本会：
1. 检查 `is_admin` 字段是否已存在
2. 如果不存在，添加该字段（默认值为 `FALSE`）
3. 将 `user_id='1'` 的用户自动设置为管理员（兼容旧数据）

## 使用方法

### 1. 首次启动
系统会自动创建默认管理员账号：
- 用户名：`admin`（可在配置文件修改）
- 密码：`admin123`（可在配置文件修改）

### 2. 登录管理员账号
使用默认账号密码登录后，请立即修改密码。

### 3. 设置其他管理员
管理员可以通过 `/user/setup-admin` 接口将其他用户提升为管理员：

```bash
POST /api/v1/user/setup-admin
{
  "user_name": "目标用户名",
  "new_password": "新密码"
}
```

需要在请求头中携带管理员的 access_token。

## 安全建议

1. **修改默认密码**：首次启动后立即修改默认管理员密码
2. **保护配置文件**：不要将包含默认密码的 `config.yaml` 提交到版本控制
3. **使用强密码**：为管理员账号设置复杂密码
4. **定期审计**：定期检查管理员列表，移除不需要的管理员权限

## 常见问题

### Q: 如何查看当前有哪些管理员？
A: 可以通过管理员后台的用户列表查看，或直接查询数据库：
```sql
SELECT user_id, user_name, user_email FROM user WHERE is_admin = TRUE;
```

### Q: 如何移除某个用户的管理员权限？
A: 目前需要直接修改数据库：
```sql
UPDATE user SET is_admin = FALSE WHERE user_id = '目标用户ID';
```

### Q: 忘记管理员密码怎么办？
A: 可以通过数据库直接重置：
```sql
-- 先找到管理员的 user_id
SELECT user_id, user_name FROM user WHERE is_admin = TRUE;

-- 然后使用迁移脚本或直接修改数据库重置密码
```

## 后续优化建议

1. 添加"移除管理员权限"的 API 接口
2. 在前端管理后台添加管理员管理页面
3. 添加管理员操作日志记录
4. 支持多级权限管理（超级管理员、普通管理员等）
