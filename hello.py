
import streamlit as st
import pandas as pd
import os
import sys
from database.standard_db import StandardDB
from database.standard_db import WhereCause
from database.page import Pageable
from database.standard_structure import StandardStructure

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# 定义标准卡片组件
def display_standard_card(standard):
    # 创建卡片容器
    with st.container():
        col1, col2 = st.columns([1, 10])
        # 左侧图标（模拟网页中的图标）
        with col1:
            st.markdown("⏳")
        # 右侧内容
        with col2:
            # 标准编号和名称
            st.subheader(f"{standard['standard_name']}")
            
            # 信息列表
            info_cols = st.columns(3)
            with info_cols[0]:
                st.markdown(f"**体系序号：** {standard['system_serial']}")
                #st.markdown(f"**流水号：** {standard['flow_number']}")
            with info_cols[1]:
                st.markdown(f"**标准号：** {standard['standard_code']}")
            with info_cols[2]:
                st.link_button('详情',url=f'/detail?standard_code={standard['standard_code']}')
            st.markdown("---")

@st.cache_resource
def init_customer_db():
    return StandardDB()

customer_db=init_customer_db()

page_size=20
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
        'system_serial': '体系编号',
        'flow_number': '流水号',
        'serial': '序号',
        'standard_code': '标准号',
        'standard_name': '标准名称'
    }

with st.form('standard_search_form'):
    col1,col2=st.columns([0.8,0.2])
    standard_name=col1.text_input('标准名称',key='standard_name',label_visibility='collapsed')
    submit=col2.form_submit_button('查询',on_click=set_current_page)


filter=WhereCause(standard_name)
pageable=Pageable(st.session_state.current_page,page_size)
page_result=customer_db.list(filter=filter,pageable=pageable)
df=pd.DataFrame(page_result.data if page_result.data else [],columns=get_column_mapping())

# for row in page_result.data:
#     display_standard_card(row)

event=st.dataframe(
    df,
    hide_index=True,  # 隐藏默认索引列
    use_container_width=True,
        column_config={
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
        "standard_code": st.column_config.TextColumn(
            "标准号",
            help="国家标准编号"
        ),
        "standard_name": st.column_config.TextColumn(
            "标准名称",
            help="标准完整名称"
        ),
    }, 
    on_select='rerun',
    selection_mode='single-row',
    #key='selected_row',
)




#standard_index = event.selection.rows

#standard_detail=df.iloc[standard_index]
#print(standard_detail['standard_code'])
#print(standard_detail['standard_name'])
#print(standard_detail['content_full'])



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

placeholder=st.empty()

with placeholder.container():
    if len(event.selection['rows']):
        selected_row = event.selection['rows'][0]
        standard_code = df.iloc[selected_row]['standard_code']

        standard_db=StandardDB()
        standard_structure=StandardStructure()
        detail=standard_db.standard_detail(standard_code)
        detail_for_markdown=standard_structure.detail_to_markdown(standard_code)
        ## 显示详情
        with st.container(height=200):
            st.subheader("标准基本信息")
            st.markdown(f"""
            :blue[{detail[0]['standard_code']}]
            """)
            st.markdown(f"#### {detail[0]['standard_name']}")

        with st.container(height=200):
            st.subheader('标准目次信息')
            
            st.markdown(detail_for_markdown)
        st.markdown("---")
        with st.container(height=200):
            st.subheader('引用列表')
            

        st.markdown("---",)
        with st.container(height=200):
            st.subheader('术语')
            st.write('hello world 2')
        st.markdown("---")
        with st.container(height=200):
            st.subheader('产品标准')
            st.write('hello world 2')
        st.markdown("---")
        with st.container(height=200):
            st.subheader('工艺标准')
            st.write('hello world 2')
        st.markdown("---")


