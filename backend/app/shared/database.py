from app import db

class BaseModel(db.Model):
    """基础模型类"""
    __abstract__ = True
    
    def save(self):
        """保存对象"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """删除对象"""
        db.session.delete(self)
        db.session.commit()
        return True
    
    @classmethod
    def get_by_id(cls, id):
        """根据ID获取对象"""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """获取所有对象"""
        return cls.query.all()
    
    @classmethod
    def filter_by(cls, **kwargs):
        """根据条件过滤对象"""
        return cls.query.filter_by(**kwargs).all()