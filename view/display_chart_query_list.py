from calendar import c
import uuid
import streamlit as st
from database.chart import init_standard_chart_db
from database.standard_db import  init_standard_db
from database.standard_index import  init_standard_index_db
from database.page import Pageable
from database.standard_db import WhereCause
from st_aggrid import AgGrid, JsCode
import pandas as pd
from view.display_standard_detail import display_standard_detail
from view.display_standard_glossary import display_standard_glossary
from view.display_standard_references import display_standard_references
from view.display_standard_detail import display_standard_detail
from view.display_product_standard import display_product_standard
from view.display_craft_standard import display_craft_standard
from view.display_standard_structure import display_standard_structure
from view.display_standard_tab_info import display_standard_tab_info

imageRenderer = JsCode("""
    class ImageRenderer {
            init(params) {
            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '100');
            this.eGui.setAttribute('height', '100');
            this.eGui.style.objectFit = 'cover';
            this.eGui.style.cursor = 'pointer';
            }
            getGui() {
                console.log(this.eGui);
                return this.eGui;
            }
        }
""")

def show_grid(data):
    df=pd.DataFrame(data if data else [],columns={
            'standard_code': '标准号',
            'standard_name': '标准名称',
            'in_text_number': '文中编号', 
            'in_text_name': '文中名称', 
            'image_file_name': '图文件名称',
        })
    df.insert(0, 'seq', range(1, len(df) + 1))  
    df["standard_info"] = df["standard_code"] + " " + df["standard_name"] + ""
    
    #使用下划线
    #df["image_file_name"]="Q_SY 01017-2018岩石物理分析成果数据存储文件结构"
    df["image_info"] = "/app/static/" + df["image_file_name"].str.replace("/", "_") + ".png"
    grid_options = {
        "suppressNoRowsOverlay": True,
        'columnDefs': [
        { 'field': "seq", 'headerName': "序号",'width':40},
        { 'field': "standard_code", 'headerName': "标准号",'hide':True},
        { 'field': "standard_name", 'headerName': "标准名称",'hide':True},
        { 'field': "in_text_number", 'headerName': "文中编号",'width':100,'hide':True},
        { 'field': "in_text_name", 'headerName': "图片名称",'width':200},
        { 'field': "image_info", 'headerName': "图片",'cellRenderer': imageRenderer,'width':100,'autoHeight':True},
        { 'field': "standard_info", 'headerName': "标准来源"},
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
    return AgGrid(
        df, 
        gridOptions=grid_options,
        height=300,
        # key=str(uuid.uuid4(),
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True
        )


def display_chart_query_list(search_term:str):
    t1, t2, t3 = st.tabs(
            [
                "**图片**",
                "**表格**",
                "**公式**",
            ]
        )
    standard_chart=init_standard_chart_db()
    with t1:
        data=standard_chart.list_all('图片',search_term)
        grid_response=show_grid(data)
    with t2:
        data=standard_chart.list_all('表格',search_term)
        grid_response=show_grid(data)
    with t3:
        data=standard_chart.list_all('公式',search_term)
        grid_response=show_grid(data)
    # df=pd.DataFrame(data if data else [],columns={
    #         'standard_code': '标准号',
    #         'standard_name': '标准名称',
    #         'in_text_number': '文中编号', 
    #         'in_text_name': '文中名称', 
    #         'image_file_name': '图文件名称',
    #     })
    # df.insert(0, 'seq', range(1, len(df) + 1))  
    # df["standard_info"] = df["standard_code"] + " " + df["standard_name"] + ""
    
    # grid_options = {
    #     "suppressNoRowsOverlay": True,
    #     'columnDefs': [
    #     { 'field': "seq", 'headerName': "序号"},
    #     { 'field': "standard_code", 'headerName': "标准号",'hide':True},
    #     { 'field': "standard_name", 'headerName': "标准名称",'hide':True},
    #     { 'field': "in_text_number", 'headerName': "文中编号"},
    #     { 'field': "in_text_name", 'headerName': "文中名称"},
    #     { 'field': "image_file_name", 'headerName': "图文件名称"},
    #     { 'field': "standard_info", 'headerName': "标准信息"},
    # ],
    # 'rowSelection': {
    #         'mode': 'singleRow',
    #         'checkboxes': False,
    #         'enableClickSelection': True
    #     },
    #     "autoSizeStrategy": {
    #         "type": "fitCellContents"
    #     },
    #     "pagination": True,
    #     ##"paginationAutoPageSize": True,
    #     "paginationPageSize": 50
    # }
    # grid_response = AgGrid(
    #     df, 
    #     gridOptions=grid_options,
    #     height=300
    #     #key='asdjflasdjkfl'
    #     )
    # selected_rows=grid_response['selected_rows']
    # if selected_rows is not None:
    #     st.session_state.selected_rows=[{'standard_code':row['standard_code'],'standard_name':row['standard_name']} for _, row in selected_rows.iterrows()]