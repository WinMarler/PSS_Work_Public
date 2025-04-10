# data_processor.py
import pandas as pd
import logging
import re
from template_db import INSTALLATION_METHODS, BUMPER_REMOVAL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(file_path):
    """加载 Excel 文件，所有列强制为字符串"""
    try:
        df = pd.read_excel(file_path, dtype=str)
        logger.info(f"成功加载 Excel 文件: {file_path}")
        return df
    except Exception as e:
        logger.error(f"加载 Excel 文件失败: {e}")
        return None

def filter_by_sequence(df, seq_number):
    """根据序号过滤数据，并确定 Listing Type"""
    if df is None:
        return None, None
    
    df_filtered = df[df['序号'].astype(str).str.strip() == str(seq_number)]
    if df_filtered.empty:
        logger.warning(f"未找到序号 {seq_number} 的数据")
        return None, None
    
    listing_type = df_filtered['Listing Type'].iloc[0].strip() if 'Listing Type' in df_filtered.columns else ""
    return df_filtered, listing_type

def check_listing_type(listing_type):
    """检查 Listing Type 是否支持"""
    supported_types = [
        "Single Product - Multiple Material Option",
        "Bundle Product - Multiple Material Option",
        "Joint Listing (Same Design for Different Model or Year)",
        "Multiple Listing"
    ]
    return listing_type in supported_types

def get_safe_value(df_or_row, column, default=""):
    """安全获取 DataFrame 或 Series 中的值，特殊处理单位和产品实际件数"""
    try:
        value = df_or_row[column]
        if pd.isna(value):
            logger.debug(f"列 '{column}' 的值为空，返回默认值: {default}")
            return default
        
        value_str = str(value).strip()
        
        if column == '单位':
            logger.debug(f"原始 '单位' 值: {value_str}")
            match = re.search(r'\b(Pair|Set|Piece|Kit)\b', value_str, re.IGNORECASE)
            if match:
                unit = match.group(1).lower()
                logger.debug(f"提取的单位: {unit}")
                return unit
            else:
                logger.warning(f"无法从 '单位' 中提取有效单位: {value_str}")
                return ""
        
        if column == '产品实际件数':
            logger.debug(f"原始 '产品实际件数' 值: {value_str}")
            match = re.match(r'\s*\(?(\d+)\s*(Pcs|pcs|Pieces|piece)?\s*\)?', value_str, re.IGNORECASE)
            if match:
                qty = match.group(1)
                unit_pcs = match.group(2) if match.group(2) else "pcs"
                normalized_value = f"{qty} {unit_pcs.lower()}"
                logger.debug(f"规范化后的 '产品实际件数' 值 (标准匹配): {normalized_value}")
                return normalized_value
            
            match_fallback = re.search(r'\d+', value_str)
            if match_fallback:
                qty = match_fallback.group(0)
                normalized_value = f"{qty} pcs"
                logger.warning(f"标准匹配失败，容错处理 '产品实际件数' 为: {normalized_value} (原始值: {value_str})")
                return normalized_value
            
            logger.warning(f"无效的 '产品实际件数' 格式: {value_str}，使用默认值: {default}")
            return default
        
        return value_str
    except (KeyError, IndexError, TypeError) as e:
        logger.warning(f"获取列 '{column}' 的值时出错: {e}，返回默认值: {default}")
        return default

def normalize_model(model_str):
    """规范化车型信息，去除多余空格"""
    if not model_str:
        return model_str
    model_str = model_str.replace('\n', ' & ')
    parts = re.split(r'/', model_str)
    normalized_parts = [part.strip() for part in parts]
    return '/'.join(normalized_parts)

def join_models(model_str):
    """将多行车型信息合并为单行，用 & 分隔，并规范化空格"""
    if not model_str:
        return model_str
    model_str = model_str.replace('\n', ' & ')
    parts = re.split(r'/', model_str)
    normalized_parts = [part.strip() for part in parts]
    model_str = '/'.join(normalized_parts)
    return ' '.join(model_str.split())

def format_year(year_str):
    """拆分年份范围，逐年列出，使用空格分隔，并处理多行"""
    if not year_str:
        return ""
    
    lines = year_str.split('\n')
    result_lines = []
    
    for line in lines:
        parts = line.split()
        if not parts:
            continue
        
        year_part = parts[-1]
        model_part = ' '.join(parts[:-1]) if len(parts) > 1 else ""
        
        if year_part.endswith("-ON"):
            result_lines.append(f"{model_part} {year_part}".strip())
            continue
        
        if '-' in year_part:
            try:
                start_year, end_year = year_part.split('-')
                start_year = int(start_year)
                end_year = int(end_year)
                years = [str(year) for year in range(start_year, end_year + 1)]
                formatted_years = ' '.join(years)
            except (ValueError, IndexError) as e:
                logger.warning(f"年份格式错误: {year_part}, 错误: {e}")
                formatted_years = year_part
        else:
            formatted_years = year_part
        
        if model_part:
            result_lines.append(f"{model_part} {formatted_years}")
        else:
            result_lines.append(formatted_years)
    
    return ' & '.join(result_lines)

def get_material(df, detailed=False):
    """获取材质信息，将 Full FRP 等同于 FRP 处理"""
    materials = df['材质 - 简写'].dropna().str.strip().unique()
    if not materials.size:
        return "Not specified"
    
    material_set = set(materials)
    
    # 如果只有一种材质，直接返回（无论是否为 Carbon/FRP）
    if len(material_set) == 1:
        material = materials[0]
        if detailed:
            # detailed=True 时，返回更简化的描述
            if material in ["FRP", "FRP or Carbon", "Full FRP"]:  # 将 Full FRP 视为 FRP
                return "FRP"
            elif material in ["Pre-preg Carbon", "Vacuumed Carbon"]:
                return "Carbon Fiber"
            elif material in ["Partial Pre-preg Carbon", "Partial Vacuumed Carbon"]:
                return "Partial Carbon Fiber"
            elif material in ["Single-sided Pre-preg Carbon", "Single-sided Vacuumed Carbon"]:
                return "Single-sided Carbon Fiber"
            elif material in ["Double-sided Pre-preg Carbon", "Double-sided Vacuumed Carbon"]:
                return "Double-sided Carbon Fiber"
            else:
                return material  # 非 Carbon/FRP 材质直接返回原始值（如 ABS、PP）
        else:
            return material  # 非 detailed 时，直接返回原始材质
    
    # 多种材质时，优先处理 Carbon 和 FRP 的组合
    if detailed:
        # 将 Full FRP 视为 FRP 处理
        if "FRP" in material_set or "FRP or Carbon" in material_set or "Full FRP" in material_set:
            return "Carbon Fiber / FRP"
        elif any(mat in material_set for mat in ["Pre-preg Carbon", "Vacuumed Carbon", "Partial Pre-preg Carbon", "Partial Vacuumed Carbon", "Single-sided Pre-preg Carbon", "Single-sided Vacuumed Carbon", "Double-sided Pre-preg Carbon", "Double-sided Vacuumed Carbon"]):
            return "Carbon Fiber"
        else:
            return " & ".join(material_set)  # 多种非 Carbon/FRP 材质用 & 分隔
    else:
        return "Carbon Fiber / FRP" if ("FRP" in material_set or "FRP or Carbon" in material_set or "Full FRP" in material_set) else "Carbon Fiber"

def get_package_content(product, unit, pcs):
    """生成 Package Content"""
    if not isinstance(pcs, str):
        pcs = str(pcs).strip()
        logger.debug(f"将 pcs 转换为字符串: {pcs} (类型: {type(pcs)})")
    
    if not pcs or pd.isna(pcs):
        normalized_pcs = "1 pcs"
    else:
        match = re.match(r'(\d+)\s*(Pcs|pcs|Pieces|piece)?', pcs, re.IGNORECASE)
        normalized_pcs = match.group(1) + " pcs" if match else "1 pcs"
        logger.debug(f"规范化后的 pcs 值: {normalized_pcs}")
    
    if unit and unit.strip():
        return f"{product} x1 {unit.capitalize()} ({normalized_pcs})"
    return f"{product} x1 ({normalized_pcs})"

def get_installation_method(method_zh, notes, need_remove):
    """生成 Installation Method"""
    if not method_zh or not method_zh.strip():
        return "Replacement with OEM mounting points"
    method_zh = method_zh.strip()
    installation_method = INSTALLATION_METHODS.get(method_zh, "Unknown Installation Method")
    
    if need_remove and need_remove.strip():
        bumper_removal = BUMPER_REMOVAL.get(need_remove.strip(), "")
        if bumper_removal:
            installation_method += f" {bumper_removal}"
    
    if notes and notes.strip():
        installation_method += f" Notes: {notes.strip()}"
    return installation_method

def process_hours(hours):
    """处理 Installation Hours，保留小数"""
    try:
        hours_float = float(hours)
        return f"{hours_float} Hour" if hours_float == 1 else f"{hours_float} Hours"
    except (ValueError, TypeError):
        return "0 Hour"