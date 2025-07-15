import os

from pathlib import Path
import sqlite3

from database.sql import standard_system_select_sql
from pandas import DataFrame
import pandas as pd
import streamlit as st

from database.page import Pageable
from database.page import PageResult

import database.sql as sql

CREATE_TABLE_STANDARD_STRUCTURE = """
CREATE TABLE IF NOT EXISTS standard_structure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_code TEXT NOT NULL,
    start_page TEXT NOT NULL,
    title_order INTEGER NOT NULL DEFAULT 0,
    chapter_level TEXT NOT NULL DEFAULT '0',
    chapter_number TEXT  NOT NULL DEFAULT '',
    title_content TEXT  NOT NULL DEFAULT '',
    page_number TEXT  NOT NULL DEFAULT '-1'
);
"""
insert_standard_structure_sql="""
INSERT INTO standard_structure(
    standard_code,
    start_page,
    title_order,
    chapter_level,
    chapter_number,
    title_content,
    page_number
) VALUES (
    ?,?,?,?,?,?,?
)
"""
class WhereCause:
    standard_code: str
    
    def __init__(self,standard_code:str=""):
        self.standard_code= standard_code

    def to_sql(self):
        sql = " WHERE 1=1 "
        if self.standard_code:
            sql += f" AND standard_code like '%{self.standard_code}%' "
        return sql
    

class StandardStructure:
    conn: sqlite3.Connection
    def __init__(self):
        db_path = Path(__file__).parent.parent / 'standard.db'
        self.conn=sqlite3.connect(db_path,check_same_thread=False)
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_structure'
        """)
        if not c.fetchone():
            c.execute(CREATE_TABLE_STANDARD_STRUCTURE)
            self.conn.commit()
        else:
            cursor = c.execute("PRAGMA table_info(standard_structure)")
            db_columns = [row[1] for row in cursor.fetchall()]  # 获取所有数据库列名
    def count(self):
        c = self.conn.cursor()
        c.execute("select count(1) from standard_structure")
        return c.fetchone()[0]
    
    def detail(self,standard_code:str):
        c = self.conn.cursor()
        c.execute(f"select * from standard_structure where standard_code='{standard_code}' order by title_order asc")
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data


    def extract_title(self,item):
        if  not item['chapter_level'] or not item['chapter_number']  or not item['title_content']:
            item['chapter_level']='0'
            item['chapter_number']=""
            item['title_content']=""
        return "&nbsp;&nbsp;&nbsp;&nbsp;"*int(float(item['chapter_level'].strip()))+" "+item['chapter_number']+" "+item['title_content']
    

    def title_list(self,standard_code:str):
        data=self.detail(standard_code)
        titles = {item['chapter_number']:item['title_content'] for item  in data if item['chapter_number']!=''}
        return titles
    
    def detail_to_markdown(self,standard_code:str):
        chapter_title=self.title_list(standard_code)

        return "\n\n".join([len(chapter.split("."))*"&nbsp;&nbsp;&nbsp;&nbsp;"+chapter+" "+title for chapter,title in chapter_title.items() if '3' not in chapter] )

    def create_table(self):
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_structure'
        """)
        if not c.fetchone():
            c.execute(CREATE_TABLE_STANDARD_STRUCTURE)
            self.conn.commit()

    def drop(self):
        c = self.conn.cursor()
        c.execute("drop table standard_structure")
        self.conn.commit()

    def view_standards(self,filter:WhereCause,pageable:Pageable) -> PageResult:
        c = self.conn.cursor()

        #build sql???
        sql=f"{standard_system_select_sql} {filter.to_sql()}"
        count_sql=f"select count(1) from ({sql})"
        sql_with_page=f"{sql} {pageable.limit_sql()}"

        c.execute(count_sql)
        total=c.fetchone()[0]

        c.execute(sql_with_page)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        #conn.close()
        total_page=total//pageable.size
        if total%pageable.size>0:
            total_page+=1
        return PageResult(data,total_page,pageable)
    

    def batch_insert(self,df:DataFrame):
        # 转换为元组列表（适配 executemany 的参数格式）
        data = [tuple(row) for row in df.itertuples(index=False)]
        c = self.conn.cursor()
        c.executemany(insert_standard_structure_sql, data)
        self.conn.commit()
        #conn.close()
    
    def load_from_excel(self,file_path:str):
        xls = pd.ExcelFile(file_path, engine="openpyxl")
        cols = xls.parse(0, nrows=0).columns.tolist()
        df = pd.read_excel(xls, engine='openpyxl',header=0).fillna("")
        self.batch_insert(df)

@st.cache_resource
def init_standard_structure_db():
    print("init standard_structure db")
    return StandardStructure()







