import streamlit as st
from st_pages import add_page_title, get_nav_from_toml, hide_pages
#from streamlit_extras.app_logo import add_logo
#add_logo("images/image19.png")  # 支持本地文件，也支持 URL

#向上移动
st.markdown(
    """
    <style>
      /* 针对 data-testid="stMainBlockContainer" 的容器，覆盖它的上内边距 */
      [data-testid="stMainBlockContainer"] {
        padding-top: 1.1rem;    /* 默认可能是 2rem 左右，你可以根据需要调小 */
        margin-top: 0;          /* 如果还有外边距，也可以同时清零 */
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

# If you want to use the no-sections version, this
# defaults to looking in .streamlit/pages.toml, so you can
# just call `get_nav_from_toml()`
#nav = get_nav_from_toml(".streamlit/pages.toml")
#hide_pages(["加载数据"])

#st.logo("images/image18.png",size='large')

#pg = st.navigation(nav)

#add_page_title(pg)


#pg.run()