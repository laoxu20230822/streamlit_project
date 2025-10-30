import streamlit as st

from database.standard_db import init_standard_db
from database.metric import init_metric_db

def display_navigator_tab():
    tab1,tab2=st.sidebar.tabs(["标准体系", "储层改造业务5级"])

    with tab1:
        def onchange():
            st.session_state.submit_type = "tixi"
            st.session_state.search_term = st.session_state.standard_term
            if "selected_rows" in st.session_state:
                del st.session_state["selected_rows"]
        
        primary = tab1.selectbox(
        "**请选择一级门类**",
        [
            "基础与通用",
            "储层改造压前评估",
            "方案优化设计",
            "储层改造材料评价",
            "装备及工具",
            "现场施工及控制",
            "测试与压后评估分析",
        ],
        )

        sub_options = {
            "基础与通用": ["术语词汇", "基础试验方法", "其他"],
            "储层改造压前评估": ["储层改造压前评估"],
            "方案优化设计": ["通用设计规范", "压裂方案及工艺设计", "酸化方案及工艺设计"],
            "储层改造材料评价": [
                "压裂液材料及评价",
                "酸液材料及评价",
                "支撑剂及评价",
                "暂堵及其他材料",
            ],
            "装备及工具": ["压裂酸化装备", "压裂酸化工具"],
            "现场施工及控制": ["操作规范", "质量控制", "健康安全与环保"],
            "测试与压后评估分析": ["裂缝监测", "返排测试", "评估分析"],
        }
        
        secondary = tab1.selectbox(
        "**请选择二级门类**", sub_options[primary], on_change=onchange
        )

        st.session_state.primary = primary
        st.session_state.secondary = secondary
    
    with tab2:
        def onchange_for_level():
            st.session_state.submit_type = "ccgz"
            #st.session_state.search_term = st.session_state.standard_term
            if "selected_rows" in st.session_state:
                del st.session_state["selected_rows"]
        standard_db = init_standard_db()
        business_level1_options = standard_db.query_stimulation_business_level1()
        #business_level1_options 再增加一个元素，全部储层改造业务
        business_level1_options.insert(0,"全部")
        level1 = tab2.selectbox(
        "**储层改造业务1级**",
        business_level1_options,on_change=onchange_for_level
        )
        level1=level1 if level1!="全部" else ''
        business_level2_options = standard_db.query_stimulation_business_level2(level1)
        business_level2_options.insert(0,"全部")
        level2 = tab2.selectbox(
        "**储层改造业务2级**",
        business_level2_options,on_change=onchange_for_level
        )
        level2=level2 if level2!="全部" else ''
        business_level3_options = standard_db.query_stimulation_business_level3(level1,level2)
        business_level3_options.insert(0,"全部")
        level3 = tab2.selectbox(
        "**储层改造业务3级**",
        business_level3_options,on_change=onchange_for_level
        )
        level3=level3 if level3!="全部" else ''
        business_level4_options = standard_db.query_stimulation_business_level4(level1,level2,level3)
        business_level4_options.insert(0,"全部")
        level4 = tab2.selectbox(
        "**储层改造业务4级**",
        business_level4_options,on_change=onchange_for_level
        )
        level4=level4 if level4!="全部" else ''
        business_level5_options = standard_db.query_stimulation_business_level5(level1,level2,level3,level4)
        business_level5_options.insert(0,"全部")
        level5 = tab2.selectbox(
        "**储层改造业务5级**",
        business_level5_options,on_change=onchange_for_level
        )
        level5=level5 if level5!="全部" else ''

        ##tab2.button("查询",on_click=onchange_for_level)
        st.session_state.level1 = level1
        st.session_state.level2 = level2
        st.session_state.level3 = level3
        st.session_state.level4 = level4
        st.session_state.level5 = level5
   