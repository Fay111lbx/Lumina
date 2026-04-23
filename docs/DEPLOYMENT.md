# 🚀 OmniAgent 云服务器部署指南

本文档将指导你如何将 OmniAgent 部署到云服务器，让其他用户可以通过互联网访问。

## 📋 目录

- [服务器选择](#服务器选择)
- [环境准备](#环境准备)
- [部署步骤](#部署步骤)
- [域名配置](#域名配置)
- [HTTPS配置](#https配置)
- [进程管理](#进程管理)
- [监控和日志](#监控和日志)
- [备份策略](#备份策略)

---

## 服务器选择

### 推荐配置

**最低配置**（适合测试/小规模使用）：
- CPU: 2核
- 内存: 4GB
- 硬盘: 40GB SSD
- 带宽: 3Mbps
- 预计支持: 10-50 并发用户

**推荐配置**（适合生产环境）：
- CPU: 4核
- 内存: 8GB
- 硬盘: 100GB SSD
- 带宽: 5Mbps
- 预计支持: 100-500 并发用户

### 云服务商推荐

| 服务商 | 优势 | 价格参考 |
|--------|------|----------|
| 阿里云 | 国内访问快，生态完善 | ¥100-300/月 |
| 腾讯云 | 性价比高，新用户优惠多 | ¥80-250/月 |
| 华为云 | 稳定性好，企业级服务 | ¥120-300/月 |
| AWS | 全球部署，功能强大 | $20-80/月 |

**新手推荐**：阿里云或腾讯云，有中文文档和客服支持。

---

## 环境准备

### 1. 购买服务器

以阿里云为例：

1. 访问 [阿里云ECS](https://www.aliyun.com/product/ecs)
2. 选择"按量付费"或"包年包月"
3. 选择地域（建议选择离用户近的地域）
4. 选择操作系统：**Ubuntu 22.04 LTS**
5. 配置安全组，开放端口：
   - 22 (SSH)
   - 80 (HTTP)
   - 443 (HTTPS)
   - 7860 (后端API，可选)
   - 8090 (前端，可选)

### 2. 连接服务器

```bash
# 使用SSH连接（替换为你的服务器IP）
ssh root@your-server-ip

# 首次登录建议修改密码
passwd
```

### 3. 安装基础环境

```bash
# 更新系统
apt update && apt upgrade -y

# 安装必要工具
apt install -y git curl wget vim

# 安装 Python 3.12+
apt install -y python3.12 python3.12-venv python3-pip

# 安装 Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# 安装 MySQL
apt install -y mysql-server
systemctl start mysql
systemctl enable mysql

# 安装 Redis
apt install -y redis-server
systemctl start redis
systemctl enable redis

# 安装 Nginx
apt install -y nginx
systemctl start nginx
systemctl enable nginx
```

---

## 部署步骤

### 1. 克隆项目

```bash
# 创建项目目录
mkdir -p /var/www
cd /var/www

# 克隆项目
git clone https://github.com/your-username/OmniAgent.git
cd OmniAgent
```

### 2. 配置数据库

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库和用户
CREATE DATABASE agentchat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'agentchat'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON agentchat.* TO 'agentchat'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. 配置后端

```bash
# 进入后端目录
cd /var/www/OmniAgent/src/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r ../../requirements.txt

# 复制配置文件
cp agentchat/config.yaml.example agentchat/config.yaml

# 编辑配置文件
vim agentchat/config.yaml
```

**重要配置项**：

```yaml
# 数据库配置
mysql:
  endpoint: "mysql+pymysql://agentchat:your_strong_password@localhost:3306/agentchat"
  async_endpoint: "mysql+aiomysql://agentchat:your_strong_password@localhost:3306/agentchat"

# Redis配置
redis:
  endpoint: "redis://localhost:6379"

# 模型配置（填入你的API Key）
multi_models:
  conversation_model:
    api_key: "sk-你的阿里云百炼API-Key"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name: "qwen3.5-plus"

# 工具配置（可选）
tools:
  weather:
    api_key: "你的高德地图Key"
  tavily:
    api_key: "你的Tavily-Key"
```

### 4. 配置前端

```bash
# 进入前端目录
cd /var/www/OmniAgent/src/frontend

# 安装依赖
npm install

# 修改API地址（生产环境）
vim .env.production
```

创建 `.env.production` 文件：

```bash
# API地址（使用你的域名或服务器IP）
VITE_API_BASE_URL=https://your-domain.com
# 或者使用IP
# VITE_API_BASE_URL=http://your-server-ip:7860
```

```bash
# 构建前端
npm run build
```

### 5. 配置 Nginx

```bash
# 创建Nginx配置
vim /etc/nginx/sites-available/omniagent
```

**Nginx配置内容**：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名或服务器IP

    # 前端静态文件
    location / {
        root /var/www/OmniAgent/src/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket支持
    location /ws/ {
        proxy_pass http://127.0.0.1:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 文件上传大小限制
    client_max_body_size 100M;
}
```

```bash
# 启用配置
ln -s /etc/nginx/sites-available/omniagent /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重启Nginx
systemctl restart nginx
```

### 6. 使用 Supervisor 管理后端进程

```bash
# 安装 Supervisor
apt install -y supervisor

# 创建配置文件
vim /etc/supervisor/conf.d/omniagent.conf
```

**Supervisor配置内容**：

```ini
[program:omniagent-backend]
command=/var/www/OmniAgent/src/backend/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860
directory=/var/www/OmniAgent/src/backend
user=root
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/omniagent/backend.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
environment=PATH="/var/www/OmniAgent/src/backend/venv/bin"
```

```bash
# 创建日志目录
mkdir -p /var/log/omniagent

# 重新加载Supervisor配置
supervisorctl reread
supervisorctl update

# 启动服务
supervisorctl start omniagent-backend

# 查看状态
supervisorctl status
```

---

## 域名配置

### 1. 购买域名

推荐域名注册商：
- 阿里云万网：https://wanwang.aliyun.com
- 腾讯云DNSPod：https://dnspod.cloud.tencent.com
- GoDaddy：https://www.godaddy.com

### 2. 配置DNS解析

在域名管理后台添加A记录：

| 记录类型 | 主机记录 | 记录值 | TTL |
|---------|---------|--------|-----|
| A | @ | 你的服务器IP | 600 |
| A | www | 你的服务器IP | 600 |

等待DNS生效（通常5-10分钟）。

### 3. 验证域名

```bash
# 测试域名解析
ping your-domain.com

# 访问测试
curl http://your-domain.com
```

---

## HTTPS配置

使用 Let's Encrypt 免费SSL证书：

```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx

# 自动配置HTTPS
certbot --nginx -d your-domain.com -d www.your-domain.com

# 按提示输入邮箱并同意协议

# 测试自动续期
certbot renew --dry-run
```

Certbot会自动修改Nginx配置，添加HTTPS支持。

---

## 进程管理

### 常用命令

```bash
# 查看服务状态
supervisorctl status

# 启动服务
supervisorctl start omniagent-backend

# 停止服务
supervisorctl stop omniagent-backend

# 重启服务
supervisorctl restart omniagent-backend

# 查看日志
tail -f /var/log/omniagent/backend.log

# 重新加载配置
supervisorctl reread
supervisorctl update
```

### 更新代码

```bash
# 进入项目目录
cd /var/www/OmniAgent

# 拉取最新代码
git pull

# 更新后端依赖
cd src/backend
source venv/bin/activate
pip install -r ../../requirements.txt

# 更新前端
cd ../frontend
npm install
npm run build

# 重启服务
supervisorctl restart omniagent-backend
```

---

## 监控和日志

### 1. 查看系统资源

```bash
# 查看CPU和内存使用
htop

# 查看磁盘使用
df -h

# 查看网络连接
netstat -tunlp
```

### 2. 查看应用日志

```bash
# 后端日志
tail -f /var/log/omniagent/backend.log

# Nginx访问日志
tail -f /var/log/nginx/access.log

# Nginx错误日志
tail -f /var/log/nginx/error.log

# MySQL日志
tail -f /var/log/mysql/error.log
```

### 3. 设置日志轮转

```bash
# 创建日志轮转配置
vim /etc/logrotate.d/omniagent
```

```
/var/log/omniagent/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
    postrotate
        supervisorctl restart omniagent-backend > /dev/null
    endscript
}
```

---

## 备份策略

### 1. 数据库备份

```bash
# 创建备份脚本
vim /root/backup-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# 备份数据库
mysqldump -u agentchat -p'your_password' agentchat > $BACKUP_DIR/agentchat_$DATE.sql

# 压缩备份
gzip $BACKUP_DIR/agentchat_$DATE.sql

# 删除30天前的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Database backup completed: agentchat_$DATE.sql.gz"
```

```bash
# 添加执行权限
chmod +x /root/backup-db.sh

# 添加定时任务（每天凌晨2点备份）
crontab -e
```

添加：
```
0 2 * * * /root/backup-db.sh >> /var/log/backup.log 2>&1
```

### 2. 代码备份

```bash
# 备份整个项目
tar -czf /var/backups/omniagent_$(date +%Y%m%d).tar.gz /var/www/OmniAgent

# 或使用Git
cd /var/www/OmniAgent
git add .
git commit -m "Backup $(date +%Y-%m-%d)"
git push
```

---

## 安全加固

### 1. 防火墙配置

```bash
# 安装UFW
apt install -y ufw

# 允许SSH
ufw allow 22/tcp

# 允许HTTP和HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# 启用防火墙
ufw enable

# 查看状态
ufw status
```

### 2. 禁用root SSH登录

```bash
# 创建普通用户
adduser deploy
usermod -aG sudo deploy

# 修改SSH配置
vim /etc/ssh/sshd_config
```

修改：
```
PermitRootLogin no
PasswordAuthentication no  # 使用密钥登录更安全
```

```bash
# 重启SSH服务
systemctl restart sshd
```

### 3. 配置Fail2ban

```bash
# 安装Fail2ban
apt install -y fail2ban

# 启动服务
systemctl start fail2ban
systemctl enable fail2ban
```

---

## 访问管理员后台

部署完成后，你可以通过以下方式访问管理员后台：

1. 访问 `https://your-domain.com/admin`
2. 使用 user_id 为 "1" 的账号登录（管理员账号）
3. 查看所有用户的使用统计

**管理员功能**：
- 查看总用户数、活跃用户、对话数、Token使用量
- 查看所有用户列表
- 查看单个用户的详细统计
- 禁用/启用用户
- 查看模型和Agent使用统计

---

## 常见问题

### 1. 服务无法启动

```bash
# 查看详细错误
supervisorctl tail -f omniagent-backend stderr

# 检查端口占用
lsof -i:7860

# 检查配置文件
python -m agentchat.main --check-config
```

### 2. 数据库连接失败

```bash
# 检查MySQL状态
systemctl status mysql

# 测试连接
mysql -u agentchat -p -h localhost agentchat

# 检查防火墙
ufw status
```

### 3. Nginx 502错误

```bash
# 检查后端是否运行
supervisorctl status

# 检查Nginx配置
nginx -t

# 查看Nginx错误日志
tail -f /var/log/nginx/error.log
```

---

## 性能优化

### 1. 数据库优化

```bash
# 编辑MySQL配置
vim /etc/mysql/mysql.conf.d/mysqld.cnf
```

添加：
```ini
[mysqld]
max_connections = 500
innodb_buffer_pool_size = 2G
innodb_log_file_size = 256M
query_cache_size = 64M
```

### 2. Redis优化

```bash
# 编辑Redis配置
vim /etc/redis/redis.conf
```

修改：
```
maxmemory 1gb
maxmemory-policy allkeys-lru
```

### 3. Nginx优化

```nginx
# 在http块中添加
worker_processes auto;
worker_connections 2048;

gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
```

---

## 下一步

- 📊 配置监控告警（如阿里云云监控）
- 🔐 配置CDN加速（如阿里云CDN）
- 📈 配置日志分析（如ELK Stack）
- 💾 配置自动备份到对象存储（如阿里云OSS）

需要帮助？查看 [常见问题FAQ](./FAQ.md) 或提交 Issue。
