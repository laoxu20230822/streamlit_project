import streamlit as st
from database.standard_db import  init_standard_db
from database.standard_index import  init_standard_index_db
from database.page import Pageable
from database.standard_db import WhereCause
from st_aggrid import AgGrid
import pandas as pd

def display_standard_query_list():
    #获取standard 列表数据
    #查询standard大表数据
    standard_db=init_standard_db()
    page_result=standard_db.list(filter=WhereCause(st.session_state.search_term),pageable=Pageable(1,50))
    standard_codes=[row['standard_code'] for row in page_result.data]
    #查询索引表
    standard_index=init_standard_index_db()
    data=standard_index.list_by_standard_codes(standard_codes)
    df=pd.DataFrame(data if data else [],columns={
            # 'system_serial': '体系编号',
            # 'flow_number': '流水号',
            # 'serial': '序号',
            'standard_code': '标准号',
            'standard_name': '标准名称',
            'status': '状态',
            'specialty':'专业',
            'release_date': '发布日期',
            'implementation_date': '实施日期'
        })
#     df.style.set_table_styles(
#         [{
#             'selector': 'th',
#             'props': [
#                 ('background-color', '#4CAF50'),
#                 ('color', 'white'),
#                 ('font-family', 'Arial, sans-serif'),
#                 ('font-size', '16px')
#             ]
#         }, 
#         {
#             'selector': 'td, th',
#             'props': [
#                 ('border', '2px solid #4CAF50')
#             ]
#         }]
#    )
    grid_options = {
        "suppressNoRowsOverlay": True,
        'columnDefs': [
        { 'field': "standard_code", 'headerName': "标准号"},
        { 'field': "standard_name", 'headerName': "标准名称"},
        { 'field': "status", 'headerName': "状态"},
        { 'field': "specialty", 'headerName': "专业"},
        { 'field': "release_date", 'headerName': "发布日期"},
        { 'field': "implementation_date", 'headerName': "实施日期"},
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
        ##"paginationAutoPageSize": True,
        "paginationPageSize": 50
    }
    grid_response = AgGrid(
        df, 
        gridOptions=grid_options,
        #key='asdjflasdjkfl'
        )
    selected_rows=grid_response['selected_rows']
    if selected_rows is not None:
        st.session_state.selected_rows=[{'standard_code':row['standard_code'],'standard_name':row['standard_name']} for _, row in selected_rows.iterrows()]
        #st.write(test)       # standard_code=row['standard_code']
            # standard_name=row['standard_name']
    #return grid_response