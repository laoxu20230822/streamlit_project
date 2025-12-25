import os

from pathlib import Path
import sqlite3

from pandas import DataFrame
import pandas as pd
import streamlit as st

from database.page import Pageable
from database.page import PageResult

import database.sql as sql
from utils.utils import build_single_column_search

CREATE_TABLE_METRICS_SQL = """CREATE TABLE metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增主键
    serial_number INTEGER,  -- 序号
    performance TEXT,  -- 性能
    project TEXT,  -- 项目
    product_category TEXT,  -- 产品类别 new
    table_header_product_name TEXT,  -- 表头产品名称
    product_name TEXT,  -- 产品名称 new
    product_model TEXT,  -- 产品型号 new
    standard_code TEXT,  -- 标准号
    table_code TEXT,  -- 表编号
    table_name TEXT,  -- 表名称
    table_serial INTEGER,  -- 表内序号
    primary_project TEXT,  -- 一级项目名称
    secondary_project TEXT,  -- 二级项目名称
    footnote_symbol TEXT,  -- 脚注符号
    unit TEXT,  -- 计量单位
    experimental_condition TEXT,  -- 实验条件
    indicator_requirement TEXT,  -- 指标要求
    remarks TEXT,  -- 备注
    table_footnote TEXT,  -- 表脚注
    indicator_item TEXT,  -- 指标项/项目
    experimental_condition_type TEXT,  -- 试验条件性质 new
    application_process TEXT,  -- 应用工艺 new
    first_classification TEXT,  -- 一级分类 new
    second_classification TEXT,  -- 二级分类 new
    third_classification TEXT,  -- 三级分类 new
    fourth_classification TEXT  -- 四级分类 new
);
"""
INSET_METRIC = """
INSERT INTO metrics (
    serial_number,
    performance,
    project,
    product_category,
    table_header_product_name,
    product_name,  
    product_model, 
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
    experimental_condition_type,  
    application_process,  
    first_classification,  
    second_classification,  
    third_classification,
    fourth_classification
) VALUES (
    ?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?
);
"""


class Metric:
    def __init__(self):
        db_path = Path(__file__).parent.parent / "standard.db"
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        c = self.conn.cursor()
        c.execute(
            """
        SELECT name FROM sqlite_master WHERE type='table' AND name='metrics'
        """
        )
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

    def batch_insert(self, df: DataFrame):
        # 转换为元组列表（适配 executemany 的参数格式）
        data = [tuple(row) for row in df.itertuples(index=False)]
        c = self.conn.cursor()
        c.executemany(INSET_METRIC, data)
        self.conn.commit()
        # conn.close()

    def query_product_category(self, product_name="", experimental_condition="", indicator_item=""):
        c = self.conn.cursor()
        SELECT_SQL = """
        select distinct product_category from metrics
        where product_name like ? and experimental_condition like ? and indicator_item like ?
        """
        c.execute(SELECT_SQL, (f"%{product_name}%", f"%{experimental_condition}%", f"%{indicator_item}%"))
        return [row[0] for row in c.fetchall() if row[0] and row[0].strip() != ""]

    def query_product_name(self, product_category="", experimental_condition="", indicator_item=""):
        c = self.conn.cursor()
        SELECT_SQL = """
        select distinct product_name from metrics
        where product_category like ? and experimental_condition like ? and indicator_item like ?
        """
        c.execute(SELECT_SQL, (f"%{product_category}%", f"%{experimental_condition}%", f"%{indicator_item}%"))
        return [row[0] for row in c.fetchall() if row[0] and row[0].strip() != ""]

    def query_indicator_item(self, product_category="", product_name="", experimental_condition=""):
        c = self.conn.cursor()
        SELECT_SQL = """
        select distinct indicator_item from metrics
        where product_category like ? and product_name like ? and experimental_condition like ?
        """
        c.execute(SELECT_SQL, (f"%{product_category}%", f"%{product_name}%", f"%{experimental_condition}%"))
        return [row[0] for row in c.fetchall() if row[0] and row[0].strip() != ""]

    def query_experimental_condition(self, product_category="", product_name="", indicator_item=""):
        c = self.conn.cursor()
        SELECT_SQL = """
        select distinct experimental_condition from metrics
        where product_category like ? and product_name like ? and indicator_item like ?
        """
        c.execute(SELECT_SQL, (f"%{product_category}%", f"%{product_name}%", f"%{indicator_item}%"))
        return [row[0] for row in c.fetchall() if row[0] and row[0].strip() != ""]

    def query_purpose(self, product_category="", product_name="", experimental_condition="", indicator_item=""):
        """获取用途非空distinct值，支持级联筛选（从standard_system表获取）"""
        c = self.conn.cursor()
        # 构建WHERE条件
        conditions = ["s.purpose IS NOT NULL", "s.purpose != ''"]
        params = []

        if product_category:
            conditions.append("m.product_category LIKE ?")
            params.append(f"%{product_category}%")
        if product_name:
            conditions.append("m.product_name LIKE ?")
            params.append(f"%{product_name}%")
        if experimental_condition:
            conditions.append("m.experimental_condition LIKE ?")
            params.append(f"%{experimental_condition}%")
        if indicator_item:
            conditions.append("m.indicator_item LIKE ?")
            params.append(f"%{indicator_item}%")

        WHERE_clause = " AND ".join(conditions)

        SELECT_SQL = f"""
        SELECT DISTINCT s.purpose
        FROM standard_system s
        INNER JOIN metrics m ON s.standard_code = m.standard_code
        WHERE {WHERE_clause}
        """
        c.execute(SELECT_SQL, params)
        return [row[0] for row in c.fetchall() if row[0] and row[0].strip() != ""]

    def load_from_excel(self, file_path: str):
        df = pd.read_excel(file_path, engine="openpyxl", header=0).fillna("")
        self.batch_insert(df)

    def create_table(self):
        c = self.conn.cursor()
        c.execute(
            """
        SELECT name FROM sqlite_master WHERE type='table' AND name='metrics'
        """
        )
        if not c.fetchone():
            c.execute(CREATE_TABLE_METRICS_SQL)
            self.conn.commit()

    def drop(self):
        c = self.conn.cursor()
        c.execute("DROP TABLE IF EXISTS metrics")
        self.conn.commit()

    # def list_standard_code_by_search_term(self,search_term:str):
    #     c = self.conn.cursor()
    #     SELECT_SQL=f"""
    #     select standard_code from metrics where
    #     indicator_item like '%{search_term}%' or
    #     product_category like '%{search_term}%' or
    #     product_name like '%{search_term}%' or
    #     table_header_product_name like '%{search_term}%' or
    #     primary_project like '%{search_term}%' or
    #     secondary_project like '%{search_term}%' group by standard_code
    #     """
    #     c.execute(SELECT_SQL)

    #     columns = [col[0] for col in c.description]
    #     data = [dict(zip(columns, row)) for row in c.fetchall()]
    #     return data

    def list_by_search_term(self, search_term: str, product_category: str, product_name: str, experimental_condition: str, indicator_item: str, purpose: str = ""):
        """
        where
        indicator_item like '%{search_term}%' or
        product_category like '%{search_term}%' or
        product_name like '%{search_term}%' or
        table_header_product_name like '%{search_term}%' or
        primary_project like '%{search_term}%' or
        secondary_project like '%{search_term}%'
        """

        indicator_item_cause = build_single_column_search(search_term, "indicator_item")
        product_category_cause = build_single_column_search(
            search_term, "product_category"
        )
        product_name_cause = build_single_column_search(search_term, "product_name")
        table_header_product_name_cause = build_single_column_search(
            search_term, "table_header_product_name"
        )
        primary_project_cause = build_single_column_search(
            search_term, "primary_project"
        )
        secondary_project_cause = build_single_column_search(
            search_term, "secondary_project"
        )
        c = self.conn.cursor()
        SELECT_SQL = f"""
        SELECT m.*, i.standard_name
        FROM metrics m
        LEFT JOIN standard_index i ON m.standard_code = i.standard_code
        LEFT JOIN standard_system s ON m.standard_code = s.standard_code
        where
        ( {indicator_item_cause} or
        {product_category_cause} or
        {product_name_cause} or
        {table_header_product_name_cause} or
        {primary_project_cause} or
        {secondary_project_cause} ) and
        m.product_category like '%{product_category}%' and
        m.product_name like '%{product_name}%' and
        m.experimental_condition like '%{experimental_condition}%' and
        m.indicator_item like '%{indicator_item}%' and
        s.purpose like '%{purpose}%'
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
