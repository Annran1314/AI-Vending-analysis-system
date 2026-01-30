# 部署指南

本指南详细说明如何使用 Docker 部署以及云端部署 AI 智能零售柜决策系统。

## 目录

- [Docker 部署](#docker-部署)
  - [前提条件](#前提条件)
  - [使用 Docker 构建和运行](#使用-docker-构建和运行)
  - [使用 Docker Compose 构建和运行](#使用-docker-compose-构建和运行)
- [云端部署](#云端部署)
  - [使用 AWS ECS 部署](#使用-aws-ecs-部署)
  - [使用 Azure App Service 部署](#使用-azure-app-service-部署)
  - [使用 Google Cloud Run 部署](#使用-google-cloud-run-部署)
  - [使用 GitHub Pages 部署](#使用-github-pages-部署)
- [环境变量配置](#环境变量配置)
- [故障排除](#故障排除)

## Docker 部署

### 前提条件

- 安装 [Docker](https://www.docker.com/get-started)
- 安装 [Docker Compose](https://docs.docker.com/compose/install/) (可选)

### 使用 Docker 构建和运行

1. **构建 Docker 镜像**

   ```bash
   docker build -t ai-retail-analysis .
   ```

2. **运行 Docker 容器**

   ```bash
   docker run -d -p 8080:80 --name ai-retail-analysis-frontend ai-retail-analysis
   ```

3. **访问应用**

   打开浏览器，访问 `http://localhost:8080`

### 使用 Docker Compose 构建和运行

1. **启动应用**

   ```bash
   docker-compose up -d
   ```

2. **停止应用**

   ```bash
   docker-compose down
   ```

3. **查看日志**

   ```bash
   docker-compose logs
   ```

4. **访问应用**

   打开浏览器，访问 `http://localhost:8080`

## 云端部署

### 使用 AWS ECS 部署

1. **创建 ECR 仓库**

   - 登录 AWS 控制台
   - 导航到 ECR 服务
   - 创建新的仓库，命名为 `ai-retail-analysis`

2. **构建并推送镜像**

   ```bash
   # 登录 ECR
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com

   # 构建镜像
   docker build -t <account-id>.dkr.ecr.<region>.amazonaws.com/ai-retail-analysis .

   # 推送镜像
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ai-retail-analysis
   ```

3. **创建 ECS 集群和服务**

   - 导航到 ECS 服务
   - 创建新的集群
   - 创建新的任务定义，使用推送的 ECR 镜像
   - 创建新的服务，使用任务定义

4. **配置负载均衡器**

   - 创建新的 ALB
   - 配置目标组指向 ECS 服务
   - 配置监听器监听 80 端口

5. **访问应用**

   使用 ALB 提供的 DNS 名称访问应用

### 使用 Azure App Service 部署

1. **创建 Azure Container Registry**

   - 登录 Azure 门户
   - 创建新的容器注册表

2. **构建并推送镜像**

   ```bash
   # 登录 ACR
   az acr login --name <registry-name>

   # 构建镜像
   docker build -t <registry-name>.azurecr.io/ai-retail-analysis .

   # 推送镜像
   docker push <registry-name>.azurecr.io/ai-retail-analysis
   ```

3. **创建 App Service**

   - 创建新的 Web 应用
   - 选择 "Docker Container" 作为发布方式
   - 选择 "Azure Container Registry" 作为镜像源
   - 选择推送的镜像

4. **访问应用**

   使用 App Service 提供的 URL 访问应用

### 使用 Google Cloud Run 部署

1. **启用 Cloud Run API**

   - 登录 Google Cloud 控制台
   - 启用 Cloud Run API

2. **构建并部署**

   ```bash
   # 构建并部署
   gcloud run deploy ai-retail-analysis \
     --source . \
     --platform managed \
     --region <region> \
     --allow-unauthenticated
   ```

3. **访问应用**

   使用 Cloud Run 提供的 URL 访问应用

### 使用 GitHub Pages 部署

1. **创建 GitHub 仓库**

   - 创建新的 GitHub 仓库
   - 将代码推送到仓库

2. **配置 GitHub Pages**

   - 导航到仓库设置
   - 找到 "Pages" 部分
   - 选择 "main" 分支作为源
   - 点击 "Save"

3. **访问应用**

   使用 GitHub Pages 提供的 URL 访问应用

## 环境变量配置

系统支持以下环境变量配置：

| 环境变量 | 描述 | 默认值 |
|---------|------|-------|
| `NGINX_HOST` | Nginx 服务器名称 | `localhost` |
| `NGINX_PORT` | Nginx 监听端口 | `80` |
| `API_BASE_URL` | API 基础 URL | `/api` |

## 故障排除

### Docker 相关问题

1. **端口已被占用**

   ```bash
   # 查看占用端口的进程
   lsof -i :8080

   # 停止占用端口的进程
   kill <PID>
   ```

2. **Docker 镜像构建失败**

   - 检查 Dockerfile 中的指令
   - 确保所有文件路径正确

3. **容器无法启动**

   ```bash
   # 查看容器日志
   docker logs ai-retail-analysis-frontend
   ```

### 云端部署相关问题

1. **部署失败**

   - 检查云端控制台中的错误日志
   - 确保镜像构建成功
   - 确保所有必要的权限已配置

2. **应用无法访问**

   - 检查网络配置
   - 确保安全组/防火墙规则允许流量
   - 检查应用日志

## 联系支持

如果您在部署过程中遇到任何问题，请联系系统管理员或开发团队获取支持。