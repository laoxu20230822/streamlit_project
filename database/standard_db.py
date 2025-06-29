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

CREATE_SQL="""
CREATE TABLE standard_system (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增主键
    system_serial_number TEXT,  -- 体系序号
    flow_number TEXT,  -- 流水号
    serial_number TEXT,  -- 序号
    standard_code TEXT,  -- 标准号
    standard_name TEXT,  -- 标准名称
    standard_content TEXT,  -- 标准内容
    body_start_page TEXT,  -- 正文起始页
    page_number TEXT,  -- 页码
    page_count TEXT,  -- 页数
    start_line_number TEXT,  -- 起始行号
    relevance TEXT,  -- 相关性
    min_chapter_clause_code TEXT,  -- 最小章条编号
    content_element TEXT,  -- 内容要素
    content_subdivision TEXT,  -- 内容要素细分
    important_prompt TEXT,  -- 重要提示引导词
    element_expression TEXT,  -- 要素表达形式
    element_form TEXT,  -- 要素的表述形式
    paragraph_nature TEXT,  -- 段落性质
    hierarchy TEXT,  -- 层次
    formula TEXT,  -- 公式
    list_item TEXT,  -- 列项
    list_symbol_number TEXT,  -- 列项符号/编号
    unknown1 TEXT, -- 分割
    performance_indicator_level1 TEXT,  -- 性能指标一级
    performance_indicator_level2 TEXT,  -- 性能指标二级
    method_name TEXT,  -- 方法名称
    sample_preparation TEXT,  -- 试样/制剂（制备）
    equipment_materials TEXT,  -- 仪器、设备、材料
    product_category1 TEXT,  -- 产品类别1
    product_category2 TEXT,  -- 产品类别2
    product_name TEXT,  -- 产品名称
    oil_gas_resource_type TEXT,  -- 油气资源类别
    product TEXT,  -- 产品
    process1 TEXT,  -- 工艺
    process2 TEXT,  -- 工艺
    stimulation_business_level1 TEXT,  -- 储层改造业务1级
    stimulation_business_level2 TEXT,  -- 储层改造业务2级
    stimulation_business_level3 TEXT,  -- 储层改造业务3级
    stimulation_business_level4 TEXT,  -- 储层改造业务4级
    stimulation_business_level5 TEXT,  -- 储层改造业务5级
    unknown2 TEXT, -- 分割
    quality_control TEXT,  -- 质量控制(施工方)
    hse_requirements TEXT,  -- 健康、安全与环境控制要求
    quality_supervision TEXT,  -- 工程质量技术监督(第三方或甲方)
    designer TEXT,  -- 设计人员
    format_template TEXT,  -- 格式-模板
    parameter_nature TEXT,  -- 参数性质
    parameter_category TEXT,  -- 参数类别
    parameter TEXT,  -- 参数
    method1 TEXT,  -- 方法1(1计算方法/2录取方法)
    method2 TEXT,  -- 方法2
    wellbore_type1 TEXT,  -- 井筒类型分类
    wellbore_type2 TEXT,  -- 井筒类型分类
    process_tech1 TEXT,  -- 工艺技术1
    process_tech2 TEXT,  -- 工艺技术2
    process_tech3 TEXT,  -- 工艺技术3
    offshore TEXT,  -- 海上
    chapter_code TEXT,  -- 章编号
    chapter_title TEXT,  -- 章标题
    level1_code TEXT,  -- 一级条编号
    level1_title TEXT,  -- 一级条标题
    level2_code TEXT,  -- 二级条编号
    level2_title TEXT,  -- 二级条标题
    level3_code TEXT,  -- 三级条编号
    level3_title TEXT,  -- 三级条标题
    level4_code TEXT,  -- 四级条编号
    level4_title TEXT,  -- 四级条标题
    level5_code TEXT,  -- 五级条编号
    level5_title TEXT,  -- 五级条标题
    level6_code TEXT,  -- 六级条编号
    level6_title TEXT,  -- 六级条标题
    `image` TEXT,  -- 图片
    `table` TEXT,  -- 表格
    formula_field TEXT,  -- 公式
    category_level1_code TEXT,  -- 一级门类编号
    category_level1 TEXT,  -- 一级门类
    category_level2_code TEXT,  -- 二级门类编号
    category_level2 TEXT,  -- 二级门类
    major TEXT,  -- 专业
    func_classification TEXT,  -- 按功能分类
    purpose_classification TEXT,  -- 按目的分类
    object_classification TEXT,  -- 按对象分类
    unknown3 TEXT, -- 分割
    min_chapter_code TEXT,  -- 最小章条编号
    hierarchy_level TEXT,  -- 层级
    min_hierarchy TEXT,  -- 最小层级
    term_entry_code TEXT,  -- 术语词条编号
    hanging_paragraph1 TEXT, -- 悬置段1
    hanging_paragraph2 TEXT  -- 悬置段2
)
"""
INSERT_STATEMENT = """
INSERT INTO standard_system (
    system_serial_number,
    flow_number,
    serial_number,
    standard_code,
    standard_name,
    standard_content,
    body_start_page, 
    page_number,
    page_count,
    start_line_number,
    relevance,
    min_chapter_clause_code,
    content_element,
    content_subdivision,
    important_prompt,
    element_expression,
    element_form,
    paragraph_nature,
    hierarchy,
    formula,
    list_item,
    list_symbol_number,
    unknown1,
    performance_indicator_level1,
    performance_indicator_level2,
    method_name,
    sample_preparation,
    equipment_materials,
    product_category1,
    product_category2,
    product_name,
    oil_gas_resource_type,
    product,
    process1,
    process2,
    stimulation_business_level1,
    stimulation_business_level2,
    stimulation_business_level3,
    stimulation_business_level4,
    stimulation_business_level5,
    unknown2,
    quality_control,
    hse_requirements,
    quality_supervision,
    designer,
    format_template,
    parameter_nature,
    parameter_category,
    parameter,
    method1,
    method2,
    wellbore_type1,
    wellbore_type2,
    process_tech1,
    process_tech2,
    process_tech3,
    offshore,
    chapter_code,
    chapter_title,
    level1_code,
    level1_title,
    level2_code,
    level2_title,
    level3_code,
    level3_title,
    level4_code,
    level4_title,
    level5_code,
    level5_title,
    level6_code,
    level6_title,
    `image`,
    `table`,
    formula_field,
    category_level1_code,
    category_level1,
    category_level2_code,
    category_level2,
    major,
    func_classification,
    purpose_classification,
    object_classification,
    unknown3,
    min_chapter_code,
    hierarchy_level,
    min_hierarchy,
    term_entry_code,
    hanging_paragraph1,
    hanging_paragraph2
) 
VALUES (
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?
)"""
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
    

class StandardDB:
    conn: sqlite3.Connection
    def __init__(self):
        db_path = Path(__file__).parent.parent / 'standard.db'
        self.conn=sqlite3.connect(db_path,check_same_thread=False)
        c = self.conn.cursor()
        c.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_system'
        """)
        if not c.fetchone():
            c.execute(CREATE_SQL)
            self.conn.commit()
        else:
            cursor = c.execute("PRAGMA table_info(standard_system)")
            db_columns = [row[1] for row in cursor.fetchall()]  # 获取所有数据库列名
    
    def count(self):
        c = self.conn.cursor()
        c.execute("select count(1) from standard_system")
        return c.fetchone()[0]
    
    def standard_detail(self,standard_code:str):
        SELECT_STATEMENT=f"""
        select * from standard_system where standard_code='{standard_code}' order by serial_number asc
        """
        c = self.conn.cursor()
        c.execute(SELECT_STATEMENT)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def product_list(self,standard_code:str):
        SELECT_STATEMENT=f"""
        select 
        standard_code,
        performance_indicator_level1,
        performance_indicator_level2,
        method_name,
        sample_preparation,
        equipment_materials,
        product_category1,
        product_category2,
        product_name from standard_system where standard_code='{standard_code}' group by 
        standard_code,
        performance_indicator_level1,
        performance_indicator_level2,
        method_name,
        sample_preparation,
        equipment_materials,
        product_category1,
        product_category2
        """
        c = self.conn.cursor()
        c.execute(SELECT_STATEMENT)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data


    def craft_list(self,standard_code:str):
        c = self.conn.cursor()
        craft_statement=f"""
        select 
        standard_code,
        quality_control,
        hse_requirements,
        quality_supervision,
        designer,
        format_template,
        parameter_nature,
        parameter_category,
        parameter,
        method1,
        method2,
        wellbore_type1,
        wellbore_type2,
        process_tech1,
        process_tech2,
        process_tech3 from standard_system 
        where standard_code='{standard_code}' 
        group by 
        standard_code,
        quality_control,
        hse_requirements,
        quality_supervision,
        designer,
        format_template,
        parameter_nature,
        parameter_category,
        parameter,
        method1,
        method2,
        wellbore_type1,
        wellbore_type2,
        process_tech1,
        process_tech2,
        process_tech3
        """
        c.execute(craft_statement)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data


    def query_category_level1_code(self,standard_code:str):
        c = self.conn.cursor()
        c.execute(f"SELECT distinct category_level1_code FROM standard_system where standard_code='{standard_code}'")
        return c.fetchone()

    #条款数据查询
    def list_for_tiaokuan(self,filter:WhereCause = WhereCause()):
        c = self.conn.cursor()
        sql=f"SELECT serial_number,standard_code, standard_name, standard_content, min_chapter_clause_code FROM standard_system {filter.to_sql()} order by serial_number asc "
        c.execute(sql)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def list(self,filter:WhereCause = WhereCause(),pageable:Pageable = Pageable(1,10)) -> PageResult:
        c = self.conn.cursor()

        #build sql???
        sql=f"SELECT standard_code, standard_name  FROM standard_system {filter.to_sql()} group by standard_code,standard_name"
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
        c.executemany(INSERT_STATEMENT, data)
        self.conn.commit()
        #conn.close()

    def load_from_excel(self,file_path:str):
        df = pd.read_excel(file_path, engine='openpyxl',header=0)
        self.batch_insert(df)


    def drop(self):
        c = self.conn.cursor()
        c.execute("DROP TABLE IF EXISTS standard_system")
        self.conn.commit()
        #conn.close()

@st.cache_resource
def init_standard_db():
    print("init standard_db")
    return StandardDB()




