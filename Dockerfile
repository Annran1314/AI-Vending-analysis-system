# 使用官方 Nginx 镜像作为基础镜像
FROM nginx:alpine

# 复制自定义 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制前端应用文件到 Nginx 的默认静态文件目录
COPY . /usr/share/nginx/html

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx 服务
CMD ["nginx", "-g", "daemon off;"]