from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
import io

from app.products.models import Product
from app.shared.utils import json_response, error_response, validate_product_data
from app.shared.decorators import admin_required

# 创建蓝图
products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
def get_products():
    """获取产品列表"""
    # 获取查询参数
    brand = request.args.get('brand')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    keyword = request.args.get('keyword')
    
    # 根据参数查询产品
    if brand:
        products = Product.get_by_brand(brand)
    elif keyword:
        products = Product.search(keyword)
    elif min_price or max_price:
        products = Product.get_by_price_range(min_price, max_price)
    else:
        products = Product.get_all()
    
    # 转换为字典列表
    products_list = [product.to_dict() for product in products]
    
    return jsonify(json_response(products_list)), 200

@products_bp.route('/<id>', methods=['GET'])
def get_product(id):
    """获取产品详情"""
    product = Product.get_by_id(id)
    
    if not product:
        return jsonify(error_response('产品不存在')), 404
    
    return jsonify(json_response(product.to_dict())), 200

@products_bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    """创建新产品"""
    data = request.get_json()
    
    if not data:
        return jsonify(error_response('请提供产品信息')), 400
    
    # 验证产品数据
    valid, message = validate_product_data(data)
    if not valid:
        return jsonify(error_response(message)), 400
    
    # 检查产品型号是否已存在
    existing_product = Product.get_by_id(data['model'])
    if existing_product:
        return jsonify(error_response('产品型号已存在')), 400
    
    # 创建产品
    current_user_id = get_jwt_identity()
    product = Product(
        id=data['model'],
        name=data['name'],
        brand=data['brand'],
        price=data['price'],
        color=data.get('color', '#000000'),
        specs=data.get('specs', {}),
        performance=data.get('performance', {}),
        created_by=current_user_id
    )
    product.save()
    
    return jsonify(json_response(product.to_dict())), 201

@products_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    """更新产品信息"""
    product = Product.get_by_id(id)
    
    if not product:
        return jsonify(error_response('产品不存在')), 404
    
    data = request.get_json()
    if not data:
        return jsonify(error_response('请提供更新信息')), 400
    
    # 更新产品信息
    if 'name' in data:
        product.name = data['name']
    if 'brand' in data:
        product.brand = data['brand']
    if 'price' in data:
        product.price = data['price']
    if 'color' in data:
        product.color = data['color']
    if 'specs' in data:
        product.specs = data['specs']
    if 'performance' in data:
        product.performance = data['performance']
    
    product.save()
    
    return jsonify(json_response(product.to_dict())), 200

@products_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    """删除产品"""
    product = Product.get_by_id(id)
    
    if not product:
        return jsonify(error_response('产品不存在')), 404
    
    product.delete()
    
    return jsonify(json_response({'message': '产品删除成功'})), 200

@products_bp.route('/import', methods=['POST'])
@jwt_required()
def import_products():
    """批量导入产品"""
    if 'file' not in request.files:
        return jsonify(error_response('请上传文件')), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(error_response('请选择文件')), 400
    
    # 检查文件类型
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify(error_response('请上传Excel文件')), 400
    
    try:
        # 读取Excel文件
        df = pd.read_excel(file)
        
        # 验证文件格式
        required_columns = ['model', 'name', 'brand', 'price']
        if not all(col in df.columns for col in required_columns):
            return jsonify(error_response('Excel文件格式错误，缺少必填列')), 400
        
        # 导入产品
        current_user_id = get_jwt_identity()
        imported_count = 0
        errors = []
        
        for _, row in df.iterrows():
            try:
                # 检查产品型号是否已存在
                existing_product = Product.get_by_id(str(row['model']))
                if existing_product:
                    errors.append(f"产品型号 {row['model']} 已存在")
                    continue
                
                # 创建产品
                product = Product(
                    id=str(row['model']),
                    name=str(row['name']),
                    brand=str(row['brand']),
                    price=float(row['price']),
                    color=str(row.get('color', '#000000')),
                    specs=dict(row.get('specs', {})),
                    performance=dict(row.get('performance', {})),
                    created_by=current_user_id
                )
                product.save()
                imported_count += 1
            except Exception as e:
                errors.append(f"导入产品 {row.get('model')} 失败: {str(e)}")
        
        return jsonify(json_response({
            'imported_count': imported_count,
            'errors': errors
        })), 200
    
    except Exception as e:
        return jsonify(error_response(f'导入失败: {str(e)}')), 500