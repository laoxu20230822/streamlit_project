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
from database.standard_index import init_standard_index_db
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
from view.display_tixi_query_list import display_tixi_query_list
from view.display_tixi_query_list import display_tixi_query_list2
from view.display_method_query_list import display_method_query_list_new
from base64 import b64encode
from view.showimg import showimg
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


st.markdown(
    f"""
        <style>
        p {{
            margin: 0;
            line-height: 1.1;
        }}
        </style>""",
    unsafe_allow_html=True,
)

# st.markdown(f"""
# <style>
# header {{ visibility: hidden; }}
# footer {{ visibility: hidden; }}
# </style>
# """,unsafe_allow_html=True)


st.set_page_config(layout="wide", initial_sidebar_state="expanded")


if "search_term" not in st.session_state:
    st.session_state.search_term = ""


# 标题
with st.container():
    st.markdown(
        f"""<div><h2 style='text-align: center; color: blue; margin-top: 0rem; margin-bottom: 1rem; padding-top: 0.5rem;'>储层改造标准知识服务系统</h2></div>""",
        unsafe_allow_html=True,
    )

# 查询表单

# showimg()

with st.form("standard_search_form"):
    # 调整按钮点击样式
    st.markdown(
        """
        <style>
        div.stFormSubmitButton > button[kind="primaryFormSubmit"] {
            background-color: #007BFF !important;  /* 蓝色 */
            color: white !important;
            border-radius: 10px;
            border-color: #007BFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    def button_submit(**kwargs: dict):
        submit_type = kwargs["submit_type"]
        st.session_state.submit_type = submit_type
        st.session_state.search_term = st.session_state.standard_term
        if "selected_rows" in st.session_state:
            del st.session_state["selected_rows"]

    primary = st.sidebar.selectbox(
        "**请选择一级门类**",
        [
            "基础与通用",
            "储层改造压前评估",
            "方案优化设计",
            "储层改造材料评价",
            "装备及工具",
            "现场施工及控制",
            "测试与压后评估分析",
        ],
    )

    sub_options = {
        "基础与通用": ["术语词汇", "基础试验方法", "其他"],
        "储层改造压前评估": ["储层改造压前评估"],
        "方案优化设计": ["通用设计规范", "压裂方案及工艺设计", "酸化方案及工艺设计"],
        "储层改造材料评价": [
            "压裂液材料及评价",
            "酸液材料及评价",
            "支撑剂及评价",
            "暂堵及其他材料",
        ],
        "装备及工具": ["压裂酸化装备", "压裂酸化工具"],
        "现场施工及控制": ["操作规范", "质量控制", "健康安全与环保"],
        "测试与压后评估分析": ["裂缝监测", "返排测试", "评估分析"],
    }

    def onchange():
        st.session_state.submit_type = "tixi"
        st.session_state.search_term = st.session_state.standard_term
        if "selected_rows" in st.session_state:
            del st.session_state["selected_rows"]

    secondary = st.sidebar.selectbox(
        "**请选择二级门类**", sub_options[primary], on_change=onchange
    )

    col1, col2, col3 = st.columns([0.4, 0.2, 0.2])
    # col.markdown('<div> 输入标准名称</div>',unsafe_allow_html=True)
    search_term = col1.text_input(
        "标准名称",
        key="standard_term",
        label_visibility="collapsed",
        placeholder="查询输入",
        width="stretch",
        value="",
    )
    standard_submit = col2.form_submit_button(
        "标准查询",
        use_container_width=True,
        kwargs={"submit_type": "standard"},
        on_click=button_submit,
        type=(
            "primary"
            if "submit_type" in st.session_state
            and st.session_state.submit_type == "standard"
            else "secondary"
        ),
    )
    tiaokuan_submit = col3.form_submit_button(
        "条款查询",
        use_container_width=True,
        kwargs={"submit_type": "tiaokuan"},
        on_click=button_submit,
        type=(
            "primary"
            if "submit_type" in st.session_state
            and st.session_state.submit_type == "tiaokuan"
            else "secondary"
        ),
    )

    button1, button2, button3, button4 = st.columns([0.2, 0.2, 0.2, 0.2])

    button1.form_submit_button(
        "标准体系",
        use_container_width=True,
        kwargs={"submit_type": "tixi"},
        on_click=button_submit,
        type=(
            "primary"
            if "submit_type" in st.session_state
            and st.session_state.submit_type == "tixi"
            else "secondary"
        ),
    )
    button2.form_submit_button(
        "术语查询",
        use_container_width=True,
        kwargs={"submit_type": "shuyu"},
        on_click=button_submit,
        type=(
            "primary"
            if "submit_type" in st.session_state
            and st.session_state.submit_type == "shuyu"
            else "secondary"
        ),
    )
    button3.form_submit_button(
        "指标查询",
        use_container_width=True,
        kwargs={"submit_type": "zhibiao"},
        on_click=button_submit,
        type=(
            "primary"
            if "submit_type" in st.session_state
            and st.session_state.submit_type == "zhibiao"
            else "secondary"
        ),
    )
    button4.form_submit_button(
        "方法查询",
        use_container_width=True,
        kwargs={"submit_type": "canshu"},
        on_click=button_submit,
        type=(
            "primary"
            if "submit_type" in st.session_state
            and st.session_state.submit_type == "canshu"
            else "secondary"
        ),
    )


def display_standard_info(standard_code, standard_name):
    # col1,col2 = st.columns(2)
    html_stype = "<hr style='margin: 0.5rem 0; border-color: grey;'></hr>"
    st.write(f"""标准号：{standard_code}""", unsafe_allow_html=True)
    st.write(
        f"""标准名称：{standard_name}   
    {html_stype}""",
        unsafe_allow_html=True,
    )
    # st.markdown(f"""
    # >:blue[{standard_code}]\n
    # >#### {standard_name}
    # """)


def get_chapter_content(data_list, selected_chapter):
    # 初始化结果列表
    result = []
    # 遍历数据列表
    for item in data_list:
        chapter = item["min_chapter_code"]
        # 检查当前章节是否是选定章节或其子章节
        # 条件1：完全匹配（当前章节）
        # 条件2：以选定章节+点开头（子章节）
        if chapter == selected_chapter or chapter.startswith(f"{selected_chapter}."):
            result.append(item["standard_content"])

    return result


def display_standard_cotent(standard_code: str):
    standard_db = init_standard_db()
    standard_detail = standard_db.standard_detail(standard_code)
    t21, t22 = t2.columns([4, 6])
    with t21.container(border=True, height=400):
        display_standard_structure(standard_code)
    with t22.container(border=True, height=400):
        if "chapter" in st.session_state and "chapter_content" in st.session_state:
            contents = get_chapter_content(standard_detail, st.session_state.chapter)
            st.markdown("\n\n".join(contents))
            # if st.session_state.chapter in st.session_state.chapter_content:
            #     content_arr=st.session_state.chapter_content[st.session_state.chapter]
            #     head=content_arr[0]
            #     st.markdown(head)
            #     for content in content_arr[1:]:
            #         st.markdown(content)


# 列表展示
placeholder = st.empty()
with placeholder.container(border=True):
    # 根据查询内容显示不同的列表

    if "submit_type" in st.session_state:
        submit_type = st.session_state.submit_type
        if submit_type == "standard":
            display_standard_query_list()
        elif submit_type == "tiaokuan":
            display_tiaokuan_query_list(st.session_state.search_term)
        elif submit_type == "tixi":
            st.session_state.primary = primary
            st.session_state.secondary = secondary
            # display_tixi_query_list(st.session_state.search_term,primary,secondary)
            display_tixi_query_list2(primary, secondary)
        elif submit_type == "shuyu":
            display_glossary_query_list(st.session_state.search_term)
        elif submit_type == "zhibiao":
            display_metric_query_list(st.session_state.search_term)
        elif submit_type == "canshu":
            #display_method_query_list(st.session_state.search_term)
            display_method_query_list_new(st.session_state.search_term)   
        else:
            print("")

    # if "selected_rows" in st.session_state:
    #     standard_code = st.session_state["selected_rows"][0]["standard_code"]
    #     standard_name = st.session_state["selected_rows"][0]["standard_name"]
    #     # 查询一级门类编号
    #     standard_db = init_standard_db()
    #     level1_code_data = standard_db.query_category_level1_code(standard_code)
    #     if level1_code_data is not None and level1_code_data[0] == "104":
    #         level1_code = level1_code_data[0]
    #         product_or_craft_tab_name = "相关产品"
    #         st.session_state.pc_type = "product"
    #     elif level1_code_data is not None and level1_code_data[0] in [
    #         "103",
    #         "106",
    #         "107",
    #     ]:
    #         product_or_craft_tab_name = "工业标准"
    #         st.session_state.pc_type = "craft"
    #     else:
    #         st.session_state.pc_type = "other"
    #     t1, t2, t3, t4, t5 = st.tabs(
    #         [
    #             "**基本信息**",
    #             "**标准目次信息**",
    #             "**引用文件信息**",
    #             "**术语**",
    #             "**" + product_or_craft_tab_name + "**",
    #         ]
    #     )
    #     # standard_code = df.iloc[selected_row]['standard_code']

    #     ## 显示标准详情
    #     with t1:
    #         display_standard_info(standard_code, standard_name)
    #         display_standard_detail(standard_code)

    #     # 显示目次信息
    #     with t2:

    #         display_standard_info(standard_code, standard_name)
    #         display_standard_cotent(standard_code)
    #     # st.markdown("---")

    #     # 引用文件
    #     with t3:
    #         display_standard_info(standard_code, standard_name)
    #         display_standard_references(standard_code)

    #     # 术语信息
    #     with t4:
    #         display_standard_info(standard_code, standard_name)
    #         display_standard_glossary(standard_code)

    #     # 工艺标准 or 产品标准
    #     with t5:
    #         display_standard_info(standard_code, standard_name)
    #         if st.session_state.pc_type == "product":
    #             display_product_standard(standard_code)
    #         elif st.session_state.pc_type == "craft":
    #             display_craft_standard(standard_code)
    #         else:
    #             st.write("other")
