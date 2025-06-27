import streamlit as st
import pandas as pd
from database.glossary import Glossary

def display_standard_glossary(standard_code:str):
    glossary=Glossary()
    data=glossary.detail(standard_code)

    df=pd.DataFrame(data,columns={
        'entry_code': '术语条目编号',
        'term': '术语词条',
        'english_term': '术语英文',
        'definition': '术语定义',
        })
    event=st.dataframe(df,
    hide_index=True,  # 隐藏默认索引列
    use_container_width=True,
    column_config={
        
        "term": st.column_config.TextColumn(
            "术语词条",
            help="术语词条"
        ),
        "english_term": st.column_config.TextColumn(
            "术语英文",
            help="术语英文"
        ),
        
        "definition": st.column_config.TextColumn(
            "术语定义",
            help="术语定义"
        ),
        "entry_code": st.column_config.TextColumn(
            "术语条目编号",
            help="术语条目编号"
        ),
        
        }
    )