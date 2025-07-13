from operator import index
import streamlit as st
import pandas as pd
from database.standard_structure import  init_standard_structure_db

def display_standard_structure(standard_code:str):
    standard_structure=init_standard_structure_db()
    detail_for_markdown=standard_structure.detail_to_markdown(standard_code)

    if '术语和定义' in detail_for_markdown:
        # for line in detail_for_markdown.splitlines():
        #      print(line)
        detail_for_markdown='\n\n'.join([line for line in detail_for_markdown.splitlines() if '3.' not in  line])
    # st.markdown(f"""
    #     <style>
    #     .compact p {{
    #         margin: 0;
    #         line-height: 1.1;
    #     }}
    #     </style><div class="compact">{detail_for_markdown}</div>
    #     """,unsafe_allow_html=True) 
    st.markdown(detail_for_markdown,unsafe_allow_html=True)