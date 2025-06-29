import streamlit as st
import pandas as pd
from database.standard_structure import  init_standard_structure_db

def display_standard_structure(standard_code:str):
    standard_structure=init_standard_structure_db()
    detail_for_markdown=standard_structure.detail_to_markdown(standard_code)
    st.markdown(detail_for_markdown,unsafe_allow_html=True)