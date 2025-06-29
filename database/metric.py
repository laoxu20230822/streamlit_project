import os

from pathlib import Path
import sqlite3

from pandas import DataFrame
import pandas as pd
import streamlit as st

from database.customer import CustomerWhereCause
from database.page import Pageable
from database.page import PageResult

import database.sql as sql

CREATE_TABLE_METRICS_SQL="""CREATE TABLE metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增主键
    serial_number INTEGER,  -- 序号
    performance TEXT,  -- 性能
    project TEXT,  -- 项目
    table_header_product_name TEXT,  -- 表头产品名称
    standard_code TEXT,  -- 标准号
    table_code TEXT,  -- 表编号
    table_name TEXT,  -- 表名称
    table_serial INTEGER,  -- 表内序号
    primary_project TEXT,  -- 一级项目名称
    secondary_project TEXT,  -- 二级项目名称
    footnote_symbol TEXT,  -- 脚注符号
    unit TEXT,  -- 单位
    experimental_condition TEXT,  -- 实验条件
    indicator_requirement TEXT,  -- 指标要求
    remarks TEXT,  -- 备注
    table_footnote TEXT,  -- 表脚注
    indicator_item TEXT,  -- 指标项/项目
    product_category TEXT,  -- 产品类别
    product_name TEXT,  -- 产品名称
    product_model TEXT  -- 产品型号
);
"""
INSET_METRIC="""
INSERT INTO metrics (
    serial_number,
    performance,
    project,
    table_header_product_name,
    standard_code,
    table_code,
    table_name,
    table_serial,
    primary_project,
    secondary_project,
    footnote_symbol,
    unit,
    experimental_condition,
    indicator_requirement,
    remarks,
    table_footnote,
    indicator_item,
    product_category,
    product_name,
    product_model
) VALUES (
    ?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,
    ?,?
);
"""   
class Metric:
    def __init__(self):
        db_path = Path(__file__).parent.parent / 'standard.db'
        self.conn=sqlite3.connect(db_path,check_same_thread=False)
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='metrics'
        """)
        if not c.fetchone():
            c.execute(CREATE_TABLE_METRICS_SQL)
            self.conn.commit()
        else:
            cursor = c.execute("PRAGMA table_info(metrics)")
            db_columns = [row[1] for row in cursor.fetchall()]  # 获取所有数据库列名
    
    def count(self):
        c = self.conn.cursor()
        c.execute("select count(1) from metrics")
        return c.fetchone()[0]

    def batch_insert(self,df:DataFrame):
        # 转换为元组列表（适配 executemany 的参数格式）
        data = [tuple(row) for row in df.itertuples(index=False)]
        c = self.conn.cursor()
        c.executemany(INSET_METRIC, data)
        self.conn.commit()
        #conn.close()

    def load_from_excel(self,file_path:str):
        df = pd.read_excel(file_path, engine='openpyxl',header=0)
        self.batch_insert(df)
    
    def drop(self):
        c = self.conn.cursor()
        c.execute("DROP TABLE IF EXISTS metrics")
        self.conn.commit()

    def list_standard_code_by_search_term(self,search_term:str):
        c = self.conn.cursor()
        SELECT_SQL=f"""
        select standard_code from metrics where
        indicator_item like '%{search_term}%' or
        product_category like '%{search_term}%' or
        product_name like '%{search_term}%' or
        table_header_product_name like '%{search_term}%' or
        primary_project like '%{search_term}%' or
        secondary_project like '%{search_term}%' group by standard_code
        """
        c.execute(SELECT_SQL)
        
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data
    
    def list_by_search_term(self,search_term:str):
        c = self.conn.cursor()
        SELECT_SQL=f"""
        select * from metrics where
        indicator_item like '%{search_term}%' or
        product_category like '%{search_term}%' or
        product_name like '%{search_term}%' or
        table_header_product_name like '%{search_term}%' or
        primary_project like '%{search_term}%' or
        secondary_project like '%{search_term}%'
        """
        c.execute(SELECT_SQL)
        
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

@st.cache_resource
def init_metric_db():
    print("init metrics db")
    return Metric()
"""
指标项，产品类别，产品名称，表头产品名称，一级项目名称，二级项目名称
indicator_item,product_category,product_name,table_header_product_name,primary_project,secondary_project
"""
    