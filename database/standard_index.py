import os

from pathlib import Path
import sqlite3

from pandas import DataFrame
import pandas as pd
import streamlit as st

from database.page import Pageable
from database.page import PageResult

CREATE_TABLE_STANDARD_INDEX = """
CREATE TABLE IF NOT EXISTS standard_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增主键
    standard_code TEXT,       -- 标准号
    serial_number INTEGER,       -- 序号
    standard_code_cn TEXT,    -- 标准号(中文)
    standard_name TEXT,       -- 标准名称
    status TEXT,                -- 状态
    professional_category TEXT,  -- 归口专业
    secondary_category TEXT,     -- 二级门类
    applicable_scope TEXT,       -- 适用界限
    specialty TEXT,             -- 专业 
    standard_nature TEXT,       -- 标准性质
    standard_type TEXT,         -- 标准类别
    responsible_unit TEXT,      -- 归口单位
    english_name TEXT,          -- 英文名称
    referenced_files TEXT,       -- 引用文件
    replaced_by TEXT,           -- 被哪个标准代替
    replacing_standard TEXT,    -- 代替标准
    adoption_level TEXT,        -- 采标程度
    adoption_number TEXT,       -- 采标号
    ccs_classification TEXT,    -- CCS分类号
    ics_classification TEXT,    -- ICS分类号
    professional_field TEXT,    -- 专业领域（名称引导元素）
    standardization_object TEXT, -- 标准化对象（名称主体元素）
    object_aspect TEXT,         -- 对象的某个方面（名称补充元素）
    total_pages INTEGER,        -- 总页数
    drafting_unit TEXT,         -- 起草单位
    first_drafting_unit TEXT,   -- 第一起草单位
    drafters TEXT,              -- 起草人
    release_date TEXT NULL,          -- 发布日期
    implementation_date TEXT NULL,  -- 实施日期
    application_scope TEXT,     -- 适用范围
    remarks TEXT,               -- 备注
    domestic_foreign TEXT,      -- 国内/国外
    hierarchy_category TEXT,    -- 层次类别
    org_classification_code TEXT, -- 标准组织分类编号
    standard_code_prefix TEXT,         -- 标准代号
    standard_sequence TEXT,     -- 标准序列号
    standard_year TEXT,         -- 标准年代号
    standard_code_category TEXT, -- 标准代号(归类)
    sequence_number1 TEXT,      -- 标准序列号1
    sequence_number2 TEXT,      -- 标准序列号2
    source_system TEXT,         -- 来源：体系标准
    source_reference TEXT       -- 来源：引用文件
);
"""

INSERT_STANDARD_INDEX = """
INSERT INTO standard_index (
    standard_code, 
    serial_number,
    standard_code_cn, 
    standard_name,
    status, 
    professional_category, 
    secondary_category, 
    applicable_scope,
    specialty, 
    standard_nature, 
    standard_type, 
    responsible_unit,
    english_name, 
    referenced_files, 
    replaced_by, 
    replacing_standard,
    adoption_level, 
    adoption_number, 
    ccs_classification, 
    ics_classification,
    professional_field, 
    standardization_object, 
    object_aspect, 
    total_pages,
    drafting_unit, 
    first_drafting_unit, 
    drafters, 
    release_date,
    implementation_date, 
    application_scope, 
    remarks, 
    domestic_foreign,
    hierarchy_category, 
    org_classification_code, 
    standard_code_prefix,
    standard_sequence, 
    standard_year, 
    standard_code_category,
    sequence_number1, 
    sequence_number2, 
    source_system, 
    source_reference
) VALUES (
    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
    ?,?
)
"""

class StandardIndex:
    conn: sqlite3.Connection
    def __init__(self):
        db_path = Path(__file__).parent.parent / 'standard.db'
        self.conn=sqlite3.connect(db_path,check_same_thread=False)
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_index'
        """)
        if not c.fetchone():
            c.execute(CREATE_TABLE_STANDARD_INDEX)
            self.conn.commit()
        else:
            cursor = c.execute("PRAGMA table_info(standard_index)")
            db_columns = [row[1] for row in cursor.fetchall()]  # 获取所有数据库列名
    def list_by_standard_codes(self,standard_codes:list[str]):
        c = self.conn.cursor()
        c.execute(f"select * from standard_index where standard_code in ({','.join(['?' for _ in standard_codes])})",standard_codes)
        
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data
    
    def count(self):
        c = self.conn.cursor()
        c.execute("select count(1) from standard_index")
        return c.fetchone()[0]
    
    def detail(self,standard_code:str):
        c = self.conn.cursor()
        c.execute(f"select * from standard_index where standard_code='{standard_code}'")
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data[0]



    def drop(self):
        c = self.conn.cursor()
        c.execute("drop table standard_index")
        self.conn.commit()

    

    def batch_insert(self,df:DataFrame):
        #处理日期格式化
        df['发布日期'] = pd.to_datetime(df['发布日期'], errors='coerce').dt.strftime('%Y-%m-%d')
        df['实施日期'] = pd.to_datetime(df['实施日期'], errors='coerce').dt.strftime('%Y-%m-%d')
        # 转换为元组列表（适配 executemany 的参数格式）
        data = [tuple(row[:42]) for row in df.itertuples(index=False)]
        c = self.conn.cursor()
        c.executemany(INSERT_STANDARD_INDEX, data)
        self.conn.commit()
        #conn.close()
    
    def load_from_excel(self,file_path:str):
        df = pd.read_excel(file_path, engine='openpyxl',header=0).fillna('')
        self.batch_insert(df)

@st.cache_resource
def init_standard_index_db():
    print("init standard_index db")
    return StandardIndex()
