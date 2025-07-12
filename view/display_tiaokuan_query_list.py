import streamlit as st
import pandas as pd
from database.standard_db import  init_standard_db
from database.standard_index import StandardIndex
from database.standard_db import Pageable
from database.standard_db import WhereCause
from st_aggrid import AgGrid


def display_grid(data:list[dict]):
    df=pd.DataFrame(data if data else [],columns={
        'standard_code': '标准号',
        'standard_name': '标准名称',
        'min_chapter_clause_code': '最小章节编号',
        'standard_content': '标准内容',
    })

    grid_options = {
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
            "type": "fitGridWidth"
        },
        "pagination": True,
        #"paginationAutoPageSize": True,
        "paginationPageSize": 20
    }
    grid_response = AgGrid(
        df, 
        gridOptions=grid_options,
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


def display_tiaokuan_query_list(search_term:str):
    standard_db=init_standard_db()
    page_result=standard_db.list(filter=WhereCause(search_term))
    for row in page_result.data:
        label=f"**{row['standard_name']}({row['standard_code']})**"
        with st.container(border=True):
            st.markdown(label)
            data=standard_db.standard_detail(row['standard_code'])
            grid_response=display_grid(data)
            



    