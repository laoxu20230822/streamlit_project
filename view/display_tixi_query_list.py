import streamlit as st
from database.standard_category import init_standard_category_db
from database.standard_db import  init_standard_db
from database.standard_index import  init_standard_index_db
from database.page import Pageable
from database.standard_db import WhereCause
from st_aggrid import AgGrid
import pandas as pd


def display_tixi_query_list(search_term:str):
    
    category_db=init_standard_category_db()
    data=category_db.list_by_categroy(search_term)

    

    df=pd.DataFrame(data if data else [],columns={
            'primary_category_id': '一级门类编号',
            'primary_category': '一级门类',
            'secondary_category_id':'二级门类编号',
            'secondary_category': '二级门类',
            'standard_size': '标准数量'
        })
    print(df)
    # 按部门和职位双重分组
    grouped = df.groupby(['primary_category_id', 'primary_category'])

    # 转换为嵌套结构
    result = [
        {
            'primary_category_id': primary_category_id,
            'primary_category': primary_category,
            'records': group.to_dict('records')
        }
        for (primary_category_id,primary_category), group in grouped
    ]
    head1,head2 = st.columns(2)
    head1.markdown(f"""**一级门类**""")
    head2.markdown(f"""**二级门类**""")
    for item in result:
        with st.container(border=True):
            col1,col2=st.columns(2)
            col1.markdown(f"""**{item['primary_category']}**""")
            for record in item['records']:
                col2.markdown(record['secondary_category'])
        
    # grid_options = {
    #     'columnDefs': [
    #     { 'field': "primary_category_id", 'headerName': "一级门类编号"},
    #     { 'field': "primary_category", 'headerName': "一级门类"},
    #     { 'field': "secondary_category_id", 'headerName': "二级门类编号"},
    #     { 'field': "secondary_category", 'headerName': "二级门类"},
    #     { 'field': "standard_size", 'headerName': "标准数量"},
    # ],
    # 'rowSelection': {
    #         'mode': 'singleRow',
    #         'checkboxes': False,
    #         'enableClickSelection': True
    #     },
    #     "autoSizeStrategy": {
    #         "type": "fitGridWidth"
    #     },
    #     "pagination": True,
    #     "paginationAutoPageSize": True,
    #     "paginationPageSize": 20
    # }
    # grid_response = AgGrid(
    #     df, 
    #     gridOptions=grid_options,
    #     #key='asdjflasdjkfl'
    #     )
  