# streamlit_aggrid_tooltip_demo_fixed.py
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

st.set_page_config(layout="wide")
st.title("AG Grid Tooltip Demo（修正版）")

# 数据
data = {
    "id": [1, 2, 3],
    "title": ["短标题", "中等标题", "很长很长的标题用来演示 Tooltip 的效果"],
    "description": [
        "这是第一条很长的描述文本，用来测试当单元格文本超出长度时只显示一部分并且在鼠标悬停时显示完整内容。它包含多句子，以便能看出 tooltip 的效果。",
        "第二条描述也比较长：AG Grid 的 tooltip 可以直接显示字段内容，这里我们演示如何在 Streamlit 中使用 tooltipField 来显示完整文本。",
        "第三条描述更长一些，包含更多细节，目的是确保即便文本非常长，悬浮仍然可以看到完整内容。你可以把鼠标移到该单元格上来查看完整文本。"
    ]
}
df = pd.DataFrame(data)

# 生成短文本列（前 50 字）
MAX_CHARS = 10
df["description_short"] = df["description"].apply(lambda s: s if len(str(s)) <= MAX_CHARS else str(s)[:MAX_CHARS] + "...")

# gridOptions（使用 dict/json 配置）
grid_options = {
    "defaultColDef": {
        "sortable": True,
        "filter": True,
        "resizable": True,
        # tooltip 的显示延迟（ms），可选
        "tooltipShowDelay": 200
    },
    "columnDefs": [
        {"field": "id", "headerName": "ID", "minWidth": 60},
        {"field": "title", "headerName": "标题", "minWidth": 200},
        {
            # 前端显示短文本列
            "field": "description_short",
            "headerName": "描述（前50字）",
            # 鼠标悬停显示完整 description 字段
            "tooltipField": "description",
            "minWidth": 400,
            # 不让单元格内容自动换行（可根据需要调整）
            "wrapText": False,
            "autoHeight": False
        }
    ],
    "rowSelection": "single",
    #"animateRows": True
}

st.markdown("表格仅显示 `description_short`（前 50 字），鼠标悬停将显示完整 `description` 文本。")

# 渲染表格
AgGrid(
    df,
    gridOptions=grid_options,
    height=300,
    fit_columns_on_grid_load=True
)
