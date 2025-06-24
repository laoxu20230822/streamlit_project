import os

from pathlib import Path
import sqlite3

from database.sql import standard_system_table_schema,insert_standard_system_sql,standard_system_select_sql
from pandas import DataFrame
import pandas as pd
import streamlit as st

from database.customer import CustomerWhereCause
from database.page import Pageable
from database.page import PageResult

import database.sql as sql


class WhereCause:
    standard_name: str
    
    def __init__(self,standard_name:str=""):
        self.standard_name= standard_name

    def to_sql(self):
        sql = " WHERE 1=1 "
        if self.standard_name:
            sql += f" AND standard_name like '%{self.standard_name}%' "
        return sql
    

class StandardDB:
    conn: sqlite3.Connection
    def __init__(self):
        db_path = Path(__file__).parent.parent / 'standard.db'
        self.conn=sqlite3.connect(db_path,check_same_thread=False)
        print(f"dbpath::::: {db_path}")
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_system'
        """)
        if not c.fetchone():
            c.execute(standard_system_table_schema)
            self.conn.commit()
        else:
            cursor = c.execute("PRAGMA table_info(standard_system)")
            db_columns = [row[1] for row in cursor.fetchall()]  # 获取所有数据库列名
            print(db_columns)
    def count(self):
        c = self.conn.cursor()
        c.execute("select count(1) from standard_system")
        return c.fetchone()[0]
    
    def standard_detail(self,standard_code:str):
        c = self.conn.cursor()
        c.execute(f"select * from standard_system where standard_code='{standard_code}'")
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def list(self,filter:WhereCause,pageable:Pageable) -> PageResult:
        c = self.conn.cursor()

        #build sql???
        sql=f"{standard_system_select_sql} {filter.to_sql()}"
        count_sql=f"select count(1) from ({sql})"
        sql_with_page=f"{sql} {pageable.limit_sql()}"

        c.execute(count_sql)
        total=c.fetchone()[0]
        print(f"total: {total}")

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
        data = [tuple(row[:35]) for row in df.itertuples(index=False)]
        c = self.conn.cursor()
        c.executemany(insert_standard_system_sql, data)
        self.conn.commit()
        #conn.close()

    def load_from_excel(self,file_path:str):
        df = pd.read_excel(file_path, engine='openpyxl',header=0)
        self.batch_insert(df)








