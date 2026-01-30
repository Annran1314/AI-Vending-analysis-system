from datetime import datetime
from app import db
from app.shared.database import BaseModel

class Product(BaseModel):
    """产品模型"""
    __tablename__ = 'products'
    
    id = db.Column(db.String(50), primary_key=True)  # 产品型号
    name = db.Column(db.String(100), nullable=False)  # 产品名称
    brand = db.Column(db.String(50), nullable=False)  # 品牌
    price = db.Column(db.Numeric(10, 2), nullable=False)  # 价格
    color = db.Column(db.String(20), nullable=False)  # 品牌颜色
    specs = db.Column(db.JSON, nullable=False, default=dict)  # 产品规格
    performance = db.Column(db.JSON, nullable=False, default=dict)  # 性能数据
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 创建用户
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'price': float(self.price),
            'color': self.color,
            'specs': self.specs,
            'performance': self.performance,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def get_by_brand(cls, brand):
        """根据品牌获取产品"""
        return cls.query.filter_by(brand=brand).all()
    
    @classmethod
    def search(cls, keyword):
        """搜索产品"""
        return cls.query.filter(
            (cls.name.ilike(f'%{keyword}%')) |
            (cls.brand.ilike(f'%{keyword}%')) |
            (cls.id.ilike(f'%{keyword}%'))
        ).all()
    
    @classmethod
    def get_by_price_range(cls, min_price, max_price):
        """根据价格范围获取产品"""
        query = cls.query
        if min_price is not None:
            query = query.filter(cls.price >= min_price)
        if max_price is not None:
            query = query.filter(cls.price <= max_price)
        return query.all()