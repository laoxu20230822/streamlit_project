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
from view.display_chart_query_list import display_chart_query_list
from view.display_ccgz_query_list import display_ccgz_query_list
from base64 import b64encode
from view.showimg import showimg
from view.display_navigator_tab import display_navigator_tab
from view.display_metric_query_list import show_metric_select_boxes


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
        f"""<div><h3 style='text-align: center; color: blue; margin-top: 0rem; margin-bottom: 1rem; padding-top: 0.5rem;'>储层改造标准知识服务系统</h3></div>""",
        unsafe_allow_html=True,
    )

# 查询表单

# showimg()

with st.form("standard_search_form", height="stretch", border=False):
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
        <style>
        div.stFormSubmitButton > button {
            min-height: 0px; 
            height: 40px;         /* 改按钮高度 */
            width: 100px;         /* 改按钮宽度 */
            font-size: 20px !important;    /* 改字体大小 */
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

    display_navigator_tab()

    col1, col2, col3, col4, button1, button2, button3, button4 = st.columns(
        [0.5, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
    )
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
        "标准",
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
        "条款",
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

    chart_submit = col4.form_submit_button(
        "图表公式",
        use_container_width=True,
        kwargs={"submit_type": "chart"},
        on_click=button_submit,
        type=(
            "primary"
            if "submit_type" in st.session_state
            and st.session_state.submit_type == "chart"
            else "secondary"
        ),
    )

    # button1, button2, button3, button4 = st.columns([0.2, 0.2, 0.2, 0.2])

    button1.form_submit_button(
        "体系",
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
        "术语",
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
        "指标",
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
        "试验方法",
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
            # st.session_state.primary = primary
            # st.session_state.secondary = secondary
            # display_tixi_query_list(st.session_state.search_term,primary,secondary)
            display_tixi_query_list2(
                st.session_state.primary, st.session_state.secondary
            )
        elif submit_type == "shuyu":
            display_glossary_query_list(st.session_state.search_term)
        elif submit_type == "zhibiao":
            show_metric_select_boxes()
            display_metric_query_list(st.session_state.search_term)
        elif submit_type == "canshu":
            # display_method_query_list(st.session_state.search_term)
            display_method_query_list_new(st.session_state.search_term)
        elif submit_type == "chart":
            display_chart_query_list(st.session_state.search_term)
        elif submit_type == "ccgz":  # 储层改造业务5级
            display_ccgz_query_list(st.session_state.search_term)
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
