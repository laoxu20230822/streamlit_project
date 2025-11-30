import streamlit as st
from database.standard_db import init_standard_db
import pandas as pd


def display_product_standard(standard_code):
    standard_db = init_standard_db()
    data = standard_db.product_list(standard_code)

    df = pd.DataFrame(
        data,
        columns={
            "performance_indicator_level1": "一级性能指标",
            "performance_indicator_level2": "二级性能指标",
            "method_name": "方法名称",
            "sample_preparation": "样本制备",
            "equipment_materials": "设备材料",
            "product_category1": "一级产品分类",
            "product_category2": "二级产品分类",
            "product_name": "产品名称",
        },
    )
    # st.subheader('引用列表')
    event = st.dataframe(
        df,
        hide_index=True,  # 隐藏默认索引列
        width="stretch",
        column_config={
            "performance_indicator_level1": st.column_config.TextColumn(
                "一级性能指标", help="一级性能指标"
            ),
            "performance_indicator_level2": st.column_config.TextColumn(
                "二级性能指标", help="二级性能指标"
            ),
            "method_name": st.column_config.TextColumn("方法名称", help="方法名称"),
            "sample_preparation": st.column_config.TextColumn(
                "样本制备", help="样本制备"
            ),
            "equipment_materials": st.column_config.TextColumn(
                "设备材料", help="设备材料"
            ),
            "product_category1": st.column_config.TextColumn(
                "一级产品分类", help="一级产品分类"
            ),
            "product_category2": st.column_config.TextColumn(
                "二级产品分类", help="二级产品分类"
            ),
            "product_name": st.column_config.TextColumn("产品名称", help="产品名称"),
        },
    )
