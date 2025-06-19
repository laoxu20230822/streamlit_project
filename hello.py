import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from database import db
from database.customer import CustomerWhereCause
from database.page import Pageable


def handle_upload_file():
    uploaded_file=st.session_state.uploaded_file
    if uploaded_file is not None:
        try:
            # 读取Excel数据
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            db.batch_insert(df,conn)
            st.success('文件上传成功！')
        except Exception as e:
            st.error(f"文件解析失败: {str(e)}")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#初始化数据库
conn=db.init_db()



name=st.sidebar.text_input('姓名',key='name')

address=st.sidebar.text_input('地址',key='address')

phone=st.sidebar.text_input('手机号',key='phone')

filter=CustomerWhereCause(name,address,phone)
uploaded_file = st.sidebar.file_uploader(
        "导入数据",
        type=['xlsx'],
        help="支持.xlsx格式文件",
        key='uploaded_file',
        on_change=handle_upload_file
    )
def get_column_mapping():
    return {
        'id': 'ID',
        'name': '姓名',
        'address': '地址',
        'phone': '电话'
    }

page_result=db.view_customers(conn=conn,filter=filter,pageable=Pageable(1,10))
st.dataframe(
    pd.DataFrame(page_result.data if page_result.data else [],columns=get_column_mapping()),
    hide_index=True,  # 隐藏默认索引列
    use_container_width=True,
    column_config={
        "id": st.column_config.TextColumn(
            "ID",
             help="Streamlit **widget** commands 🎈",
            # default="st.",
            # max_chars=50,
            # validate=r"^st\.[a-z_]+$",
        ),
        "name": st.column_config.TextColumn(
            "姓名",
        ),
        "address": st.column_config.TextColumn(
            "地址",
        ),
        "phone": st.column_config.TextColumn(
            "手机号",
        )
    },  # 表格宽度自适应容器
)
# # Add a placeholder
st.empty()
col1, col2,col3,col4,col5 = st.columns([0.6,0.1,0.1,0.1,0.1])  # 调整列宽比例
with col2:
    st.write(f'共{page_result.total}页')
with col3:
    st.button('prev')
with col4:
    st.number_input('current_page',label_visibility='collapsed',min_value=1,max_value=10)
with col5:
    st.button('next')




