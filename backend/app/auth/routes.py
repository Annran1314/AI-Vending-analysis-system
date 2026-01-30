from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.auth.models import User
from app.shared.utils import json_response, error_response

# 创建蓝图
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    # 验证输入
    if not data:
        return jsonify(error_response('请提供注册信息')), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify(error_response('缺少必填字段')), 400
    
    # 检查用户名是否已存在
    if User.get_by_username(username):
        return jsonify(error_response('用户名已存在')), 400
    
    # 检查邮箱是否已存在
    if User.get_by_email(email):
        return jsonify(error_response('邮箱已存在')), 400
    
    # 创建新用户
    user = User(
        username=username,
        email=email,
        role='user'  # 默认角色
    )
    user.set_password(password)
    user.save()
    
    # 创建访问令牌
    access_token = create_access_token(identity=user.id)
    
    return jsonify(json_response({
        'user': user.to_dict(),
        'access_token': access_token
    })), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    # 验证输入
    if not data:
        return jsonify(error_response('请提供登录信息')), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify(error_response('缺少用户名或密码')), 400
    
    # 查找用户
    user = User.get_by_username(username)
    if not user or not user.check_password(password):
        return jsonify(error_response('用户名或密码错误')), 401
    
    # 创建访问令牌
    access_token = create_access_token(identity=user.id)
    
    return jsonify(json_response({
        'user': user.to_dict(),
        'access_token': access_token
    })), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户信息"""
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    
    if not user:
        return jsonify(error_response('用户不存在')), 404
    
    return jsonify(json_response(user.to_dict())), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新用户信息"""
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    
    if not user:
        return jsonify(error_response('用户不存在')), 404
    
    data = request.get_json()
    if not data:
        return jsonify(error_response('请提供更新信息')), 400
    
    # 更新用户信息
    if 'email' in data:
        # 检查邮箱是否已被其他用户使用
        existing_user = User.get_by_email(data['email'])
        if existing_user and existing_user.id != current_user_id:
            return jsonify(error_response('邮箱已被使用')), 400
        user.email = data['email']
    
    if 'password' in data:
        user.set_password(data['password'])
    
    user.save()
    
    return jsonify(json_response(user.to_dict())), 200