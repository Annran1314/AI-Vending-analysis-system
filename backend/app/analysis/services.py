def analyze_product_performance(product):
    """分析产品性能"""
    performance = product.get('performance', {})
    
    # 计算综合性能得分
    if performance:
        scores = list(performance.values())
        avg_score = sum(scores) / len(scores)
        
        # 性能等级
        if avg_score >= 90:
            level = '优秀'
        elif avg_score >= 80:
            level = '良好'
        elif avg_score >= 70:
            level = '中等'
        else:
            level = '一般'
        
        return {
            'overall_score': avg_score,
            'level': level,
            'details': performance
        }
    
    return {
        'overall_score': 0,
        'level': '一般',
        'details': {}
    }

def analyze_price_position(product, market_average):
    """分析价格定位"""
    price = product.get('price', 0)
    
    if price == 0:
        return {
            'position': '未知',
            'comparison': '无数据'
        }
    
    # 价格定位
    if price < market_average * 0.8:
        position = '低价'
        comparison = '低于市场平均'
    elif price < market_average * 1.2:
        position = '中价'
        comparison = '接近市场平均'
    else:
        position = '高价'
        comparison = '高于市场平均'
    
    return {
        'position': position,
        'comparison': comparison,
        'price': price,
        'market_average': market_average
    }

def generate_product_recommendations(products):
    """生成产品推荐"""
    if not products:
        return []
    
    # 计算市场平均价格
    avg_price = sum(p.get('price', 0) for p in products) / len(products)
    
    recommendations = []
    
    for product in products:
        # 分析性能
        performance_analysis = analyze_product_performance(product)
        # 分析价格定位
        price_analysis = analyze_price_position(product, avg_price)
        
        # 生成推荐
        if performance_analysis['overall_score'] >= 80 and price_analysis['position'] in ['中价', '低价']:
            recommendations.append({
                'product_id': product['id'],
                'product_name': product['name'],
                'recommendation': '推荐产品',
                'reason': f'性能{performance_analysis["level"]}，价格{price_analysis["position"]}，性价比高'
            })
        elif performance_analysis['overall_score'] >= 90:
            recommendations.append({
                'product_id': product['id'],
                'product_name': product['name'],
                'recommendation': '高端推荐',
                'reason': f'性能{performance_analysis["level"]}，适合对性能有高要求的客户'
            })
        elif price_analysis['position'] == '低价':
            recommendations.append({
                'product_id': product['id'],
                'product_name': product['name'],
                'recommendation': '入门推荐',
                'reason': f'价格{price_analysis["position"]}，适合预算有限的客户'
            })
    
    return recommendations

def analyze_brand_strength(brand_products):
    """分析品牌实力"""
    if not brand_products:
        return {
            'strength': '弱',
            'reason': '无产品数据'
        }
    
    # 计算品牌统计数据
    prices = [p.get('price', 0) for p in brand_products]
    avg_price = sum(prices) / len(prices)
    
    # 分析性能
    total_performance = 0
    performance_count = 0
    for product in brand_products:
        performance = product.get('performance', {})
        if performance:
            scores = list(performance.values())
            total_performance += sum(scores) / len(scores)
            performance_count += 1
    
    avg_performance = total_performance / performance_count if performance_count > 0 else 0
    
    # 评估品牌实力
    if len(brand_products) >= 5 and avg_performance >= 80:
        strength = '强'
        reason = '产品种类丰富，性能表现优秀'
    elif len(brand_products) >= 3 and avg_performance >= 70:
        strength = '中等'
        reason = '产品种类适中，性能表现良好'
    else:
        strength = '弱'
        reason = '产品种类较少或性能表现一般'
    
    return {
        'strength': strength,
        'reason': reason,
        'product_count': len(brand_products),
        'average_price': avg_price,
        'average_performance': avg_performance
    }

def generate_market_insights(products):
    """生成市场洞察"""
    if not products:
        return []
    
    insights = []
    
    # 分析价格分布
    prices = [p.get('price', 0) for p in products]
    avg_price = sum(prices) / len(prices)
    
    # 分析品牌分布
    brands = list(set(p.get('brand', '') for p in products))
    brand_count = len(brands)
    
    # 分析性能分布
    performances = []
    for product in products:
        performance = product.get('performance', {})
        if performance:
            scores = list(performance.values())
            performances.append(sum(scores) / len(scores))
    
    avg_performance = sum(performances) / len(performances) if performances else 0
    
    # 生成洞察
    if avg_price > 10000:
        insights.append('市场整体定位高端')
    elif avg_price > 5000:
        insights.append('市场整体定位中端')
    else:
        insights.append('市场整体定位低端')
    
    if brand_count >= 10:
        insights.append('市场竞争激烈，品牌众多')
    elif brand_count >= 5:
        insights.append('市场有一定竞争，品牌数量适中')
    else:
        insights.append('市场竞争较少，品牌数量有限')
    
    if avg_performance >= 80:
        insights.append('市场产品整体性能表现优秀')
    elif avg_performance >= 70:
        insights.append('市场产品整体性能表现良好')
    else:
        insights.append('市场产品整体性能表现一般')
    
    return insights