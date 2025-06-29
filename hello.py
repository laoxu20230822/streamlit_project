
from altair import Data
import streamlit as st
import pandas as pd
import os
import sys

from streamlit.elements.lib.layout_utils import Height
from database.glossary import Glossary
from database.standard_db import init_standard_db
from database.standard_db import WhereCause
from database.page import Pageable
from database.standard_index import StandardIndex
from database.standard_structure import StandardStructure
from st_aggrid import AgGrid, GridOptionsBuilder

from view.display_standard_glossary import display_standard_glossary
from view.display_standard_references import display_standard_references
from view.display_standard_detail import display_standard_detail
from view.display_standard_query_list import display_standard_query_list
from view.display_product_standard import display_product_standard
from view.display_craft_standard import display_craft_standard
from view.display_standard_structure import display_standard_structure
from view.display_tiaokuan_query_list import display_tiaokuan_query_list
from view.display_glossary_query_list import display_glossary_query_list
from view.display_metric_query_list import display_metric_query_list

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if 'search_term' not in st.session_state:
    st.session_state.search_term=''

    

#标题
with st.container():
    st.markdown("<h1 style='text-align: center; color: blue;'>储层改造标准知识服务</h1>", unsafe_allow_html=True)
    st.markdown("---")

#查询表单
with st.form('standard_search_form'):
    def button_submit(**kwargs:dict):
        submit_type=kwargs['submit_type']
        st.session_state.submit_type=submit_type
        st.session_state.search_term=st.session_state.standard_term
        if 'selected_rows' in st.session_state:
            del st.session_state['selected_rows']

    col1,col2,col3=st.columns([0.4,0.2,0.2])
    #col.markdown('<div> 输入标准名称</div>',unsafe_allow_html=True)
    search_term=col1.text_input('标准名称',key='standard_term',label_visibility='collapsed',placeholder='查询输入',width='stretch',value='')
    standard_submit=col2.form_submit_button('标准查询',use_container_width=True,kwargs={'submit_type':'standard'},on_click=button_submit)
    tiaokuan_submit=col3.form_submit_button('条款查询',use_container_width=True,kwargs={'submit_type':'tiaokuan'},on_click=button_submit)

    button1,button2,button3,button4=st.columns([0.2,0.2,0.2,0.2])

    button1.form_submit_button('标准体系',use_container_width=True,kwargs={'submit_type':'tixi'},on_click=button_submit,disabled=True)
    button2.form_submit_button('术语',use_container_width=True,kwargs={'submit_type':'shuyu'},on_click=button_submit)
    button3.form_submit_button('指标',use_container_width=True,kwargs={'submit_type':'zhibiao'},on_click=button_submit)
    button4.form_submit_button('参数',use_container_width=True,kwargs={'submit_type':'canshu'},on_click=button_submit,disabled=True)


    
def display_standard_info(standard_code,standard_name):
    col1,col2 = st.columns(2)
    col1.write(f"""标准号：{standard_code}""",unsafe_allow_html=True)
    col2.write(f"""标准名称：{standard_name}""")
    # st.markdown(f"""
    # >:blue[{standard_code}]\n
    # >#### {standard_name}
    # """)

#列表展示
placeholder=st.empty()
with placeholder.container(border=True):
    #根据查询内容显示不同的列表

    if 'submit_type' in st.session_state:
        submit_type=st.session_state.submit_type
        if submit_type == 'standard':
            display_standard_query_list()
        elif submit_type == 'tiaokuan':
            display_tiaokuan_query_list(st.session_state.search_term)
            print('TODO')
        elif submit_type == 'tixi':
            #display_tixi_query_list()
            print('TODO')
        elif submit_type == 'shuyu':
            display_glossary_query_list(st.session_state.search_term)
        elif submit_type == 'zhibiao':
            display_metric_query_list(st.session_state.search_term)
            print('TODO')
        elif submit_type == 'canshu':
            #display_canshu_query_list()
            print('TODO')
        else:
            print('')


    if 'selected_rows' in st.session_state:
        standard_code=st.session_state['selected_rows'][0]['standard_code']
        standard_name=st.session_state['selected_rows'][0]['standard_name']
        #查询一级门类编号
        standard_db=init_standard_db()
        level1_code_data=standard_db.query_category_level1_code(standard_code)
        if level1_code_data is not None and level1_code_data[0] == '104':
            level1_code=level1_code_data[0]
            product_or_craft_tab_name='产品标准'
            st.session_state.pc_type='product'
        elif level1_code_data is not None and level1_code_data[0] in ['103','106','107']:
            product_or_craft_tab_name='工业标准'
            st.session_state.pc_type='craft'
        else:
            st.session_state.pc_type='other'
        t1,t2,t3,t4,t5=st.tabs(['**基本信息**','**标准目次信息**','**引用文件信息**','**术语**','**'+product_or_craft_tab_name+'**'])
        #standard_code = df.iloc[selected_row]['standard_code']

        
        
        ## 显示标准详情
        with t1:
            display_standard_info(standard_code,standard_name)
            display_standard_detail(standard_code)
        
        # 显示目次信息
        with t2:
            display_standard_info(standard_code,standard_name)
            display_standard_structure(standard_code)
        #st.markdown("---")

        #引用文件
        with t3:
            display_standard_info(standard_code,standard_name)
            display_standard_references(standard_code)

        # 术语信息
        with t4:
            display_standard_info(standard_code,standard_name)
            display_standard_glossary(standard_code)

        # 工艺标准 or 产品标准
        with t5:
            display_standard_info(standard_code,standard_name)
            if st.session_state.pc_type == 'product':
                display_product_standard(standard_code)
            elif st.session_state.pc_type == 'craft':
                display_craft_standard(standard_code)
            else:
                st.write("other")
        


