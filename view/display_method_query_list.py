import streamlit as st
import pandas as pd
from streamlit.elements.lib.layout_utils import Height
from database.metric import init_metric_db
from database.standard_index import StandardIndex
from database.standard_db import Pageable, StandardDB
from database.standard_db import WhereCause
from st_aggrid import AgGrid, GridOptionsBuilder

from database.standard_structure import StandardStructure
from view.display_standard_tab_info import display_standard_tab_info


def display_method_query_list_new(search_term: str):

    standard_db = StandardDB()

    # 从session_state获取筛选条件，处理"全部"转换为空字符串
    performance_indicator_level1 = st.session_state.get(
        "performance_indicator_level1", ""
    )
    performance_indicator_level2 = st.session_state.get(
        "performance_indicator_level2", ""
    )
    method_name = st.session_state.get("method_name", "")
    product_category1 = st.session_state.get("product_category1", "")
    product_category2 = st.session_state.get("product_category2", "")
    product_name = st.session_state.get("product_name", "")

    data = standard_db.query_by_stimulation_business_level2(
        search_term,
        performance_indicator_level1,
        performance_indicator_level2,
        method_name,
        product_category1,
        product_category2,
        product_name,
    )
    df = pd.DataFrame(
        data if data else [],
        columns={
            "standard_code": "标准号",
            "standard_name": "标准名称",
            "standard_content": "标准内容",
            "stimulation_business_level2": "刺激业务等级2",
        },
    )
    df_pivot = (
        df.groupby(["standard_code", "standard_name", "stimulation_business_level2"])
        .agg({"standard_content": lambda x: "\n".join(x)})  # 把同一类内容拼接
        .reset_index()
        .pivot(
            index=["standard_code", "standard_name"],
            columns="stimulation_business_level2",
            values="standard_content",
        )
        .reset_index()
    )

    grid_options = {
        "defaultColDef": {
            "filter": True,  # 开启过滤
            # "floatingFilter": True,   # 列头下方的小输入框
            "sortable": True,  # 可排序
            "resizable": True,  # 可拖动列宽
        },
        "enableCellTextSelection": True,
        "suppressNoRowsOverlay": True,
        "columnDefs": [
            {"field": "standard_code", "headerName": "标准号", "width": 120},
            {"field": "standard_name", "headerName": "标准名称", "width": 200},
            {
                "field": "方法提要",
                "headerName": "方法提要",
                "autoHeight": True,
                "wrapText": False,
                "cellStyle": {
                    "whiteSpace": "pre-wrap",  # 保留原始换行符和空格
                    "wordBreak": "normal",  # 正常的单词换行规则
                },
            },
            {
                "field": "仪器设备、试剂或材料",
                "headerName": "仪器设备、试剂或材料",
                "autoHeight": True,
                "wrapText": False,
                "cellStyle": {
                    "whiteSpace": "pre-wrap",  # 保留原始换行符和空格
                    "wordBreak": "normal",  # 正常的单词换行规则
                },
            },
            {
                "field": "试验步骤",
                "headerName": "试验步骤",
                "autoHeight": True,
                "wrapText": False,
                "cellStyle": {
                    "whiteSpace": "pre-wrap",  # 保留原始换行符和空格
                    "wordBreak": "normal",  # 正常的单词换行规则
                },
            },
            {
                "field": "试验数据处理",
                "headerName": "试验数据处理",
                "autoHeight": True,
                "wrapText": False,
                "cellStyle": {
                    "whiteSpace": "pre-wrap",  # 保留原始换行符和空格
                    "wordBreak": "normal",  # 正常的单词换行规则
                },
            },  # 启用文本换行},
        ],
        "rowSelection": {
            "mode": "singleRow",
            "checkboxes": False,
            "enableClickSelection": True,
        },
        # "autoSizeStrategy": {
        #     "type": "fitCellContents"
        # },
        "pagination": True,
        # "paginationAutoPageSize": True,
        "paginationPageSize": 50,
    }
    # gb_options=GridOptionsBuilder.build()
    # gb_options.update(grid_options)

    grid_response = AgGrid(
        df_pivot,
        gridOptions=grid_options,
        height=500,
        # key='asdjflasdjkfl'
    )
    selected_rows = grid_response["selected_rows"]

    if selected_rows is not None:
        st.session_state.selected_rows = [
            {
                "standard_code": row["standard_code"],
                "standard_name": row["standard_name"],
            }
            for _, row in selected_rows.iterrows()
        ]
    if "selected_rows" in st.session_state:
        display_standard_tab_info()


def onchange_for_method():
    st.session_state.submit_type = "canshu"
    if "selected_rows" in st.session_state:
        del st.session_state["selected_rows"]


def show_method_select_boxes():
    """显示试验方法筛选框，参考show_metric_select_boxes实现"""
    standard_db = StandardDB()

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        performance_indicator_level1_options = (
            standard_db.query_performance_indicator_level1()
        )
        performance_indicator_level1_options.insert(0, "全部")
        performance_indicator_level1 = st.selectbox(
            "**性能指标一级**",
            performance_indicator_level1_options,
            on_change=onchange_for_method,
        )
        

    with c2:
        performance_indicator_level2_options = (
            standard_db.query_performance_indicator_level2()
        )
        performance_indicator_level2_options.insert(0, "全部")
        performance_indicator_level2 = st.selectbox(
            "**性能指标二级**",
            performance_indicator_level2_options,
            on_change=onchange_for_method,
        )

    with c3:
        method_name_options = standard_db.query_method_name()
        method_name_options.insert(0, "全部")
        method_name = st.selectbox(
            "**方法名称**", method_name_options, on_change=onchange_for_method
        )

    with c4:
        product_category1_options = standard_db.query_product_category1()
        product_category1_options.insert(0, "全部")
        product_category1 = st.selectbox(
            "**产品类别1**", product_category1_options, on_change=onchange_for_method
        )

    with c5:
        product_category2_options = standard_db.query_product_category2()
        product_category2_options.insert(0, "全部")
        product_category2 = st.selectbox(
            "**产品类别2**", product_category2_options, on_change=onchange_for_method
        )

    with c6:
        product_name_options = standard_db.query_product_name()
        product_name_options.insert(0, "全部")
        product_name = st.selectbox(
            "**产品名称**", product_name_options, on_change=onchange_for_method
        )

    # 将选择的值存储到session_state，处理"全部"转换为空字符串
    st.session_state.performance_indicator_level1 = (
        "" if performance_indicator_level1 == "全部" else performance_indicator_level1
    )
    st.session_state.performance_indicator_level2 = (
        "" if performance_indicator_level2 == "全部" else performance_indicator_level2
    )
    st.session_state.method_name = "" if method_name == "全部" else method_name
    st.session_state.product_category1 = (
        "" if product_category1 == "全部" else product_category1
    )
    st.session_state.product_category2 = (
        "" if product_category2 == "全部" else product_category2
    )
    st.session_state.product_name = "" if product_name == "全部" else product_name
