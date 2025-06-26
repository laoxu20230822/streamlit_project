import os

from pathlib import Path
import sqlite3

from database.sql import CREATE_TABLE_REFERENCE_STANDARDS,reference_standards_insert_sql
from pandas import DataFrame
import pandas as pd
import streamlit as st

from database.customer import CustomerWhereCause
from database.page import Pageable
from database.page import PageResult

import database.sql as sql


class WhereCause:
    standard_code: str
    
    def __init__(self,standard_code:str=""):
        self.standard_code= standard_code

    def to_sql(self):
        sql = " WHERE 1=1 "
        if self.standard_code:
            sql += f" AND standard_code like '%{self.standard_code}%' "
        return sql
    

class ReferenceStandards:
    conn: sqlite3.Connection
    def __init__(self):
        db_path = Path(__file__).parent.parent / 'standard.db'
        self.conn=sqlite3.connect(db_path,check_same_thread=False)
        print(f"dbpath::::: {db_path}")
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='reference_standards'
        """)
        if not c.fetchone():
            c.execute(CREATE_TABLE_REFERENCE_STANDARDS)
            self.conn.commit()
        else:
            cursor = c.execute("PRAGMA table_info(reference_standards)")
            db_columns = [row[1] for row in cursor.fetchall()]  # 获取所有数据库列名
            print(db_columns)
    def count(self):
        c = self.conn.cursor()
        c.execute("select count(1) from reference_standards")
        return c.fetchone()[0]
    
    def detail(self,standard_code:str):
        c = self.conn.cursor()
        sql=f"""
        select 
        r.cited_standard_original,
        r.cited_standard_normalized,
        r.standard_name_normalized,
        i.status 
        from reference_standards r left join  standard_index i 
        on r.cited_standard_normalized=i.standard_code
        where r.standard_code = '{standard_code}'
        """
        c.execute(sql)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data


    def drop(self):
        c = self.conn.cursor()
        c.execute("drop table reference_standards")
        self.conn.commit()

    def view_standards(self,filter:WhereCause,pageable:Pageable) -> PageResult:
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
        data = [tuple(row) for row in df.itertuples(index=False)]
        c = self.conn.cursor()
        c.executemany(reference_standards_insert_sql, data)
        self.conn.commit()
        #conn.close()
    
    def load_from_excel(self,file_path:str):
        df = pd.read_excel(file_path, engine='openpyxl',header=0)
        self.batch_insert(df)








