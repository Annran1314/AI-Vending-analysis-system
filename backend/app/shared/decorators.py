from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify

from app.auth.models import User

def roles_required(*roles):
    """角色权限装饰器"""
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.get_by_id(current_user_id)
            if not user or user.role not in roles:
                return jsonify({
                    "status": "error",
                    "message": "权限不足",
                    "status_code": 403
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(fn):
    """管理员权限装饰器"""
    return roles_required('admin')(fn)