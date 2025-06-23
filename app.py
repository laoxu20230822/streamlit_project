from base64 import standard_b64decode
import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from database.standard_db import StandardDB
from database.standard_db import WhereCause
from database.customer import CustomerWhereCause
from database.page import Pageable

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@st.cache_resource
def init_customer_db():
    return StandardDB()

customer_db=init_customer_db()

page_size=50
def init_current_page():
    if 'current_page' not in st.session_state:
        st.session_state.current_page=1

def reset_current_page():
    print('reset current page')
    st.session_state.current_page=1

def set_current_page():
    st.session_state.current_page=st.session_state.current_page_key

def prev_page():
    if st.session_state.current_page>1:
        st.session_state.current_page=st.session_state.current_page_key-1

def next_page():
    st.session_state.current_page=st.session_state.current_page_key+1

init_current_page()

def get_column_mapping():
    return {
        'id': 'ID',
        'system_serial': '体系编号',
        'flow_number': '流水号',
        'serial': '序号',
        'standard_code': '标准号',
        'standard_name': '标准名称',
        'content_full': '标准全文'
    }


standard_name=st.sidebar.text_input('标准名称',key='standard_name',on_change=reset_current_page)
filter=WhereCause(standard_name)
pageable=Pageable(st.session_state.current_page,page_size)
page_result=customer_db.view_standards(filter=filter,pageable=pageable)
df=pd.DataFrame(page_result.data if page_result.data else [],columns=get_column_mapping())
event=st.dataframe(
    df,
    hide_index=True,  # 隐藏默认索引列
    use_container_width=True,
        column_config={
        "id": st.column_config.TextColumn(
            "ID",
             help="体系唯一标识符",
        ),
        "system_serial": st.column_config.TextColumn(
            "体系编号",
            help="标准体系序列号"
        ),
        "flow_number": st.column_config.TextColumn(
            "流水号",
            help="唯一流水编号"
        ),
        "serial": st.column_config.TextColumn(
            "序号",
            help="标准排序序号"
        ),
        "standard_code": st.column_config.LinkColumn(
            "标准号",
            help="国家标准编号"
        ),
        "standard_name": st.column_config.TextColumn(
            "标准名称",
            help="标准完整名称"
        ),
        "content_full": st.column_config.TextColumn(
            "标准全文",
            help="标准完整文本内容"
        ),
    }, 
    on_select='rerun',
    selection_mode='single-row',
    #key='selected_row',
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]
    standard_code = df.iloc[selected_row]['standard_code']

    st.session_state['standard_code'] = {'standard_code': standard_code}
    #https://docs.streamlit.io/develop/api-reference/widgets/st.page_link
    st.page_link('pages/page_1.py', label=f'Goto {standard_code} Page', icon='🗺️')


#standard_index = event.selection.rows

#standard_detail=df.iloc[standard_index]
#print(standard_detail['standard_code'])
#print(standard_detail['standard_name'])
#print(standard_detail['content_full'])



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






