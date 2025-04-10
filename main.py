# main.py
from data_processor import check_listing_type
from data_cache import get_filtered_data
from header_generator import generate_title, generate_description
from table_generator import generate_html_table  # 修改导入名称
from metadata_generator import generate_page_title, generate_meta_description
from price_calculator import process_price_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        seq_number = int(input("请输入序号 . "))
    except ValueError:
        logger.error("输入错误 . 请输入一个有效的整数序号")
        return
    
    df_filtered, listing_type = get_filtered_data(seq_number)
    
    if df_filtered is None or not listing_type:
        print("====================")
        print("===== 错误信息 =====")
        print(f"序号 {seq_number} 未找到对应的产品信息 . ")
        print("====================")
        return
    
    if not check_listing_type(listing_type):
        print("====================")
        print("===== 错误信息 =====")
        print(f"不支持的 Listing Type . {listing_type}，仅支持标准类型 . ")
        print("====================")
        return
    
    # 生成HTML表格并获取数据
    table_data = generate_html_table(seq_number)
    
    meta_description = generate_meta_description(seq_number).strip()
    page_title = generate_page_title(seq_number).strip()
    title = generate_title(seq_number).strip()
    description = generate_description(seq_number).strip()
    # 修改此处使用生成的表格数据
    table = [line.strip() for line in table_data if line.strip()]
    price_results, weight_info = process_price_data(seq_number)
    
    print("====================")
    print("===== Title =====")
    print(f"Title : {title}")
    print("====================")
    print("===== Description =====")
    print(f"Description : {description}")
    print("====================")
    print("===== Table =====")
    for line in table:
        print(line)
    print("====================")
    print("===== Page Title =====")
    print(f"Page Title : {page_title}")
    print("====================")
    print("===== Meta Description =====")
    print(f"Meta Description : {meta_description}")
    print("====================")
    if price_results:
        print("===== Price Information =====")
        print("SKU : PRICE : COM")
        for result, comment in price_results:
            print(f"{result}{comment}\n")
        print("\n===== Weight Information =====")
        print(weight_info)
        print("====================")
    
    print("===== Image URLs =====")
    try:
        image_urls = df_filtered['图片地址'].dropna().unique()
        image_info = "Image URLs: " + ", ".join(str(url) for url in image_urls) if image_urls.size > 0 else "Image URLs: None"
    except KeyError:
        logger.warning("列 '图片地址' 不存在，图片信息将设置为 None")
        image_info = "Image URLs: None"
    print(image_info)
    print("====================")

if __name__ == "__main__":
    main()