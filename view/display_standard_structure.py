import streamlit as st
import pandas as pd
from database.standard_structure import StandardStructure

def display_standard_structure(standard_code:str):
    standard_structure=StandardStructure()
    detail_for_markdown=standard_structure.detail_to_markdown(standard_code)
    st.markdown(detail_for_markdown,unsafe_allow_html=True)