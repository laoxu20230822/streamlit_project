import os

from pathlib import Path
import sqlite3

from database.sql import standard_system_select_sql
from pandas import DataFrame
import pandas as pd
import streamlit as st

from database.customer import CustomerWhereCause
from database.page import Pageable
from database.page import PageResult

import database.sql as sql


CREATE_TABLE_GLOSSARY="""
CREATE TABLE glossary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     /* 主键 */
    term_id TEXT,                             /* 术语序号 */
    term TEXT  NULL,                       /* 术语词条 */
    english_term TEXT,                        /* 术语英文 */
    derived_terms TEXT,                       /* 派生词 */
    definition TEXT  NULL,                 /* 术语定义 */
    entry_code TEXT,                          /* 术语条目编号 */
    synonyms TEXT,                            /* 同义词/简化词 */
    abbreviation TEXT,                        /* 缩略语 */
    symbol TEXT,                              /* 符号 */
    source TEXT,                              /* 来源 */
    note TEXT,                                /* 注 */
    nature TEXT,                              /* 性质 */
    system_id INTEGER,                        /* 体系序号 */
    standard_code TEXT,                     /* 标准号 */
    standard_name TEXT,                       /* 标准名称 */
    unknown1 TEXT,                            /* 分割列 */
    professional_field TEXT,                  /* 标准所属专业 */
    primary_heading TEXT,                     /* 一级条标题 */
    secondary_heading TEXT,                   /* 二级条标题 */
    tertiary_heading TEXT,                    /* 三级条标题 */
    mentioned_in_tech BOOLEAN,                /* 是否在技术要素中提及 */
    term_length INTEGER                       /* 术语字数 */
);
"""

glossary_insert_sql="""
INSERT INTO glossary (
    term_id,
    term,
    english_term,
    derived_terms,
    definition,
    entry_code,
    synonyms,
    abbreviation,
    symbol,
    source,
    note,
    nature,
    system_id,
    standard_code,
    standard_name,
    unknown1,
    professional_field,
    primary_heading,
    secondary_heading,
    tertiary_heading,
    mentioned_in_tech,
    term_length
) VALUES (
    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
    

class Glossary:
    conn: sqlite3.Connection
    def __init__(self):
        db_path = Path(__file__).parent.parent / 'standard.db'
        self.conn=sqlite3.connect(db_path,check_same_thread=False)
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='glossary'
        """)
        if not c.fetchone():
            c.execute(CREATE_TABLE_GLOSSARY)
            self.conn.commit()
        else:
            cursor = c.execute("PRAGMA table_info(glossary)")
            db_columns = [row[1] for row in cursor.fetchall()]  # 获取所有数据库列名
    def count(self):
        c = self.conn.cursor()
        c.execute("select count(1) from glossary")
        return c.fetchone()[0]
    
    def update_by_standard_code(self,standard_code_old:str,standard_code_new:str):
        c = self.conn.cursor()
        c.execute(f"update glossary set standard_code='{standard_code_new}' where standard_code='{standard_code_old}'")
        self.conn.commit()
    
    def list(self,search_term:str):
        c = self.conn.cursor()
        c.execute(f"select * from glossary where term like '%{search_term}%' or english_term like '%{search_term}%'")
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def detail(self,standard_code:str):
        c = self.conn.cursor()
        c.execute(f"select * from glossary where standard_code='{standard_code}'")
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    
    def drop(self):
        c = self.conn.cursor()
        c.execute("drop table glossary")
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
        c.executemany(glossary_insert_sql, data)
        self.conn.commit()
        #conn.close()

    def load_from_excel(self,file_path:str):
        df = pd.read_excel(file_path, engine='openpyxl',header=0).fillna('')
        self.batch_insert(df)

@st.cache_resource
def init_glossary_db():
    print("init glossary db")
    return Glossary()




