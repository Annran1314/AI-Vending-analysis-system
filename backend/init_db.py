from app import create_app, db
from app.auth.models import User
from app.products.models import Product
from app.reports.models import Report

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 创建管理员用户
        admin_user = User(
            username='admin',
            email='admin@ai-retail.com',
            role='admin'
        )
        admin_user.set_password('admin123')
        admin_user.save()
        
        # 创建测试用户
        test_user = User(
            username='test',
            email='test@ai-retail.com',
            role='user'
        )
        test_user.set_password('test123')
        test_user.save()
        
        # 创建示例产品数据
        sample_products = [
            {
                'id': 'HAHA-100',
                'name': 'HAHA智能零售柜100型',
                'brand': 'HAHA',
                'price': 12999.00,
                'color': '#3b82f6',
                'specs': {
                    '屏幕尺寸': '15.6英寸',
                    '识别技术': 'AI视觉识别',
                    '识别准确率': '98.5%',
                    '货道数量': '24',
                    '最大容量': '120L',
                    '支付方式': '微信、支付宝、刷脸支付',
                    '尺寸': '1200×800×2000mm',
                    '重量': '85kg',
                    '功率': '300W',
                    '制冷方式': '压缩机制冷',
                    '温度范围': '2-8℃',
                    '网络连接': 'WiFi、4G',
                    '操作系统': 'Android 10',
                    'CPU': 'RK3399 4核',
                    '内存': '4GB',
                    '存储': '64GB',
                    '触摸屏': '15.6英寸电容触摸屏',
                    '摄像头数量': '4',
                    'AI芯片': 'RKNN加速器',
                    '电池续航': 'UPS 2小时',
                    '防盗系统': '电子锁+监控',
                    '远程管理': '支持',
                    '故障诊断': '智能诊断',
                    '维护成本': '低',
                    '使用寿命': '8-10年',
                    '售后服务': '全国联保',
                    '软件更新': 'OTA升级',
                    '数据安全': '加密存储',
                    '能源效率': '一级能效',
                    '噪音水平': '≤45dB',
                    '安装难度': '中等'
                },
                'performance': {
                    '识别速度': 95,
                    '系统响应': 90,
                    '稳定性': 92,
                    '节能性': 88,
                    '扩展性': 85,
                    '用户体验': 90
                },
                'created_by': admin_user.id
            },
            {
                'id': 'MM-200',
                'name': 'Micromart智能柜200型',
                'brand': 'Micromart',
                'price': 11500.00,
                'color': '#8b5cf6',
                'specs': {
                    '屏幕尺寸': '14英寸',
                    '识别技术': 'RFID+视觉识别',
                    '识别准确率': '96.0%',
                    '货道数量': '20',
                    '最大容量': '100L',
                    '支付方式': '微信、支付宝',
                    '尺寸': '1100×750×1800mm',
                    '重量': '75kg',
                    '功率': '250W',
                    '制冷方式': '压缩机制冷',
                    '温度范围': '3-10℃',
                    '网络连接': 'WiFi',
                    '操作系统': 'Android 9',
                    'CPU': 'RK3328 4核',
                    '内存': '3GB',
                    '存储': '32GB',
                    '触摸屏': '14英寸电阻触摸屏',
                    '摄像头数量': '2',
                    'AI芯片': '无',
                    '电池续航': 'UPS 1.5小时',
                    '防盗系统': '电子锁',
                    '远程管理': '支持',
                    '故障诊断': '基础诊断',
                    '维护成本': '中等',
                    '使用寿命': '6-8年',
                    '售后服务': '区域联保',
                    '软件更新': 'OTA升级',
                    '数据安全': '加密存储',
                    '能源效率': '二级能效',
                    '噪音水平': '≤50dB',
                    '安装难度': '简单'
                },
                'performance': {
                    '识别速度': 85,
                    '系统响应': 80,
                    '稳定性': 85,
                    '节能性': 82,
                    '扩展性': 75,
                    '用户体验': 82
                },
                'created_by': admin_user.id
            },
            {
                'id': '365-300',
                'name': '365智能零售柜300型',
                'brand': '365',
                'price': 9999.00,
                'color': '#10b981',
                'specs': {
                    '屏幕尺寸': '13.3英寸',
                    '识别技术': '二维码扫描',
                    '识别准确率': '95.0%',
                    '货道数量': '18',
                    '最大容量': '90L',
                    '支付方式': '微信、支付宝、银联',
                    '尺寸': '1000×700×1700mm',
                    '重量': '70kg',
                    '功率': '200W',
                    '制冷方式': '半导体制冷',
                    '温度范围': '4-12℃',
                    '网络连接': 'WiFi',
                    '操作系统': 'Android 8',
                    'CPU': 'RK3288 4核',
                    '内存': '2GB',
                    '存储': '16GB',
                    '触摸屏': '13.3英寸电容触摸屏',
                    '摄像头数量': '1',
                    'AI芯片': '无',
                    '电池续航': 'UPS 1小时',
                    '防盗系统': '机械锁',
                    '远程管理': '支持',
                    '故障诊断': '基础诊断',
                    '维护成本': '低',
                    '使用寿命': '5-7年',
                    '售后服务': '区域联保',
                    '软件更新': 'OTA升级',
                    '数据安全': '加密存储',
                    '能源效率': '二级能效',
                    '噪音水平': '≤55dB',
                    '安装难度': '简单'
                },
                'performance': {
                    '识别速度': 75,
                    '系统响应': 75,
                    '稳定性': 80,
                    '节能性': 85,
                    '扩展性': 70,
                    '用户体验': 78
                },
                'created_by': admin_user.id
            }
        ]
        
        # 创建产品
        for product_data in sample_products:
            product = Product(**product_data)
            product.save()
        
        # 创建示例报告
        sample_report = Report(
            title='2024年Q1竞品分析报告',
            description='对主要竞品进行综合分析',
            products=['HAHA-100', 'MM-200', '365-300'],
            analysis_data={
                'total_products': 3,
                'average_price': 11499.33,
                'price_range': {'min': 9999.00, 'max': 12999.00},
                'performance_comparison': {
                    'HAHA-100': 90.0,
                    'MM-200': 81.67,
                    '365-300': 77.17
                }
            },
            ai_insights={
                'market_leader': 'HAHA-100',
                'price_competitive': '365-300',
                'performance_leader': 'HAHA-100',
                'recommendations': [
                    'HAHA产品在性能和价格方面具有明显优势',
                    'Micromart产品在识别技术方面有改进空间',
                    '365产品价格竞争力强，但性能有待提升'
                ]
            },
            created_by=admin_user.id
        )
        sample_report.save()
        
        print("数据库初始化完成！")
        print(f"创建了 {User.query.count()} 个用户")
        print(f"创建了 {Product.query.count()} 个产品")
        print(f"创建了 {Report.query.count()} 个报告")
        print("\n默认管理员账号：")
        print("用户名: admin")
        print("密码: admin123")
        print("\n默认测试账号：")
        print("用户名: test")
        print("密码: test123")

if __name__ == '__main__':
    init_database()