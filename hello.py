
from altair import Data
import streamlit as st
import pandas as pd
import os
import sys

from streamlit.elements.lib.layout_utils import Height
from database.glossary import Glossary
from database.reference_standards import ReferenceStandards
from database.standard_db import StandardDB
from database.standard_db import WhereCause
from database.page import Pageable
from database.standard_index import StandardIndex
from database.standard_structure import StandardStructure
from st_aggrid import AgGrid, GridOptionsBuilder

sys.path.append(os.path.dirname(os.path.abspath(__file__)))



@st.cache_resource
def init_standard_db():
    return StandardDB()
    

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




page_size=20
# def init_current_page():
#     if 'current_page' not in st.session_state:
#         st.session_state.current_page=1

# def reset_current_page():
#     print('reset current page')
#     st.session_state.current_page=1

# def set_current_page():
#     st.session_state.current_page=st.session_state.current_page_key

# def prev_page():
#     if st.session_state.current_page>1:
#         st.session_state.current_page=st.session_state.current_page_key-1

# def next_page():
#     st.session_state.current_page=st.session_state.current_page_key+1

#init_current_page()

st.markdown("<h1 style='text-align: center; color: blue;'>储层改造标准知识服务</h1>", unsafe_allow_html=True)

st.markdown("---")

with st.form('standard_search_form'):
    col1,col2,col3=st.columns([0.4,0.2,0.2])
    #col.markdown('<div> 输入标准名称</div>',unsafe_allow_html=True)
    search_term=col1.text_input('标准名称',key='standard_name',label_visibility='collapsed',placeholder='查询输入',width='stretch')
    submit=col2.form_submit_button('标准查询',use_container_width=True)
    reset=col3.form_submit_button('条款查询',use_container_width=True,disabled=True)

    button1,button2,button3,button4=st.columns([0.2,0.2,0.2,0.2])
    button1.form_submit_button('标准体系',use_container_width=True,disabled=True)
    button2.form_submit_button('术语',use_container_width=True,disabled=True)
    button3.form_submit_button('指标',use_container_width=True,disabled=True)
    button4.form_submit_button('参数',use_container_width=True,disabled=True)








#获取standard 列表数据
#查询standard大表数据
standard_db=init_standard_db()
page_result=standard_db.list(filter=WhereCause(search_term),pageable=Pageable(1,page_size))
standard_codes=[row['standard_code'] for row in page_result.data]
#查询索引表
standard_index=StandardIndex()
data=standard_index.list_by_standard_codes(standard_codes)
df=pd.DataFrame(data if data else [],columns={
        # 'system_serial': '体系编号',
        # 'flow_number': '流水号',
        # 'serial': '序号',
        'standard_code': '标准号',
        'standard_name': '标准名称',
        'status': '状态',
        'specialty':'专业',
        'release_date': '发布日期',
        'implementation_date': '实施日期',
    })




grid_options = {
    'columnDefs': [
    { 'field': "standard_code", 'headerName': "标准号"},
    { 'field': "standard_name", 'headerName': "标准名称"},
    { 'field': "status", 'headerName': "状态"},
    { 'field': "specialty", 'headerName': "专业"},
    { 'field': "release_date", 'headerName': "发布日期"},
    { 'field': "implementation_date", 'headerName': "实施日期"},
  ],
  'rowSelection': {
        'mode': 'singleRow',
        'checkboxes': False,
        'enableClickSelection': True
    },
    "autoSizeStrategy": {
        "type": "fitGridWidth"
    }
}
grid_response = AgGrid(
    df, 
    gridOptions=grid_options,
    #key='asdjflasdjkfl'
    )

selected_rows = grid_response['selected_rows']


placeholder=st.empty()

def display_standard_info(standard_code,standard_name):
    st.markdown(f"""
    >:blue[{standard_code}]\n
    >#### {standard_name}
    """)
with placeholder.container():
    if selected_rows is not  None:
        standard_code=''
        standard_name=''
        for index, row in selected_rows.iterrows():
            standard_code=row['standard_code']
            standard_name=row['standard_name']
        t1,t2,t3,t4,t5,t6=st.tabs(['基本信息','标准目次信息','引用文件信息','术语','产品标准','工业标准'])
        #standard_code = df.iloc[selected_row]['standard_code']

        ## 显示详情
        with t1:
            display_standard_info(standard_code,standard_name)
            standard_index=StandardIndex()
            detail=standard_index.detail(standard_code)
            st.markdown("##### 基本信息\n\n---")
            st.markdown("**标准英文名称：**")
            st.write(detail['english_name'])
            st.markdown("---")
            col1,col2=st.columns(2)
            with col1:
                col1.markdown("**标准分类：**")
                col1.write(detail['standard_type'])
                col1.markdown("---")
                col1.markdown("**专业：**")
                col1.write(detail['specialty'])
                col1.markdown("---")           
                col1.markdown("**ICS分类号：**")
                col1.write(detail['ics_classification'])
                col1.markdown("---")
                col1.markdown("**发布日期：**")
                col1.write(detail['release_date'])
                col1.markdown("---")
                
            with col2:
                col2.markdown("**标准状态：**")
                col2.write(detail['status'])
                col2.markdown("---")           
                col2.markdown("**标准性质：**")
                col2.write(detail['standard_nature'])     
                col2.markdown("---")           
                col2.markdown("**CCS分类号：**")
                col2.write(detail['ccs_classification'])
                col2.markdown("---")
                col2.markdown("**实施日期：**")
                col2.write(detail['implementation_date'])
                col2.markdown("---")
            st.markdown("##### 起草单位及其他")
            st.markdown("**起草单位：**")
            st.write(detail['drafting_unit'])
            st.markdown("---")
            st.markdown("**技术委员会（或技术归口单位）：**")
            st.write(detail['responsible_unit'])
            st.markdown("---")
        #with st.expander("标准目次信息"):
        with t2:
            display_standard_info(standard_code,standard_name)
            standard_structure=StandardStructure()
            detail_for_markdown=standard_structure.detail_to_markdown(standard_code)
            #st.subheader('标准目次信息')
            st.markdown(detail_for_markdown)
        #st.markdown("---")

        #with st.expander("查看引用文件信息"):
        with t3:
            display_standard_info(standard_code,standard_name)
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

        #st.markdown("---",)
        #with st.expander("查看术语信息"):
        with t4:
            display_standard_info(standard_code,standard_name)
            glossary=Glossary()
            data=glossary.detail(standard_code)

            df=pd.DataFrame(data,columns={
                'entry_code': '术语条目编号',
                'term': '术语词条',
                'english_term': '术语英文',
                'definition': '术语定义',
                })
            event=st.dataframe(df,
            hide_index=True,  # 隐藏默认索引列
            use_container_width=True,
            column_config={
               
                "term": st.column_config.TextColumn(
                    "术语词条",
                    help="术语词条"
                ),
                "english_term": st.column_config.TextColumn(
                    "术语英文",
                    help="术语英文"
                ),
               
                "definition": st.column_config.TextColumn(
                    "术语定义",
                    help="术语定义"
                ),
                "entry_code": st.column_config.TextColumn(
                    "术语条目编号",
                    help="术语条目编号"
                ),
               
                }
            )
        #st.markdown("---")
        #with st.expander("查看产品标准"):
        with t5:
            display_standard_info(standard_code,standard_name)
            st.write('TODO')
        #st.markdown("---")
        #with st.expander("查看工艺标准"):
        with t6:
            display_standard_info(standard_code,standard_name)
            st.write('TODO')
        #st.markdown("---")


