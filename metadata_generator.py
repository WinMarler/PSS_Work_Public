# metadata_generator.py
from data_processor import get_material, get_safe_value, check_listing_type, join_models
from data_cache import get_filtered_data

def generate_page_title(seq_number):
    """根据序号生成 Page Title"""
    df_filtered, listing_type = get_filtered_data(seq_number)
    
    if df_filtered is None or not listing_type:
        return f"序号 {seq_number} 未找到对应的产品信息"
    
    if not check_listing_type(listing_type):
        return f"不支持的 Listing Type . {listing_type}，仅支持标准类型"
    
    material = get_material(df_filtered, detailed=True)  # 使用 detailed=True 获取 Carbon Fiber 或 Carbon Fiber / FRP
    row = df_filtered.iloc[0]
    
    make = get_safe_value(row, 'Make', "").strip()
    model_year = join_models(get_safe_value(row, 'Model / Chassis / Year'))
    vehicle_part = " ".join(filter(None, [make, model_year]))
    
    brand = get_safe_value(row, 'Product Brand', "").strip()
    product = get_safe_value(row, '产品', "").strip()
    product_parts = [part for part in [brand, product] if part]
    product_part = " ".join(product_parts)
    
    product_part += f" {material}"
    
    return f"{vehicle_part} Aftermarket Parts - {product_part}".strip()

def generate_meta_description(seq_number):
    """根据序号生成 Meta Description"""
    df_filtered, listing_type = get_filtered_data(seq_number)
    
    if df_filtered is None or not listing_type:
        return ""
    
    if not check_listing_type(listing_type):
        return ""
    
    material = get_material(df_filtered, detailed=True)  # 已正确使用 detailed=True
    row = df_filtered.iloc[0]
    
    make = get_safe_value(row, 'Make', "").strip()
    model_year = join_models(get_safe_value(row, 'Model / Chassis / Year'))
    vehicle_part = " ".join(filter(None, [make, model_year]))
    
    brand = get_safe_value(row, 'Product Brand', "").strip()
    product = get_safe_value(row, '产品', "").strip()
    style = get_safe_value(row, '款式', "").strip()
    material_part = material.strip() if material else ""
    product_material = " ".join(filter(None, [product, style, material_part]))
    
    return f"Upgrade Your {vehicle_part} with {brand}'s Aftermarket Parts - {product_material}. A complete transformation of style and performance."

if __name__ == "__main__":
    try:
        seq_number = int(input("请输入序号 . "))
    except ValueError:
        print("输入错误 . 请输入一个有效的整数序号")
        exit()
    page_title = generate_page_title(seq_number)
    meta_description = generate_meta_description(seq_number)
    print(f"Page Title: {page_title}")
    print(f"Meta Description: {meta_description}")