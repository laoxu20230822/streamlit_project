# Example from: https://github.com/PablocFonseca/streamlit-aggrid-examples (Author of Streamlit-aggrid)
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import pandas as pd
import numpy as np
import requests

# url = "https://www.ag-grid.com/example-assets/master-detail-data.json"
# r  = requests.get(url)
# data = r.json()


# df = pd.read_json(url)

data = [
    {'部门': '技术部', '职位': '工程师', '姓名': '张三'},
    {'部门': '技术部', '职位': '工程师', '姓名': '李四'},
    {'部门': '技术部', '职位': '经理', '姓名': '王五'},
    {'部门': '市场部', '职位': '专员', '姓名': '赵六'}
]

df = pd.DataFrame(data)

# 按部门和职位双重分组
grouped = df.groupby(['部门', '职位'])

# 转换为嵌套结构
result = [
    {
        '部门': department,
        '职位': position,
        'records': group.to_dict('records')
    }
    for (department, position), group in grouped
]

df = pd.DataFrame(result)
#AgGrid(df, key="original")
#df["records"] = df["成员列表"].apply(lambda x: pd.json_normalize(x))
#
gridOptions = {
    # MasterDetail: refers to a top level grid called a Master Grid having rows that expand
    "masterDetail": True,
    # Like we saw earlier, and enable the selection of a single column
    "rowSelection": "single",
    # the first Column is configured to use agGroupCellRenderer
    "columnDefs": [
        {
            "field": "部门",
            "cellRenderer": "agGroupCellRenderer",
            "checkboxSelection": False,
        },
        {"field": "职位"},
    ],
    "defaultColDef": {
        "flex": 1,
    },
    # provide Detail Cell Renderer Params
    "detailCellRendererParams": {
        # provide the Grid Options to use on the Detail Grid
        "detailGridOptions": {
            "rowSelection": "multiple",
            "suppressRowClickSelection": True,
            "enableRangeSelection": True,
            "pagination": True,
            "paginationAutoPageSize": True,
            "columnDefs": [
                {"field": "部门", "checkboxSelection": False},
                {"field": "职位"},
                {"field": "姓名", "minWidth": 150},
            ],
            "defaultColDef": {
                "sortable": True,
                "flex": 1,
            },
        },
        # get the rows for each Detail Grid
        "getDetailRowData": JsCode(
            """function (params) {
                params.successCallback(params.data.records);
    }"""
        ),
        
    },
    "rowData": result
}

tabs = st.tabs(["Grid", "Underlying Data", "Grid Options", "Grid Return"])

with tabs[0]:
    r = AgGrid(
        df,
        gridOptions=gridOptions,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True,
        key="an_unique_key",
    )

    st.write(r['selected_rows'])

with tabs[1]:
    st.write(data)

with tabs[2]:
    st.write(gridOptions)