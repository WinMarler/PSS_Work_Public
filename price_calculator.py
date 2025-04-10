import pandas as pd
import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 材质分类映射
MATERIAL_MAPPING = {
    'FRP': 'FRP or Carbon',
    'Pre-preg Carbon': 'Full Carbon',
    'Partial Pre-preg Carbon': 'Partial Carbon',
    'Single-sided Pre-preg Carbon': 'Single-sided Carbon',
    'Double-sided Pre-preg Carbon': 'Double-sided Carbon',
    'Vacuumed Carbon': 'Full Carbon',
    'Partial Vacuumed Carbon': 'Partial Carbon',
    'Single-sided Vacuumed Carbon': 'Single-sided Carbon',
    'Double-sided Vacuumed Carbon': 'Double-sided Carbon',
    'FRP or Carbon': 'FRP or Carbon',
    'Full FRP':'FRP or Carbon',
}

# 附加选项加成因子
ADD_ON_FACTORS = {
    'Matte': 1.1,
    'Forged': 1.2,
    'Honeycomb': 1.2,
    'Forged and Woven Carbon Fiber Mix': 1.2
}

def classify_material(material_short):
    """根据材质简写分类材质类型"""
    return MATERIAL_MAPPING.get(material_short.strip() if material_short else 'Unknown', 'Other')

def infer_prices(prices_by_material):
    """根据已知价格推算其他材质价格，返回价格和计算注释"""
    known_prices = {mat: price for mat, price in prices_by_material.items() if price is not None}
    inferred_prices = {mat: prices_by_material.get(mat, None) for mat in MATERIAL_MAPPING.values()}
    price_source = {mat: f"{int(price)} (direct)" for mat, price in known_prices.items() if price is not None}

    if not known_prices:
        for mat in inferred_prices:
            inferred_prices[mat] = 0
            price_source[mat] = "0 (default)"
        return inferred_prices, price_source

    # 优先处理已知价格推算
    if 'Single-sided Carbon' in known_prices:
        base_single = known_prices['Single-sided Carbon']
        if 'Double-sided Carbon' not in known_prices:
            inferred_prices['Double-sided Carbon'] = math.ceil(base_single * 1.4)
            price_source['Double-sided Carbon'] = f"{int(base_single)} * 1.4 = {inferred_prices['Double-sided Carbon']}"
        if 'FRP or Carbon' not in known_prices:
            inferred_prices['FRP or Carbon'] = math.ceil(base_single * 0.75)
            price_source['FRP or Carbon'] = f"{int(base_single)} * 0.75 = {inferred_prices['FRP or Carbon']}"

    elif 'Double-sided Carbon' in known_prices:
        base_double = known_prices['Double-sided Carbon']
        if 'Single-sided Carbon' not in known_prices:
            inferred_prices['Single-sided Carbon'] = math.ceil(base_double / 1.4)
            price_source['Single-sided Carbon'] = f"{int(base_double)} / 1.4 = {inferred_prices['Single-sided Carbon']}"
        if 'FRP or Carbon' not in known_prices:
            inferred_prices['FRP or Carbon'] = math.ceil(inferred_prices['Single-sided Carbon'] * 0.75)
            price_source['FRP or Carbon'] = f"{int(inferred_prices['Single-sided Carbon'])} * 0.75 = {inferred_prices['FRP or Carbon']}"

    # 未推算的材质设为 0
    for mat in inferred_prices:
        if inferred_prices[mat] is None:
            inferred_prices[mat] = 0
            price_source[mat] = "0 (default)"

    return inferred_prices, price_source

def calculate_compare_at_price(price):
    """计算 Compare-at Price"""
    if price == 0:
        return 0
    if price < 500:
        return price + 60
    elif 500 <= price < 1600:
        return price + 100
    elif 1600 <= price < 2800:
        return price + 200
    elif price >= 2800:
        return price + 350
    return price

def calculate_add_on_price(base_price, add_on_type):
    """计算附加选项加成后的价格"""
    factor = ADD_ON_FACTORS.get(add_on_type, 1.0)
    return math.ceil(base_price * factor)

def process_price_data(seq_number, excel_file="prduct.xls", df=None):
    """处理指定序号的产品价格数据"""
    if df is None:
        try:
            df = pd.read_excel(excel_file, dtype=str)
        except FileNotFoundError:
            logger.error(f"Excel 文件 '{excel_file}' 未找到")
            return [], "Weight: N/A"
    
    df_filtered = df[df['序号'].astype(str).str.strip() == str(seq_number)]
    if df_filtered.empty:
        logger.error(f"未找到序号 {seq_number} 的数据")
        return [], "Weight: N/A"

    results = []
    weights = {}

    # 按材质收集基准价格
    prices_by_material = {}
    for _, row in df_filtered.iterrows():
        material_short = row.get('材质 - 简写', 'Unknown')
        material = classify_material(material_short)
        price = row.get('Retail Price', None)
        try:
            price = float(price) if price and not pd.isna(price) else None
        except (ValueError, TypeError):
            price = None
        if material not in prices_by_material or (price is not None and prices_by_material[material] is None):
            prices_by_material[material] = price

    # 推算价格
    inferred_prices, price_source = infer_prices(prices_by_material)

    # 处理每个 SKU
    for _, row in df_filtered.iterrows():
        sku = row.get('PSS SKU', "Unknown SKU")
        material_short = row.get('材质 - 简写', 'Unknown')
        material = classify_material(material_short)
        texture = str(row.get('纹路', '')).strip()
        finish = str(row.get('封层', '')).strip()
        retail_price = row.get('Retail Price', None)
        weight = row.get('Shipping Weight', None)

        try:
            base_price = float(retail_price) if retail_price and not pd.isna(retail_price) else None
        except (ValueError, TypeError):
            base_price = None

        # 使用已知价格或推算价格
        if base_price is not None:
            price = base_price
            comment = f"{int(price)} (direct)"
        else:
            price = inferred_prices.get(material, 0)
            comment = price_source.get(material, "0 (default)")

        # 应用附加选项
        add_on_type = None
        if texture in ADD_ON_FACTORS:
            add_on_type = texture
        elif finish in ADD_ON_FACTORS:
            add_on_type = finish
        
        if add_on_type:
            base_for_add_on = price
            price = calculate_add_on_price(price, add_on_type)
            comment = f"{int(base_for_add_on)} * {ADD_ON_FACTORS[add_on_type]} = {int(price)}"

        # 计算 Compare-at Price
        compare_at_price = calculate_compare_at_price(price)
        price = int(price + 0.99)
        compare_at_price = int(compare_at_price + 0.99)

        results.append((f"{sku} : {price} : {compare_at_price}", f" # {comment}"))
        weights[sku] = weight if weight and not pd.isna(weight) else "none"

    # 修改重量信息生成部分
    valid_weights = [w for w in weights.values() if w != "none"]
    if valid_weights:
        weight_info = f"Weight: {', '.join(valid_weights)}"
    else:
        weight_info = "Weight: N/A"
    
    return results, weight_info

if __name__ == "__main__":
    try:
        seq_number = int(input("请输入序号 . "))
    except ValueError:
        logger.error("输入错误 . 请输入一个有效的整数序号")
        exit()

    price_results, weight_info = process_price_data(seq_number)
    print("===== Price Information =====")
    print("SKU : PRICE : COM")
    for result, comment in price_results:
        print(f"{result}{comment}")
    print(weight_info)