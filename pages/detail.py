import streamlit as st
from database import standard_db
from database import standard_structure
from database.standard_db import StandardDB
from database.standard_structure import StandardStructure

standard_code=st.query_params['standard_code']
standard_db=StandardDB()
standard_structure=StandardStructure()
detail=standard_db.standard_detail(standard_code)
detail_for_markdown=standard_structure.detail_to_markdown(standard_code)

with st.container(height=200):
    
    st.markdown(f"""
    :blue[标准代码{detail[0]['standard_code']}]: {detail[0]['standard_code']}
    """)
    st.markdown(f"#### {detail[0]['standard_name']}")

with st.container(height=200):
    st.subheader('标准目次信息')
    
    st.markdown(detail_for_markdown)
st.markdown("---")
with st.container(height=200):
    st.subheader('引用列表')
    st.write('hello world 2')
st.markdown("---",)
with st.container(height=200):
    st.subheader('术语')
    st.write('hello world 2')
st.markdown("---")
with st.container(height=200):
    st.subheader('产品标准')
    st.write('hello world 2')
st.markdown("---")
with st.container(height=200):
    st.subheader('工艺标准')
    st.write('hello world 2')
st.markdown("---")
