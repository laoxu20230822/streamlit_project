import streamlit as st
import pandas as pd
from database.standard_db import init_standard_db
from database.standard_index import init_standard_index_db
from database.standard_structure import init_standard_structure_db
from database.glossary import init_glossary_db
from database.metric import init_metric_db
from database.reference_standards import init_reference_standards_db
from database.standard_category import init_standard_category_db
st.set_page_config(
    layout='wide'
)
@st.fragment
def fragment_00():
    container_00=st.container(border=True)
    with container_00:
        file=st.file_uploader(
            "00-全部标准索引库（体系相关）",
            type=['xlsx'],
            help="支持.xlsx格式文件",
            key='uploaded_file_00',
        )
        if file is not None:
            try:
                # 读取Excel数据
                db=init_standard_index_db()
                db.drop()
                db.create_table()
                db.load_from_excel(file)
                container_00.success('文件上传成功！')
            except Exception as e:
                container_00.error(f"文件解析失败: {str(e)}")
            

        

@st.fragment()
def fragment_01():
    container_01=st.container(border=True)
    with container_01:
        # 术语词库2024.9.27-术语分词
        file=st.file_uploader(
            "01-储层改造领域标准目录",
            type=['xlsx'],
            help="支持.xlsx格式文件",
            key='uploaded_file_standard_01',
        ) 
        if file is not None:
            try:
                # 读取Excel数据
                db=init_standard_category_db()
                db.drop()
                db.create_table()
                db.load_from_excel(file)
                container_01.success('文件上传成功！')
            except Exception as e:
                container_01.error(f"文件解析失败: {str(e)}")


@st.fragment
def fragment_02():
    container_02=st.container(border=True)
    with container_02:
        file=st.file_uploader(
                "02-标准全文--体系范围标准-正文数据源",
                type=['xlsx'],
                help="支持.xlsx格式文件",
                key='uploaded_file_02',
            )
        if file is not None:
            try:
                # 读取Excel数据
                db=init_standard_db()
                db.drop()
                db.create_table()
                db.load_from_excel(file)
                container_02.success('文件上传成功！')
            except Exception as e:
                container_02.error(f"文件解析失败: {str(e)}")
        



@st.fragment
def fragment_05():
    container_05=st.container(border=True)
    with container_05:
         # 术语词库2024.9.27-术语分词
        file=st.file_uploader(
            "05-规范性引用文件",
            type=['xlsx'],
            help="支持.xlsx格式文件",
            key='uploaded_file_standard_05',
        )  
        # 05-规范性引用文件
        if file is not None:
            try:
                # 读取Excel数据
                db=init_reference_standards_db()
                db.drop()
                db.create_table()
                db.load_from_excel(file)
                container_05.success('文件上传成功！')
            except Exception as e:
                container_05.error(f"文件解析失败: {str(e)}")
    

@st.fragment
def fragment_06():
    container_06=st.container(border=True)
    with container_06:
        # 术语词库2024.9.27-术语分词
        file=st.file_uploader(
            "06术语词库2024.9.27-术语分词",
            type=['xlsx'],
            help="支持.xlsx格式文件",
            key='uploaded_file_standard_term',
        )
        if file is not None:
            try:
                # 读取Excel数据
                db=init_glossary_db()
                db.drop()
                db.create_table()
                db.load_from_excel(file)
                container_06.success('文件上传成功！')
            except Exception as e:
                container_06.error(f"文件解析失败: {str(e)}")
        

@st.fragment
def fragment_13():
    #13指标13-104-材料技术指标汇总表
    container_13=st.container(border=True)
    with container_13:
        # 术语词库2024.9.27-术语分词
        file=st.file_uploader(
            "13-104-材料技术指标汇总表",
            type=['xlsx'],
            help="支持.xlsx格式文件",
            key='uploaded_file_standard_13',
        )
        if file is not None:
            try:
                # 读取Excel数据
                db=init_metric_db()
                db.drop()
                db.create_table()
                db.load_from_excel(file)
                container_13.success('文件上传成功！')
            except Exception as e:
                container_13.error(f"文件解析失败: {str(e)}")
        


@st.fragment
def fragment_structure():
    container_structure=st.container(border=True)
    with container_structure:
        # 最终目次页（17-18-19-20-24合）
        file=st.file_uploader(
            "最终目次页（17-18-19-20-24合）",
            type=['xlsx'],
            help="支持.xlsx格式文件",
            key='uploaded_file_standard_structure',
        )
        if file is not None:
            try:
                # 读取Excel数据
                db=init_standard_structure_db()
                db.drop()
                db.create_table()
                db.load_from_excel(file)
                container_structure.success('文件上传成功！')
            except Exception as e:
                container_structure.error(f"文件解析失败: {str(e)}")
        

fragment_00()
fragment_01()
fragment_02()
fragment_05()
fragment_06()
fragment_13()
fragment_structure()
