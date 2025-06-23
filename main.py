import streamlit as st
import pandas as pd
from database.glossary import Glossary
from database.page import Pageable
import database.sql as sql
from database.standard_db import StandardDB
from database.standard_db import WhereCause
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

reference_standards=ReferenceStandards()
reference_standards.drop()
reference_standards=ReferenceStandards()
reference_standards.load_from_excel('/Users/xuminghui/code/uv_project_install/streamlit_project/file/05-规范性引用文件2.xlsx')
print(reference_standards.count())
detail=reference_standards.detail('GB/T 2091-2008')
print(detail)


    
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