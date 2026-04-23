# 📦 OmniAgent 安装部署指南

本文档将指导你从零开始部署 OmniAgent 项目。

## 📋 目录

- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [详细安装步骤](#详细安装步骤)
- [配置说明](#配置说明)
- [启动服务](#启动服务)
- [验证安装](#验证安装)
- [常见问题](#常见问题)

## 环境要求

### 必需环境

- **Python**: 3.12+ (推荐 3.13)
- **Node.js**: 16+ (推荐 18+)
- **MySQL**: 5.7+ 或 8.0+
- **Redis**: 6.0+

### 可选环境

- **Docker**: 20.10+ (用于容器化部署)
- **ChromaDB/Milvus**: 向量数据库 (用于RAG功能)
- **MinIO**: 对象存储 (用于文件管理)

### 操作系统

- macOS 10.15+
- Ubuntu 20.04+
- Windows 10+ (需要 WSL2)

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/your-username/OmniAgent.git
cd OmniAgent

# 2. 安装依赖
# 后端
pip install -r requirements.txt

# 前端
cd src/frontend
npm install

# 3. 配置数据库
mysql -u root -p < scripts/init_db.sql

# 4. 配置环境
cp src/backend/agentchat/config.yaml.example src/backend/agentchat/config.yaml
# 编辑 config.yaml 填入你的配置

# 5. 启动服务
# 后端 (在项目根目录)
python src/backend/agentchat/main.py

# 前端 (新终端)
cd src/frontend
npm run dev
```

访问 http://localhost:8090 即可使用！

## 详细安装步骤

### 1. 安装 Python 环境

**macOS:**
```bash
brew install python@3.13
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3-pip
```

**Windows (WSL2):**
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3-pip
```

### 2. 安装 Node.js

**macOS:**
```bash
brew install node
```

**Ubuntu:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Windows:**
下载安装包：https://nodejs.org/

### 3. 安装 MySQL

**macOS:**
```bash
brew install mysql
brew services start mysql
```

**Ubuntu:**
```bash
sudo apt install mysql-server
sudo systemctl start mysql
```

**Docker (推荐):**
```bash
docker run -d \
  --name mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=123456789 \
  -e MYSQL_DATABASE=agentchat \
  mysql:8.0
```

### 4. 安装 Redis

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu:**
```bash
sudo apt install redis-server
sudo systemctl start redis
```

**Docker (推荐):**
```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7-alpine
```

### 5. 创建数据库

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE agentchat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出
exit;
```

### 6. 安装 Python 依赖

```bash
# 创建虚拟环境 (推荐)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 7. 安装前端依赖

```bash
cd src/frontend
npm install
# 或使用 pnpm (更快)
# npm install -g pnpm
# pnpm install
```

## 配置说明

### 1. 复制配置文件

```bash
cp src/backend/agentchat/config.yaml.example src/backend/agentchat/config.yaml
```

### 2. 编辑配置文件

打开 `src/backend/agentchat/config.yaml`，修改以下关键配置：

#### 数据库配置

```yaml
mysql:
  endpoint: "mysql+pymysql://root:你的密码@localhost:3306/agentchat"
  async_endpoint: "mysql+aiomysql://root:你的密码@localhost:3306/agentchat"

redis:
  endpoint: "redis://localhost:6379"
```

#### 模型配置 (必需)

```yaml
multi_models:
  conversation_model:
    api_key: "你的阿里云百炼API Key"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name: "qwen3.5-plus"
```

> 📌 **如何获取阿里云百炼API Key？**
> 1. 访问 https://dashscope.aliyun.com
> 2. 注册/登录阿里云账号
> 3. 开通百炼服务
> 4. 在控制台获取 API Key

#### 工具配置 (可选)

```yaml
tools:
  # 天气查询 (免费)
  weather:
    api_key: "你的高德地图API Key"
    endpoint: "https://restapi.amap.com/v3/weather/weatherInfo?parameters"
  
  # 联网搜索 (免费额度)
  tavily:
    api_key: "你的Tavily API Key"
  
  # 快递查询 (付费/免费试用)
  delivery:
    api_key: "你的阿里云市场AppCode"
    endpoint: "https://qyexpress.market.alicloudapi.com/composite/queryexpress"
```

详细的API密钥获取指南请查看 [API_KEYS.md](./API_KEYS.md)

## 启动服务

### 方式一：手动启动 (开发模式)

**启动后端:**
```bash
# 在项目根目录
python src/backend/agentchat/main.py
```

后端将运行在 http://127.0.0.1:7860

**启动前端:**
```bash
# 新开一个终端
cd src/frontend
npm run dev
```

前端将运行在 http://localhost:8090

### 方式二：使用脚本启动

```bash
# macOS/Linux
chmod +x scripts/start.sh
./scripts/start.sh

# Windows
scripts\start.bat
```

### 方式三：Docker 部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

详细的 Docker 部署指南请查看 [DOCKER.md](./DOCKER.md)

## 验证安装

### 1. 检查后端服务

访问 http://127.0.0.1:7860/docs 查看 API 文档

或使用 curl:
```bash
curl http://127.0.0.1:7860/api/v1/health
```

预期返回:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "status": "healthy"
  }
}
```

### 2. 检查前端服务

访问 http://localhost:8090

你应该能看到登录页面。

### 3. 注册并登录

1. 点击"注册"按钮
2. 填写用户名和密码
3. 注册成功后登录
4. 进入主页，开始使用！

## 常见问题

### 1. 后端启动失败

**问题**: `ModuleNotFoundError: No module named 'xxx'`

**解决**:
```bash
pip install -r requirements.txt
```

**问题**: `Can't connect to MySQL server`

**解决**:
- 检查 MySQL 是否启动: `mysql -u root -p`
- 检查 config.yaml 中的数据库配置是否正确
- 确认数据库 `agentchat` 已创建

**问题**: `Address already in use (port 7860)`

**解决**:
```bash
# macOS/Linux
lsof -ti:7860 | xargs kill -9

# Windows
netstat -ano | findstr :7860
taskkill /PID <PID> /F
```

### 2. 前端启动失败

**问题**: `npm install` 失败

**解决**:
```bash
# 清除缓存
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# 或使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install
```

**问题**: 前端无法连接后端

**解决**:
- 检查后端是否启动
- 检查 `src/frontend/vite.config.ts` 中的代理配置
- 确认防火墙没有阻止端口

### 3. 数据库问题

**问题**: 表不存在

**解决**:
```bash
# 后端会自动创建表，如果没有创建，检查日志
# 或手动执行初始化脚本
mysql -u root -p agentchat < scripts/init_db.sql
```

### 4. API Key 相关

**问题**: 模型调用失败

**解决**:
- 检查 config.yaml 中的 api_key 是否正确
- 确认 API Key 有足够的额度
- 检查网络连接

### 5. 向量数据库问题

**问题**: ChromaDB 连接失败

**解决**:
```bash
# 安装 ChromaDB
pip install chromadb

# 或使用 Docker
docker run -d -p 8000:8000 chromadb/chroma
```

## 下一步

- 📖 阅读 [API密钥配置指南](./API_KEYS.md) 了解如何获取各种API密钥
- 🐳 阅读 [Docker部署指南](./DOCKER.md) 了解生产环境部署
- ❓ 查看 [常见问题FAQ](./FAQ.md) 解决更多问题
- 📚 阅读 [用户手册](./USER_GUIDE.md) 学习如何使用各项功能

## 需要帮助？

- 提交 Issue: https://github.com/your-username/OmniAgent/issues
- 查看文档: https://github.com/your-username/OmniAgent/wiki
- 加入社区: [知识星球链接]
