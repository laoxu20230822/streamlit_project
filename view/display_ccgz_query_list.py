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
    def onchange_for_level():
        st.session_state.submit_type = "ccgz"
        # st.session_state.search_term = st.session_state.standard_term
        if "selected_rows" in st.session_state:
            del st.session_state["selected_rows"]
    standard_db = init_standard_db()
    col1, col2, col3, col4, col5 = st.columns(5)
    # 新增五个选择框
    oil_gas_resource_options = standard_db.query_oil_gas_resource_type()
    oil_gas_resource_options.insert(0, "全部")
    oil_gas_resource = col1.selectbox(
        "**油气资源类别**", oil_gas_resource_options, on_change=onchange_for_level
    )
    oil_gas_resource = oil_gas_resource if oil_gas_resource != "全部" else ""

    process1_options = standard_db.query_process1()
    process1_options.insert(0, "全部")
    process1 = col2.selectbox(
        "**工艺类型1**", process1_options, on_change=onchange_for_level
    )
    process1 = process1 if process1 != "全部" else ""

    process2_options = standard_db.query_process2()
    process2_options.insert(0, "全部")
    process2 = col3.selectbox(  
        "**工艺类型2**", process2_options, on_change=onchange_for_level
    )
    process2 = process2 if process2 != "全部" else ""

    wellbore_type1_options = standard_db.query_wellbore_type1()
    wellbore_type1_options.insert(0, "全部")
    wellbore_type1 = col4.selectbox(
        "**井筒类型1**", wellbore_type1_options, on_change=onchange_for_level
    )
    wellbore_type1 = wellbore_type1 if wellbore_type1 != "全部" else ""

    wellbore_type2_options = standard_db.query_wellbore_type2()
    wellbore_type2_options.insert(0, "全部")
    wellbore_type2 = col5.selectbox(
        "**井筒类型2**", wellbore_type2_options, on_change=onchange_for_level
    )
    wellbore_type2 = wellbore_type2 if wellbore_type2 != "全部" else ""

    ##tab2.button("查询",on_click=onchange_for_level)
    st.session_state.oil_gas_resource_type = oil_gas_resource
    st.session_state.process1 = process1
    st.session_state.process2 = process2
    st.session_state.wellbore_type1 = wellbore_type1
    st.session_state.wellbore_type2 = wellbore_type2
    
