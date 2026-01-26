import os
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "false"

from altair import Data
import streamlit as st
import pandas as pd
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
from database.glossary import init_glossary_db
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
from view.display_method_query_list import show_method_select_boxes
from view.display_ccgz_query_list import show_ccgz_select_boxes
from view.display_ccgz_query_list import group_ccgz_list
from view.display_chart_query_list import init_standard_chart_db


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
if "quality_control" not in st.session_state:
    st.session_state.quality_control = ""
if "hse_requirements" not in st.session_state:
    st.session_state.hse_requirements = ""

# 初始化术语查询筛选参数
if "oil_gas_resource_type" not in st.session_state:
    st.session_state.oil_gas_resource_type = ""
if "process1" not in st.session_state:
    st.session_state.process1 = ""
if "process2" not in st.session_state:
    st.session_state.process2 = ""
if "wellbore_type1" not in st.session_state:
    st.session_state.wellbore_type1 = ""
if "wellbore_type2" not in st.session_state:
    st.session_state.wellbore_type2 = ""

# 初始化图表查询筛选参数
if "chart_oil_gas_resource_type" not in st.session_state:
    st.session_state.chart_oil_gas_resource_type = ""
if "chart_process1" not in st.session_state:
    st.session_state.chart_process1 = ""
if "chart_process2" not in st.session_state:
    st.session_state.chart_process2 = ""
if "chart_wellbore_type1" not in st.session_state:
    st.session_state.chart_wellbore_type1 = ""
if "chart_wellbore_type2" not in st.session_state:
    st.session_state.chart_wellbore_type2 = ""
if "chart_quality_control" not in st.session_state:
    st.session_state.chart_quality_control = ""
if "chart_hse_requirements" not in st.session_state:
    st.session_state.chart_hse_requirements = ""

if "ccgz_quality_control" not in st.session_state:
    st.session_state.ccgz_quality_control = ""
if "ccgz_hse_requirements" not in st.session_state:
    st.session_state.ccgz_hse_requirements = ""
if "ccgz_special_condition" not in st.session_state:
    st.session_state.ccgz_special_condition = ""


# 标题
with st.container():
    st.markdown(
        f"""<div><h3 style='text-align: center; color: blue; margin-top: 0rem; margin-bottom: 1rem; padding-top: 0.5rem;'>标准知识服务系统</h3></div>""",
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
        # 初始化session_state中的所有参数
        st.session_state.performance_indicator_level1 = "全部"
        st.session_state.performance_indicator_level2 = "全部"
        st.session_state.product_category1 = "全部"
        st.session_state.product_category2 = "全部"
        st.session_state.product_name = "全部"
        st.session_state.quality_control = ""
        st.session_state.hse_requirements = ""

        # 初始化术语查询相关的筛选参数
        # st.session_state.oil_gas_resource_type=""
        st.session_state.process1 = ""
        st.session_state.process2 = ""
        st.session_state.wellbore_type1 = ""
        st.session_state.wellbore_type2 = ""

        # 初始化图表查询相关的筛选参数
        st.session_state.chart_oil_gas_resource_type = ""
        st.session_state.chart_process1 = ""
        st.session_state.chart_process2 = ""
        st.session_state.chart_wellbore_type1 = ""
        st.session_state.chart_wellbore_type2 = ""
        st.session_state.chart_quality_control = ""
        st.session_state.chart_hse_requirements = ""
        st.session_state.chart_special_condition = ""


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
        width="stretch",
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
        width="stretch",
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
        width="stretch",
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
        width="stretch",
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
        width="stretch",
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
        width="stretch",
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
        width="stretch",
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


import re


def normalize_chapter_code(code: str):
    s = str(code).strip()
    m = re.search(r"附录\s*([A-Za-z])", s)
    if m:
        return m.group(1).upper()
    parts = re.findall(r"[A-Za-z0-9.]+", s)
    return parts[0] if parts else s


def get_chapter_content(data_list, selected_chapter):
    result = []
    selected_norm = normalize_chapter_code(selected_chapter)
    variants = [selected_norm, str(selected_chapter).strip()]
    for item in data_list:
        chapter = str(item.get("min_chapter_code", "")).strip()
        if any(chapter == v or chapter.startswith(f"{v}.") for v in variants):
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


# 列表展示
placeholder = st.empty()
with placeholder.container(border=True):
    # 根据查询内容显示不同的列表

    if "submit_type" in st.session_state:
        submit_type = st.session_state.submit_type
        if submit_type == "standard":
            display_standard_query_list()
        elif submit_type == "tiaokuan":
            oil_gas_resource_type = (
                st.session_state.tiaokuan_oil_gas_resource_type
                if "tiaokuan_oil_gas_resource_type" in st.session_state
                and st.session_state.tiaokuan_oil_gas_resource_type != "全部"
                else ""
            )
            process1 = (
                st.session_state.tiaokuan_process1
                if "tiaokuan_process1" in st.session_state
                and st.session_state.tiaokuan_process1 != "全部"
                else ""
            )
            process2 = (
                st.session_state.tiaokuan_process2
                if "tiaokuan_process2" in st.session_state
                and st.session_state.tiaokuan_process2 != "全部"
                else ""
            )
            wellbore_type1 = (
                st.session_state.tiaokuan_wellbore_type1
                if "tiaokuan_wellbore_type1" in st.session_state
                and st.session_state.tiaokuan_wellbore_type1 != "全部"
                else ""
            )
            wellbore_type2 = (
                st.session_state.tiaokuan_wellbore_type2
                if "tiaokuan_wellbore_type2" in st.session_state
                and st.session_state.tiaokuan_wellbore_type2 != "全部"
                else ""
            )
            quality_control = (
                st.session_state.tiaokuan_quality_control
                if "tiaokuan_quality_control" in st.session_state
                and st.session_state.tiaokuan_quality_control != "全部"
                else ""
            )
            hse_requirements = (
                st.session_state.tiaokuan_hse_requirements
                if "tiaokuan_hse_requirements" in st.session_state
                and st.session_state.tiaokuan_hse_requirements != "全部"
                else ""
            )
            special_condition = (
                st.session_state.tiaokuan_special_condition
                if "tiaokuan_special_condition" in st.session_state
                and st.session_state.tiaokuan_special_condition != "全部"
                else ""
            )
            standard_db=init_standard_db()
            data = standard_db.query_tiaokuan_data(
                search_term=st.session_state.search_term,
                oil_gas_resource_type=oil_gas_resource_type,
                process1=process1,
                process2=process2,
                wellbore_type1=wellbore_type1,
                wellbore_type2=wellbore_type2,
                quality_control=quality_control,
                hse_requirements=hse_requirements,
                special_condition=special_condition,
            )
            show_ccgz_select_boxes(prefix="tiaokuan",data=data)
            display_tiaokuan_query_list(
                search_term=st.session_state.search_term,
                data=data
            )
        elif submit_type == "tixi":
            # st.session_state.primary = primary
            # st.session_state.secondary = secondary
            # display_tixi_query_list(st.session_state.search_term,primary,secondary)
            display_tixi_query_list2(
                st.session_state.primary, st.session_state.secondary
            )
        elif submit_type == "shuyu":
            # selectbox 如果选择了全部，则转换为'' 视图层逻辑
            oil_gas_resource_type = (
                st.session_state.shuyu_oil_gas_resource_type
                if "shuyu_oil_gas_resource_type" in st.session_state
                and st.session_state.shuyu_oil_gas_resource_type != "全部"
                else ""
            )
            process1 = (
                st.session_state.shuyu_process1
                if "shuyu_process1" in st.session_state
                and st.session_state.shuyu_process1 != "全部"
                else ""
            )
            process2 = (
                st.session_state.shuyu_process2
                if "shuyu_process2" in st.session_state
                and st.session_state.shuyu_process2 != "全部"
                else ""
            )
            wellbore_type1 = (
                st.session_state.shuyu_wellbore_type1
                if "shuyu_wellbore_type1" in st.session_state
                and st.session_state.shuyu_wellbore_type1 != "全部"
                else ""
            )
            wellbore_type2 = (
                st.session_state.shuyu_wellbore_type2
                if "shuyu_wellbore_type2" in st.session_state
                and st.session_state.shuyu_wellbore_type2 != "全部"
                else ""
            )
            quality_control = (
                st.session_state.shuyu_quality_control
                if "shuyu_quality_control" in st.session_state
                and st.session_state.shuyu_quality_control != "全部"
                else ""
            )
            hse_requirements = (
                st.session_state.shuyu_hse_requirements
                if "shuyu_hse_requirements" in st.session_state
                and st.session_state.shuyu_hse_requirements != "全部"
                else ""
            )
            special_condition = (
                st.session_state.shuyu_special_condition
                if "shuyu_special_condition" in st.session_state
                and st.session_state.shuyu_special_condition != "全部"
                else ""
            )
            glossary = init_glossary_db()
            data = glossary.list_with_filters(
                search_term=st.session_state.search_term,
                oil_gas_resource_type=oil_gas_resource_type,
                process1=process1,
                process2=process2,
                wellbore_type1=wellbore_type1,
                wellbore_type2=wellbore_type2,
                quality_control=quality_control,
                hse_requirements=hse_requirements,
                special_condition=special_condition,
            )
            show_ccgz_select_boxes(prefix="shuyu", data=data)
            display_glossary_query_list(data=data)
        elif submit_type == "zhibiao":
            show_metric_select_boxes()
            display_metric_query_list(st.session_state.search_term)
        elif submit_type == "canshu":
            # display_method_query_list(st.session_state.search_term)
            show_method_select_boxes()
            display_method_query_list_new(st.session_state.search_term)
        elif submit_type == "chart":
            oil_gas_resource_type = (
                st.session_state.chart_oil_gas_resource_type
                if "chart_oil_gas_resource_type" in st.session_state
                and st.session_state.chart_oil_gas_resource_type != "全部"
                else ""
            )
            process1 = (
                st.session_state.chart_process1
                if "chart_process1" in st.session_state
                and st.session_state.chart_process1 != "全部"
                else ""
            )
            process2 = (
                st.session_state.chart_process2
                if "chart_process2" in st.session_state
                and st.session_state.chart_process2 != "全部"
                else ""
            )
            wellbore_type1 = (
                st.session_state.chart_wellbore_type1
                if "chart_wellbore_type1" in st.session_state
                and st.session_state.chart_wellbore_type1 != "全部"
                else ""
            )
            wellbore_type2 = (
                st.session_state.chart_wellbore_type2
                if "chart_wellbore_type2" in st.session_state
                and st.session_state.chart_wellbore_type2 != "全部"
                else ""
            )
            quality_control = (
                st.session_state.chart_quality_control
                if "chart_quality_control" in st.session_state
                and st.session_state.chart_quality_control != "全部"
                else ""
            )
            hse_requirements = (
                st.session_state.chart_hse_requirements
                if "chart_hse_requirements" in st.session_state
                and st.session_state.chart_hse_requirements != "全部"
                else ""
            )
            special_condition = (
                st.session_state.chart_special_condition
                if "chart_special_condition" in st.session_state
                and st.session_state.chart_special_condition != "全部"
                else ""
            )

            # 一次性查询所有类型（性能优化：3次查询 → 1次查询）
            standard_chart = init_standard_chart_db()
            all_chart_data = standard_chart.query_chart_data_all(
                search_term=search_term,
                oil_gas_resource_type=oil_gas_resource_type,
                process1=process1,
                process2=process2,
                wellbore_type1=wellbore_type1,
                wellbore_type2=wellbore_type2,
                quality_control=quality_control,
                hse_requirements=hse_requirements,
                special_condition=special_condition,
            )

            display_chart_query_list(
                search_term=st.session_state.search_term,
                imageData=all_chart_data['image'],
                tableData=all_chart_data['table'],
                formulaData=all_chart_data['formula'],
            )
        elif submit_type == "ccgz":  # 储层改造业务5级
            # selectbox 如果选择了全部，则转换为'' 视图层逻辑
            oil_gas_resource_type = (
                st.session_state.ccgz_oil_gas_resource_type
                if "ccgz_oil_gas_resource_type" in st.session_state
                and st.session_state.ccgz_oil_gas_resource_type != "全部"
                else ""
            )
            process1 = (
                st.session_state.ccgz_process1
                if "ccgz_process1" in st.session_state
                and st.session_state.ccgz_process1 != "全部"
                else ""
            )
            process2 = (
                st.session_state.ccgz_process2
                if "ccgz_process2" in st.session_state
                and st.session_state.ccgz_process2 != "全部"
                else ""
            )
            wellbore_type1 = (
                st.session_state.ccgz_wellbore_type1
                if "ccgz_wellbore_type1" in st.session_state
                and st.session_state.ccgz_wellbore_type1 != "全部"
                else ""
            )
            wellbore_type2 = (
                st.session_state.ccgz_wellbore_type2
                if "ccgz_wellbore_type2" in st.session_state
                and st.session_state.ccgz_wellbore_type2 != "全部"
                else ""
            )
            quality_control = (
                st.session_state.ccgz_quality_control
                if "ccgz_quality_control" in st.session_state
                and st.session_state.ccgz_quality_control != "全部"
                else ""
            )
            hse_requirements = (
                st.session_state.ccgz_hse_requirements
                if "ccgz_hse_requirements" in st.session_state
                and st.session_state.ccgz_hse_requirements != "全部"
                else ""
            )
            special_condition = (
                st.session_state.ccgz_special_condition
                if "ccgz_special_condition" in st.session_state
                and st.session_state.ccgz_special_condition != "全部"
                else ""
            )

            standard_db = init_standard_db()
            data = standard_db.get_by_ccgz(
                st.session_state.level1,
                st.session_state.level2,
                st.session_state.level3,
                st.session_state.level4,
                st.session_state.level5,
                oil_gas_resource_type,
                process1,
                process2,
                wellbore_type1,
                wellbore_type2,
                quality_control,
                hse_requirements,
                special_condition,
            )
            new_data = group_ccgz_list(data)
            show_ccgz_select_boxes(prefix="ccgz", data=data)
            display_ccgz_query_list(st.session_state.search_term, data=new_data)
        else:
            print("")
