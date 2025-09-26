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
            "in_text_number": "文中编号",
            "in_text_name": "文中名称",
            "image_file_name": "图文件名称",
        },
    )
    df.insert(0, "seq", range(1, len(df) + 1))
    df["standard_info"] = df["standard_code"] + " " + df["standard_name"] + ""
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
            {
                "field": "seq",
                "headerName": "序号",
                "width": 60,
                "suppressSizeToFit": True,
            },
            {"field": "standard_info", "headerName": "标准来源", "width": 400},
             {
                "field": "standard_code",
                "headerName": "标准号",
                "hide": True,
            },
            {"field": "standard_name", "headerName": "标准名称", "hide": True},
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
    }
    return AgGrid(
        df,
        gridOptions=grid_options,
        height=300,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
    )

def display_ccgz_query_list(search_term):
    # standard_index = init_standard_index_db()
    
    standard_db = init_standard_db()
    st.session_state.level1
    data=standard_db.fetch_by_ccgz(
        st.session_state.level1,
        st.session_state.level2,
        st.session_state.level3,
        st.session_state.level4,
        st.session_state.level5)
    
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