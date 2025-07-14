# pages/01_dashboard.py
import streamlit as st
from st_pages import show_pages

# ① 可选：用 st_pages 注册当前这一页（让它出现在 sidebar 的一级菜单里）
show_pages(
    [
        {"path": "pages/01_dashboard.py", "name": "仪表盘"},
    ]
)

# ② 在 sidebar 做一级导航
primary = st.sidebar.selectbox(
    "请选择一级分类",
    ["产品线 A", "产品线 B", "产品线 C"]
)

# ③ 根据一级分类动态生成二级导航
sub_options = {
    "产品线 A": ["A1", "A2", "A3"],
    "产品线 B": ["B1", "B2"],
    "产品线 C": ["C1", "C2", "C3", "C4"],
}
secondary = st.sidebar.selectbox(
    "请选择二级维度",
    sub_options[primary]
)

# ④ 用选中的一级 + 二级去查询／渲染页面主体
st.header(f"{primary} – {secondary} 的数据展示")
# 举例：假装从数据库里拉数据
@st.cache_data
def load_data(line, dim):
    # 这里替换成你真正的查询逻辑
    import pandas as pd
    return pd.DataFrame({
        "指标": ["销量", "营收", "利润"],
        dim: [100, 200, 300]
    })

df = load_data(primary, secondary)
st.table(df)
