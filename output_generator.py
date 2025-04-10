import pandas as pd
import os
from data_processor import check_listing_type
from data_cache import get_filtered_data
from header_generator import generate_title, generate_description
from table_generator import generate_html_table
from metadata_generator import generate_page_title, generate_meta_description
from price_calculator import process_price_data
import logging
from openpyxl import load_workbook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_html_file(seq_number):
    """读取指定序号的 HTML 文件内容"""
    file_path = f"table_html/table_seq{seq_number}.html"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.warning(f"HTML 文件未找到: {file_path}")
        return "HTML 文件未生成"
    except Exception as e:
        logger.error(f"读取 HTML 文件失败: {file_path}, 错误: {e}")
        return f"读取错误: {str(e)}"

def generate_output_for_seq(seq_number):
    """为指定序号生成所有输出数据"""
    df_filtered, listing_type = get_filtered_data(seq_number)
    
    if df_filtered is None or not listing_type:
        return {
            "Seq": seq_number,
            "Title": f"序号 {seq_number} 未找到对应的产品信息",
            "Description": "",
            "Page Title": f"序号 {seq_number} 未找到对应的产品信息",
            "Meta Description": "",
            "Price Information": "N/A",
            "HTML Content": "未生成"
        }
    
    if not check_listing_type(listing_type):
        return {
            "Seq": seq_number,
            "Title": f"不支持的 Listing Type . {listing_type}，仅支持标准类型",
            "Description": "",
            "Page Title": f"不支持的 Listing Type . {listing_type}，仅支持标准类型",
            "Meta Description": "",
            "Price Information": "N/A",
            "HTML Content": "未生成"
        }
    
    # 生成数据（遵循 main.py 的调用顺序）
    table_data = generate_html_table(seq_number)
    meta_description = generate_meta_description(seq_number).strip()
    page_title = generate_page_title(seq_number).strip()
    title = generate_title(seq_number).strip()
    description = generate_description(seq_number).strip()
    price_results, weight_info = process_price_data(seq_number)
    
    # 格式化 Price Information
    price_info = "SKU : PRICE : COM\n"
    if price_results:
        for result, comment in price_results:
            price_info += f"{result}{comment}\n"
        price_info += f"\nWeight: {weight_info}"
    else:
        price_info += "N/A"
    
    # 读取 HTML 文件内容
    html_content = read_html_file(seq_number) if table_data is not None else "未生成"
    
    return {
        "Seq": seq_number,
        "Title": title,
        "Description": description,
        "Page Title": page_title,
        "Meta Description": meta_description,
        "Price Information": price_info.strip(),
        "HTML Content": html_content
    }

def generate_output_excel(excel_file="prduct.xls", output_file="output.xlsx"):
    """遍历 Excel 文件中的所有序号并生成输出到 Excel"""
    try:
        df = pd.read_excel(excel_file, dtype=str)
    except FileNotFoundError:
        logger.error(f"Excel 文件 '{excel_file}' 未找到")
        return
    
    # 获取所有唯一序号
    seq_numbers = df['序号'].astype(str).str.strip().unique()
    logger.info(f"找到 {len(seq_numbers)} 个唯一序号")
    
    # 生成数据
    output_data = []
    for seq_number in seq_numbers:
        try:
            seq_int = int(seq_number)
            logger.info(f"处理序号: {seq_int}")
            data = generate_output_for_seq(seq_int)
            output_data.append(data)
        except ValueError:
            logger.warning(f"无效的序号: {seq_number}，跳过")
            continue
    
    # 创建 DataFrame
    output_df = pd.DataFrame(output_data, columns=[
        "Seq", "Title", "Description", "Page Title", "Meta Description", "Price Information", "HTML Content"
    ])
    
    # 保存到 Excel
    try:
        output_df.to_excel(output_file, index=False)
        logger.info(f"输出已保存到: {os.path.abspath(output_file)}")
    except Exception as e:
        logger.error(f"保存 Excel 文件失败: {e}")

if __name__ == "__main__":
    generate_output_excel()