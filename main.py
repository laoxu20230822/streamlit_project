from numpy import place
import streamlit as st
import pandas as pd
from database.glossary import Glossary
from database.metric import Metric
from database.page import Pageable
import database.sql as sql
from database.standard_category import StandardCategory
from database.standard_db import StandardDB
from database.standard_db import WhereCause
from database.standard_index import StandardIndex
from database.standard_structure import StandardStructure
from database.reference_standards import ReferenceStandards

# standard_db=StandardDB()
# standard_db.load_from_excel('/Users/xuminghui/code/uv_project_install/streamlit_project/file/标准全文--体系范围标准-正文数据源-2025.6.21.xlsx')


# standard_structure=StandardStructure()
# standard_structure.load_from_excel('/Users/xuminghui/code/uv_project_install/streamlit_project/file/最终目次页（17-18-19-20-24合）2024.3.13.xlsx')

# data=standard_structure.detail_to_markdown('Q/SY 01145-2020')


# glossary=Glossary()
# glossary.drop()
# glossary=Glossary()
# glossary.load_from_excel('/Users/xuminghui/code/uv_project_install/streamlit_project/file/术语词库2024.9.27-术语分词.xlsx')

# print(glossary.count())
# print(glossary.detail('SY/T 5510-2021'))

# glossary=Glossary()
# glossary.update_by_standard_code('SY/T 5745-2008','SY/T 5289-2016')

    
# data=glossary.detail('SY/T 5289-2016')
# print(data)
#pageable=Pageable(1,10)
#page_result=standard_structure.detail(WhereCause('油气井管柱完整性管理'),pageable)
#print(page_result.data)

# for index, row in df.iterrows():
#     if index == 0:
#         print(row)



#遍历df的第一行的内容
# for index, row in df.iterrows():
#     #我需要遍历row的各个列
#     for i in range(row.size):
#         print(row[i])

# standard_db=StandardDB()
# standard_db.drop()
# standard_db=StandardDB()
# standard_db.load_from_excel('/Users/xuminghui/code/uv_project_install/streamlit_project/file/标准全文--体系范围标准-正文数据源-2025.6.21.xlsx')
# print(standard_db.count())

# from database.standard_index import StandardIndex
# standard_index=StandardIndex()
# standard_index.drop()
# standard_index=StandardIndex()
# standard_index.load_from_excel("/Users/xuminghui/code/uv_project_install/streamlit_project/file/00-全部标准索引库（体系相关）2025.3.25.xlsx")
# print(standard_index.detail('GB/T 150.1-2011'))

# standard_codes=['GB/T 150.1-2011','GB/T 229-2020']
# placeholders=','.join(['?']* len(standard_codes))
# print(placeholders)


# standard_index=StandardIndex()
# data=standard_index.list_by_standard_codes(standard_codes)
# print(data)

# standard_db=StandardDB()
# list=standard_db.list_for_tiaokuan()
# print(list)

# metric=Metric()
# metric.load_from_excel('/Users/xuminghui/code/uv_project_install/streamlit_project/file/13-104-材料技术指标汇总表2024.10.30.xlsx')
# print(metric.count())
# print(metric.list_by_search_term('外观'))

# standard_db=StandardDB()
# standard_db.drop()
# standard_db=StandardDB()
# standard_db.load_from_excel('/Users/xuminghui/code/uv_project_install/streamlit_project/file/标准全文--体系范围标准-正文数据源-2025.6.21.xlsx')

# standard_category_db=StandardCategory()
# standard_category_db.drop()
# standard_category_db=StandardCategory()
# standard_category_db.load_from_excel('/Users/xuminghui/code/uv_project_install/streamlit_project/file/01-储层改造领域标准目录（含引用标准）--韩20224.1.31--根据专家意见整理后(1).xlsx')
# data=standard_category_db.list_by_categroy('','')
# print(data)
# print(standard_category_db.count())

import base64

@st.cache_resource()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img =rf"""
    <style>
    body {{background-image: url('data:image/jpg;base64,{bin_str}');background-size: cover;}}
    </style>
    """
    print(page_bg_img)
    st.markdown(page_bg_img,unsafe_allow_html=False)
    st.markdown("<body class='test'>abcdef</body>", unsafe_allow_html=True)
    return

set_png_as_page_bg('images/1.jpg')

