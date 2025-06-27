import streamlit as st
import pandas as pd
from database.reference_standards import ReferenceStandards

def display_standard_references(standard_code:str):
    reference_standards=ReferenceStandards()
    data=reference_standards.detail(standard_code)
    df=pd.DataFrame(data,columns={
        'cited_standard_original': '引用文件标准号',
        'cited_standard_normalized': '引用文件标准号（规范后）',
        'standard_name_normalized': '引用文件标准名称（规范后）',
        'status': '状态'
        })
    #st.subheader('引用列表')
    event=st.dataframe(
    df,
    hide_index=True,  # 隐藏默认索引列
    use_container_width=True,
    column_config={
        "cited_standard_original": st.column_config.TextColumn(
            "引用文件标准号",
            help="引用文件标准号"
        ),
        "cited_standard_normalized": st.column_config.TextColumn(
            "引用文件标准号（规范后）",
            help="引用文件标准号（规范后）"
        ),
        "standard_name_normalized": st.column_config.TextColumn(
            "引用文件标准名称（规范后）",
            help="引用文件标准名称（规范后）"
        ),
        "status": st.column_config.TextColumn(
            "状态",
            help="状态"
        ),
        
    }, 
    #on_select='rerun',
    #selection_mode='single-row',
    #key='selected_row',
    )