import json
from datetime import datetime

def serialize_datetime(obj):
    """序列化日期时间对象"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def json_response(data, status_code=200):
    """返回JSON响应"""
    return {
        "status": "success" if status_code < 400 else "error",
        "data": data,
        "status_code": status_code
    }

def error_response(message, status_code=400):
    """返回错误响应"""
    return {
        "status": "error",
        "message": message,
        "status_code": status_code
    }

def validate_product_data(data):
    """验证产品数据"""
    required_fields = ['model', 'name', 'brand', 'price']
    for field in required_fields:
        if field not in data:
            return False, f"缺少必填字段: {field}"
    return True, "验证通过"