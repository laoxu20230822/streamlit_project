import streamlit as st
import pandas as pd
from database.metric import  init_metric_db
from database.standard_index import StandardIndex
from database.standard_db import Pageable
from database.standard_db import WhereCause
from st_aggrid import AgGrid



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
        'columnDefs': [
        { 'field': "standard_code", 'headerName': "标准号"},
        { 'field': "table_code", 'headerName': "表编号"},
        { 'field': "table_name", 'headerName': "表名称"},
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
        }
    }
    grid_response = AgGrid(
        df, 
        gridOptions=grid_options,
        #key='asdjflasdjkfl'
        )



    