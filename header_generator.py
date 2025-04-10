# header_generator.py
import pandas as pd
import logging
from data_processor import get_material, get_safe_value, check_listing_type, format_year, normalize_model, join_models
from data_cache import get_filtered_data

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_title(seq_number):
    """根据序号生成 Title"""
    df_filtered, listing_type = get_filtered_data(seq_number)
    
    if df_filtered is None or not listing_type:
        return f"序号 {seq_number} 未找到对应的产品信息"
    
    if not check_listing_type(listing_type):
        return f"不支持的 Listing Type . {listing_type}，仅支持标准类型"
    
    material = get_material(df_filtered, detailed=True)  # 使用 detailed=True 获取 Carbon Fiber 或 Carbon Fiber / FRP
    row = df_filtered.iloc[0]
    
    if listing_type == "Single Product - Multiple Material Option":
        brand = get_safe_value(row, 'Product Brand', "")
        style = get_safe_value(row, '款式', "")
        product = get_safe_value(row, '产品', "")
        brand_product = " ".join(filter(None, [brand, style, product]))
        model_year = normalize_model(get_safe_value(row, 'Model / Chassis / Year'))
        return (
            f"{brand_product} "
            "for "
            f"{get_safe_value(row, 'Make')} "
            f"{model_year} "
            f"{material}"
        )
    elif listing_type == "Bundle Product - Multiple Material Option":
        products = df_filtered[['产品', '款式']].drop_duplicates().apply(
            lambda x: " ".join(filter(None, [get_safe_value(x, '款式', ""), get_safe_value(x, '产品')])), axis=1)
        models = df_filtered['Model / Chassis / Year'].unique()
        models = join_models(models[0])
        return (
            f"{get_safe_value(df_filtered, 'Product Brand', '').iloc[0]} "
            f"{' & '.join(products)} "
            "for "
            f"{get_safe_value(df_filtered, 'Make', '').iloc[0]} "
            f"{models} "
            f"{material}"
        )
    elif listing_type == "Joint Listing (Same Design for Different Model or Year)":
        models = df_filtered['Model / Chassis / Year'].unique()
        models = join_models(models[0])
        brand = get_safe_value(df_filtered, 'Product Brand', "").iloc[0]
        style = get_safe_value(row, '款式', "")
        product = get_safe_value(row, '产品', "")
        brand_product = " ".join(filter(None, [brand, style, product]))
        return (
            f"{brand_product} "
            "for "
            f"{get_safe_value(df_filtered, 'Make', '').iloc[0]} "
            f"{models} "
            f"{material}"
        )
    elif listing_type == "Multiple Listing":
        products = df_filtered[['产品', '款式']].drop_duplicates().apply(
            lambda x: " ".join(filter(None, [get_safe_value(x, '款式', ""), get_safe_value(x, '产品')])), axis=1)
        models = df_filtered['Model / Chassis / Year'].unique()
        models = join_models(models[0])
        return (
            f"{get_safe_value(df_filtered, 'Product Brand', '').iloc[0]} "
            f"{' & '.join(products)} "
            "for "
            f"{get_safe_value(df_filtered, 'Make', '').iloc[0]} "
            f"{models} "
            f"{material}"
        )
    return f"未知的 Listing Type . {listing_type}"

def generate_description(seq_number):
    """根据序号生成 Description"""
    df_filtered, listing_type = get_filtered_data(seq_number)
    
    if df_filtered is None or not listing_type:
        return ""
    
    if not check_listing_type(listing_type):
        return ""
    
    material = get_material(df_filtered, detailed=True)  # 已正确使用 detailed=True
    row = df_filtered.iloc[0]
    
    if listing_type == "Single Product - Multiple Material Option":
        style = get_safe_value(row, '款式', "")
        model_year = get_safe_value(row, 'Model / Chassis / Year')
        formatted_model = format_year(model_year)
        product_part = f"{style} {get_safe_value(row, '产品')}".strip()
        logger.debug(f"Model Year input: {model_year}, Formatted output: {formatted_model}")
        return (
            f"Upgrade Your "
            f"{get_safe_value(row, 'Make')} "
            f"{formatted_model} "
            "with Aftermarket Parts - "
            f"{product_part} "
            f"{material} "
            "from "
            f"{get_safe_value(row, 'Product Brand')}"
        )
    elif listing_type == "Bundle Product - Multiple Material Option":
        products = df_filtered[['产品', '款式']].drop_duplicates().apply(
            lambda x: f"{get_safe_value(x, '款式', '')} {get_safe_value(x, '产品')}".strip(), axis=1)
        models = df_filtered['Model / Chassis / Year'].unique()
        formatted_models = format_year(join_models(models[0]))
        logger.debug(f"Model Year input: {join_models(models[0])}, Formatted output: {formatted_models}")
        return (
            f"Upgrade Your "
            f"{get_safe_value(df_filtered, 'Make', '').iloc[0]} "
            f"{formatted_models} "
            "with Aftermarket Parts - "
            f"{' & '.join(products)} "
            f"{material} "
            "from "
            f"{get_safe_value(df_filtered, 'Product Brand', '').iloc[0]}"
        )
    elif listing_type == "Joint Listing (Same Design for Different Model or Year)":
        models = df_filtered['Model / Chassis / Year'].unique()
        formatted_models = format_year(join_models(models[0]))
        logger.debug(f"Model Year input: {join_models(models[0])}, Formatted output: {formatted_models}")
        style = get_safe_value(row, '款式', "")
        product_part = f"{style} {get_safe_value(row, '产品')}".strip()
        return (
            f"Upgrade Your "
            f"{get_safe_value(df_filtered, 'Make', '').iloc[0]} "
            f"{formatted_models} "
            "with Aftermarket Parts - "
            f"{product_part} "
            f"{material} "
            "from "
            f"{get_safe_value(df_filtered, 'Product Brand', '').iloc[0]}"
        )
    elif listing_type == "Multiple Listing":
        products = df_filtered[['产品', '款式']].drop_duplicates().apply(
            lambda x: f"{get_safe_value(x, '款式', '')} {get_safe_value(x, '产品')}".strip(), axis=1)
        models = df_filtered['Model / Chassis / Year'].unique()
        formatted_models = format_year(join_models(models[0]))
        logger.debug(f"Model Year input: {join_models(models[0])}, Formatted output: {formatted_models}")
        return (
            f"Upgrade Your "
            f"{get_safe_value(df_filtered, 'Make', '').iloc[0]} "
            f"{formatted_models} "
            "with Aftermarket Parts - "
            f"{' & '.join(products)} "
            f"{material} "
            "from "
            f"{get_safe_value(df_filtered, 'Product Brand', '').iloc[0]}"
        )
    return ""

if __name__ == "__main__":
    try:
        seq_number = int(input("请输入序号 . "))
    except ValueError:
        print("输入错误 . 请输入一个有效的整数序号")
        exit()
    title = generate_title(seq_number)
    description = generate_description(seq_number)
    print(f"===== Title =====")
    print(f"Title: {title}")
    print(f"===== Description =====")
    print(f"Description: {description}")