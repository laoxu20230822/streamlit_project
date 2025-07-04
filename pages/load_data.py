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

with st.container(border=True):

    def handle_upload_file_00():
        uploaded_file=st.session_state.uploaded_file_00
        if uploaded_file is not None:
            try:
                # 读取Excel数据
                df = pd.read_excel(uploaded_file, engine='openpyxl').fillna('')
                db=init_standard_index_db()
                db.drop()
                db.create_table()
                db.load_from_excel(uploaded_file)
                st.success('文件上传成功！')
            except Exception as e:
                st.error(f"文件解析失败: {str(e)}")

    st.file_uploader(
        "00-全部标准索引库（体系相关）",
        type=['xlsx'],
        help="支持.xlsx格式文件",
        key='uploaded_file_00',
        on_change=handle_upload_file_00
    )

with st.container(border=True):
    # 01-储层改造领域标准目录
    def handle_upload_file_01():
        uploaded_file=st.session_state.uploaded_file_standard_01
        if uploaded_file is not None:
            try:
                # 读取Excel数据
                df = pd.read_excel(uploaded_file, engine='openpyxl').fillna('')
                db=init_standard_category_db()
                db.drop()
                db.create_table()
                db.load_from_excel(uploaded_file)
                st.success('文件上传成功！')
            except Exception as e:
                st.error(f"文件解析失败: {str(e)}")
    # 术语词库2024.9.27-术语分词
    st.file_uploader(
        "01-储层改造领域标准目录",
        type=['xlsx'],
        help="支持.xlsx格式文件",
        key='uploaded_file_standard_01',
        on_change=handle_upload_file_01
    ) 

with st.container(border=True):
    def handle_upload_file_02():
        uploaded_file=st.session_state.uploaded_file_02
        if uploaded_file is not None:
            try:
                # 读取Excel数据
                df = pd.read_excel(uploaded_file, engine='openpyxl').fillna('')
                db=init_standard_db()
                db.drop()
                db.create_table()
                db.load_from_excel(uploaded_file)
                st.success('文件上传成功！')
            except Exception as e:
                st.error(f"文件解析失败: {str(e)}")
    st.file_uploader(
            "02-标准全文--体系范围标准-正文数据源",
            type=['xlsx'],
            help="支持.xlsx格式文件",
            key='uploaded_file_02',
            on_change=handle_upload_file_02
        )

with st.container(border=True):
    # 05-规范性引用文件
    def handle_upload_file_05():
        uploaded_file=st.session_state.uploaded_file_standard_05
        if uploaded_file is not None:
            try:
                # 读取Excel数据
                df = pd.read_excel(uploaded_file, engine='openpyxl').fillna('')
                db=init_reference_standards_db()
                db.drop()
                db.create_table()
                db.load_from_excel(uploaded_file)
                st.success('文件上传成功！')
            except Exception as e:
                st.error(f"文件解析失败: {str(e)}")
    # 术语词库2024.9.27-术语分词
    st.file_uploader(
        "05-规范性引用文件",
        type=['xlsx'],
        help="支持.xlsx格式文件",
        key='uploaded_file_standard_05',
        on_change=handle_upload_file_05
    )  

with st.container(border=True):
    def handle_upload_file_term():
        uploaded_file=st.session_state.uploaded_file_standard_term
        if uploaded_file is not None:
            try:
                # 读取Excel数据
                df = pd.read_excel(uploaded_file, engine='openpyxl').fillna('')
                db=init_glossary_db()
                db.drop()
                db.create_table()
                db.load_from_excel(uploaded_file)
                st.success('文件上传成功！')
            except Exception as e:
                st.error(f"文件解析失败: {str(e)}")
    # 术语词库2024.9.27-术语分词
    st.file_uploader(
        "06术语词库2024.9.27-术语分词",
        type=['xlsx'],
        help="支持.xlsx格式文件",
        key='uploaded_file_standard_term',
        on_change=handle_upload_file_term
    )

#13指标13-104-材料技术指标汇总表
with st.container(border=True):
    def handle_upload_file_13():
        uploaded_file=st.session_state.uploaded_file_standard_13
        if uploaded_file is not None:
            try:
                # 读取Excel数据
                df = pd.read_excel(uploaded_file, engine='openpyxl').fillna('')
                db=init_metric_db()
                db.drop()
                db.create_table()
                db.load_from_excel(uploaded_file)
                st.success('文件上传成功！')
            except Exception as e:
                st.error(f"文件解析失败: {str(e)}")
    # 术语词库2024.9.27-术语分词
    st.file_uploader(
        "13-104-材料技术指标汇总表",
        type=['xlsx'],
        help="支持.xlsx格式文件",
        key='uploaded_file_standard_13',
        on_change=handle_upload_file_13
    )


with st.container(border=True):
    def handle_upload_file_structure():
        uploaded_file=st.session_state.uploaded_file_standard_structure
        if uploaded_file is not None:
            try:
                # 读取Excel数据
                df = pd.read_excel(uploaded_file, engine='openpyxl').fillna('')
                db=init_standard_structure_db()
                db.drop()
                db.create_table()
                db.load_from_excel(uploaded_file)
                st.success('文件上传成功！')
            except Exception as e:
                st.error(f"文件解析失败: {str(e)}")
    # 最终目次页（17-18-19-20-24合）
    st.file_uploader(
        "最终目次页（17-18-19-20-24合）",
        type=['xlsx'],
        help="支持.xlsx格式文件",
        key='uploaded_file_standard_structure',
        on_change=handle_upload_file_structure
    )
