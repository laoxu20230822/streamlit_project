import streamlit as st
import pandas as pd
from streamlit.elements.lib.layout_utils import Height
from database.metric import  init_metric_db
from database.standard_index import StandardIndex
from database.standard_db import Pageable, StandardDB
from database.standard_db import WhereCause
from st_aggrid import AgGrid,GridOptionsBuilder

from database.standard_structure import StandardStructure





# def display_grid(data:list[dict]):
#     df=pd.DataFrame(data if data else [],columns={
#         'standard_code': '标准号',
#         'standard_name': '标准名称',
#         'standard_content': '标准内容',
#     })

#     grid_options = {
#         'suppressNoRowsOverlay': True,
#         'columnDefs': [
#         { 'field': "standard_code", 'headerName': "标准号"},
#         { 'field': "standard_name", 'headerName': "标准名称"},
#         { 'field': "standard_content", 'headerName': "标准内容"},
#     ],
#     'rowSelection': {
#             'mode': 'singleRow',
#             'checkboxes': False,
#             'enableClickSelection': True
#         },
#         "autoSizeStrategy": {
#             "type": "fitCellContents"
#         },
#         "pagination": True,
#         #"paginationAutoPageSize": True,
#         "paginationPageSize": 50
#     }
#     grid_response = AgGrid(
#         df, 
#         gridOptions=grid_options,
#         height=300,
#         #key='asdjflasdjkfl'
#         )
#     selected_rows=grid_response['selected_rows']
    
#     if selected_rows is not None:
#         standard_content= [row['standard_content'] for _, row in selected_rows.iterrows()][0]
#         st.container(border=True).markdown(standard_content)
#         st.session_state.selected_rows=[{'standard_code':row['standard_code'],'standard_name':row['standard_name']} for _, row in selected_rows.iterrows()]
#     #     #st.write(test)       # standard_code=row['standard_code']
#     #         # standard_name=row['standard_name']
#     #     if grid_response['selected_rows'] is not None:
#     #             for index,row_chapter in grid_response['selected_rows'].iterrows():
#     #                 st.container(border=True).markdown(row_chapter['standard_content'])
#     return grid_response

# def display_method_query_list(search_term:str):
#     metric=init_metric_db()
#     data=metric.list_standard_code_by_search_term(search_term)
#     standard_db=StandardDB()
#     structure_db=StandardStructure()
#     for item in data:
#         standard_code=item['standard_code']
#         standard_name=standard_db.standard_detail_by_method_query(standard_code,search_term)[0]['standard_name']
#         content=structure_db.detail_to_markdown(standard_code)
#         with st.expander(standard_name+'('+standard_code+')'):
#             st.markdown(content,unsafe_allow_html=True)

def display_method_query_list_new(search_term:str):
    standard_db=StandardDB()
    data=standard_db.query_by_stimulation_business_level2(search_term)
    df=pd.DataFrame(data if data else [],columns={
            'standard_code': '标准号',
            'standard_name': '标准名称',
            'standard_content': '标准内容',
            'stimulation_business_level2':'刺激业务等级2'
        })
    df_pivot = (
        df.groupby(["standard_code", "standard_name", "stimulation_business_level2"])
        .agg({"standard_content": lambda x: "\n".join(x)})  # 把同一类内容拼接
        .reset_index()
        .pivot(index=["standard_code", "standard_name"],
                columns="stimulation_business_level2",
                values="standard_content")
        .reset_index()
    )

    
    
    grid_options = {
            'suppressNoRowsOverlay': True,
            'columnDefs': [
            { 'field': "standard_code", 'headerName': "标准号",'width':120},
            { 'field': "standard_name", 'headerName': "标准名称",'width':200},
            { 'field': "方法提要", 'headerName': "方法提要",'autoHeight':True,'wrapText': False,'cellStyle': {
                    'whiteSpace': 'pre-wrap',  # 保留原始换行符和空格
                    'wordBreak': 'normal'      # 正常的单词换行规则
                }},
            { 'field': "仪器设备、试剂或材料", 'headerName': "仪器设备、试剂或材料",'autoHeight':True,'wrapText': False,'cellStyle': {
                    'whiteSpace': 'pre-wrap',  # 保留原始换行符和空格
                    'wordBreak': 'normal'      # 正常的单词换行规则
                }},
            { 'field': "试验步骤", 'headerName': "试验步骤",'autoHeight':True,'wrapText': False,'cellStyle': {
                    'whiteSpace': 'pre-wrap',  # 保留原始换行符和空格
                    'wordBreak': 'normal'      # 正常的单词换行规则
                }},
            { 'field': "试验数据处理", 'headerName': "试验数据处理",'autoHeight':True,'wrapText': False,'cellStyle': {
                    'whiteSpace': 'pre-wrap',  # 保留原始换行符和空格
                    'wordBreak': 'normal'      # 正常的单词换行规则
                } } # 启用文本换行},
        ],
        'rowSelection': {
                'mode': 'singleRow',
                'checkboxes': False,
                'enableClickSelection': False 
            },
        # "autoSizeStrategy": {
        #     "type": "fitCellContents"
        # },
        "pagination": True,
        #"paginationAutoPageSize": True,
        "paginationPageSize": 50
        }
    # gb_options=GridOptionsBuilder.build()
    # gb_options.update(grid_options)
    
    grid_response = AgGrid(
            df_pivot, 
            gridOptions=grid_options,
            height=500,
            #key='asdjflasdjkfl'
            ) 

    