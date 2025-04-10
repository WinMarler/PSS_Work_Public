import pandas as pd
import os
import html
import re
from data_processor import get_material, get_package_content, get_installation_method, get_safe_value, process_hours, check_listing_type
from data_cache import get_filtered_data
from template_db import MATERIAL_OPTIONS, PATTERN_OPTIONS
from config import DEFAULT_PCS, DEFAULT_HOURS
from trie import Trie
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

material_trie = Trie()
for mat_key, mat_info in MATERIAL_OPTIONS.items():
    variant = mat_info["variant"].lower().replace("/paintable", "").strip()
    material_trie.insert(variant, (mat_info["variant"], mat_info["description"]))

def generate_html_table(seq_number):
    """生成 HTML 表格并保存到文件"""
    df_filtered, listing_type = get_filtered_data(seq_number)
    
    if df_filtered is None or not listing_type:
        return None
    
    if not check_listing_type(listing_type):
        return None
    
    materials = df_filtered['材质 - 简写'].dropna().str.lower().unique()
    patterns = df_filtered['纹路'].dropna().str.strip().unique()
    finishes = df_filtered.get('Finish', pd.Series([])).dropna().str.strip().unique()  # 获取 Finish 列
    has_frp = any("frp" in mat for mat in materials)
    product_name = get_safe_value(df_filtered.iloc[0], '产品', "")
    
    try:
        row = df_filtered.iloc[0]
    except IndexError:
        return []

    # 定义品牌链接
    brand_links = {
        "ArmorExtend": {"url": "https://armorextend.com", "title": "Armorextend Home Page"},
        "CMST Tuning": {"url": "https://cmsttuning.com", "title": "CMST Tuning Home Page"},
        "Future Design Carbon": {"url": "https://futuredesigncarbon.com", "title": "Future Design Carbon Home Page"},
        "Karbel Carbon": {"url": "https://karbelcarbon.com", "title": "Karbel Carbon Home Page"},
        "TAKD Carbon": {"url": "https://takdcarbon.com", "title": "TAKD Carbon Home Page"},
        "Robot Craftsman": {"url": "https://robotcraftsman.com", "title": "Robot Craftsman Home Page"},
        "Ventus Veloce": {"url": "https://www.ventusveloce.com", "title": "Ventus Veloce Home Page"},
        "SOOQOO": {"url": "https://sooqoocarbon.com", "title": "SOOQOO Home Page"},
    }

    # 生成 HTML
    html = '<figure class="table" style="width:97.86%;">\n'
    html += '    <table class="ck-table-resized">\n'
    html += '        <colgroup>\n            <col style="width:22.43%;">\n            <col style="width:77.57%;">\n        </colgroup>\n'
    html += '        <tbody>\n'

    # 动态字段顺序（根据年份数量和材质调整）
    fields = ["Vehicle Make"]
    model_year_fields = []  # 稍后根据年份数量填充
    base_fields = [
        "Vehicle Body Type",
        "Brand",
        "Product Category",
        "Installation Method",
        "Professional Installation Recommendation",
        "Installation Guide",
        "Package Content",
        "Material / Material Options"
    ]
    carbon_related_fields = [
        "Pattern / Color Options",
        "Finish Options"
    ]
    remaining_fields = [
        "Estimate Installation Hours",
        "Additional Information"
    ]

    # 定义非碳纤维材质
    non_carbon_materials = {"abs", "pp", "304不锈钢", "钛合金"}

    # 检查是否所有材质都是非碳纤维材质
    is_non_carbon_only = all(mat in non_carbon_materials for mat in materials)
    
    # 根据材质动态调整字段
    fields.extend(base_fields)
    if not is_non_carbon_only:
        fields.extend(carbon_related_fields)
    fields.extend(remaining_fields)

    # 生成表格数据（纯文本，用于控制台）
    table_data = []
    table_data.append(f"Vehicle Make : {get_safe_value(row, 'Make')}")
    
    if listing_type in ["Joint Listing (Same Design for Different Model or Year)", "Multiple Listing", "Bundle Product - Multiple Material Option"]:
        models = df_filtered['Model / Chassis / Year'].unique()
        model_lines = models[0].split('\n')
        table_data.append("Vehicle Model & Chassis & Year :")
        for line in model_lines:
            if line.strip():
                table_data.append(line.strip())
    else:
        model_year = get_safe_value(row, 'Model / Chassis / Year')
        model_lines = model_year.split('\n')
        table_data.append("Vehicle Model & Chassis & Year :")
        for line in model_lines:
            if line.strip():
                table_data.append(line.strip())
    
    table_data.append(f"Vehicle Body Type : {get_safe_value(row, '车身类型 （全）')}")
    table_data.append(f"Brand : {get_safe_value(row, 'Product Brand')}")
    table_data.append(f"Product Category : {get_safe_value(row, 'Product Type')}")
    
    method_zh = get_safe_value(row, 'Installation Method')
    notes = get_safe_value(row, 'Installation Method Notes')
    need_remove = get_safe_value(row, '是否需拆杠')
    installation_method = get_installation_method(method_zh, notes, need_remove)
    table_data.append(f"Installation Method : {installation_method}")
    
    table_data.append("Professional Installation Recommendation : Professional installation recommended.")
    table_data.append("Installation Guide : Call in for instruction")
    
    if listing_type in ["Bundle Product - Multiple Material Option", "Multiple Listing"]:
        try:
            products = df_filtered[['产品', '单位', '产品实际件数']].drop_duplicates()
            contents = []
            for _, product_row in products.iterrows():
                product = get_safe_value(product_row, '产品')
                unit = get_safe_value(product_row, '单位')
                pcs = get_safe_value(product_row, '产品实际件数', DEFAULT_PCS)
                content = get_package_content(product, unit, pcs)
                contents.append(content)
            table_data.append(f"Package Content : {' & '.join(contents)}")
        except Exception as e:
            table_data.append(f"Package Content : Error processing products . {str(e)}")
    else:
        try:
            product = get_safe_value(row, '产品')
            unit = get_safe_value(row, '单位')
            pcs = get_safe_value(row, '产品实际件数', DEFAULT_PCS)
            content = get_package_content(product, unit, pcs)
            table_data.append(f"Package Content : {content}")
        except Exception as e:
            table_data.append(f"Package Content : Error processing content . {str(e)}")

    # Material Options（纯文本）
    table_data.append("Material Options :")
    if len(materials) == 0:
        table_data.append("Not specified")
    else:
        for mat in materials:
            found = False
            if mat in MATERIAL_OPTIONS:
                variant = MATERIAL_OPTIONS[mat]["variant"]
                description = MATERIAL_OPTIONS[mat]["description"]
                table_data.append(f"{variant}:")
                for desc_line in description.split('\n'):
                    cleaned_line = desc_line.lstrip('-').strip()
                    if cleaned_line:
                        table_data.append(f"- {cleaned_line}")
                found = True
            else:
                mat_base = mat.lower().replace("/paintable", "").strip()
                result = material_trie.search(mat_base)
                if result:
                    variant, description = result
                    table_data.append(f"{variant}:")
                    for desc_line in description.split('\n'):
                        cleaned_line = desc_line.lstrip('-').strip()
                        if cleaned_line:
                            table_data.append(f"- {cleaned_line}")
                    found = True
            if not found:
                logger.warning(f"Seq {seq_number} - Material not found in MATERIAL_OPTIONS: {mat}")
                table_data.append(f"{mat}:")
                table_data.append("- Unknown material")

    # Pattern / Color Options（纯文本，仅在非全非碳纤维材质时生成）
    if not is_non_carbon_only:
        table_data.append("Pattern / Color Options :")
        if len(patterns) == 0:
            # 如果是碳纤维材质且纹路为空，默认使用 Woven 3k
            if any("碳纤" in mat for mat in materials):
                variant = PATTERN_OPTIONS["斜纹3K"]["variant"]
                description = PATTERN_OPTIONS["斜纹3K"]["description"]
                table_data.append(f"{variant}:")
                table_data.append(f"{description}")
            else:
                table_data.append("Not specified")
        else:
            pattern_map = {
                "woven 3k": "斜纹3K",
                "forged": "锻造",
                "honeycomb": "蜂窝纹",
                "3k": "斜纹3K"  # 添加对 "3k" 的支持
            }
            for pattern in patterns:
                pattern_key = pattern.lower().strip()
                pattern_key = pattern_map.get(pattern_key, pattern_key)
                if pattern_key in PATTERN_OPTIONS:
                    variant = PATTERN_OPTIONS[pattern_key]["variant"]
                    description = PATTERN_OPTIONS[pattern_key]["description"]
                    table_data.append(f"{variant}:")
                    table_data.append(f"{description}")
                else:
                    logger.warning(f"Seq {seq_number} - Pattern not found in PATTERN_OPTIONS: {pattern}")
                    table_data.append(f"{pattern}:")
                    table_data.append("Unknown pattern")

    # Finish Options（纯文本，仅在非全非碳纤维材质时生成）
    if not is_non_carbon_only:
        if len(finishes) == 1 and "gloss" in finishes[0].lower():
            table_data.append("Finish Options : Gloss Finish (default option)")
        elif len(finishes) > 0:
            if has_frp:
                table_data.append("Finish Options : Gloss Finish (default option) / Matte Finish (10% extra charge, made to order) / FRP or Carbon / Paintable")
            else:
                table_data.append("Finish Options : Gloss Finish (default option) / Matte Finish (10% extra charge, made to order)")
        else:
            if has_frp:
                table_data.append("Finish Options : Gloss Finish (default option) / Matte Finish (10% extra charge, made to order) / FRP or Carbon / Paintable")
            else:
                table_data.append("Finish Options : Gloss Finish (default option) / Matte Finish (10% extra charge, made to order)")
    
    hours_series = df_filtered['Installation Hours']
    first_non_null_hour = DEFAULT_HOURS
    for hour in hours_series:
        if pd.notna(hour):
            first_non_null_hour = hour
            break
    table_data.append(f"Estimate Installation Hours : {process_hours(first_non_null_hour)}")
    
    additional_info = "-" if "hood" not in product_name.lower() and "trunk lid" not in product_name.lower() else \
        "For Hoods, Trunk Lids Product, unless stated otherwise, may require re-use of some factory parts for a complete installation"
    table_data.append(f"Additional Information : {additional_info}")

    # 处理 Vehicle Model & Chassis 和 Vehicle Year（HTML）
    model_chassis = ""
    vehicle_year = ""
    model_year_lines = []
    start_index = -1
    for i, line in enumerate(table_data):
        if line.startswith("Vehicle Model & Chassis & Year :"):
            start_index = i + 1
            break
    if start_index != -1:
        for line in table_data[start_index:]:
            if line.startswith("Vehicle Body Type :"):
                break
            if line.strip():
                model_year_lines.append(line.strip())
        
        if model_year_lines:
            year_pattern = r'\d{4}(?:-\d{4}|-ON)?'
            years = []
            for line in model_year_lines:
                matches = re.findall(year_pattern, line)
                years.extend(matches)
            unique_years = list(dict.fromkeys(years))  # 去重并保持顺序
            
            if len(unique_years) == 1:
                vehicle_year = unique_years[0]
                model_chassis_lines = [re.sub(year_pattern, '', line).strip() for line in model_year_lines]
                model_chassis = "<br>".join([line for line in model_chassis_lines if line])
                model_year_fields = ["Vehicle Model & Chassis", "Vehicle Year"]
            else:
                model_chassis = "<br>".join(model_year_lines)
                model_year_fields = ["Vehicle Model & Chassis & Year"]
    
    # 更新字段列表
    fields[1:1] = model_year_fields

    # Material Options（HTML）
    material_html = ""
    if len(materials) == 0:
        material_html = "<p>Not specified</p>"
    else:
        material_entries = []
        for mat in materials:
            found = False
            if mat in MATERIAL_OPTIONS:
                variant = MATERIAL_OPTIONS[mat]["variant"]
                description = MATERIAL_OPTIONS[mat]["description"]
                desc_lines = [f"- {line.lstrip('-').strip()}" for line in description.split('\n') if line.strip()]
                formatted_desc = '<br>'.join(desc_lines)
                material_entries.append(f"<p><u>{variant}:</u></p>\n<p>{formatted_desc}</p>")
                found = True
            else:
                mat_base = mat.lower().replace("/paintable", "").strip()
                result = material_trie.search(mat_base)
                if result:
                    variant, description = result
                    desc_lines = [f"- {line.lstrip('-').strip()}" for line in description.split('\n') if line.strip()]
                    formatted_desc = '<br>'.join(desc_lines)
                    material_entries.append(f"<p><u>{variant}:</u></p>\n<p>{formatted_desc}</p>")
                    found = True
            if not found:
                logger.warning(f"Seq {seq_number} - Material not found in MATERIAL_OPTIONS: {mat}")
                material_entries.append(f"<p><u>{mat}:</u></p>\n<p>Unknown material</p>")
        material_html = "<p> </p>\n".join(material_entries)

    # Pattern / Color Options（HTML，仅在非全非碳纤维材质时生成）
    pattern_html = ""
    if not is_non_carbon_only:
        pattern_map = {
            "woven 3k": "斜纹3K",
            "forged": "锻造",
            "honeycomb": "蜂窝纹",
        }
        if len(patterns) == 0:
            if any("碳纤" in mat for mat in materials):
                variant = PATTERN_OPTIONS["斜纹3K"]["variant"]
                description = PATTERN_OPTIONS["斜纹3K"]["description"]
                pattern_html = f"<p><u>{variant}:</u></p>\n<p>{description}</p>"
            else:
                pattern_html = "<p>Not specified</p>"
        else:
            pattern_entries = []
            for pattern in patterns:
                pattern_key = pattern.lower().strip()
                pattern_key = pattern_map.get(pattern_key, pattern_key)
                if pattern_key in PATTERN_OPTIONS:
                    variant = PATTERN_OPTIONS[pattern_key]["variant"]
                    description = PATTERN_OPTIONS[pattern_key]["description"]
                    pattern_entries.append(f"<p><u>{variant}:</u></p>\n<p>{description}</p>")
                else:
                    logger.warning(f"Seq {seq_number} - Pattern not found in PATTERN_OPTIONS: {pattern}")
                    pattern_entries.append(f"<p><u>{pattern}:</u></p>\n<p>Unknown pattern</p>")
            pattern_html = "<p> </p>\n".join(pattern_entries)
        pattern_html += '<p><br><br>*To place order for other bespoke or creative options, please email or call in.</p>\n<p> </p>'

    # Finish Options（HTML，仅在非全非碳纤维材质时生成）
    finish_html = ""
    if not is_non_carbon_only:
        finish_options = []
        has_gloss = any("gloss" in f.lower() for f in finishes)
        has_matte = any("matte" in f.lower() for f in finishes)
        
        if has_gloss or len(finishes) == 0:  # 如果没有指定，默认包含 Gloss
            finish_options.append("Gloss Finish (default option)")
        if has_matte:
            finish_options.append("Matte Finish (10% extra charge, made to order)")
        if has_frp:
            finish_options.append("FRP or Carbon / Paintable")
        
        finish_html = " / ".join(finish_options)

    # 填充 HTML
    for field in fields:
        value = ""
        if field == "Vehicle Model & Chassis":
            value = model_chassis
        elif field == "Vehicle Year":
            value = vehicle_year
        elif field == "Vehicle Model & Chassis & Year":
            value = model_chassis
        elif field == "Material / Material Options":
            value = material_html
        elif field == "Pattern / Color Options":
            value = pattern_html
        elif field == "Finish Options":
            value = finish_html
        else:
            for line in table_data:
                if line.startswith(f"{field} :"):
                    value = line.split(':', 1)[1].strip()
                    break
        # 特殊处理 Vehicle Body Type，添加 <br> 分隔
        if field == "Vehicle Body Type" and value:
            value = value.replace('\n', '<br>')
        if field == "Brand":
            if value in brand_links:
                link_info = brand_links[value]
                value = f'<a style="color:#2b69d1;" href="{link_info["url"]}" title="{link_info["title"]}"><span style="color:#2b69d1;">{value}</span></a>'
            else:
                value = f'<span style="color:#2b69d1;">{value}</span>'
        html += f'        <tr>\n            <th>{field}</th>\n            <td>{value}</td>\n        </tr>\n'

    html += '        </tbody>\n    </table>\n</figure>\n'

    # 保存到文件
    os.makedirs("table_html", exist_ok=True)
    file_path = f"table_html/table_seq{seq_number}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"HTML 表格文件已保存到: {os.path.abspath(file_path)}")
    return table_data

if __name__ == "__main__":
    try:
        seq_number = int(input("请输入序号 . "))
    except ValueError:
        print("输入错误 . 请输入一个有效的整数序号")
        exit()
    table_data = generate_html_table(seq_number)
    if table_data:
        print("===== Generated Table =====")
        for line in table_data:
            print(line)
        print("==========================")