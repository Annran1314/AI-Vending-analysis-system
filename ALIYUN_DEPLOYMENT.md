# 阿里云部署指南

本指南详细说明如何将 AI 智能零售柜决策系统部署到阿里云服务器上。

## 目录

- [部署选项](#部署选项)
  - [使用阿里云容器服务 ACK 部署](#使用阿里云容器服务-ack-部署)
  - [使用阿里云弹性容器实例 ECI 部署](#使用阿里云弹性容器实例-eci-部署)
  - [使用阿里云轻量应用服务器部署](#使用阿里云轻量应用服务器部署)
  - [使用阿里云云服务器 ECS 部署](#使用阿里云云服务器-ecs-部署)
- [环境变量配置](#环境变量配置)
- [故障排除](#故障排除)

## 部署选项

### 使用阿里云容器服务 ACK 部署

#### 前提条件

- 已注册阿里云账号并完成实名认证
- 已开通容器服务 ACK
- 已安装并配置阿里云 CLI (`aliyun` 命令行工具)
- 已安装 Docker 和 Docker Compose

#### 步骤

1. **创建容器镜像服务 ACR 实例**

   - 登录阿里云控制台
   - 导航到 "容器镜像服务 ACR"
   - 创建新的 ACR 实例，选择合适的地域和规格
   - 创建新的命名空间，例如 `ai-retail-analysis`

2. **构建并推送镜像到 ACR**

   ```bash
   # 登录阿里云 CLI
   aliyun configure

   # 登录 ACR
   aliyun cr GetAuthorizationToken --RegionId <region-id> | docker login --username=ACR_<account-id> --password-stdin <registry-id>.mirror.aliyuncs.com

   # 构建镜像
   docker build -t <registry-id>.mirror.aliyuncs.com/ai-retail-analysis/frontend:latest .

   # 推送镜像
   docker push <registry-id>.mirror.aliyuncs.com/ai-retail-analysis/frontend:latest
   ```

3. **创建 ACK 集群**

   - 导航到 "容器服务 ACK"
   - 创建新的 Kubernetes 集群，选择合适的节点规格和数量
   - 等待集群创建完成

4. **部署应用到 ACK 集群**

   - 创建 Kubernetes 部署文件 `deployment.yaml`:

     ```yaml
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: ai-retail-analysis-frontend
       namespace: default
     spec:
       replicas: 2
       selector:
         matchLabels:
           app: ai-retail-analysis-frontend
       template:
         metadata:
           labels:
             app: ai-retail-analysis-frontend
         spec:
           containers:
           - name: frontend
             image: <registry-id>.mirror.aliyuncs.com/ai-retail-analysis/frontend:latest
             ports:
             - containerPort: 80
             resources:
               limits:
                 cpu: "1"
                 memory: "1Gi"
               requests:
                 cpu: "500m"
                 memory: "512Mi"
     ---
     apiVersion: v1
     kind: Service
     metadata:
       name: ai-retail-analysis-frontend
       namespace: default
     spec:
       selector:
         app: ai-retail-analysis-frontend
       ports:
       - port: 80
         targetPort: 80
       type: LoadBalancer
     ```

   - 应用部署文件:

     ```bash
     # 配置 kubectl 连接到 ACK 集群
     aliyun cs GetKubeConfig --ClusterId <cluster-id> > kubeconfig.yaml
     export KUBECONFIG=kubeconfig.yaml

     # 部署应用
     kubectl apply -f deployment.yaml

     # 查看部署状态
     kubectl get pods
     kubectl get services
     ```

5. **访问应用**

   - 获取负载均衡器的公网 IP:

     ```bash
     kubectl get services ai-retail-analysis-frontend
     ```

   - 打开浏览器，访问 `http://<load-balancer-ip>`

### 使用阿里云弹性容器实例 ECI 部署

#### 前提条件

- 已注册阿里云账号并完成实名认证
- 已开通弹性容器实例 ECI
- 已安装并配置阿里云 CLI
- 已安装 Docker

#### 步骤

1. **创建容器镜像服务 ACR 实例**

   按照上文 ACK 部署的步骤 1 操作。

2. **构建并推送镜像到 ACR**

   按照上文 ACK 部署的步骤 2 操作。

3. **创建 ECI 实例**

   - 登录阿里云控制台
   - 导航到 "弹性容器实例 ECI"
   - 点击 "创建容器组"
   - 填写基本信息，例如容器组名称、地域等
   - 选择 "镜像部署"，填写 ACR 镜像地址
   - 配置容器端口映射，将容器端口 80 映射到主机端口
   - 配置网络，选择 "公网 IP" 获取公网访问地址
   - 点击 "创建"

4. **访问应用**

   - 容器组创建完成后，在 ECI 控制台查看公网 IP
   - 打开浏览器，访问 `http://<eci-public-ip>`

### 使用阿里云轻量应用服务器部署

#### 前提条件

- 已注册阿里云账号并完成实名认证
- 已开通轻量应用服务器

#### 步骤

1. **创建轻量应用服务器实例**

   - 登录阿里云控制台
   - 导航到 "轻量应用服务器"
   - 点击 "创建实例"
   - 选择地域、镜像（推荐选择 "Docker 镜像"）、实例规格和套餐
   - 设置实例名称和密码
   - 点击 "创建"

2. **连接到服务器**

   ```bash
   ssh root@<server-ip>
   ```

3. **部署应用**

   ```bash
   # 克隆代码仓库
   git clone <repository-url> ai-retail-analysis
   cd ai-retail-analysis

   # 使用 Docker Compose 启动应用
   docker-compose up -d
   ```

4. **访问应用**

   - 打开浏览器，访问 `http://<server-ip>:8080`

### 使用阿里云云服务器 ECS 部署

#### 前提条件

- 已注册阿里云账号并完成实名认证
- 已开通云服务器 ECS

#### 步骤

1. **创建 ECS 实例**

   - 登录阿里云控制台
   - 导航到 "云服务器 ECS"
   - 点击 "创建实例"
   - 选择地域、实例规格、镜像（推荐选择 "Ubuntu 20.04 LTS" 或 "CentOS 7.9"）
   - 设置实例名称、密码和安全组（确保开放 8080 端口）
   - 点击 "创建"

2. **连接到服务器**

   ```bash
   ssh root@<server-ip>
   ```

3. **安装依赖**

   ```bash
   # Ubuntu
   apt update && apt install -y docker.io docker-compose

   # CentOS
   yum install -y docker docker-compose
   systemctl start docker
   systemctl enable docker
   ```

4. **部署应用**

   ```bash
   # 克隆代码仓库
   git clone <repository-url> ai-retail-analysis
   cd ai-retail-analysis

   # 使用 Docker Compose 启动应用
   docker-compose up -d
   ```

5. **访问应用**

   - 打开浏览器，访问 `http://<server-ip>:8080`

## 环境变量配置

系统支持以下环境变量配置：

| 环境变量 | 描述 | 默认值 |
|---------|------|-------|
| `NGINX_HOST` | Nginx 服务器名称 | `localhost` |
| `NGINX_PORT` | Nginx 监听端口 | `80` |
| `API_BASE_URL` | API 基础 URL | `/api` |

### 在阿里云部署中配置环境变量

1. **在 ACK 部署中配置**

   在 `deployment.yaml` 文件中添加环境变量：

   ```yaml
   spec:
     containers:
     - name: frontend
       image: <registry-id>.mirror.aliyuncs.com/ai-retail-analysis/frontend:latest
       ports:
       - containerPort: 80
       env:
       - name: API_BASE_URL
         value: "https://api.example.com"
   ```

2. **在 ECI 部署中配置**

   在创建 ECI 实例时，在 "高级配置" 中添加环境变量。

3. **在轻量应用服务器和 ECS 部署中配置**

   在 `docker-compose.yml` 文件中添加环境变量：

   ```yaml
   services:
     frontend:
       build: .
       ports:
         - "8080:80"
       environment:
         - API_BASE_URL=https://api.example.com
   ```

## 故障排除

### 阿里云部署相关问题

1. **镜像推送失败**

   - 检查 ACR 实例是否已开通
   - 检查阿里云 CLI 是否已正确配置
   - 检查网络连接是否正常

2. **容器启动失败**

   - 查看容器日志：

     ```bash
     # Docker
     docker logs ai-retail-analysis-frontend

     # ACK
     kubectl logs <pod-name>

     # ECI
     在 ECI 控制台查看容器日志
     ```

3. **应用无法访问**

   - 检查安全组规则是否开放了相应端口
   - 检查网络 ACL 是否允许流量
   - 检查容器是否正常运行
   - 检查负载均衡器配置是否正确

4. **性能问题**

   - 增加容器实例的 CPU 和内存资源
   - 增加 ACK 集群的节点数量
   - 优化 Nginx 配置，增加缓存

## 联系支持

如果您在部署过程中遇到任何问题，请联系阿里云技术支持或系统管理员获取帮助。