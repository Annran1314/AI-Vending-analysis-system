from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.products.models import Product
from app.shared.utils import json_response, error_response

# 创建蓝图
analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/compare', methods=['POST'])
def compare_products():
    """产品对比分析"""
    data = request.get_json()
    
    if not data or 'products' not in data:
        return jsonify(error_response('请提供要对比的产品列表')), 400
    
    product_ids = data['products']
    if not isinstance(product_ids, list) or len(product_ids) < 2:
        return jsonify(error_response('请至少提供两个产品进行对比')), 400
    
    # 获取产品信息
    products = []
    for product_id in product_ids:
        product = Product.get_by_id(product_id)
        if product:
            products.append(product.to_dict())
    
    if len(products) < 2:
        return jsonify(error_response('至少需要两个有效产品进行对比')), 400
    
    # 生成对比分析
    analysis = generate_product_comparison(products)
    
    return jsonify(json_response(analysis)), 200

@analysis_bp.route('/ai', methods=['POST'])
def ai_analysis():
    """AI分析"""
    data = request.get_json()
    
    if not data or 'products' not in data:
        return jsonify(error_response('请提供要分析的产品列表')), 400
    
    product_ids = data['products']
    if not isinstance(product_ids, list) or len(product_ids) == 0:
        return jsonify(error_response('请提供至少一个产品进行分析')), 400
    
    # 获取产品信息
    products = []
    for product_id in product_ids:
        product = Product.get_by_id(product_id)
        if product:
            products.append(product.to_dict())
    
    if len(products) == 0:
        return jsonify(error_response('没有找到有效的产品')), 400
    
    # 生成AI分析
    analysis = generate_ai_analysis(products)
    
    return jsonify(json_response(analysis)), 200

@analysis_bp.route('/brand', methods=['POST'])
def brand_analysis():
    """品牌分析"""
    data = request.get_json()
    
    if not data or 'brands' not in data:
        return jsonify(error_response('请提供要分析的品牌列表')), 400
    
    brands = data['brands']
    if not isinstance(brands, list) or len(brands) == 0:
        return jsonify(error_response('请提供至少一个品牌进行分析')), 400
    
    # 生成品牌分析
    analysis = generate_brand_analysis(brands)
    
    return jsonify(json_response(analysis)), 200

@analysis_bp.route('/trends', methods=['GET'])
def get_trends():
    """获取行业趋势"""
    # 生成行业趋势分析
    trends = generate_industry_trends()
    
    return jsonify(json_response(trends)), 200

def generate_product_comparison(products):
    """生成产品对比分析"""
    # 提取共同的规格和性能指标
    common_specs = set()
    common_performance = set()
    
    for product in products:
        common_specs.update(product['specs'].keys())
        common_performance.update(product['performance'].keys())
    
    # 生成对比数据
    comparison_data = {
        'products': products,
        'common_specs': list(common_specs),
        'common_performance': list(common_performance),
        'price_comparison': [{'id': p['id'], 'name': p['name'], 'price': p['price']} for p in products],
        'performance_comparison': {}
    }
    
    # 性能指标对比
    for metric in common_performance:
        comparison_data['performance_comparison'][metric] = [
            {'id': p['id'], 'name': p['name'], 'value': p['performance'].get(metric, 0)}
            for p in products
        ]
    
    return comparison_data

def generate_ai_analysis(products):
    """生成AI分析"""
    # 基于规则的AI分析
    analysis = {
        'products': products,
        'insights': [],
        'recommendations': [],
        'market_position': {}
    }
    
    # 分析每个产品
    for product in products:
        # 价格分析
        if product['price'] < 5000:
            analysis['insights'].append(f"{product['name']} 价格较低，适合预算有限的客户")
        elif product['price'] > 15000:
            analysis['insights'].append(f"{product['name']} 价格较高，定位高端市场")
        else:
            analysis['insights'].append(f"{product['name']} 价格适中，适合大众市场")
        
        # 性能分析
        performance_scores = list(product['performance'].values())
        if performance_scores:
            avg_performance = sum(performance_scores) / len(performance_scores)
            if avg_performance > 80:
                analysis['insights'].append(f"{product['name']} 性能优秀")
            elif avg_performance > 60:
                analysis['insights'].append(f"{product['name']} 性能良好")
            else:
                analysis['insights'].append(f"{product['name']} 性能一般")
    
    # 生成建议
    analysis['recommendations'].append("根据市场需求，建议关注中高端产品的开发")
    analysis['recommendations'].append("加强产品性能和用户体验的提升")
    analysis['recommendations'].append("建立完善的售后服务体系")
    
    # 市场定位分析
    analysis['market_position']['price_range'] = {
        'low': min(p['price'] for p in products),
        'high': max(p['price'] for p in products),
        'average': sum(p['price'] for p in products) / len(products)
    }
    
    return analysis

def generate_brand_analysis(brands):
    """生成品牌分析"""
    analysis = {
        'brands': brands,
        'brand_data': {}
    }
    
    for brand in brands:
        # 获取品牌产品
        products = Product.get_by_brand(brand)
        product_list = [p.to_dict() for p in products]
        
        if product_list:
            # 计算品牌统计数据
            prices = [p['price'] for p in product_list]
            analysis['brand_data'][brand] = {
                'product_count': len(product_list),
                'average_price': sum(prices) / len(prices),
                'min_price': min(prices),
                'max_price': max(prices),
                'products': product_list
            }
        else:
            analysis['brand_data'][brand] = {
                'product_count': 0,
                'average_price': 0,
                'min_price': 0,
                'max_price': 0,
                'products': []
            }
    
    return analysis

def generate_industry_trends():
    """生成行业趋势分析"""
    # 获取所有产品
    all_products = Product.get_all()
    product_list = [p.to_dict() for p in all_products]
    
    # 计算行业统计数据
    if product_list:
        prices = [p['price'] for p in product_list]
        brands = list(set(p['brand'] for p in product_list))
        
        trends = {
            'total_products': len(product_list),
            'total_brands': len(brands),
            'average_price': sum(prices) / len(prices),
            'price_distribution': {
                'low': len([p for p in product_list if p['price'] < 5000]),
                'medium': len([p for p in product_list if 5000 <= p['price'] <= 15000]),
                'high': len([p for p in product_list if p['price'] > 15000])
            },
            'brand_distribution': {}
        }
        
        # 品牌分布
        for brand in brands:
            trends['brand_distribution'][brand] = len([p for p in product_list if p['brand'] == brand])
    else:
        trends = {
            'total_products': 0,
            'total_brands': 0,
            'average_price': 0,
            'price_distribution': {'low': 0, 'medium': 0, 'high': 0},
            'brand_distribution': {}
        }
    
    return trends