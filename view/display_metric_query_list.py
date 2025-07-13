import streamlit as st
import pandas as pd
from database.metric import  init_metric_db
from database.standard_index import StandardIndex
from database.standard_db import Pageable, StandardDB
from database.standard_db import WhereCause
from st_aggrid import AgGrid

def display_grid(data:list[dict]):
    df=pd.DataFrame(data if data else [],columns={
        'standard_code': '标准号',
        'standard_name': '标准名称',
        'standard_content': '标准内容',
    })

    grid_options = {
        'suppressNoRowsOverlay': True,
        'columnDefs': [
        { 'field': "standard_code", 'headerName': "标准号"},
        { 'field': "standard_name", 'headerName': "标准名称"},
        { 'field': "standard_content", 'headerName': "标准内容"},
    ],
    'rowSelection': {
            'mode': 'singleRow',
            'checkboxes': False,
            'enableClickSelection': True
        },
        "autoSizeStrategy": {
            "type": "fitGridWidth"
        },
        "pagination": True,
        #"paginationAutoPageSize": True,
        "paginationPageSize": 50
    }
    grid_response = AgGrid(
        df, 
        gridOptions=grid_options,
        #key='asdjflasdjkfl'
        )
    selected_rows=grid_response['selected_rows']
    
    if selected_rows is not None:
        standard_content= [row['standard_content'] for _, row in selected_rows.iterrows()][0]
        st.container(border=True).markdown(standard_content)
        st.session_state.selected_rows=[{'standard_code':row['standard_code'],'standard_name':row['standard_name']} for _, row in selected_rows.iterrows()]
    #     #st.write(test)       # standard_code=row['standard_code']
    #         # standard_name=row['standard_name']
    #     if grid_response['selected_rows'] is not None:
    #             for index,row_chapter in grid_response['selected_rows'].iterrows():
    #                 st.container(border=True).markdown(row_chapter['standard_content'])
    return grid_response

def display_metric_query_list(search_term:str):
    metric=init_metric_db()
    data=metric.list_by_search_term(search_term)

    """
    标准号，表编号，表名称，一级项目名称，二级项目名称,单位，实验条件，指标要求,备注,表脚注
    standard_code,table_code,table_name,primary_project,secondary_project,unit,experimental_condition,indicator_requirement,remarks,table_footnote
    """
    df=pd.DataFrame(data if data else [],columns={
            'standard_code': '标准号',
            'table_code': '表编号',
            'table_name': '表名称',
            'product_name': '产品名称',
            'indicator_item': '指标项',
            'primary_project': '一级项目名称',
            'secondary_project': '二级项目名称',
            'unit': '单位',
            'experimental_condition': '实验条件',
            'indicator_requirement': '指标要求',
            'remarks': '备注',
            'table_footnote': '表脚注'
        })
    grid_options = {
        'suppressNoRowsOverlay': True,
        'columnDefs': [
        { 'field': "standard_code", 'headerName': "标准号"},
        { 'field': "table_code", 'headerName': "表编号"},
        { 'field': "table_name", 'headerName': "表名称"},
        { 'field': "product_name", 'headerName': "产品名称"},
        { 'field': "indicator_item", 'headerName': "指标项"},
        { 'field': "primary_project", 'headerName': "一级项目名称"},
        { 'field': "secondary_project", 'headerName': "二级项目名称"},
        { 'field': "unit", 'headerName': "单位"},
        { 'field': "experimental_condition", 'headerName': "实验条件"},
        { 'field': "indicator_requirement", 'headerName': "指标要求"},
        { 'field': "remarks", 'headerName': "备注"},
        { 'field': "table_footnote", 'headerName': "表脚注"},
    ],
    'rowSelection': {
            'mode': 'singleRow',
            'checkboxes': False,
            'enableClickSelection': True
        },
        "autoSizeStrategy": {
            "type": "fitGridWidth"
        },
        "pagination": True,
        #"paginationAutoPageSize": True,
        "paginationPageSize": 50,
    }
    grid_response = AgGrid(
        df, 
        gridOptions=grid_options,
        #key='asdjflasdjkfl'
        )
    selected_rows=grid_response['selected_rows']
    #  if selected_rows is not None:
        # st.session_state.selected_rows=[{'standard_code':row['standard_code'],'standard_name':row['standard_name']} for _, row in selected_rows.iterrows()]
    if selected_rows is not None:
        metric_term= [row['indicator_item'] for _, row in selected_rows.iterrows()][0]
        standard_code=[row['standard_code'] for _, row in selected_rows.iterrows()][0]
        standard_db=StandardDB()
        metrics_for_standard=standard_db.query_by_metrics(metric_term,standard_code)
        display_grid(metrics_for_standard)


    