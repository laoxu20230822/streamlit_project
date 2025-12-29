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
from utils.utils import build_single_column_search


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
        term_cause=build_single_column_search(search_term,'term')
        english_term_cause=build_single_column_search(search_term,'english_term')
        c.execute(f"select * from glossary where ({term_cause} or {english_term_cause})")
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def list_with_filters(self, search_term: str = "",
                         oil_gas_resource_type: str = "",
                         process1: str = "",
                         process2: str = "",
                         wellbore_type1: str = "",
                         wellbore_type2: str = "",
                         quality_control: str = "",
                         hse_requirements: str = ""):
        """
        带筛选条件的术语查询方法
        通过 standard_code 关联 glossary 和 standard_system 表
        """
        c = self.conn.cursor()

        # 构建术语搜索条件
        where_conditions = ["1=1"]
        if search_term:
            term_cause = build_single_column_search(search_term, 'g.term')
            english_term_cause = build_single_column_search(search_term, 'g.english_term')
            where_conditions.append(f"({term_cause} or {english_term_cause})")

        # 构建筛选条件
        if oil_gas_resource_type:
            where_conditions.append(f"s.oil_gas_resource_type like '%{oil_gas_resource_type}%'")
        if process1:
            where_conditions.append(f"s.process1 like '%{process1}%'")
        if process2:
            where_conditions.append(f"s.process2 like '%{process2}%'")
        if wellbore_type1:
            where_conditions.append(f"s.wellbore_type1 like '%{wellbore_type1}%'")
        if wellbore_type2:
            where_conditions.append(f"s.wellbore_type2 like '%{wellbore_type2}%'")
        if quality_control:
            where_conditions.append(f"s.quality_control like '%{quality_control}%'")
        if hse_requirements:
            where_conditions.append(f"s.hse_requirements like '%{hse_requirements}%'")

        # 构建完整查询SQL，返回glossary表所有字段加上standard_system表的筛选字段
        sql = f"""
        SELECT DISTINCT g.*,
               s.oil_gas_resource_type,
               s.process1,
               s.process2,
               s.wellbore_type1,
               s.wellbore_type2,
               s.quality_control,
               s.hse_requirements
        FROM glossary g
        LEFT JOIN standard_system s ON g.standard_code = s.standard_code
        WHERE {' AND '.join(where_conditions)}
        ORDER BY g.term
        """

        c.execute(sql)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        c.close()
        return data

    def detail(self,standard_code:str):
        c = self.conn.cursor()
        c.execute(f"select * from glossary where standard_code='{standard_code}'")
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def create_table(self):
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='glossary'
        """)
        if not c.fetchone():
            c.execute(CREATE_TABLE_GLOSSARY)
            self.conn.commit()

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




