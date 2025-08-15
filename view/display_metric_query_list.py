import streamlit as st
import pandas as pd
from database.metric import init_metric_db
from database.standard_index import StandardIndex
from database.standard_db import Pageable, StandardDB
from database.standard_db import WhereCause
from st_aggrid import AgGrid
from database.standard_structure import StandardStructure


def display_details(data: list[dict]):
    df = pd.DataFrame(
        data if data else [],
        columns={
            "standard_code": "标准号",
            "standard_name": "标准名称",
            "standard_content": "标准内容",
        },
    )

    # builder = GridOptionsBuilder.from_dataframe(data)
    # builder.configure_default_column(wrapText=True, autoHeight=True)
    # builder.configure_grid_options(domLayout='normal')  # 允许自动高度

    grid_options = {
        "suppressNoRowsOverlay": True,
        "columnDefs": [
            {
                "field": "standard_code",
                "headerName": "标准号",
                "wrapText": True,
                "autoHeight": True,
            },
            {
                "field": "standard_name",
                "headerName": "标准名称",
                "wrapText": True,
                "autoHeight": True,
            },
            {
                "field": "standard_content",
                "headerName": "标准内容",
                "wrapText": True,
                "autoHeight": True,
            },
        ],
        "rowSelection": {
            "mode": "singleRow",
            "checkboxes": False,
            "enableClickSelection": True,
        },
        "autoSizeStrategy": {"type": "fitCellContents"},
        "pagination": True,
        # "paginationAutoPageSize": True,
        "paginationPageSize": 50,
    }
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        # fit_columns_on_grid_load=False,
        # allow_unsafe_jscode=True
        # key='asdjflasdjkfl'
    )
    selected_rows = grid_response["selected_rows"]

    # if selected_rows is not None:
    #    standard_content= [row['standard_content'] for _, row in selected_rows.iterrows()][0]
    #    st.container(border=True).markdown(standard_content)
    #    st.session_state.selected_rows=[{'standard_code':row['standard_code'],'standard_name':row['standard_name']} for _, row in selected_rows.iterrows()]
    #     #st.write(test)       # standard_code=row['standard_code']
    #         # standard_name=row['standard_name']
    #     if grid_response['selected_rows'] is not None:
    #             for index,row_chapter in grid_response['selected_rows'].iterrows():
    #                 st.container(border=True).markdown(row_chapter['standard_content'])
    return grid_response


def display_metric_query_list(search_term: str):
    metric = init_metric_db()
    data = metric.list_by_search_term(search_term)

    """
    标准号，表编号，表名称，一级项目名称，二级项目名称,单位，实验条件，指标要求,备注,表脚注
    standard_code,table_code,table_name,primary_project,secondary_project,unit,experimental_condition,indicator_requirement,remarks,table_footnote
    """
    df = pd.DataFrame(
        data if data else [],
        columns={
            "standard_code": "标准号",
            "table_code": "表编号",
            "table_name": "表名称",
            "product_name": "产品名称",
            "indicator_item": "指标项",
            "primary_project": "一级项目名称",
            "secondary_project": "二级项目名称",
            "unit": "单位",
            "experimental_condition": "实验条件",
            "indicator_requirement": "指标要求",
            "remarks": "备注",
            "table_footnote": "表脚注",
        },
    )
    grid_options = {
        "suppressNoRowsOverlay": True,
        "columnDefs": [
            {"field": "standard_code", "headerName": "标准号"},
            {"field": "table_code", "headerName": "表编号"},
            {"field": "table_name", "headerName": "表名称"},
            {"field": "product_name", "headerName": "产品名称"},
            {"field": "indicator_item", "headerName": "指标项"},
            {"field": "primary_project", "headerName": "一级项目名称"},
            {"field": "secondary_project", "headerName": "二级项目名称"},
            {"field": "unit", "headerName": "单位"},
            {"field": "experimental_condition", "headerName": "实验条件"},
            {"field": "indicator_requirement", "headerName": "指标要求"},
            {"field": "remarks", "headerName": "备注"},
            {"field": "table_footnote", "headerName": "表脚注"},
        ],
        "rowSelection": {
            "mode": "singleRow",
            "checkboxes": False,
            "enableClickSelection": True,
        },
        "autoSizeStrategy": {"type": "fitCellContents"},
        "pagination": True,
        # "paginationAutoPageSize": True,
        "paginationPageSize": 50,
    }
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        # key='asdjflasdjkfl'
    )
    selected_rows = grid_response["selected_rows"]
    #  if selected_rows is not None:
    # st.session_state.selected_rows=[{'standard_code':row['standard_code'],'standard_name':row['standard_name']} for _, row in selected_rows.iterrows()]
    if selected_rows is not None:
        metric_term = [row["indicator_item"] for _, row in selected_rows.iterrows()][0]
        standard_code = [row["standard_code"] for _, row in selected_rows.iterrows()][0]
        standard_db = StandardDB()
        metrics_for_standard = standard_db.query_by_metrics(metric_term, standard_code)
        # display_details(metrics_for_standard)

        filtered_df = df[df["standard_code"] == standard_code]
        display_details_new(standard_code, filtered_df)


def display_details_new(standard_code: str, df: pd.DataFrame):
    # 获取标准号，标准名称，标准内容（目前在02标准中没有产品名称无法进行过滤）
    standard_db = StandardDB()
    structure_db = StandardStructure()
    metrics_for_standard = standard_db.query_by_metrics("", standard_code)

    standard_df = pd.DataFrame(
        metrics_for_standard if metrics_for_standard else [],
        columns={
            "standard_code": "标准号",
            "standard_name": "标准名称",
            "standard_content": "标准内容",
            "paragraph_nature": "段落性质",
        },
    )

    
    standard_content_list = standard_df["standard_content"].tolist()
    # return "\n\n".join(
    #     [
    #         len(chapter.split(".")) * "&nbsp;&nbsp;&nbsp;&nbsp;" + chapter + " " + title
    #         for chapter, title in chapter_title.items()
    #         if "3" not in chapter
    #     ]
    # )

    standard_name = metrics_for_standard[0]["standard_name"]

    # 删除不展示的列
    df = df.drop("standard_code", axis=1)

    # 按product_name分组
    grouped_df = df.groupby("product_name")

    # 设置tab_names
    tab_names = grouped_df.groups.keys()
    tabs = st.tabs([f"**{name}**" for name in tab_names])
    for i, tab_name in enumerate(tab_names):
        with tabs[i]:
            st.container().markdown(
                f"标准编号: **{standard_code}** &nbsp;&nbsp; 标准名称: **{standard_name}**"
            )
            st.markdown("---")
            col1, col2 = st.columns([0.6, 0.4])
            with col1:
                show_metric_grid(df[df["product_name"] == tab_name], i)
            with col2:
                #content = structure_db.detail_to_markdown(standard_code)
                show_content(standard_df)
                #st.container(border=True).markdown(content, unsafe_allow_html=True)


def show_content(df: pd.DataFrame):
    """
            standard_code": "标准号",
            "standard_name": "标准名称",
            "standard_content": "标准内容",
            "paragraph_nature": "段落性质",
    """

    all_lines=[]
    for index, row in df.iterrows():
        all_lines.append(row['standard_content'])
    st.container(border=True,height=400).markdown("\n\n".join(all_lines))

# 选择一个标准号之后，显示该标准号下的所有指标，需要按照产品名称进行过滤
def show_metric_grid(df: pd.DataFrame, tab_index: int):
    grid_options = {
        "suppressNoRowsOverlay": True,
        "columnDefs": [
            {"field": "table_code", "headerName": "表编号"},
            {"field": "table_name", "headerName": "表名称"},
            {"field": "product_name", "headerName": "产品名称"},
            {"field": "indicator_item", "headerName": "指标项"},
            {"field": "primary_project", "headerName": "一级项目名称"},
            {"field": "secondary_project", "headerName": "二级项目名称"},
            {"field": "unit", "headerName": "单位"},
            {"field": "experimental_condition", "headerName": "实验条件"},
            {"field": "indicator_requirement", "headerName": "指标要求"},
            {"field": "remarks", "headerName": "备注"},
            {"field": "table_footnote", "headerName": "表脚注"},
        ],
        "rowSelection": {
            "mode": "singleRow",
            "checkboxes": False,
            "enableClickSelection": False,
        },
        "autoSizeStrategy": {"type": "fitCellContents"},
        "pagination": True,
        # "paginationAutoPageSize": True,
        "paginationPageSize": 50,
    }
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        key=f"grid_{tab_index}",
    )
    # for product_name, group in grouped_df:
    #     st.write(f"产品名称: {product_name}")
    #     st.write(group)
    #     st.write("\n\n")  # 分隔不同产品的输出
