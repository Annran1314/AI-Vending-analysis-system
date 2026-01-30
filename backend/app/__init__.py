from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.config import Config

# 初始化数据库
db = SQLAlchemy()
# 初始化迁移工具
migrate = Migrate()
# 初始化JWT
jwt = JWTManager()
# 初始化CORS
cors = CORS()

def create_app(config_class=Config):
    """创建Flask应用实例"""
    app = Flask(__name__, static_folder='../../', static_url_path='/')
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    
    # 注册蓝图
    from app.auth.routes import auth_bp
    from app.products.routes import products_bp
    from app.analysis.routes import analysis_bp
    from app.reports.routes import reports_bp
    from app.users.routes import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    # 处理根路径
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    
    return app