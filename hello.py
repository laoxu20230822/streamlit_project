import streamlit as st
from st_pages import add_page_title, get_nav_from_toml, hide_pages
#from streamlit_extras.app_logo import add_logo
#add_logo("images/image19.png")  # 支持本地文件，也支持 URL

#向上移动
st.markdown(
    """
    <style>
      /* 隐藏顶部的header空白区域 */
      [data-testid="stHeader"] {
        display: none;
      }
      
      /* 减少主容器的顶部内边距 */
      [data-testid="stMainBlockContainer"] {
        padding-top: 0rem !important;
        margin-top: -2rem !important;
      }
      
      /* 减少应用容器的顶部内边距 */
      [data-testid="stAppViewContainer"] {
        padding-top: 0rem !important;
      }
      
      /* 调整顶部工具栏位置 */
      [data-testid="stToolbar"] {
        top: 0rem !important;
        right: 0.5rem !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

home_page =st.Page("home.py", title="首页", icon="🏠")
load_data_page = st.Page("pages/load_data.py", title="加载数据", icon="📂")

pg = st.navigation([home_page,load_data_page,])
#https://docs.streamlit.io/develop/tutorials/multipage/dynamic-navigation

st.set_page_config(layout="wide")

pg.run()

