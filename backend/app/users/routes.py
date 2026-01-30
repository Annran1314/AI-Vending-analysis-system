from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.auth.models import User
from app.shared.utils import json_response, error_response
from app.shared.decorators import admin_required

# 创建蓝图
users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
@admin_required
def get_users():
    """获取用户列表（管理员）"""
    users = User.get_all()
    users_list = [user.to_dict() for user in users]
    
    return jsonify(json_response(users_list)), 200

@users_bp.route('/<id>', methods=['GET'])
@admin_required
def get_user(id):
    """获取用户详情（管理员）"""
    user = User.get_by_id(id)
    
    if not user:
        return jsonify(error_response('用户不存在')), 404
    
    return jsonify(json_response(user.to_dict())), 200

@users_bp.route('/<id>', methods=['PUT'])
@admin_required
def update_user(id):
    """更新用户信息（管理员）"""
    user = User.get_by_id(id)
    
    if not user:
        return jsonify(error_response('用户不存在')), 404
    
    data = request.get_json()
    if not data:
        return jsonify(error_response('请提供更新信息')), 400
    
    # 更新用户信息
    if 'email' in data:
        # 检查邮箱是否已被其他用户使用
        existing_user = User.get_by_email(data['email'])
        if existing_user and existing_user.id != int(id):
            return jsonify(error_response('邮箱已被使用')), 400
        user.email = data['email']
    
    if 'role' in data:
        user.role = data['role']
    
    if 'password' in data:
        user.set_password(data['password'])
    
    user.save()
    
    return jsonify(json_response(user.to_dict())), 200

@users_bp.route('/<id>', methods=['DELETE'])
@admin_required
def delete_user(id):
    """删除用户（管理员）"""
    user = User.get_by_id(id)
    
    if not user:
        return jsonify(error_response('用户不存在')), 404
    
    user.delete()
    
    return jsonify(json_response({'message': '用户删除成功'})), 200