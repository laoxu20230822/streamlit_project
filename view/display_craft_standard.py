import streamlit as st
from database.standard_db import  init_standard_db
import pandas as pd

def display_craft_standard(standard_code):
    standard_db=init_standard_db()
    data=standard_db.craft_list(standard_code)
          
    df=pd.DataFrame(data,columns={
        'quality_control': '质量控制(施工方)',
        'hse_requirements': '健康、安全与环境控制要求',
        'quality_supervision': '工程质量技术监督(第三方或甲方)',
        'designer': '设计人员',
        'format_template':'格式-模板',
        'parameter_nature':'参数性质',
        'parameter_category':'参数类别',
        'parameter':'参数',
        'method1':'方法1(1计算方法/2录取方法)',
        'method2':'方法2',
        'wellbore_type1':'井筒类型分类',
        'wellbore_type2':'井筒类型分类',
        'process_tech1':'工艺技术1',
        'process_tech2':'工艺技术2',
        'process_tech3':'工艺技术3',
        })
    #st.subheader('引用列表')
    event=st.dataframe(
    df,
    hide_index=True,  # 隐藏默认索引列
    use_container_width=True,
    column_config={
        "quality_control": st.column_config.TextColumn(
            "质量控制(施工方)",
            help="质量控制(施工方)"
        ),
        "hse_requirements": st.column_config.TextColumn(
            "健康、安全与环境控制要求",
            help="健康、安全与环境控制要求"
        ),
        "quality_supervision": st.column_config.TextColumn(
            "工程质量技术监督(第三方或甲方)",
            help="工程质量技术监督(第三方或甲方)"
        ),
        "designer": st.column_config.TextColumn(
            "设计人员",
            help="设计人员"
        ),
        "format_template": st.column_config.TextColumn(
            "格式-模板",
            help="格式-模板"
        ),
        "parameter_nature": st.column_config.TextColumn(
            "参数性质",
            help="参数性质"
        ),
        "parameter_category": st.column_config.TextColumn(
            "参数类别",
            help="参数类别"
        ),
        "parameter": st.column_config.TextColumn(
            "参数",
            help="参数"
        ),
        "method1": st.column_config.TextColumn(
            "方法1(1计算方法/2录取方法)",
            help="方法1(1计算方法/2录取方法)"
        ),
        "method2": st.column_config.TextColumn(
            "方法2",
            help="方法2"
        ),
        "wellbore_type1": st.column_config.TextColumn(
            "井筒类型分类",
            help="井筒类型分类"
        ),
        "wellbore_type2": st.column_config.TextColumn(
            "井筒类型分类",
            help="井筒类型分类"
        ),
        "process_tech1": st.column_config.TextColumn(
            "工艺技术1",
            help="工艺技术1"
        ),
        "process_tech2": st.column_config.TextColumn(
            "工艺技术2",
            help="工艺技术2"
        ),
        "process_tech3": st.column_config.TextColumn(
            "工艺技术3",
            help="工艺技术3"
        ),
    }
    )