# data_cache.py
import pandas as pd
from data_processor import load_data, filter_by_sequence
from functools import lru_cache

# 全局缓存字典
_excel_cache = None
_filtered_cache = {}

def get_excel_data():
    """获取 Excel 数据，使用全局缓存"""
    global _excel_cache
    if _excel_cache is None:
        _excel_cache = load_data("prduct.xls")
    return _excel_cache

@lru_cache(maxsize=128)
def get_filtered_data(seq_number):
    """获取过滤后的数据，使用 LRU 缓存"""
    df = get_excel_data()
    df_filtered, listing_type = filter_by_sequence(df, seq_number)
    return df_filtered, listing_type