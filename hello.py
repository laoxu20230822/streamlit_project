
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
from database.standard_structure import StandardStructure

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



customer_db=init_standard_db()

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



with st.form('standard_search_form'):
    col,col1,col2=st.columns([0.2,0.6,0.2])
    col.markdown('<div> 输入标准名称：</div>',unsafe_allow_html=True)
    standard_name=col1.text_input('标准名称',key='standard_name',label_visibility='collapsed',)
    submit=col2.form_submit_button('查询',on_click=set_current_page)


#获取standard 列表数据
page_result=customer_db.list(filter=WhereCause(standard_name),pageable=Pageable(st.session_state.current_page,page_size))
df=pd.DataFrame(page_result.data if page_result.data else [],columns={
        'system_serial': '体系编号',
        'flow_number': '流水号',
        'serial': '序号',
        'standard_code': '标准号',
        'standard_name': '标准名称'
    })



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

#分页处理
col1, col2,col3,col4,col5 = st.columns([0.55,0.1,0.1,0.1,0.1])  # 调整列宽比例
with col2:
    st.write(f'共{page_result.total}页')
with col3:
    st.button('上页',on_click=prev_page,key='prev_key')
with col4:
    st.number_input(
        'current_page',
        label_visibility='collapsed',
        value=st.session_state.current_page,
        key='current_page_key',
        on_change=set_current_page
        )
with col5:
    st.button('下页',on_click=next_page,key='next_key')

placeholder=st.empty()

with placeholder.container():
    if len(event.selection['rows']):
        selected_row = event.selection['rows'][0]
        standard_code = df.iloc[selected_row]['standard_code']

        ## 显示详情
        with st.container(height=200):
            standard_db=StandardDB()
            detail=standard_db.standard_detail(standard_code)
            st.subheader("标准基本信息")
            st.markdown(f""":blue[{detail[0]['standard_code']}]""")
            st.markdown(f"#### {detail[0]['standard_name']}")

        st.markdown("---",)
        with st.expander("标准目次信息"):
            standard_structure=StandardStructure()
            detail_for_markdown=standard_structure.detail_to_markdown(standard_code)
            #st.subheader('标准目次信息')
            st.markdown(detail_for_markdown)
        st.markdown("---")

        with st.expander("查看引用文件信息"):
            reference_standards=ReferenceStandards()
            data=reference_standards.detail(standard_code)
            df=pd.DataFrame(data,columns={
                'standard_code': '标准号',
                'cited_standard_original': '引用文件标准号',
                'citation_type': '引用文件类型',
                'has_edition_year': '是否带年代号引用',
                'cited_standard_normalized': '引用文件标准号（规范后）',
                'standard_name_normalized': '引用文件标准名称（规范后）',
                'standard_code_prefix': '标准代号',
                'serial_number': '标准序列号',
                'edition_year': '标准年代号',
                'statistical_code': '标准代号（统计用）',
                'serial_number1': '标准序列号1',
                'serial_number2': '标准序列号2',
                'org_classification_code': '标准组织分类编号',
                'standard_category': '标准类别',
                'is_referenced': '是否引用文件'
                })
            #st.subheader('引用列表')
            event=st.dataframe(
            df,
            hide_index=True,  # 隐藏默认索引列
            use_container_width=True,
            column_config={
                "standard_code": st.column_config.TextColumn(
                    "标准号",
                    help="国家标准编号"
                ),
                "cited_standard_original": st.column_config.TextColumn(
                    "引用文件标准号",
                    help="引用文件标准号"
                ),
                "citation_type": st.column_config.TextColumn(
                    "引用文件类型",
                    help="引用文件类型"
                ),
                "has_edition_year": st.column_config.TextColumn(
                    "是否带年代号引用",
                    help="是否带年代号引用"
                ),
                "cited_standard_normalized": st.column_config.TextColumn(
                    "引用文件标准号（规范后）",
                    help="引用文件标准号（规范后）"
                ),
                "standard_name_normalized": st.column_config.TextColumn(
                    "引用文件标准名称（规范后）",
                    help="引用文件标准名称（规范后）"
                ),
                "standard_code_prefix": st.column_config.TextColumn(
                    "标准代号",
                    help="标准代号"
                ),
                "serial_number": st.column_config.TextColumn(
                    "标准序列号",
                    help="标准序列号"
                ),
                "edition_year": st.column_config.TextColumn(
                    "标准年代号",
                    help="标准年代号"
                ),
                "statistical_code": st.column_config.TextColumn(
                    "标准代号（统计用）",
                    help="标准代号（统计用）"
                ),
                "serial_number1": st.column_config.TextColumn(
                    "标准序列号1",
                    help="标准序列号1"
                ),
                "serial_number2": st.column_config.TextColumn(
                    "标准序列号2",
                    help="标准序列号2"
                ),
                "org_classification_code": st.column_config.TextColumn(
                    "标准组织分类编号",
                    help="标准组织分类编号"
                ),
                "standard_category": st.column_config.TextColumn(
                    "标准类别",
                    help="标准类别"
                ),
                "is_referenced": st.column_config.TextColumn(
                    "是否引用文件",
                    help="是否引用文件"
                ),
                
            }, 
            on_select='rerun',
            selection_mode='single-row',
            #key='selected_row',
        )

        st.markdown("---",)
        with st.expander("查看术语信息"):
            glossary=Glossary()
            data=glossary.detail(standard_code)
            df=pd.DataFrame(data,columns={
                'term_id': '术语序号',
                'term': '术语词条',
                'english_term': '术语英文',
                'derived_terms': '派生词',
                'definition': '术语定义',
                'entry_code': '术语条目编号',
                'synonyms': '同义词',
                'abbreviation': '缩略语',
                'symbol': '符号',
                'source': '来源',
                'note': '注',
                'nature': '性质',
                'system_id': '体系序号',
                'standard_code': '标准号',
                'standard_name': '标准名称',
                'unknown1': '分割列',
                'professional_field': '标准所属专业',
                'primary_heading': '一级条标题',
                'secondary_heading': '二级条标题',
                'tertiary_heading': '三级条标题',
                'mentioned_in_tech': '是否在技术要素中提及',
                'term_length': '术语字数',
                })
            event=st.dataframe(df,
            hide_index=True,  # 隐藏默认索引列
            use_container_width=True,
            column_config={
                "term_id": st.column_config.TextColumn(
                    "术语序号",
                    help="术语序号"
                ),
                "term": st.column_config.TextColumn(
                    "术语词条",
                    help="术语词条"
                ),
                "english_term": st.column_config.TextColumn(
                    "术语英文",
                    help="术语英文"
                ),
                "derived_terms": st.column_config.TextColumn(
                    "派生词",
                    help="派生词"
                ),
                "definition": st.column_config.TextColumn(
                    "术语定义",
                    help="术语定义"
                ),
                "entry_code": st.column_config.TextColumn(
                    "术语条目编号",
                    help="术语条目编号"
                ),
                "synonyms": st.column_config.TextColumn(
                    "同义词",
                    help="同义词"
                ),
                "abbreviation": st.column_config.TextColumn(
                    "缩略语",
                    help="缩略语"
                ),
                "symbol": st.column_config.TextColumn(
                    "符号",
                    help="符号"
                ),
                "source": st.column_config.TextColumn(
                    "来源",
                    help="来源"
                ),
                "note": st.column_config.TextColumn(
                    "注",
                    help="注"
                ),
                "nature": st.column_config.TextColumn(
                    "性质",
                    help="性质"
                ),
                "system_id": st.column_config.TextColumn(
                    "体系序号",
                    help="体系序号"
                ),
                "standard_code": st.column_config.TextColumn(
                    "标准号",
                    help="标准号"
                ),
                "standard_name": st.column_config.TextColumn(
                    "标准名称",
                    help="标准名称"
                ),
                "unknown1": st.column_config.TextColumn(
                    "分割列",
                    help="分割列"
                ),
                "professional_field": st.column_config.TextColumn(
                    "标准所属专业",
                    help="标准所属专业"
                ),
                "primary_heading": st.column_config.TextColumn(
                    "一级条标题",
                    help="一级条标题"
                ),
                "secondary_heading": st.column_config.TextColumn(
                    "二级条标题",
                    help="二级条标题"
                ),
                "tertiary_heading": st.column_config.TextColumn(
                    "三级条标题",
                    help="三级条标题"
                ),
                "mentioned_in_tech": st.column_config.TextColumn(
                    "是否在技术要素中提及",
                    help="是否在技术要素中提及"
                ),
                "term_length": st.column_config.TextColumn(
                    "术语字数",
                )
                }
            )
        st.markdown("---")
        with st.container(height=200):
            st.subheader('产品标准')
            st.write('hello world 2')
        st.markdown("---")
        with st.container(height=200):
            st.subheader('工艺标准')
            st.write('hello world 2')
        st.markdown("---")


