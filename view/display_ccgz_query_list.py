import streamlit as st
from database import standard_index
from database.standard_db import init_standard_db
from database.standard_index import init_standard_index_db
from database.standard_db import init_standard_db
from st_aggrid import AgGrid
import pandas as pd
from view.display_standard_tab_info import display_standard_tab_info
from utils.data_utils import count_unique_standard_codes, get_selectbox_index


def show_grid(data):
    df = pd.DataFrame(
        data if data else [],
        columns={
            "standard_code": "标准号",
            "standard_name": "标准名称",
            "standard_content": "标准内容",
            "min_chapter_clause_code": "最小章节条款号",
        },
    )
    df.insert(0, "seq", range(1, len(df) + 1))
    df["standard_info"] = df["standard_code"] + " " + df["standard_name"] + ""
    # df['standard_content'] = df['min_chapter_clause_code'] + '\n' + df['standard_content']
    # 展示短文本
    # 生成短文本列（前 50 字）
    MAX_CHARS = 50
    df["standard_info_short"] = df["standard_info"].apply(
        lambda s: s if len(str(s)) <= MAX_CHARS else str(s)[:MAX_CHARS] + "..."
    )

    grid_options = {
        "defaultColDef": {
            "filter": True,  # 开启过滤
            # "floatingFilter": True,   # 列头下方的小输入框
            "sortable": True,  # 可排序
            "resizable": True,  # 可拖动列宽
            "tooltipComponent": None,  # 使用内置 tooltip
        },
        "enableCellTextSelection": True,
        "suppressNoRowsOverlay": True,
        "columnDefs": [
            {
                "field": "seq",
                "headerName": "序号",
                "width": 60,
                "suppressSizeToFit": True,
            },
            {
                "field": "standard_info",
                "headerName": "标准来源",
                "width": 250,
                # "valueFormatter": "x.data.standard_info ? x.data.standard_info.substring(0,3) : ''",
                "tooltipField": "standard_info",
            },
            {
                "field": "standard_code",
                "headerName": "标准号",
                "hide": True,
            },
            {"field": "standard_name", "headerName": "标准名称", "hide": True},
            {
                "field": "standard_content",
                "headerName": "标准内容",
                "tooltipField": "standard_content",
                "width": 400,
                "autoHeight": True,
                "wrapText": True,
                "cellStyle": {
                    "whiteSpace": "pre-wrap",  # 保留原始换行符和空格
                    "wordBreak": "normal",  # 正常的单词换行规则
                },
            },
        ],
        "rowSelection": {
            "mode": "singleRow",
            "checkboxes": False,
            "enableClickSelection": True,
        },
        "autoSizeStrategy": {"type": "fitCellContents"},
        "pagination": True,
        ##"paginationAutoPageSize": True,
        "paginationPageSize": 50,
        # "animateRows": True,
    }
    # 显示统计信息
    unique_count = count_unique_standard_codes(df)
    st.markdown(f"**查询标准总数: {unique_count}**")

    return AgGrid(
        df,
        gridOptions=grid_options,
        height=500,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
    )


def display_ccgz_query_list(search_term,data):
    grid_response = show_grid(data)
    selected_rows = grid_response["selected_rows"]
    if selected_rows is not None:
        st.session_state.selected_rows = [
            {
                "standard_code": row["standard_code"],
                "standard_name": row["standard_name"],
            }
            for _, row in selected_rows.iterrows()
        ]
    display_standard_tab_info()

def group_ccgz_list(
        data):
        # 按照standard_code分组
        from collections import defaultdict
        grouped_data = defaultdict(
            lambda: {
                "standard_code": "",
                "standard_name": "",
                "standard_content": [],
                "min_chapter_clause_code": "",
            }
        )

        for item in data:
            code = item["standard_code"]
            grouped_data[code]["standard_code"] = code
            grouped_data[code]["standard_name"] = "#" + item["standard_name"] + "#"
            grouped_data[code]["standard_content"].append(item["standard_content"])
            grouped_data[code]["min_chapter_clause_code"] = item[
                "min_chapter_clause_code"
            ]

        # 拼接内容并转换为新的列表
        new_data = []
        for v in grouped_data.values():
            # 用回车符（\n）拼接内容
            v["standard_content"] = "\n".join(v["standard_content"])
            new_data.append(v)
        return new_data

def show_ccgz_select_boxes(data, prefix: str = "ccgz"):

    """显示级联筛选下拉框

    Args:
        prefix: 业务类型前缀，决定显示的筛选框数量和 session_state key 前缀
                支持的值: 'ccgz', 'tiaokuan', 'shuyu', 'chart'
    """

    def onchange_for_ccgz(prefix, key):
        # 清除选中行
        if "selected_rows" in st.session_state:
            del st.session_state["selected_rows"]

    standard_db = init_standard_db()

    # 为不同的查询类型设置不同的 session_state key
    oil_gas_key = f"{prefix}_oil_gas_resource_type"
    process1_key = f"{prefix}_process1"
    process2_key = f"{prefix}_process2"
    wellbore_type1_key = f"{prefix}_wellbore_type1"
    wellbore_type2_key = f"{prefix}_wellbore_type2"
    quality_control_key = f"{prefix}_quality_control"
    hse_key = f"{prefix}_hse_requirements"


    # 根据prefix决定显示的筛选框数量
    if prefix == "shuyu":
        # 术语：隐藏“特殊工况”(col4)、“管理控制点”(col6)、“知识属性”(col7)
        col1, col2, col3, col5 = st.columns(4)
        col4 = None
        show_extra_filters = False

        # 默认值设为全部
        st.session_state[f"{prefix}_special_condition"] = "全部"
        st.session_state[f"{prefix}_quality_control"] = "全部"
        st.session_state[f"{prefix}_hse_requirements"] = "全部"

    elif prefix in ["ccgz", "tiaokuan", "chart"]:
        # 显示全部7个筛选框
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        show_extra_filters = True
    else:
        # 其他功能：只显示5个筛选框
        col1, col2, col3, col4, col5 = st.columns(5)
        show_extra_filters = False

    # 油气资源类别 - 使用级联查询
    with col1:
        # 从data中获取列表
        oil_gas_resource_options = list(
            dict.fromkeys(
                filter(None, (item.get("oil_gas_resource_type") for item in data))
            )
        )
        if not oil_gas_resource_options and (prefix in ["shuyu", "ccgz", "tiaokuan", "chart"]):
            oil_gas_resource_options = standard_db.get_distinct_values(
                "oil_gas_resource_type"
            )
        oil_gas_resource_options.insert(0, "全部")
        st.selectbox(
            "**油气资源类别**",
            oil_gas_resource_options,
            index=get_selectbox_index(oil_gas_resource_options, oil_gas_key),
            key=f"{oil_gas_key}",
            args=(prefix, oil_gas_key),
            on_change=onchange_for_ccgz,
        )

    # 工艺类型1 - 使用级联查询
    with col2:
        # 从data中获取列表
        process1_options = list(
            dict.fromkeys(filter(None, (item.get("process1") for item in data)))
        )
        if not process1_options and (prefix in ["shuyu", "ccgz", "tiaokuan", "chart"]):
            process1_options = standard_db.get_distinct_values("process1")
        process1_options.insert(0, "全部")
        process1 = st.selectbox(
            "**工艺类型1**",
            process1_options,
            index=get_selectbox_index(process1_options, process1_key),
            key=f"{process1_key}",
            args=(prefix, f"{process1_key}"),
            on_change=onchange_for_ccgz,
        )

    # 工艺类型2 - 使用级联查询
    with col3:
        # 从data中获取列表
        process2_options = list(
            dict.fromkeys(filter(None, (item.get("process2") for item in data)))
        )
        if not process2_options and (prefix in ["shuyu", "ccgz", "tiaokuan", "chart"]):
            process2_options = standard_db.get_distinct_values("process2")
        process2_options.insert(0, "全部")
        print(process2_options)
        process2 = st.selectbox(
            "**工艺类型2**",
            process2_options,
            index=get_selectbox_index(process2_options, process2_key),
            key=f"{process2_key}",
            args=(prefix, f"{process2_key}"),
            on_change=onchange_for_ccgz,
        )
        #print(get_selectbox_index(process2_options, process2_key))

    # 第4列：所有类型都显示“特殊工况”
    if col4:
        with col4:
            special_condition_key = f"{prefix}_special_condition"
            special_condition_options = list(
                dict.fromkeys(filter(None, (item.get("special_condition") for item in data)))
            )
            if not special_condition_options:
                special_condition_options = standard_db.get_distinct_values(
                    "special_condition"
                )
            special_condition_options.insert(0, "全部")
            st.selectbox(
                "**特殊工况**",
                special_condition_options,
                index=get_selectbox_index(special_condition_options, special_condition_key),
                key=f"{special_condition_key}",
                args=(prefix, f"{special_condition_key}"),
                on_change=onchange_for_ccgz,
            )

    # 第5列：所有类型都显示“井筒类型”
    with col5:
        # 从data中获取列表
        wellbore_type1_options = list(
            dict.fromkeys(filter(None, (item.get("wellbore_type1") for item in data)))
        )
        if not wellbore_type1_options:
            wellbore_type1_options = standard_db.get_distinct_values("wellbore_type1")
        wellbore_type1_options.insert(0, "全部")
        wellbore_type1 = st.selectbox(
            "**井筒类型**",
            wellbore_type1_options,
            index=get_selectbox_index(wellbore_type1_options, wellbore_type1_key),
            key=f"{wellbore_type1_key}",
            args=(prefix, f"{wellbore_type1_key}"),
            on_change=onchange_for_ccgz,
        )

    # 管理控制点和知识属性：只在储层改造5级和术语中显示
    quality_control = ""
    hse_requirements = ""

    if show_extra_filters:
        # 管理控制点 - 使用级联查询
        with col6:
            quality_control_options = list(
                dict.fromkeys(filter(None, (item.get("quality_control") for item in data)))
            )
            if not quality_control_options and (prefix in ["shuyu", "ccgz", "tiaokuan", "chart"]):
                quality_control_options = standard_db.get_distinct_values("quality_control")
            quality_control_options.insert(0, "全部")

            quality_control = st.selectbox(
                "**管理控制点**",
                quality_control_options,
                key=f"{quality_control_key}",
                index=get_selectbox_index(quality_control_options, quality_control_key),
                args=(prefix, f"{quality_control_key}"),
                on_change=onchange_for_ccgz,
            )

        # 知识属性 - 使用级联查询
        with col7:
            hse_requirements_options = list(
                dict.fromkeys(filter(None, (item.get("hse_requirements") for item in data)))
            )
            if not hse_requirements_options and (prefix in ["shuyu", "ccgz", "tiaokuan", "chart"]):
                hse_requirements_options = standard_db.get_distinct_values(
                    "hse_requirements"
                )
            hse_requirements_options.insert(0, "全部")


            hse_requirements = st.selectbox(
                "**知识属性**",
                hse_requirements_options,
                index=get_selectbox_index(hse_requirements_options, hse_key),
                key=f"{hse_key}",
                args=(prefix, f"{hse_key}"),
                on_change=onchange_for_ccgz,
            )