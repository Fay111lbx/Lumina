# 🌍 免费云服务器部署推荐

## 国外免费服务器推荐

### 1. ⭐ Oracle Cloud Free Tier（强烈推荐）

**免费配置**：
- 2个AMD VM实例：1 OCPU + 1GB RAM（永久免费）
- 4个ARM VM实例：4 OCPU + 24GB RAM（永久免费）
- 200GB块存储
- 10TB/月出站流量

**优点**：
- ✅ 永久免费，无需信用卡
- ✅ ARM实例性能强大（4核24G）
- ✅ 流量充足（10TB/月）
- ✅ 支持多个数据中心（日本、韩国、新加坡等）
- ✅ 可以运行Docker、K8s

**缺点**：
- ❌ 注册需要信用卡验证（不扣费）
- ❌ 部分地区IP可能被墙

**注册地址**：https://www.oracle.com/cloud/free/

**推荐配置**：
```bash
# ARM实例（推荐）
CPU: 4 OCPU (ARM)
内存: 24GB
存储: 100GB
系统: Ubuntu 22.04
```

---

### 2. 🚀 Google Cloud Platform (GCP) Free Tier

**免费配置**：
- 1个e2-micro实例：0.25 vCPU + 1GB RAM（永久免费）
- 30GB标准持久化磁盘
- 1GB/月出站流量（北美）

**优点**：
- ✅ 永久免费
- ✅ 网络速度快
- ✅ 稳定性好
- ✅ 支持多个地区

**缺点**：
- ❌ 配置较低（1GB内存）
- ❌ 流量限制（1GB/月）
- ❌ 需要信用卡验证

**注册地址**：https://cloud.google.com/free

**适合场景**：轻量级应用、测试环境

---

### 3. 💎 AWS Free Tier

**免费配置**：
- 1个t2.micro实例：1 vCPU + 1GB RAM（12个月免费）
- 30GB EBS存储
- 15GB/月出站流量

**优点**：
- ✅ 服务稳定
- ✅ 生态完善
- ✅ 文档丰富

**缺点**：
- ❌ 仅12个月免费
- ❌ 配置较低
- ❌ 流量限制
- ❌ 需要信用卡

**注册地址**：https://aws.amazon.com/free/

---

### 4. 🔷 Azure Free Tier

**免费配置**：
- 1个B1S实例：1 vCPU + 1GB RAM（12个月免费）
- 64GB SSD存储
- 15GB/月出站流量

**优点**：
- ✅ 微软生态
- ✅ 企业级稳定性

**缺点**：
- ❌ 仅12个月免费
- ❌ 配置较低
- ❌ 网络速度一般

**注册地址**：https://azure.microsoft.com/free/

---

### 5. 🎯 Render（推荐用于快速部署）

**免费配置**：
- Web服务：512MB RAM
- PostgreSQL数据库：1GB存储（90天后删除）
- 静态站点：无限制

**优点**：
- ✅ 无需信用卡
- ✅ 自动部署（Git集成）
- ✅ 免费SSL证书
- ✅ 支持Docker

**缺点**：
- ❌ 15分钟无请求会休眠
- ❌ 数据库90天后删除
- ❌ 配置较低

**注册地址**：https://render.com/

**部署方式**：
```bash
# 1. 连接GitHub仓库
# 2. 选择Web Service
# 3. 配置启动命令
# 4. 自动部署
```

---

### 6. 🐳 Railway（推荐用于全栈应用）

**免费配置**：
- $5/月免费额度
- 512MB RAM
- 1GB存储
- 支持MySQL、PostgreSQL、Redis

**优点**：
- ✅ 无需信用卡
- ✅ 支持多种数据库
- ✅ 自动部署
- ✅ 免费SSL

**缺点**：
- ❌ 免费额度有限（$5/月）
- ❌ 超出额度需付费

**注册地址**：https://railway.app/

---

### 7. 🌐 Vercel（推荐用于前端）

**免费配置**：
- 无限静态站点
- 100GB带宽/月
- Serverless函数：100GB-小时

**优点**：
- ✅ 完全免费
- ✅ 自动部署
- ✅ 全球CDN
- ✅ 免费SSL

**缺点**：
- ❌ 仅支持前端和Serverless
- ❌ 不支持长连接

**注册地址**：https://vercel.com/

**适合场景**：前端部署 + Serverless后端

---

### 8. 🔥 Fly.io

**免费配置**：
- 3个共享CPU VM
- 256MB RAM/VM
- 3GB持久化存储
- 160GB/月出站流量

**优点**：
- ✅ 无需信用卡
- ✅ 支持Docker
- ✅ 全球部署
- ✅ 免费SSL

**缺点**：
- ❌ 配置较低
- ❌ 文档较少

**注册地址**：https://fly.io/

---

## 🎯 推荐方案对比

| 服务商 | 配置 | 流量 | 免费期限 | 推荐指数 | 适合场景 |
|--------|------|------|----------|----------|----------|
| **Oracle Cloud** | 4核24G | 10TB/月 | 永久 | ⭐⭐⭐⭐⭐ | 生产环境 |
| **GCP** | 1核1G | 1GB/月 | 永久 | ⭐⭐⭐ | 测试环境 |
| **AWS** | 1核1G | 15GB/月 | 12个月 | ⭐⭐⭐ | 学习测试 |
| **Render** | 512MB | 无限 | 永久 | ⭐⭐⭐⭐ | 快速部署 |
| **Railway** | 512MB | 无限 | 永久 | ⭐⭐⭐⭐ | 全栈应用 |
| **Vercel** | Serverless | 100GB/月 | 永久 | ⭐⭐⭐⭐ | 前端部署 |
| **Fly.io** | 256MB | 160GB/月 | 永久 | ⭐⭐⭐ | 小型应用 |

---

## 🚀 针对本项目的推荐方案

### 方案1：Oracle Cloud（最佳方案）

**配置**：ARM实例 4核24G

**部署架构**：
```
前端 (Nginx) → 后端 (FastAPI) → MySQL + ChromaDB
```

**优点**：
- 配置强大，可以运行完整项目
- 流量充足（10TB/月）
- 永久免费

**月成本**：$0

---

### 方案2：Render + Railway（快速部署）

**配置**：
- Render：部署后端API（512MB）
- Railway：部署MySQL数据库
- Vercel：部署前端

**优点**：
- 无需服务器运维
- 自动部署
- 免费SSL

**月成本**：$0（在免费额度内）

---

### 方案3：GCP + Vercel（经济方案）

**配置**：
- GCP e2-micro：部署后端 + MySQL（1GB RAM）
- Vercel：部署前端

**优点**：
- 永久免费
- 稳定可靠

**缺点**：
- 配置较低，需要优化

**月成本**：$0

---

## 📝 部署步骤（以Oracle Cloud为例）

### 1. 注册Oracle Cloud账号

1. 访问 https://www.oracle.com/cloud/free/
2. 点击"Start for free"
3. 填写信息（需要信用卡验证，不扣费）
4. 选择数据中心（推荐：日本、韩国、新加坡）

### 2. 创建VM实例

```bash
# 选择配置
Shape: VM.Standard.A1.Flex (ARM)
OCPU: 4
Memory: 24GB
Boot Volume: 100GB
OS: Ubuntu 22.04

# 配置网络
VCN: 创建新的VCN
Subnet: 公共子网
Public IP: 分配公网IP
```

### 3. 配置防火墙

```bash
# 开放端口
Ingress Rules:
- 80 (HTTP)
- 443 (HTTPS)
- 22 (SSH)
- 7860 (后端API，可选)
```

### 4. SSH连接服务器

```bash
ssh -i your-key.pem ubuntu@your-server-ip
```

### 5. 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo apt install docker-compose -y

# 安装Nginx
sudo apt install nginx -y

# 安装MySQL
sudo apt install mysql-server -y
```

### 6. 部署项目

参考 [DEPLOYMENT.md](./DEPLOYMENT.md) 文档进行部署。

### 7. 配置域名和HTTPS

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 申请SSL证书
sudo certbot --nginx -d yourdomain.com
```

---

## 💰 成本估算

| 方案 | 配置 | 月成本 | 适合规模 |
|------|------|--------|----------|
| Oracle Cloud ARM | 4核24G | $0 | 1000+用户 |
| Render + Railway | 512MB | $0-5 | 100用户 |
| GCP e2-micro | 1核1G | $0 | 50用户 |
| 自建VPS | 2核4G | $5-10 | 500用户 |

---

## 🔒 安全建议

1. **启用HTTPS**：必须使用SSL证书
2. **配置防火墙**：只开放必要端口
3. **定期更新**：及时更新系统和依赖
4. **备份数据**：定期备份数据库
5. **监控日志**：使用日志监控工具
6. **限流保护**：配置Nginx限流
7. **密钥管理**：使用环境变量存储敏感信息

---

## 📚 相关文档

- [部署指南](./DEPLOYMENT.md)
- [管理员设置](./ADMIN_SETUP.md)
- [API密钥申请](./API_KEYS.md)
- [安装文档](./INSTALLATION.md)

---

## 🆘 常见问题

### Q: Oracle Cloud注册失败怎么办？

A: 
1. 尝试更换浏览器（Chrome无痕模式）
2. 使用国外信用卡
3. 联系客服

### Q: 服务器IP被墙怎么办？

A: 
1. 使用CDN（Cloudflare）
2. 更换服务器地区
3. 使用域名访问

### Q: 免费额度用完了怎么办？

A: 
1. Oracle Cloud ARM实例永久免费
2. 其他服务可以迁移到Oracle Cloud
3. 或者升级到付费套餐

### Q: 如何监控服务器资源使用？

A: 
```bash
# 安装监控工具
sudo apt install htop iotop nethogs -y

# 查看资源使用
htop           # CPU和内存
iotop          # 磁盘IO
nethogs        # 网络流量
```
