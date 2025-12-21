import streamlit as st
import pandas as pd
from database.standard_db import  init_standard_db
from database.standard_index import StandardIndex
from database.standard_db import Pageable
from database.standard_db import WhereCause
from st_aggrid import AgGrid
from utils.data_utils import count_unique_standard_codes


def display_grid(data:list[dict],key:str):
    df=pd.DataFrame(data if data else [],columns={
        'standard_code': '标准号',
        'standard_name': '标准名称',
        'min_chapter_clause_code': '最小章节编号',
        'standard_content': '标准内容',
    })
    #对df的某一列进行过滤，不包含某些内容
    #去掉“前言”
    df=df[~df['standard_content'].str.contains("前言",case=False,na=False)]
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
        { 'field': "min_chapter_clause_code", 'headerName': "最小章节编号",'hide':True},
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
        "paginationPageSize": 20
    }
    grid_response = AgGrid(
        df, 
        gridOptions=grid_options,
        height=300,
        key=key
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


def display_tiaokuan_query_list(search_term: str,
                                oil_gas_resource_type: str = "",
                                process1: str = "",
                                process2: str = "",
                                wellbore_type1: str = "",
                                wellbore_type2: str = "",
                                quality_control: str = "",
                                hse_requirements: str = ""):
    standard_db = init_standard_db()

    # 判断是否使用筛选查询
    use_filters = any([oil_gas_resource_type, process1, process2, wellbore_type1, wellbore_type2, quality_control, hse_requirements])

    if use_filters:
        # 使用带筛选的查询
        data = standard_db.list_for_tiaokuan_with_filters(
            search_term=search_term,
            oil_gas_resource_type=oil_gas_resource_type,
            process1=process1,
            process2=process2,
            wellbore_type1=wellbore_type1,
            wellbore_type2=wellbore_type2,
            quality_control=quality_control,
            hse_requirements=hse_requirements
        )
    else:
        # 使用原有查询方法
        data = standard_db.list_for_tiaokuan(filter=WhereCause(search_term))

    # 对查询结果按标准号分组
    from collections import defaultdict
    grouped_data = defaultdict(list)
    for item in data:
        grouped_data[item['standard_code']].append(item)

    # 在页面顶部显示总体统计信息
    unique_standard_count = len(grouped_data)
    st.markdown(f"**查询标准总数: {unique_standard_count}**")

    # 显示分组后的结果
    for standard_code, items in grouped_data.items():
        if items:  # 确保列表不为空
            first_item = items[0]
            label = f"**{first_item['standard_name']}({first_item['standard_code']})**"
            with st.container(border=True):
                st.markdown(label)
                # 使用当前标准的数据显示grid
                grid_response = display_grid(items, key=f"grid_{standard_code}")
            



    