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

### 标准号	流水号	提及位置流水号	图片性质	文中编号	文中名称	图文件名称	章条号	正文起始页	页数	页码

CREATE_SQL = """CREATE TABLE IF NOT EXISTS standard_chart (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    standard_code TEXT, -- 标准号
    serial_number TEXT, -- 流水号
    reference_location_serial_number TEXT, -- 提及位置流水号
    image_type TEXT, -- 图片性质
    in_text_number TEXT, -- 文中编号
    in_text_name TEXT, -- 文中名称
    image_file_name TEXT, -- 图文件名称
    chapter_section_number TEXT, -- 章条号
    content_start_page TEXT, -- 正文起始页
    page_count TEXT, -- 页数
    page_number TEXT -- 页码
);
"""

INSERT_SQL = """
INSERT INTO standard_chart (
    standard_code,
    serial_number,
    reference_location_serial_number,
    image_type,
    in_text_number,
    in_text_name,
    image_file_name,
    chapter_section_number,
    content_start_page,
    page_count,
    page_number
) VALUES (
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
);
"""


class StandardChart:
    conn: sqlite3.Connection

    def __init__(self):
        db_path = Path(__file__).parent.parent / "standard.db"
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        c = self.conn.cursor()
        c.execute(
            """
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_chart'
        """
        )
        if not c.fetchone():
            c.execute(CREATE_SQL)
            self.conn.commit()
        else:
            cursor = c.execute("PRAGMA table_info(standard_chart)")
            db_columns = [row[1] for row in cursor.fetchall()]  # 获取所有数据库列名

        # 创建索引以提升查询性能
        self._create_indexes()

    def _create_indexes(self):
        """创建性能优化索引"""
        c = self.conn.cursor()

        # 检查并创建 image_type 索引（用于按图片类型筛选）
        c.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name='idx_standard_chart_image_type'
        """)
        if not c.fetchone():
            c.execute("""
                CREATE INDEX idx_standard_chart_image_type ON standard_chart(image_type)
            """)
            print("Created index: idx_standard_chart_image_type")

        # 检查并创建 standard_code 索引（用于 JOIN 操作）
        c.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name='idx_standard_chart_standard_code'
        """)
        if not c.fetchone():
            c.execute("""
                CREATE INDEX idx_standard_chart_standard_code ON standard_chart(standard_code)
            """)
            print("Created index: idx_standard_chart_standard_code")

        # 检查并创建 in_text_name 索引（用于搜索）
        c.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name='idx_standard_chart_in_text_name'
        """)
        if not c.fetchone():
            c.execute("""
                CREATE INDEX idx_standard_chart_in_text_name ON standard_chart(in_text_name)
            """)
            print("Created index: idx_standard_chart_in_text_name")

        # 检查并创建 image_file_name 索引（用于搜索）
        c.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name='idx_standard_chart_image_file_name'
        """)
        if not c.fetchone():
            c.execute("""
                CREATE INDEX idx_standard_chart_image_file_name ON standard_chart(image_file_name)
            """)
            print("Created index: idx_standard_chart_image_file_name")

        self.conn.commit()

    def list_all(self,image_type:str,search_term:str=''):
        in_text_name_cause=build_single_column_search(search_term,'c.in_text_name')
        image_file_name_cause=build_single_column_search(search_term,'c.image_file_name')
        where_cause=f"""
        c.image_type like '%{image_type}%' and ({in_text_name_cause} or {image_file_name_cause})
        """
        c = self.conn.cursor()
        SQL=f"""
        select c.*,i.standard_name from standard_chart c
        LEFT JOIN standard_index i ON c.standard_code = i.standard_code
        WHERE {where_cause}
        """
        c.execute(
            SQL
        )

        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def list_all_with_filters(self, image_type: str = "",
                             search_term: str = "",
                             oil_gas_resource_type: str = "",
                             process1: str = "",
                             process2: str = "",
                             wellbore_type1: str = "",
                             wellbore_type2: str = "",
                             quality_control: str = "",
                             hse_requirements: str = "",
                             special_condition: str = ""):
        """
        带筛选条件的图表公式查询方法
        通过 standard_code 关联 standard_chart 和 standard_system 表

        Args:
            image_type: 图片类型（可选，为空则查询所有类型）
            ...其他参数
        """
        c = self.conn.cursor()

        # 构建搜索条件
        where_conditions = []
        if image_type:
            where_conditions.append(f"c.image_type like '%{image_type}%'")

        if search_term:
            in_text_name_cause = build_single_column_search(search_term, 'c.in_text_name')
            image_file_name_cause = build_single_column_search(search_term, 'c.image_file_name')
            where_conditions.append(f"({in_text_name_cause} or {image_file_name_cause})")

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
        if special_condition:
            where_conditions.append(f"s.special_condition like '%{special_condition}%'")

        # 构建完整查询SQL
        where_clause = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""
        sql = f"""
        SELECT c.*, i.standard_name, s.oil_gas_resource_type,
        s.process1, s.process2, s.wellbore_type1, s.wellbore_type2,
        s.quality_control, s.hse_requirements, s.special_condition
        FROM standard_chart c
        LEFT JOIN (
            SELECT standard_code, standard_name
            FROM standard_index
            GROUP BY standard_code
        ) i ON c.standard_code = i.standard_code
        LEFT JOIN (
            SELECT standard_code,
                   MAX(oil_gas_resource_type) as oil_gas_resource_type,
                   MAX(process1) as process1,
                   MAX(process2) as process2,
                   MAX(wellbore_type1) as wellbore_type1,
                   MAX(wellbore_type2) as wellbore_type2,
                   MAX(quality_control) as quality_control,
                   MAX(hse_requirements) as hse_requirements,
                   MAX(special_condition) as special_condition
            FROM standard_system
            GROUP BY standard_code
        ) s ON c.standard_code = s.standard_code
        {where_clause}
        ORDER BY c.standard_code, c.in_text_number
        """

        c.execute(sql)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        c.close()
        return data
    
    def query_chart_data(self, image_type: str,
                           search_term: str = "",
                           oil_gas_resource_type: str = "",
                           process1: str = "",
                           process2: str = "",
                           wellbore_type1: str = "",
                           wellbore_type2: str = "",
                           quality_control: str = "",
                           hse_requirements: str = "",
                           special_condition: str = ""):
        """
        查询图表公式数据（原始数据）

        Args:
            image_type: 图片类型（图片/表格/公式）
            search_term: 搜索词
            oil_gas_resource_type: 油气资源类别
            process1: 工艺类型1
            process2: 工艺类型2
            wellbore_type1: 井筒类型1
            wellbore_type2: 井筒类型2
            quality_control: 管理控制点
            hse_requirements: 知识属性
            special_condition: 特殊工况

        Returns:
            list: 图表公式数据列表
        """

        return self.list_all_with_filters(
            image_type=image_type,
            search_term=search_term,
            oil_gas_resource_type=oil_gas_resource_type,
            process1=process1,
            process2=process2,
            wellbore_type1=wellbore_type1,
            wellbore_type2=wellbore_type2,
            quality_control=quality_control,
            hse_requirements=hse_requirements,
            special_condition=special_condition
        )

    def query_chart_data_all(self,
                             search_term: str = "",
                             oil_gas_resource_type: str = "",
                             process1: str = "",
                             process2: str = "",
                             wellbore_type1: str = "",
                             wellbore_type2: str = "",
                             quality_control: str = "",
                             hse_requirements: str = "",
                             special_condition: str = ""):
        """
        一次性查询所有类型的图表公式数据（性能优化版本）

        与分别调用三次 query_chart_data 相比，此方法只执行一次数据库查询，
        然后在应用层按 image_type 分组，减少 66% 的数据库访问次数。

        Args:
            search_term: 搜索词
            oil_gas_resource_type: 油气资源类别
            process1: 工艺类型1
            process2: 工艺类型2
            wellbore_type1: 井筒类型1
            wellbore_type2: 井筒类型2
            quality_control: 管理控制点
            hse_requirements: 知识属性
            special_condition: 特殊工况

        Returns:
            dict: 包含三种类型数据的字典
                {
                    'image': [...],   # 图片类型数据
                    'table': [...],  # 表格类型数据
                    'formula': [...]  # 公式类型数据
                }
        """
        # 一次性查询所有类型
        all_data = self.list_all_with_filters(
            image_type="",  # 不限制类型
            search_term=search_term,
            oil_gas_resource_type=oil_gas_resource_type,
            process1=process1,
            process2=process2,
            wellbore_type1=wellbore_type1,
            wellbore_type2=wellbore_type2,
            quality_control=quality_control,
            hse_requirements=hse_requirements,
            special_condition=special_condition
        )

        # 在应用层按 image_type 分组
        result = {
            'image': [],
            'table': [],
            'formula': []
        }

        for item in all_data:
            image_type = item.get('image_type', '')
            if '图片' in image_type:
                result['image'].append(item)
            elif '表格' in image_type:
                result['table'].append(item)
            elif '公式' in image_type:
                result['formula'].append(item)

        return result


    def count(self):
        c = self.conn.cursor()
        c.execute("select count(1) from standard_index")
        return c.fetchone()[0]

    def detail(self, standard_code: str):
        c = self.conn.cursor()
        c.execute(f"select * from standard_index where standard_code='{standard_code}'")
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data[0]

    def create_table(self):
        c = self.conn.cursor()
        c.execute(
            """
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_chart'
        """
        )
        if not c.fetchone():
            c.execute(CREATE_SQL)
            self.conn.commit()

    def drop(self):
        c = self.conn.cursor()
        c.execute("drop table standard_chart")
        self.conn.commit()

    def batch_insert(self, df: DataFrame):
        # 转换为元组列表（适配 executemany 的参数格式）
        data = [tuple(row[:11]) for row in df.itertuples(index=False)]
        c = self.conn.cursor()
        c.executemany(INSERT_SQL, data)
        self.conn.commit()
        # conn.close()

    def load_from_excel(self, file_path: str):
        df = pd.read_excel(file_path, engine="openpyxl", header=0).fillna("")
        self.batch_insert(df)


@st.cache_resource
def init_standard_chart_db():
    print("init standard_chart db")
    return StandardChart()
