import streamlit as st
from database import standard_index
from database.standard_db import init_standard_db
from database.standard_index import init_standard_index_db
from database.standard_db import init_standard_db
from st_aggrid import AgGrid
import pandas as pd
from view.display_standard_tab_info import display_standard_tab_info
from utils.data_utils import count_unique_standard_codes


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
    #df['standard_content'] = df['min_chapter_clause_code'] + '\n' + df['standard_content']
    #展示短文本
    # 生成短文本列（前 50 字）
    MAX_CHARS = 50
    df["standard_info_short"] = df["standard_info"].apply(lambda s: s if len(str(s)) <= MAX_CHARS else str(s)[:MAX_CHARS] + "...")


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
                #"valueFormatter": "x.data.standard_info ? x.data.standard_info.substring(0,3) : ''",
                "tooltipField": "standard_info",
            },
            {
                "field": "standard_code",
                "headerName": "标准号",
                "hide": True,
            },
            {"field": "standard_name", "headerName": "标准名称", "hide": True},
            {"field": "standard_content", "headerName": "标准内容",'tooltipField':'standard_content',
             "width": 400, 'autoHeight': True, "wrapText": True, 'cellStyle': {
                    'whiteSpace': 'pre-wrap',  # 保留原始换行符和空格
                    'wordBreak': 'normal'      # 正常的单词换行规则
                }},
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
        #"animateRows": True,
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


def display_ccgz_query_list(search_term):
    
    # standard_index = init_standard_index_db()

    standard_db = init_standard_db()
    data = standard_db.fetch_by_ccgz(
        st.session_state.level1,
        st.session_state.level2,
        st.session_state.level3,
        st.session_state.level4,
        st.session_state.level5,
        st.session_state.oil_gas_resource_type,
        st.session_state.process1,
        st.session_state.process2,
        st.session_state.wellbore_type1,
        st.session_state.wellbore_type2,
        st.session_state.quality_control,
        st.session_state.hse_requirements,
    )


    
    #--------

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

def show_ccgz_select_boxes():
    def onchange_for_ccgz():
        """级联筛选回调函数"""
        # 获取触发变更的selectbox的key
        select_box_key = st.session_state.get("trigger_select_box", "")

        # 获取当前选择的值和选项列表
        current_value = st.session_state.get(select_box_key, "全部")
        option_list = st.session_state.get(f"{select_box_key}_options", [])

        # 根据不同的key更新对应的session_state
        prefix = st.session_state.get('submit_type', 'ccgz')

        if select_box_key == f"{prefix}_oil_gas_resource_type_selectbox":
            key = f"{prefix}_oil_gas_resource_type"
            st.session_state[key] = current_value if current_value != "全部" else ""
            if current_value != "全部":
                st.session_state[f"{key}_option"] = option_list
        elif select_box_key == f"{prefix}_process1_selectbox":
            key = f"{prefix}_process1"
            st.session_state[key] = current_value if current_value != "全部" else ""
            if current_value != "全部":
                st.session_state[f"{key}_option"] = option_list
        elif select_box_key == f"{prefix}_process2_selectbox":
            key = f"{prefix}_process2"
            st.session_state[key] = current_value if current_value != "全部" else ""
            if current_value != "全部":
                st.session_state[f"{key}_option"] = option_list
        elif select_box_key == f"{prefix}_wellbore_type1_selectbox":
            key = f"{prefix}_wellbore_type1"
            st.session_state[key] = current_value if current_value != "全部" else ""
            if current_value != "全部":
                st.session_state[f"{key}_option"] = option_list
        elif select_box_key == f"{prefix}_wellbore_type2_selectbox":
            key = f"{prefix}_wellbore_type2"
            st.session_state[key] = current_value if current_value != "全部" else ""
            if current_value != "全部":
                st.session_state[f"{key}_option"] = option_list
        elif select_box_key == f"{prefix}_quality_control_selectbox":
            key = f"{prefix}_quality_control"
            st.session_state[key] = current_value if current_value != "全部" else ""
            if current_value != "全部":
                st.session_state[f"{key}_option"] = option_list
        elif select_box_key == f"{prefix}_hse_requirements_selectbox":
            key = f"{prefix}_hse_requirements"
            st.session_state[key] = current_value if current_value != "全部" else ""
            if current_value != "全部":
                st.session_state[f"{key}_option"] = option_list

        # 清除选中行
        if "selected_rows" in st.session_state:
            del st.session_state["selected_rows"]

    # 根据不同的 submit_type 使用不同的 key
    prefix = st.session_state.get('submit_type', 'ccgz')

    standard_db = init_standard_db()

    # 为不同的查询类型设置不同的 session_state key
    oil_gas_key = f"{prefix}_oil_gas_resource_type"
    process1_key = f"{prefix}_process1"
    process2_key = f"{prefix}_process2"
    wellbore_type1_key = f"{prefix}_wellbore_type1"
    wellbore_type2_key = f"{prefix}_wellbore_type2"
    quality_control_key = f"{prefix}_quality_control"
    hse_key = f"{prefix}_hse_requirements"

    # 初始化这些 key（如果不存在）
    for key in [oil_gas_key, process1_key, process2_key, wellbore_type1_key,
                wellbore_type2_key, quality_control_key, hse_key]:
        if key not in st.session_state:
            st.session_state[key] = ""

    # 从session_state获取当前选择的值，如果不存在则默认为"全部"
    oil_gas_resource = st.session_state.get(oil_gas_key, "全部") or "全部"
    process1 = st.session_state.get(process1_key, "全部") or "全部"
    process2 = st.session_state.get(process2_key, "全部") or "全部"
    wellbore_type1 = st.session_state.get(wellbore_type1_key, "全部") or "全部"
    wellbore_type2 = st.session_state.get(wellbore_type2_key, "全部") or "全部"
    quality_control = st.session_state.get(quality_control_key, "全部") or "全部"
    hse_requirements = st.session_state.get(hse_key, "全部") or "全部"

    # 转换为查询参数（"全部"转换为空字符串）
    oil_gas_resource_param = oil_gas_resource if oil_gas_resource != "全部" else ""
    process1_param = process1 if process1 != "全部" else ""
    process2_param = process2 if process2 != "全部" else ""
    wellbore_type1_param = wellbore_type1 if wellbore_type1 != "全部" else ""
    wellbore_type2_param = wellbore_type2 if wellbore_type2 != "全部" else ""
    quality_control_param = quality_control if quality_control != "全部" else ""
    hse_requirements_param = hse_requirements if hse_requirements != "全部" else ""

    # 根据prefix决定显示的筛选框数量
    if prefix == 'ccgz':
        # 储层改造5级：显示全部7个筛选框
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        show_extra_filters = True
    else:
        # 其他功能：只显示5个筛选框
        col1, col2, col3, col4, col5 = st.columns(5)
        show_extra_filters = False

    # 油气资源类别 - 使用级联查询
    with col1:
        oil_gas_resource_options = standard_db.query_oil_gas_resource_type(
            process1_param, process2_param, wellbore_type1_param, wellbore_type2_param,
            quality_control_param, hse_requirements_param
        )
        oil_gas_resource_options.insert(0, "全部")

        # 确保当前选择在选项列表中
        if oil_gas_resource not in oil_gas_resource_options:
            oil_gas_resource = "全部"

        index = oil_gas_resource_options.index(oil_gas_resource)
        st.session_state[f"{oil_gas_key}_selectbox_options"] = oil_gas_resource_options
        st.session_state["trigger_select_box"] = f"{oil_gas_key}_selectbox"
        oil_gas_resource = st.selectbox(
            "**油气资源类别**",
            oil_gas_resource_options,
            index=index,
            key=f"{oil_gas_key}_selectbox",
            on_change=onchange_for_ccgz,
        )
        oil_gas_resource = oil_gas_resource if oil_gas_resource != "全部" else ""
        oil_gas_resource_param = oil_gas_resource

    # 工艺类型1 - 使用级联查询
    with col2:
        process1_options = standard_db.query_process1(
            oil_gas_resource_param, process2_param, wellbore_type1_param, wellbore_type2_param,
            quality_control_param, hse_requirements_param
        )
        process1_options.insert(0, "全部")

        # 确保当前选择在选项列表中
        if process1 not in process1_options:
            process1 = "全部"

        index = process1_options.index(process1)
        st.session_state[f"{process1_key}_selectbox_options"] = process1_options
        st.session_state["trigger_select_box"] = f"{process1_key}_selectbox"
        process1 = st.selectbox(
            "**工艺类型1**",
            process1_options,
            index=index,
            key=f"{process1_key}_selectbox",
            on_change=onchange_for_ccgz,
        )
        process1 = process1 if process1 != "全部" else ""
        process1_param = process1

    # 工艺类型2 - 使用级联查询
    with col3:
        process2_options = standard_db.query_process2(
            oil_gas_resource_param, process1_param, wellbore_type1_param, wellbore_type2_param,
            quality_control_param, hse_requirements_param
        )
        process2_options.insert(0, "全部")

        # 确保当前选择在选项列表中
        if process2 not in process2_options:
            process2 = "全部"

        index = process2_options.index(process2)
        st.session_state[f"{process2_key}_selectbox_options"] = process2_options
        st.session_state["trigger_select_box"] = f"{process2_key}_selectbox"
        process2 = st.selectbox(
            "**工艺类型2**",
            process2_options,
            index=index,
            key=f"{process2_key}_selectbox",
            on_change=onchange_for_ccgz,
        )
        process2 = process2 if process2 != "全部" else ""
        process2_param = process2

    # 井筒类型1 - 使用级联查询
    with col4:
        wellbore_type1_options = standard_db.query_wellbore_type1(
            oil_gas_resource_param, process1_param, process2_param, wellbore_type2_param,
            quality_control_param, hse_requirements_param
        )
        wellbore_type1_options.insert(0, "全部")

        # 确保当前选择在选项列表中
        if wellbore_type1 not in wellbore_type1_options:
            wellbore_type1 = "全部"

        index = wellbore_type1_options.index(wellbore_type1)
        st.session_state[f"{wellbore_type1_key}_selectbox_options"] = wellbore_type1_options
        st.session_state["trigger_select_box"] = f"{wellbore_type1_key}_selectbox"
        wellbore_type1 = st.selectbox(
            "**井筒类型1**",
            wellbore_type1_options,
            index=index,
            key=f"{wellbore_type1_key}_selectbox",
            on_change=onchange_for_ccgz,
        )
        wellbore_type1 = wellbore_type1 if wellbore_type1 != "全部" else ""
        wellbore_type1_param = wellbore_type1

    # 井筒类型2 - 使用级联查询
    with col5:
        wellbore_type2_options = standard_db.query_wellbore_type2(
            oil_gas_resource_param, process1_param, process2_param, wellbore_type1_param,
            quality_control_param, hse_requirements_param
        )
        wellbore_type2_options.insert(0, "全部")

        # 确保当前选择在选项列表中
        if wellbore_type2 not in wellbore_type2_options:
            wellbore_type2 = "全部"

        index = wellbore_type2_options.index(wellbore_type2)
        st.session_state[f"{wellbore_type2_key}_selectbox_options"] = wellbore_type2_options
        st.session_state["trigger_select_box"] = f"{wellbore_type2_key}_selectbox"
        wellbore_type2 = st.selectbox(
            "**井筒类型2**",
            wellbore_type2_options,
            index=index,
            key=f"{wellbore_type2_key}_selectbox",
            on_change=onchange_for_ccgz,
        )
        wellbore_type2 = wellbore_type2 if wellbore_type2 != "全部" else ""
        wellbore_type2_param = wellbore_type2

    # 管理控制点和知识属性：只在储层改造5级中显示
    quality_control = ""
    hse_requirements = ""

    if show_extra_filters:
        # 管理控制点 - 使用级联查询
        with col6:
            quality_control_options = standard_db.query_quality_control(
                oil_gas_resource_param, process1_param, process2_param, wellbore_type1_param, wellbore_type2_param, hse_requirements_param
            )
            quality_control_options.insert(0, "全部")

            # 确保当前选择在选项列表中
            if quality_control not in quality_control_options:
                quality_control = "全部"

            index = quality_control_options.index(quality_control)
            st.session_state[f"{quality_control_key}_selectbox_options"] = quality_control_options
            st.session_state["trigger_select_box"] = f"{quality_control_key}_selectbox"
            quality_control = st.selectbox(
                "**管理控制点**",
                quality_control_options,
                index=index,
                key=f"{quality_control_key}_selectbox",
                on_change=onchange_for_ccgz,
            )
            quality_control = quality_control if quality_control != "全部" else ""
            quality_control_param = quality_control

        # 知识属性 - 使用级联查询
        with col7:
            hse_requirements_options = standard_db.query_hse_requirements(
                oil_gas_resource_param, process1_param, process2_param, wellbore_type1_param, wellbore_type2_param, quality_control_param
            )
            hse_requirements_options.insert(0, "全部")

            # 确保当前选择在选项列表中
            if hse_requirements not in hse_requirements_options:
                hse_requirements = "全部"

            index = hse_requirements_options.index(hse_requirements)
            st.session_state[f"{hse_key}_selectbox_options"] = hse_requirements_options
            st.session_state["trigger_select_box"] = f"{hse_key}_selectbox"
            hse_requirements = st.selectbox(
                "**知识属性**",
                hse_requirements_options,
                index=index,
                key=f"{hse_key}_selectbox",
                on_change=onchange_for_ccgz,
            )
            hse_requirements = hse_requirements if hse_requirements != "全部" else ""

    # 更新对应的前缀的 session_state
    st.session_state[oil_gas_key] = oil_gas_resource
    st.session_state[process1_key] = process1
    st.session_state[process2_key] = process2
    st.session_state[wellbore_type1_key] = wellbore_type1
    st.session_state[wellbore_type2_key] = wellbore_type2
    st.session_state[quality_control_key] = quality_control
    st.session_state[hse_key] = hse_requirements

    # 为了兼容性，也更新原来的 session_state（仅当 submit_type 是 ccgz 或 tiaokuan 时）
    if prefix in ['ccgz', 'tiaokuan']:
        st.session_state.oil_gas_resource_type = oil_gas_resource
        st.session_state.process1 = process1
        st.session_state.process2 = process2
        st.session_state.wellbore_type1 = wellbore_type1
        st.session_state.wellbore_type2 = wellbore_type2
        st.session_state.quality_control = quality_control
        st.session_state.hse_requirements = hse_requirements
    
