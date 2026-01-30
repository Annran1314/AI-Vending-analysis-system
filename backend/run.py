from app import create_app

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    # 启动服务器
    app.run(host='0.0.0.0', port=8080, debug=True)