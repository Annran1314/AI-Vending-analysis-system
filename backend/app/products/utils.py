def get_brand_color(brand):
    """根据品牌获取颜色"""
    brand_colors = {
        '可口可乐': '#E61D2B',
        '百事可乐': '#004691',
        '娃哈哈': '#FF6600',
        '康师傅': '#FF0000',
        '统一': '#0066CC',
        '农夫山泉': '#00A859',
        '怡宝': '#0066CC',
        '脉动': '#FF6600',
        '红牛': '#D6001C',
        '东鹏特饮': '#FF6600'
    }
    return brand_colors.get(brand, '#666666')

def validate_product_import_data(data):
    """验证产品导入数据"""
    required_fields = ['model', 'name', 'brand', 'price']
    errors = []
    
    for i, row in enumerate(data, 1):
        for field in required_fields:
            if field not in row or not row[field]:
                errors.append(f"第{i}行缺少必填字段: {field}")
        
        # 验证价格
        if 'price' in row:
            try:
                float(row['price'])
            except ValueError:
                errors.append(f"第{i}行价格格式错误")
    
    return len(errors) == 0, errors

def normalize_product_data(data):
    """标准化产品数据"""
    normalized_data = []
    
    for row in data:
        normalized_row = {
            'model': str(row.get('model', '')).strip(),
            'name': str(row.get('name', '')).strip(),
            'brand': str(row.get('brand', '')).strip(),
            'price': float(row.get('price', 0)),
            'color': get_brand_color(str(row.get('brand', ''))),
            'specs': dict(row.get('specs', {})),
            'performance': dict(row.get('performance', {}))
        }
        normalized_data.append(normalized_row)
    
    return normalized_data