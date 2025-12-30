from typing import Optional
from re import search
import streamlit as st
import pandas as pd
from database.glossary import Glossary, init_glossary_db
from database.standard_db import StandardDB
from database.standard_index import StandardIndex
from database.standard_db import Pageable
from database.standard_db import WhereCause
from st_aggrid import AgGrid
from view.display_standard_tab_info import display_standard_tab_info
from utils.data_utils import count_unique_standard_codes



def display_grid(data:list[dict]):
    df=pd.DataFrame(data if data else [],columns={
        'standard_code': '标准号',
        'standard_name': '标准名称',
        'min_chapter_clause_code': '最小章节编号',
        'standard_content': '标准内容',
    })

    grid_options = {
        "defaultColDef": {
            "filter": True,           # 开启过滤
            #"floatingFilter": True,   # 列头下方的小输入框
            "sortable": True,         # 可排序
            "resizable": True         # 可拖动列宽
        },
        "enableCellTextSelection": True,
         'suppressNoRowsOverlay': True,
        'columnDefs': [
        { 'field': "standard_code", 'headerName': "标准号",'hide':True},
        { 'field': "standard_name", 'headerName': "标准名称",'hide':True},
        { 'field': "min_chapter_clause_code", 'headerName': "最小章节编号"},
        { 'field': "standard_content", 'headerName': "标准内容"},
    ],
    'rowSelection': {
            'mode': 'singleRow',
            'checkboxes': False,
            'enableClickSelection': True
        },
        "autoSizeStrategy": {
            "type": "fitCellContents"
        },
        "pagination": True,
        #"paginationAutoPageSize": True,
        "paginationPageSize": 50
    }
    # 显示统计信息
    unique_count = count_unique_standard_codes(df)
    st.markdown(f"**查询标准总数: {unique_count}**")

    grid_response = AgGrid(
        df, 
        gridOptions=grid_options,
        height=300,
        #key='asdjflasdjkfl'
        )
    selected_rows=grid_response['selected_rows']
    if selected_rows is not None:
        st.session_state.selected_rows=[{'standard_code':row['standard_code'],'standard_name':row['standard_name'],'min_chapter_clause_code':row['min_chapter_clause_code']} for _, row in selected_rows.iterrows()]
        #st.write(test)       # standard_code=row['standard_code']
            # standard_name=row['standard_name']
        if grid_response['selected_rows'] is not None:
                for index,row_chapter in grid_response['selected_rows'].iterrows():
                    st.container(border=True).markdown(row_chapter['standard_content'])
    return grid_response


def display_glossary_query_list(search_term: str = "",
                               oil_gas_resource_type: str = "",
                               process1: str = "",
                               process2: str = "",
                               wellbore_type1: str = "",
                               wellbore_type2: str = "",
                               quality_control: str = "",
                               hse_requirements: str = "",
                               data: Optional[list[dict]] = None):
    # 如果传入了data参数，直接使用，否则执行查询
    if data is None:
        glossary = init_glossary_db()

        # 检查搜索词是否变化，如果变化则重置筛选条件
        last_search_term = st.session_state.get("glossary_last_search_term", "")
        if search_term != last_search_term:
            # 重置所有筛选条件
            prefix = "shuyu"
            for key_suffix in ["oil_gas_resource_type", "process1", "process2", "wellbore_type1", "wellbore_type2", "quality_control", "hse_requirements"]:
                st.session_state[f"{prefix}_{key_suffix}"] = ""
            st.session_state["glossary_last_search_term"] = search_term

        # 只使用搜索词查询，不应用筛选条件（筛选条件在pandas层处理）
        data = glossary.list_with_filters(
            search_term=search_term,
            oil_gas_resource_type="",
            process1="",
            process2="",
            wellbore_type1="",
            wellbore_type2="",
            quality_control="",
            hse_requirements=""
        )
    # for item in data:
    #     st.markdown(f"""**术语词条：** {item['term']}   **术语英文：** {item['english_term']}""")
    #     st.markdown(f"""**术语定义：** {item['definition']}""")
    #     st.markdown(f"""**标准号**：{item['standard_code']}   **标准名**：{item['standard_name']}   **术语条目编号**： {item['entry_code']}""")
    #     st.markdown("---")
    # for row in page_result.data:
    #     label=f"**{row['standard_name']}({row['standard_code']})**"
    #     with st.container(border=True):
    #         st.markdown(label)
    #         data=standard_db.standard_detail(row['standard_code'])
    #         grid_response=display_grid(data)

    # 构建DataFrame，包含展示字段和筛选字段
    df=pd.DataFrame(data if data else [])

    # 确保所有需要的列都存在（如果数据中没有，创建空列）
    required_columns = [
        'term', 'english_term', 'definition', 'standard_code',
        'standard_name', 'entry_code', 'oil_gas_resource_type',
        'process1', 'process2', 'wellbore_type1', 'wellbore_type2',
        'quality_control', 'hse_requirements'
    ]
    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    # 只保留需要的列，并按指定顺序排列
    df = df[required_columns]

    # 存储完整的基础DataFrame到session_state（不应用筛选）
    st.session_state.glossary_base_df = df

    # 在pandas层应用筛选条件
    if oil_gas_resource_type:
        df = df[df['oil_gas_resource_type'].astype(str).str.contains(oil_gas_resource_type, na=False)]
    if process1:
        df = df[df['process1'].astype(str).str.contains(process1, na=False)]
    if process2:
        df = df[df['process2'].astype(str).str.contains(process2, na=False)]
    if wellbore_type1:
        df = df[df['wellbore_type1'].astype(str).str.contains(wellbore_type1, na=False)]
    if wellbore_type2:
        df = df[df['wellbore_type2'].astype(str).str.contains(wellbore_type2, na=False)]
    if quality_control:
        df = df[df['quality_control'].astype(str).str.contains(quality_control, na=False)]
    if hse_requirements:
        df = df[df['hse_requirements'].astype(str).str.contains(hse_requirements, na=False)]

    grid_options = {
        "defaultColDef": {
            "filter": True,           # 开启过滤
            #"floatingFilter": True,   # 列头下方的小输入框
            "sortable": True,         # 可排序
            "resizable": True         # 可拖动列宽
        },
        "enableCellTextSelection": True,
        'suppressNoRowsOverlay': True,
        'columnDefs': [
        { 'field': "term", 'headerName': "术语词条",'width': 150},
        { 'field': "english_term", 'headerName': "术语英文",'width': 150},
        { 'field': "definition", 'tooltipField':'definition', 'headerName': "术语定义", 'width': 400, 'autoHeight': True, "wrapText": True, 'cellStyle': {
                    'whiteSpace': 'pre-wrap',  # 保留原始换行符和空格
                    'wordBreak': 'normal'      # 正常的单词换行规则
                }},
        { 'field': "standard_code", 'headerName': "标准号",'width': 150},
        { 'field': "standard_name", 'headerName': "标准名称",'width': 150},
        { 'field': "entry_code", 'headerName': "术语条目编号",'width': 100},
        # 筛选字段列（隐藏但保留在数据中，供selectbox使用）
        { 'field': "oil_gas_resource_type", 'hide': True },
        { 'field': "process1", 'hide': True },
        { 'field': "process2", 'hide': True },
        { 'field': "wellbore_type1", 'hide': True },
        { 'field': "wellbore_type2", 'hide': True },
        { 'field': "quality_control", 'hide': True },
        { 'field': "hse_requirements", 'hide': True },
    ],
    'rowSelection': {
            'mode': 'singleRow',
            'checkboxes': False,
            'enableClickSelection': True
        },
        # "autoSizeStrategy": {
        #     "type": "fitCellContents"
        # },
        "pagination": True,
        ##"paginationAutoPageSize": True,
        "paginationPageSize": 50
    }
    # 显示统计信息
    unique_count = count_unique_standard_codes(df)
    st.markdown(f"**查询标准总数: {unique_count}**")

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        height=500
        #key='asdjflasdjkfl'
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

    