import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from database import db
from database import customer
from database.customer import CustomerWhereCause
from database.page import Pageable

@st.cache_resource
def init_customer_db():
    return db.CustomerDB()

customer_db=init_customer_db()

page_size=10
def init_current_page():
    if 'current_page' not in st.session_state:
        st.session_state.current_page=1

def reset_current_page():

    st.session_state.current_page=1

def set_current_page():
    st.session_state.current_page=st.session_state.current_page_key

def prev_page():
    if st.session_state.current_page>1:
        st.session_state.current_page=st.session_state.current_page_key-1

def next_page():
    st.session_state.current_page=st.session_state.current_page_key+1

init_current_page()

def handle_upload_file():
    reset_current_page()
    uploaded_file=st.session_state.uploaded_file
    if uploaded_file is not None:
        try:
            # 读取Excel数据
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            # db.batch_insert(df,conn)
            customer_db.batch_insert(df)
            st.success('文件上传成功！')
        except Exception as e:
            st.error(f"文件解析失败: {str(e)}")




sys.path.append(os.path.dirname(os.path.abspath(__file__)))




name=st.sidebar.text_input('姓名',key='name')

address=st.sidebar.text_input('地址',key='address')

phone=st.sidebar.text_input('手机号',key='phone')

if name or address or phone:
    reset_current_page()

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

pageable=Pageable(st.session_state.current_page,page_size)
page_result=customer_db.view_customers(filter=filter,pageable=pageable)
df=pd.DataFrame(page_result.data if page_result.data else [],columns=get_column_mapping())
st.dataframe(
    df,
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
    st.button('prev',on_click=prev_page,key='prev_key')
with col4:
    st.number_input(
        'current_page',
        label_visibility='collapsed',
        value=st.session_state.current_page,
        key='current_page_key',
        on_change=set_current_page
        )
with col5:
    st.button('next',on_click=next_page,key='next_key')


"""
设置页面
"""
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

@st.fragment
def test():
    input=st.text_input('test')
    button=st.button('abc')
    print(f"{input},----- {button}")

test()






