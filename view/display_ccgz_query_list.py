import streamlit as st
from database import standard_index
from database.standard_db import init_standard_db
from database.standard_index import init_standard_index_db
from database.standard_db import init_standard_db
from st_aggrid import AgGrid
import pandas as pd
from view.display_standard_tab_info import display_standard_tab_info


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
    df['standard_content'] = df['min_chapter_clause_code'] + '\n' + df['standard_content']
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
    )

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
