import streamlit as st

# 设置 sidebar 的 logo 和标题（使用列布局）
with st.sidebar:
    # 创建两列：一列放 logo，一列放文字
    col1, col2 = st.columns([1, 3])  # 可以调整比例
    with col1:
        st.image("images/logo.png", width=40)  # 替换为你的 logo 路径
    with col2:
        st.markdown("""
        <h3 style='margin-top: 0; margin-bottom: 0;'>我的系统</h3>
        <p style='font-size: 12px; color: gray;'>副标题描述</p>
        """, unsafe_allow_html=True)

    st.markdown("---")  # 分隔线

    # 首页菜单和其他菜单
    page = st.radio("导航", ["首页", "数据分析", "设置"], label_visibility="collapsed")

# 根据菜单选择渲染主内容
if page == "首页":
    st.title("欢迎来到首页")
elif page == "数据分析":
    st.title("数据分析页面")
elif page == "设置":
    st.title("设置页面")
