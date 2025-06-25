import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from database.standard_db import  StandardDB


standard_db = StandardDB()
page_result = standard_db.list()
#df = pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")
df=pd.DataFrame(page_result.data if page_result.data else [],columns={
        # 'system_serial': '体系编号',
        # 'flow_number': '流水号',
        # 'serial': '序号',
        'standard_code': '标准号',
        'standard_name': '标准名称'
    })
#定制化表格
gb = GridOptionsBuilder.from_dataframe(df)
#gb.configure_column('athlete', header_name="ABC")
#gb.configure_pagination(enabled=True, paginationPageSize=5)
#gb.configure_selection(selection_mode="single", use_checkbox=False)


#需要修复
#grid_options = gb.build()
grid_options = {
    'columnDefs': [
    { 'field': "standard_code", 'headerName': "标准号",'width':'300'},
    { 'field': "standard_name", 'headerName': "标准名称",'width':'300'}
  ],
  'rowSelection': {
        'mode': 'singleRow',
        'checkboxes': False,
        'enableClickSelection': True
    },
    "autoSizeStrategy": {
        "type": "fitGridWidth"
    },
}

available_themes = ["streamlit", "alpine", "balham", "material"]

# Create a selectbox for theme selection
selected_theme = st.selectbox("Theme", available_themes)
grid_response = AgGrid(
    df, 
    gridOptions=grid_options,
    theme='streamlit',
    height=None)
selected_rows = grid_response['selected_rows']

if selected_rows is not  None:
    for index, row in selected_rows.iterrows():
        st.write(row['standard_code'])