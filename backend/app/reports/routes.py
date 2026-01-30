from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.reports.models import Report
from app.products.models import Product
from app.shared.utils import json_response, error_response

# 创建蓝图
reports_bp = Blueprint('reports', __name__)

@reports_bp.route('', methods=['GET'])
@jwt_required()
def get_reports():
    """获取报告列表"""
    current_user_id = get_jwt_identity()
    
    # 获取用户的报告
    reports = Report.get_by_user(current_user_id)
    
    # 转换为字典列表
    reports_list = [report.to_dict() for report in reports]
    
    return jsonify(json_response(reports_list)), 200

@reports_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_report(id):
    """获取报告详情"""
    report = Report.get_by_id(id)
    
    if not report:
        return jsonify(error_response('报告不存在')), 404
    
    # 验证权限
    current_user_id = get_jwt_identity()
    if report.created_by != current_user_id:
        return jsonify(error_response('无权限访问此报告')), 403
    
    return jsonify(json_response(report.to_dict())), 200

@reports_bp.route('', methods=['POST'])
@jwt_required()
def create_report():
    """创建分析报告"""
    data = request.get_json()
    
    if not data:
        return jsonify(error_response('请提供报告信息')), 400
    
    # 验证必填字段
    if 'title' not in data or not data['title']:
        return jsonify(error_response('缺少报告标题')), 400
    
    if 'products' not in data or not isinstance(data['products'], list):
        return jsonify(error_response('请提供要分析的产品列表')), 400
    
    # 获取产品信息
    products = []
    for product_id in data['products']:
        product = Product.get_by_id(product_id)
        if product:
            products.append(product.to_dict())
    
    if len(products) == 0:
        return jsonify(error_response('没有找到有效的产品')), 400
    
    # 创建报告
    current_user_id = get_jwt_identity()
    report = Report(
        title=data['title'],
        description=data.get('description', ''),
        products=data['products'],
        analysis_data=data.get('analysis_data', {}),
        ai_insights=data.get('ai_insights', {}),
        created_by=current_user_id
    )
    report.save()
    
    return jsonify(json_response(report.to_dict())), 201

@reports_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update_report(id):
    """更新报告"""
    report = Report.get_by_id(id)
    
    if not report:
        return jsonify(error_response('报告不存在')), 404
    
    # 验证权限
    current_user_id = get_jwt_identity()
    if report.created_by != current_user_id:
        return jsonify(error_response('无权限修改此报告')), 403
    
    data = request.get_json()
    if not data:
        return jsonify(error_response('请提供更新信息')), 400
    
    # 更新报告信息
    if 'title' in data:
        report.title = data['title']
    if 'description' in data:
        report.description = data['description']
    if 'analysis_data' in data:
        report.analysis_data = data['analysis_data']
    if 'ai_insights' in data:
        report.ai_insights = data['ai_insights']
    
    report.save()
    
    return jsonify(json_response(report.to_dict())), 200

@reports_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_report(id):
    """删除报告"""
    report = Report.get_by_id(id)
    
    if not report:
        return jsonify(error_response('报告不存在')), 404
    
    # 验证权限
    current_user_id = get_jwt_identity()
    if report.created_by != current_user_id:
        return jsonify(error_response('无权限删除此报告')), 403
    
    report.delete()
    
    return jsonify(json_response({'message': '报告删除成功'})), 200

@reports_bp.route('/export', methods=['POST'])
@jwt_required()
def export_report():
    """导出报告"""
    data = request.get_json()
    
    if not data or 'report_id' not in data:
        return jsonify(error_response('请提供报告ID')), 400
    
    # 获取报告
    report = Report.get_by_id(data['report_id'])
    
    if not report:
        return jsonify(error_response('报告不存在')), 404
    
    # 验证权限
    current_user_id = get_jwt_identity()
    if report.created_by != current_user_id:
        return jsonify(error_response('无权限导出此报告')), 403
    
    # 生成导出数据
    export_data = {
        'report': report.to_dict(),
        'export_format': data.get('format', 'json'),
        'export_time': report.updated_at.isoformat()
    }
    
    return jsonify(json_response(export_data)), 200