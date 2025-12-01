from operator import index
import streamlit as st
import pandas as pd
from database.standard_structure import  init_standard_structure_db
from database.standard_db import init_standard_db
from streamlit_extras.stylable_container import stylable_container


if 'chapter_content' in st.session_state:
    #remove chapter_content
    del st.session_state.chapter_content
if 'chapter' in st.session_state:
    del st.session_state.chapter

def handle_click(**kwargs):
    st.session_state.chapter=kwargs['chapter']


def display_standard_structure(standard_code:str):

    standard_structure=init_standard_structure_db()
    standard_db=init_standard_db()
    standard_detail=standard_db.standard_detail(standard_code)
    def group_by_key(arr,key):
        return {k: [d['standard_content'] for d in arr if d[key] == k] for k in set(item[key] for item in arr)}
    chapter_content=group_by_key(standard_detail,'min_chapter_code')
    ##在这里处理chapter_content即可，是一个数组

    st.session_state.chapter_content=chapter_content
    chapter_title=standard_structure.title_list(standard_code)
    def display_title(chapter:str,title:str,key:str):
        css_styles="""
                    button {
                        all: unset; 
                        #color: red;
                        #line-height: 1;
                        display: block;
                        cursor: pointer;
                        # margin:10px;
                        # padding:10px;
                        #border: 1px solid #ccc;
                    }
                    """
        with stylable_container(key=key,css_styles=css_styles):
            content = len(chapter.split("."))*"&nbsp;&nbsp;&nbsp;&nbsp;"+chapter+" "+title
            if '3' not in  chapter:
                st.button(content,key=key,kwargs={"chapter":chapter},on_click=handle_click)

    import uuid;
    for chapter,title in chapter_title.items():
        display_title(chapter,title,str(uuid.uuid4()))
    
    