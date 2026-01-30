from datetime import datetime
from app import db
from app.shared.database import BaseModel

class Report(BaseModel):
    """分析报告模型"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)  # 报告ID
    title = db.Column(db.String(100), nullable=False)  # 报告标题
    description = db.Column(db.Text, nullable=True)  # 报告描述
    products = db.Column(db.JSON, nullable=False, default=list)  # 分析的产品列表
    analysis_data = db.Column(db.JSON, nullable=False, default=dict)  # 分析数据
    ai_insights = db.Column(db.JSON, nullable=True, default=dict)  # AI分析洞察
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 创建用户
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'products': self.products,
            'analysis_data': self.analysis_data,
            'ai_insights': self.ai_insights,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def get_by_user(cls, user_id):
        """根据用户获取报告"""
        return cls.query.filter_by(created_by=user_id).all()
    
    @classmethod
    def search_by_title(cls, title):
        """根据标题搜索报告"""
        return cls.query.filter(cls.title.ilike(f'%{title}%')).all()