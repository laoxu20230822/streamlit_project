import streamlit as st
def display_navigator_tab():
    tab1,tab2=st.sidebar.tabs(["标准体系", "储层改造5级"])

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
        tab2.markdown("**储层改造(TODO)**")
