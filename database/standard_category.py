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

CREATE_STANDARD_CATEGORY_SQL="""
-- 建表语句
CREATE TABLE standard_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     /* 主键 */
    standard_code TEXT '标准号',
    sequence_number INTEGER COMMENT '序号',
    standard_code_1 TEXT COMMENT '标准号1',
    standard_name TEXT COMMENT '标准名称',
    primary_category_id TEXT COMMENT '一级门类编号',
    primary_category TEXT COMMENT '一级门类',
    secondary_category_id TEXT COMMENT '二级门类编号',
    secondary_category TEXT COMMENT '二级门类',
    is_identified TEXT COMMENT '是否识别',
    standard_type TEXT COMMENT '标准类别',
    specialty TEXT COMMENT '专业',
    keywords TEXT COMMENT '关键词',
    functional_category TEXT COMMENT '功能类别',
    purpose_category TEXT COMMENT '目的类别',
    object_category TEXT COMMENT '对象类别',
    scope TEXT COMMENT '标准规定及适用范围',
    content TEXT COMMENT '标准主题内容',
    applicable_boundary TEXT COMMENT '适用界限',
    exclusion_boundary TEXT COMMENT '不适用界限',
    status TEXT COMMENT '状态',
    fracturing_acidizing TEXT COMMENT '压裂/酸化',
    fracturing TEXT COMMENT '压裂',
    acidizing TEXT COMMENT '酸化',
    remarks TEXT COMMENT '备注',
    xml_data TEXT COMMENT 'XML',
    standard_code2 TEXT COMMENT '标准号',
    standard_code_index TEXT COMMENT '标准代号编号',
    standard_code_prefix TEXT COMMENT '标准代号',
    standard_serial_number TEXT COMMENT '标准序列号',
    standard_year TEXT COMMENT '标准年代号'
);
"""

INSERT_STANDARD_CATEGORY_SQL = """
INSERT INTO standard_category (
    standard_code,
    sequence_number,
    standard_code_1,
    standard_name,
    primary_category_id,
    primary_category,
    secondary_category_id,
    secondary_category,
    is_identified,
    standard_type,
    specialty,
    keywords,
    functional_category,
    purpose_category,
    object_category,
    scope,
    content,
    applicable_boundary,
    exclusion_boundary,
    `status`,
    fracturing_acidizing,
    fracturing,
    acidizing,
    remarks,
    xml_data,
    standard_code2,
    standard_code_index,
    standard_code_prefix,
    standard_serial_number,
    standard_year
) VALUES (
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?
)
"""
class WhereCause:
    search_term: str
    
    def __init__(self,search_term:str=""):
        self.search_term= search_term

    def to_sql(self):
        sql = " WHERE 1=1 "
        if self.search_term:
            # sql += f" AND standard_content like '%{self.search_term}%' "
            sql += f"""and (
            standard_content like '%{self.search_term}%' 
            OR performance_indicator_level1 LIKE '%{self.search_term}%'
            OR performance_indicator_level2 LIKE '%{self.search_term}%'
            OR method_name LIKE '%{self.search_term}%'
            OR sample_preparation LIKE '%{self.search_term}%'
            OR equipment_materials LIKE '%{self.search_term}%'
            OR product_category1 LIKE '%{self.search_term}%'
            OR product_category2 LIKE '%{self.search_term}%'
            OR product_name LIKE '%{self.search_term}%'
            OR oil_gas_resource_type LIKE '%{self.search_term}%'
            OR product LIKE '%{self.search_term}%'
            OR process1 LIKE '%{self.search_term}%'
            OR process2 LIKE '%{self.search_term}%'
            OR stimulation_business_level1 LIKE '%{self.search_term}%'
            OR stimulation_business_level2 LIKE '%{self.search_term}%'
            OR stimulation_business_level3 LIKE '%{self.search_term}%'
            OR stimulation_business_level4 LIKE '%{self.search_term}%'
            OR stimulation_business_level5 LIKE '%{self.search_term}%'
            OR quality_control LIKE '%{self.search_term}%'
            OR hse_requirements LIKE '%{self.search_term}%'
            OR quality_supervision LIKE '%{self.search_term}%'
            OR designer LIKE '%{self.search_term}%'
            OR format_template LIKE '%{self.search_term}%'
            OR parameter_nature LIKE '%{self.search_term}%'
            OR parameter_category LIKE '%{self.search_term}%'
            OR parameter LIKE '%{self.search_term}%'
            OR method1 LIKE '%{self.search_term}%'
            OR method2 LIKE '%{self.search_term}%'
            OR wellbore_type1 LIKE '%{self.search_term}%'
            OR wellbore_type2 LIKE '%{self.search_term}%'
            OR process_tech1 LIKE '%{self.search_term}%'
            OR process_tech2 LIKE '%{self.search_term}%'
            OR process_tech3 LIKE '%{self.search_term}%'
            OR offshore LIKE '%{self.search_term}%'
            )
            """
        return sql
    

class StandardCategory:
    conn: sqlite3.Connection
    def __init__(self):
        db_path = Path(__file__).parent.parent / 'standard.db'
        self.conn=sqlite3.connect(db_path,check_same_thread=False)
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_category'
        """)
        if not c.fetchone():
            c.execute(CREATE_STANDARD_CATEGORY_SQL)
            self.conn.commit()
        else:
            cursor = c.execute("PRAGMA table_info(standard_category)")
            db_columns = [row[1] for row in cursor.fetchall()]  # 获取所有数据库列名
    
    def count(self):
        c = self.conn.cursor()
        c.execute("select count(1) from standard_category")
        return c.fetchone()[0]
    
    def detail(self,standard_code:str):
        SELECT_STATEMENT=f"""
        select * from standard_category where standard_code='{standard_code}' 
        """
        c = self.conn.cursor()
        c.execute(SELECT_STATEMENT)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def list_by_categroy(self,category_term:str):
        SELECT_STATEMENT=f"""
        select 
        primary_category_id,
        primary_category,
        secondary_category_id,
        secondary_category,
        count(standard_code) as standard_size
         from standard_category 
         where 
         primary_category like '%{category_term}%' 
         or secondary_category like '%{category_term}%' 
        group by primary_category_id,primary_category,secondary_category_id,secondary_category
        """
        c = self.conn.cursor()
        c.execute(SELECT_STATEMENT)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def batch_insert(self,df:DataFrame):
        # 转换为元组列表（适配 executemany 的参数格式）
        data = [tuple(row) for row in df.itertuples(index=False)]
        c = self.conn.cursor()
        c.executemany(INSERT_STANDARD_CATEGORY_SQL, data)
        self.conn.commit()
        #conn.close()

    def load_from_excel(self,file_path:str):
        df = pd.read_excel(file_path, engine='openpyxl',header=0,sheet_name='储层改造标准目录').fillna('')
        self.batch_insert(df)

    def create_table(self):
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_category'
        """)
        if not c.fetchone():
            c.execute(CREATE_STANDARD_CATEGORY_SQL)
            self.conn.commit()

    def drop(self):
        c = self.conn.cursor()
        c.execute("DROP TABLE IF EXISTS standard_category")
        self.conn.commit()
        #conn.close()

@st.cache_resource
def init_standard_category_db():
    print("init standard_category_db")
    return StandardCategory()




