from re import search
import streamlit as st
import pandas as pd
from database.glossary import Glossary, init_glossary_db
from database.standard_db import StandardDB
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
        st.session_state.selected_rows=[{'standard_code':row['standard_code'],'standard_name':row['standard_name'],'min_chapter_clause_code':row['min_chapter_clause_code']} for _, row in selected_rows.iterrows()]
        #st.write(test)       # standard_code=row['standard_code']
            # standard_name=row['standard_name']
        if grid_response['selected_rows'] is not None:
                for index,row_chapter in grid_response['selected_rows'].iterrows():
                    st.container(border=True).markdown(row_chapter['standard_content'])
    return grid_response


def display_glossary_query_list(search_term:str):
    glossary=init_glossary_db()
    data=glossary.list(search_term)
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
    df=pd.DataFrame(data if data else [],columns={
        'term': '术语词条',
        'english_term': '术语英文',
        'definition': '术语定义',
        'standard_code': '标准号',
        'standard_name': '标准名称',
        'entry_code': '术语条目编号',
    })

    grid_options = {
        'suppressNoRowsOverlay': True,
        'columnDefs': [
        { 'field': "term", 'headerName': "术语词条"},
        { 'field': "english_term", 'headerName': "术语英文"},
        { 'field': "definition", 'headerName': "术语定义"},
        { 'field': "standard_code", 'headerName': "标准号"},
        { 'field': "standard_name", 'headerName': "标准名称"},
        { 'field': "entry_code", 'headerName': "术语条目编号"},
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
        ##"paginationAutoPageSize": True,
        "paginationPageSize": 50
    }
    grid_response = AgGrid(
        df, 
        gridOptions=grid_options,
        #key='asdjflasdjkfl'
        )  



    