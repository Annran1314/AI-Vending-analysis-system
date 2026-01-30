from flask_jwt_extended import decode_token

from app.auth.models import User

def get_current_user(token):
    """从token中获取当前用户"""
    try:
        decoded = decode_token(token)
        user_id = decoded.get('sub')
        if user_id:
            return User.get_by_id(int(user_id))
        return None
    except Exception:
        return None

def validate_token(token):
    """验证token"""
    try:
        decoded = decode_token(token)
        return True, decoded
    except Exception as e:
        return False, str(e)