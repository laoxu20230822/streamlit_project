import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from database import db
from database.customer import CustomerWhereCause

def handle_upload_file():
    uploaded_file=st.session_state.uploaded_file
    if uploaded_file is not None:
        try:
            # 读取Excel数据
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            db.batch_insert(df,conn)
            st.success('文件上传成功！')
            
            # 显示数据预览
            filter=CustomerWhereCause(
                st.session_state.name,
                st.session_state.address,
                st.session_state.phone);
            df=db.view_customers(conn,filter)
            print(df)
        except Exception as e:
            st.error(f"文件解析失败: {str(e)}")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#初始化数据库
conn=db.init_db()



name=st.sidebar.text_input('姓名',key='name')

address=st.sidebar.text_input('地址',key='address')

phone=st.sidebar.text_input('手机号',key='phone')

customer=CustomerWhereCause(name,address,phone)
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

customer_datas=db.view_customers(conn,customer)



st.dataframe(
    pd.DataFrame(customer_datas if customer_datas else [],columns=get_column_mapping()),
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
# latest_iteration = st.empty()


