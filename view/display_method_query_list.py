import streamlit as st
import pandas as pd
from database.metric import  init_metric_db
from database.standard_index import StandardIndex
from database.standard_db import Pageable, StandardDB
from database.standard_db import WhereCause
from st_aggrid import AgGrid

from database.standard_structure import StandardStructure

def display_grid(data:list[dict]):
    df=pd.DataFrame(data if data else [],columns={
        'standard_code': '标准号',
        'standard_name': '标准名称',
        'standard_content': '标准内容',
    })

    grid_options = {
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
        "paginationAutoPageSize": True,
        "paginationPageSize": 20
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

def display_method_query_list(search_term:str):
    metric=init_metric_db()
    data=metric.list_standard_code_by_search_term(search_term)
    standard_db=StandardDB()
    structure_db=StandardStructure()
    for item in data:
        standard_code=item['standard_code']
        standard_name=standard_db.standard_detail(standard_code)[0]['standard_name']
        content=structure_db.detail_to_markdown(standard_code)
        with st.expander(standard_name+'('+standard_code+')'):
            st.markdown(content,unsafe_allow_html=True)
    