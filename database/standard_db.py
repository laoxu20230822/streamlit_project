import os
from utils.utils import build_single_column_search
from pathlib import Path
import sqlite3

from database.sql import standard_system_select_sql
from pandas import DataFrame
import pandas as pd
import streamlit as st

from database.page import Pageable
from database.page import PageResult

import database.sql as sql
from collections import defaultdict

CREATE_SQL = """
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

    def __init__(self, search_term: str = ""):
        self.search_term = search_term

    def to_sql_new(self):
        sql = " WHERE 1=1 "
        if self.search_term:
            # sql += f" AND standard_content like '%{self.search_term}%' "
            sql += f"""and (
            {build_single_column_search(self.search_term, "standard_content")}
             or {build_single_column_search(self.search_term, "performance_indicator_level1")}
             or {build_single_column_search(self.search_term, "performance_indicator_level2")}
             or {build_single_column_search(self.search_term, "method_name")}
             or {build_single_column_search(self.search_term, "sample_preparation")}
             or {build_single_column_search(self.search_term, "equipment_materials")}
             or {build_single_column_search(self.search_term, "product_category1")}
             or {build_single_column_search(self.search_term, "product_category2")}
             or {build_single_column_search(self.search_term, "product_name")}
             or {build_single_column_search(self.search_term, "oil_gas_resource_type")}
             or {build_single_column_search(self.search_term, "product")}
             or {build_single_column_search(self.search_term, "process1")}
             or {build_single_column_search(self.search_term, "process2")}
             or {build_single_column_search(self.search_term, "stimulation_business_level1")}
             or {build_single_column_search(self.search_term, "stimulation_business_level2")}
             or {build_single_column_search(self.search_term, "stimulation_business_level3")}
             or {build_single_column_search(self.search_term, "stimulation_business_level4")}
             or {build_single_column_search(self.search_term, "stimulation_business_level5")}
             or {build_single_column_search(self.search_term, "quality_control")}
             or {build_single_column_search(self.search_term, "hse_requirements")}
             or {build_single_column_search(self.search_term, "quality_supervision")}
             or {build_single_column_search(self.search_term, "designer")}
             or {build_single_column_search(self.search_term, "format_template")}
             or {build_single_column_search(self.search_term, "parameter_nature")}
             or {build_single_column_search(self.search_term, "parameter_category")}
             or {build_single_column_search(self.search_term, "parameter")}
             or {build_single_column_search(self.search_term, "method1")}
             or {build_single_column_search(self.search_term, "method2")}
             or {build_single_column_search(self.search_term, "wellbore_type1")}
             or {build_single_column_search(self.search_term, "wellbore_type2")}
             or {build_single_column_search(self.search_term, "process_tech1")}
             or {build_single_column_search(self.search_term, "process_tech2")}
             or {build_single_column_search(self.search_term, "process_tech3")}
             or {build_single_column_search(self.search_term, "offshore")}
            )
            """
        return sql

    # def to_sql(self):
    #     sql = " WHERE 1=1 "
    #     if self.search_term:
    #         # sql += f" AND standard_content like '%{self.search_term}%' "
    #         sql += f"""and (
    #         standard_content like '%{self.search_term}%'
    #         OR performance_indicator_level1 LIKE '%{self.search_term}%'
    #         OR performance_indicator_level2 LIKE '%{self.search_term}%'
    #         OR method_name LIKE '%{self.search_term}%'
    #         OR sample_preparation LIKE '%{self.search_term}%'
    #         OR equipment_materials LIKE '%{self.search_term}%'
    #         OR product_category1 LIKE '%{self.search_term}%'
    #         OR product_category2 LIKE '%{self.search_term}%'
    #         OR product_name LIKE '%{self.search_term}%'
    #         OR oil_gas_resource_type LIKE '%{self.search_term}%'
    #         OR product LIKE '%{self.search_term}%'
    #         OR process1 LIKE '%{self.search_term}%'
    #         OR process2 LIKE '%{self.search_term}%'
    #         OR stimulation_business_level1 LIKE '%{self.search_term}%'
    #         OR stimulation_business_level2 LIKE '%{self.search_term}%'
    #         OR stimulation_business_level3 LIKE '%{self.search_term}%'
    #         OR stimulation_business_level4 LIKE '%{self.search_term}%'
    #         OR stimulation_business_level5 LIKE '%{self.search_term}%'
    #         OR quality_control LIKE '%{self.search_term}%'
    #         OR hse_requirements LIKE '%{self.search_term}%'
    #         OR quality_supervision LIKE '%{self.search_term}%'
    #         OR designer LIKE '%{self.search_term}%'
    #         OR format_template LIKE '%{self.search_term}%'
    #         OR parameter_nature LIKE '%{self.search_term}%'
    #         OR parameter_category LIKE '%{self.search_term}%'
    #         OR parameter LIKE '%{self.search_term}%'
    #         OR method1 LIKE '%{self.search_term}%'
    #         OR method2 LIKE '%{self.search_term}%'
    #         OR wellbore_type1 LIKE '%{self.search_term}%'
    #         OR wellbore_type2 LIKE '%{self.search_term}%'
    #         OR process_tech1 LIKE '%{self.search_term}%'
    #         OR process_tech2 LIKE '%{self.search_term}%'
    #         OR process_tech3 LIKE '%{self.search_term}%'
    #         OR offshore LIKE '%{self.search_term}%'
    #         )
    #         """
    #     return sql


class StandardDB:
    conn: sqlite3.Connection

    def __init__(self):
        db_path = Path(__file__).parent.parent / "standard.db"
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        c = self.conn.cursor()
        c.execute(
            """
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_system'
        """
        )
        if not c.fetchone():
            c.execute(CREATE_SQL)
            self.conn.commit()
        else:
            cursor = c.execute("PRAGMA table_info(standard_system)")
            db_columns = [row[1] for row in cursor.fetchall()]  # 获取所有数据库列名

    def create_table(self):
        c = self.conn.cursor()
        c.execute(
            """
        SELECT name FROM sqlite_master WHERE type='table' AND name='standard_system'
        """
        )
        if not c.fetchone():
            c.execute(CREATE_SQL)
            self.conn.commit()

    def count(self):
        c = self.conn.cursor()
        c.execute("select count(1) from standard_system")
        return c.fetchone()[0]

    def standard_detail(self, standard_code: str):
        SELECT_STATEMENT = f"""
        select * from standard_system where standard_code='{standard_code}' order by serial_number asc
        """
        c = self.conn.cursor()
        c.execute(SELECT_STATEMENT)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    ## 新增 performance_indicator_level1 TEXT,  -- 性能指标一级
    ##performance_indicator_level2 TEXT,  -- 性能指标二级
    ## method_name TEXT,  -- 方法名称
    ## method2
    # def standard_detail_by_method_query(self,standard_code:str,search_term:str):
    #     SELECT_STATEMENT=f"""
    #     select * from standard_system where
    #     standard_code='{standard_code}' and
    #     (method_name like '%{search_term}%' or
    #     method2 like '%{search_term}%' or
    #     performance_indicator_level1 like '%{search_term}%' or
    #     performance_indicator_level2 like '%{search_term}%'
    #      )  order by serial_number asc
    #     """
    #     c = self.conn.cursor()
    #     c.execute(SELECT_STATEMENT)
    #     columns = [col[0] for col in c.description]
    #     data = [dict(zip(columns, row)) for row in c.fetchall()]
    #     return data

    def product_list(self, standard_code: str):
        SELECT_STATEMENT = f"""
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

    def craft_list(self, standard_code: str):
        c = self.conn.cursor()
        craft_statement = f"""
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

    def query_category_level1_code(self, standard_code: str):
        c = self.conn.cursor()
        c.execute(
            f"SELECT distinct category_level1_code FROM standard_system where standard_code='{standard_code}'"
        )
        return c.fetchone()

    # 条款数据查询
    def list_for_tiaokuan(self, filter: WhereCause = WhereCause()):
        c = self.conn.cursor()
        sql = f"SELECT serial_number,standard_code, standard_name, standard_content, min_chapter_clause_code FROM standard_system {filter.to_sql_new()} order by serial_number asc "
        c.execute(sql)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def list_for_tiaokuan_with_filters(self,
                                      search_term: str = "",
                                      oil_gas_resource_type: str = "",
                                      process1: str = "",
                                      process2: str = "",
                                      wellbore_type1: str = "",
                                      wellbore_type2: str = "",
                                      quality_control: str = "",
                                      hse_requirements: str = ""):
        """
        带筛选条件的条款查询方法
        """
        c = self.conn.cursor()

        # 构建基础WHERE条件
        where_conditions = []

        # 如果有搜索词，添加搜索条件
        if search_term:
            filter = WhereCause(search_term)
            # 获取搜索词的WHERE子句，去掉"WHERE "前缀
            search_where = filter.to_sql_new().replace(" WHERE ", "")
            where_conditions.append(search_where)

        # 添加筛选条件
        if oil_gas_resource_type:
            where_conditions.append(f"oil_gas_resource_type like '%{oil_gas_resource_type}%'")
        if process1:
            where_conditions.append(f"process1 like '%{process1}%'")
        if process2:
            where_conditions.append(f"process2 like '%{process2}%'")
        if wellbore_type1:
            where_conditions.append(f"wellbore_type1 like '%{wellbore_type1}%'")
        if wellbore_type2:
            where_conditions.append(f"wellbore_type2 like '%{wellbore_type2}%'")
        if quality_control:
            where_conditions.append(f"quality_control like '%{quality_control}%'")
        if hse_requirements:
            where_conditions.append(f"hse_requirements like '%{hse_requirements}%'")

        # 构建SQL
        base_sql = "SELECT serial_number, standard_code, standard_name, standard_content, min_chapter_clause_code FROM standard_system"

        if where_conditions:
            # 有条件时添加WHERE子句
            where_clause = " AND ".join(where_conditions)
            final_sql = f"{base_sql} WHERE {where_clause}"
        else:
            # 没有条件时不加WHERE子句
            final_sql = base_sql

        final_sql += " ORDER BY serial_number ASC"

        c.execute(final_sql)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        c.close()
        return data

    def build_where_clause(
        self,
        level1: str = "",
        level2: str = "",
        level3: str = "",
        level4: str = "",
        level5: str = "",
        oil_gas_resource_type: str = "",
        process1: str = "",
        process2: str = "",
        wellbore_type1: str = "",
        wellbore_type2: str = "",
        quality_control: str = "",
        hse_requirements: str = "",
    ) -> str:
        """
        根据level1～level5参数动态生成WHERE语句，空字符串的参数会被忽略

        Args:
            level1: 一级业务层级
            level2: 二级业务层级
            level3: 三级业务层级
            level4: 四级业务层级
            level5: 五级业务层级
            oil_gas_resource_type: 油藏资源类型
            process1: 工艺类型1
            process2: 工艺类型2
            wellbore_type1: 井体类型1
            wellbore_type2: 井体类型2

        Returns:
            str: 生成的WHERE语句，如果没有有效参数则返回空字符串
        """
        # 清理参数，去除None值和前后空格
        level1 = level1.strip() if level1 is not None else ""
        level2 = level2.strip() if level2 is not None else ""
        level3 = level3.strip() if level3 is not None else ""
        level4 = level4.strip() if level4 is not None else ""
        level5 = level5.strip() if level5 is not None else ""

        # 构建条件列表
        conditions = []

        if level1:
            conditions.append(f"stimulation_business_level1 like '%{level1}%'")
        if level2:
            conditions.append(f"stimulation_business_level2 like '%{level2}%'")
        if level3:
            conditions.append(f"stimulation_business_level3 like '%{level3}%'")
        if level4:
            conditions.append(f"stimulation_business_level4 like '%{level4}%'")
        if level5:
            conditions.append(f"stimulation_business_level5 like '%{level5}%'")
        if oil_gas_resource_type:
            conditions.append(f"oil_gas_resource_type like '%{oil_gas_resource_type}%'")
        if process1:
            conditions.append(f"process_tech1 like '%{process1}%'")
        if process2:
            conditions.append(f"process_tech2 like '%{process2}%'")
        if wellbore_type1:
            conditions.append(f"wellbore_type1 like '%{wellbore_type1}%'")
        if wellbore_type2:
            conditions.append(f"wellbore_type2 like '%{wellbore_type2}%'")
        if quality_control:
            conditions.append(f"quality_control like '%{quality_control}%'")
        if hse_requirements:
            conditions.append(f"hse_requirements like '%{hse_requirements}%'")

        # 组合WHERE语句
        if conditions:
            return " and ".join(conditions)
        else:
            return "1=1"

    def get_chapter(self, standard_code: str, chapter: str):
        c = self.conn.cursor()
        c.execute(
            f"SELECT standard_code, standard_name,standard_content FROM standard_system where standard_code='{standard_code}' and min_chapter_clause_code='{chapter}%'"
        )
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        c.close()
        return data

    def fetch_by_ccgz(
        self,
        level1: str = "",
        level2: str = "",
        level3: str = "",
        level4: str = "",
        level5: str = "",
        oil_gas_resource_type: str = "",
        process1: str = "",
        process2: str = "",
        wellbore_type1: str = "",
        wellbore_type2: str = "",
        quality_control: str = "",
        hse_requirements: str = "",
    ):
        where_clause = self.build_where_clause(
            level1,
            level2,
            level3,
            level4,
            level5,
            oil_gas_resource_type,
            process1,
            process2,
            wellbore_type1,
            wellbore_type2,
            quality_control,
            hse_requirements,
        )

        c = self.conn.cursor()

        data_all = c.execute(
            f"""SELECT standard_code, standard_name,standard_content,min_chapter_clause_code FROM standard_system"""
        )
        columns = [col[0] for col in c.description]
        data_all = [dict(zip(columns, row)) for row in data_all]
        c.close()
        c = self.conn.cursor()

        c.execute(
            f"""SELECT standard_code, standard_name,standard_content,min_chapter_clause_code FROM standard_system 
            where   {where_clause} """
        )
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        c.close()
        # 按照standard_code分组
        from collections import defaultdict

        grouped_data = defaultdict(
            lambda: {
                "standard_code": "",
                "standard_name": "",
                "standard_content": [],
                "min_chapter_clause_code": "",
            }
        )

        for item in data:
            code = item["standard_code"]
            grouped_data[code]["standard_code"] = code
            grouped_data[code]["standard_name"] = "#" + item["standard_name"] + "#"
            grouped_data[code]["standard_content"].append(item["standard_content"])
            grouped_data[code]["min_chapter_clause_code"] = item[
                "min_chapter_clause_code"
            ]

        # 拼接内容并转换为新的列表
        new_data = []
        for v in grouped_data.values():
            # 用回车符（\n）拼接内容
            v["standard_content"] = "\n".join(v["standard_content"])
            new_data.append(v)
        return new_data

    def list(
        self, filter: WhereCause = WhereCause(), pageable: Pageable = Pageable(1, 10)
    ) -> PageResult:
        c = self.conn.cursor()

        # build sql???
        sql = f"SELECT standard_code, standard_name  FROM standard_system {filter.to_sql_new()} group by standard_code,standard_name"
        count_sql = f"select count(1) from ({sql})"
        sql_with_page = f"{sql} {pageable.limit_sql()}"

        c.execute(count_sql)
        total = c.fetchone()[0]

        c.execute(sql_with_page)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        # conn.close()
        total_page = total // pageable.size
        if total % pageable.size > 0:
            total_page += 1
        return PageResult(data, total_page, pageable)

    def query_by_stimulation_business_level2(
        self,
        search_term: str = "",
        performance_indicator_level1: str = "",
        performance_indicator_level2: str = "",
        product_category1: str = "",
        product_category2: str = "",
        product_name: str = "",
    ):
        performance_indicator_level1_cause = build_single_column_search(
            search_term, "performance_indicator_level1"
        )
        performance_indicator_level2_cause = build_single_column_search(
            search_term, "performance_indicator_level2"
        )
        # method1_cause = build_single_column_search(search_term, "method1")
        # method2_cause = build_single_column_search(search_term, "method2")
        method_name_cause = build_single_column_search(search_term, "method_name")
        product_category1_cause = build_single_column_search(
            search_term, "product_category1"
        )
        product_category2_cause = build_single_column_search(
            search_term, "product_category2"
        )
        product_name_cause = build_single_column_search(search_term, "product_name")
        sql = f"""
SELECT standard_code, standard_name, standard_content, stimulation_business_level2
FROM standard_system where stimulation_business_level2 in ('方法提要','试验步骤','试验数据处理','仪器设备、试剂或材料') 
and 
(
{performance_indicator_level1_cause} or 
{performance_indicator_level2_cause} or 
{method_name_cause} or
{product_category1_cause} or
{product_category2_cause} or
{product_name_cause}
)
and 
(
    performance_indicator_level1 like '%{performance_indicator_level1}%' and
    performance_indicator_level2 like '%{performance_indicator_level2}%' and
    product_category1 like '%{product_category1}%' and
    product_category2 like '%{product_category2}%' and
    product_name like '%{product_name}%'
)
"""
        c = self.conn.cursor()
        c.execute(sql)
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]

        return data

    def query_by_metrics(self, metric: str, standard_code: str):
        c = self.conn.cursor()
        #      performance_indicator_level1 TEXT,  -- 性能指标一级
        # performance_indicator_level2 TEXT,  -- 性能指标二级
        c.execute(
            f"""SELECT  standard_code,standard_name, standard_content
         FROM standard_system 
         where 
         standard_code='{standard_code}' 
         and 
         (performance_indicator_level1 like '%{metric}%' 
         or 
         performance_indicator_level2 like '%{metric}%')
         """
        )
        columns = [col[0] for col in c.description]
        data = [dict(zip(columns, row)) for row in c.fetchall()]
        return data

    def batch_insert(self, df: DataFrame):
        # 转换为元组列表（适配 executemany 的参数格式）
        data = [tuple(row) for row in df.itertuples(index=False)]
        c = self.conn.cursor()
        c.executemany(INSERT_STATEMENT, data)
        self.conn.commit()
        # conn.close()

    def load_from_excel(self, file_path: str):
        df = pd.read_excel(file_path, engine="openpyxl", header=0).fillna("")
        self.batch_insert(df)

    def drop(self):
        c = self.conn.cursor()
        c.execute("DROP TABLE IF EXISTS standard_system")
        self.conn.commit()
        # conn.close()

    def query_stimulation_business_level1(self):
        """
        查询储层改造业务1级分类

        Returns:
            1级分类列表
        """
        from database.ccgz_level_dict import init_ccgz_level_dict_db
        db = init_ccgz_level_dict_db()
        return db.query_level1()

    def query_stimulation_business_level2(self, level1: str = ""):
        """
        根据level1查询储层改造业务2级分类

        Args:
            level1: 1级分类

        Returns:
            2级分类列表
        """
        from database.ccgz_level_dict import init_ccgz_level_dict_db
        db = init_ccgz_level_dict_db()
        return db.query_level2(level1)

    def query_stimulation_business_level3(self, level1: str = "", level2: str = ""):
        """
        根据level1和level2查询储层改造业务3级分类

        Args:
            level1: 1级分类
            level2: 2级分类

        Returns:
            3级分类列表
        """
        from database.ccgz_level_dict import init_ccgz_level_dict_db
        db = init_ccgz_level_dict_db()
        return db.query_level3(level1, level2)

    def query_stimulation_business_level4(
        self, level1: str = "", level2: str = "", level3: str = ""
    ):
        """
        根据level1/level2/level3查询储层改造业务4级分类

        Args:
            level1: 1级分类
            level2: 2级分类
            level3: 3级分类

        Returns:
            4级分类列表
        """
        from database.ccgz_level_dict import init_ccgz_level_dict_db
        db = init_ccgz_level_dict_db()
        return db.query_level4(level1, level2, level3)

    def query_stimulation_business_level5(
        self, level1: str = "", level2: str = "", level3: str = "", level4: str = ""
    ):
        """
        根据level1/level2/level3/level4查询储层改造业务5级分类

        Args:
            level1: 1级分类
            level2: 2级分类
            level3: 3级分类
            level4: 4级分类

        Returns:
            5级分类列表
        """
        from database.ccgz_level_dict import init_ccgz_level_dict_db
        db = init_ccgz_level_dict_db()
        return db.query_level5(level1, level2, level3, level4)

    def query_performance_indicator_level1(self, performance_indicator_level2: str = "", product_category1: str = "", product_category2: str = "", product_name: str = ""):
        """获取性能指标一级非空distinct值，支持筛选联动"""
        c = self.conn.cursor()
        
        # 构建WHERE条件
        conditions = []
        if performance_indicator_level2:
            conditions.append(f"performance_indicator_level2 LIKE '%{performance_indicator_level2}%'")
        if product_category1:
            conditions.append(f"product_category1 LIKE '%{product_category1}%'")
        if product_category2:
            conditions.append(f"product_category2 LIKE '%{product_category2}%'")
        if product_name:
            conditions.append(f"product_name LIKE '%{product_name}%'")
        
        where_clause = " AND " + " AND ".join(conditions) if conditions else ""
        
        c.execute(
            f"SELECT DISTINCT performance_indicator_level1 FROM standard_system WHERE performance_indicator_level1 IS NOT NULL AND performance_indicator_level1 != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_performance_indicator_level2(self, performance_indicator_level1: str = "", product_category1: str = "", product_category2: str = "", product_name: str = ""):
        """获取性能指标二级非空distinct值，支持筛选联动"""
        c = self.conn.cursor()
        
        # 构建WHERE条件
        conditions = []
        if performance_indicator_level1:
            conditions.append(f"performance_indicator_level1 LIKE '%{performance_indicator_level1}%'")
        if product_category1:
            conditions.append(f"product_category1 LIKE '%{product_category1}%'")
        if product_category2:
            conditions.append(f"product_category2 LIKE '%{product_category2}%'")
        if product_name:
            conditions.append(f"product_name LIKE '%{product_name}%'")
        
        where_clause = " AND " + " AND ".join(conditions) if conditions else ""
        
        c.execute(
            f"SELECT DISTINCT performance_indicator_level2 FROM standard_system WHERE performance_indicator_level2 IS NOT NULL AND performance_indicator_level2 != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_product_category1(self, performance_indicator_level1: str = "", performance_indicator_level2: str = "", product_category2: str = "", product_name: str = ""):
        """获取产品类别1非空distinct值，支持筛选联动"""
        c = self.conn.cursor()
        
        # 构建WHERE条件
        conditions = []
        if performance_indicator_level1:
            conditions.append(f"performance_indicator_level1 LIKE '%{performance_indicator_level1}%'")
        if performance_indicator_level2:
            conditions.append(f"performance_indicator_level2 LIKE '%{performance_indicator_level2}%'")
        if product_category2:
            conditions.append(f"product_category2 LIKE '%{product_category2}%'")
        if product_name:
            conditions.append(f"product_name LIKE '%{product_name}%'")
        
        where_clause = " AND " + " AND ".join(conditions) if conditions else ""
        
        c.execute(
            f"SELECT DISTINCT product_category1 FROM standard_system WHERE product_category1 IS NOT NULL AND product_category1 != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_product_category2(self, performance_indicator_level1: str = "", performance_indicator_level2: str = "", product_category1: str = "", product_name: str = ""):
        """获取产品类别2非空distinct值，支持筛选联动"""
        c = self.conn.cursor()
        
        # 构建WHERE条件
        conditions = []
        if performance_indicator_level1:
            conditions.append(f"performance_indicator_level1 LIKE '%{performance_indicator_level1}%'")
        if performance_indicator_level2:
            conditions.append(f"performance_indicator_level2 LIKE '%{performance_indicator_level2}%'")
        if product_category1:
            conditions.append(f"product_category1 LIKE '%{product_category1}%'")
        if product_name:
            conditions.append(f"product_name LIKE '%{product_name}%'")
        
        where_clause = " AND " + " AND ".join(conditions) if conditions else ""
        
        c.execute(
            f"SELECT DISTINCT product_category2 FROM standard_system WHERE product_category2 IS NOT NULL AND product_category2 != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_product_name(self, performance_indicator_level1: str = "", performance_indicator_level2: str = "", product_category1: str = "", product_category2: str = ""):
        """获取产品名称非空distinct值，支持筛选联动"""
        c = self.conn.cursor()
        
        # 构建WHERE条件
        conditions = []
        if performance_indicator_level1:
            conditions.append(f"performance_indicator_level1 LIKE '%{performance_indicator_level1}%'")
        if performance_indicator_level2:
            conditions.append(f"performance_indicator_level2 LIKE '%{performance_indicator_level2}%'")
        if product_category1:
            conditions.append(f"product_category1 LIKE '%{product_category1}%'")
        if product_category2:
            conditions.append(f"product_category2 LIKE '%{product_category2}%'")
        
        where_clause = " AND " + " AND ".join(conditions) if conditions else ""
        
        c.execute(
            f"SELECT DISTINCT product_name FROM standard_system WHERE product_name IS NOT NULL AND product_name != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_oil_gas_resource_type(self, process1: str = "", process2: str = "", wellbore_type1: str = "", wellbore_type2: str = "", quality_control: str = "", hse_requirements: str = ""):
        """获取油气资源类别非空distinct值，支持级联筛选"""
        c = self.conn.cursor()

        # 构建WHERE条件
        conditions = []
        if process1:
            conditions.append(f"process1 LIKE '%{process1}%'")
        if process2:
            conditions.append(f"process2 LIKE '%{process2}%'")
        if wellbore_type1:
            conditions.append(f"wellbore_type1 LIKE '%{wellbore_type1}%'")
        if wellbore_type2:
            conditions.append(f"wellbore_type2 LIKE '%{wellbore_type2}%'")
        if quality_control:
            conditions.append(f"quality_control LIKE '%{quality_control}%'")
        if hse_requirements:
            conditions.append(f"hse_requirements LIKE '%{hse_requirements}%'")

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        c.execute(
            f"SELECT DISTINCT oil_gas_resource_type FROM standard_system WHERE oil_gas_resource_type IS NOT NULL AND oil_gas_resource_type != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_process1(self, oil_gas_resource_type: str = "", process2: str = "", wellbore_type1: str = "", wellbore_type2: str = "", quality_control: str = "", hse_requirements: str = ""):
        """获取工艺1非空distinct值，支持级联筛选"""
        c = self.conn.cursor()

        # 构建WHERE条件
        conditions = []
        if oil_gas_resource_type:
            conditions.append(f"oil_gas_resource_type LIKE '%{oil_gas_resource_type}%'")
        if process2:
            conditions.append(f"process2 LIKE '%{process2}%'")
        if wellbore_type1:
            conditions.append(f"wellbore_type1 LIKE '%{wellbore_type1}%'")
        if wellbore_type2:
            conditions.append(f"wellbore_type2 LIKE '%{wellbore_type2}%'")
        if quality_control:
            conditions.append(f"quality_control LIKE '%{quality_control}%'")
        if hse_requirements:
            conditions.append(f"hse_requirements LIKE '%{hse_requirements}%'")

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        c.execute(
            f"SELECT DISTINCT process1 FROM standard_system WHERE process1 IS NOT NULL AND process1 != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_process2(self, oil_gas_resource_type: str = "", process1: str = "", wellbore_type1: str = "", wellbore_type2: str = "", quality_control: str = "", hse_requirements: str = ""):
        """获取工艺2非空distinct值，支持级联筛选"""
        c = self.conn.cursor()

        # 构建WHERE条件
        conditions = []
        if oil_gas_resource_type:
            conditions.append(f"oil_gas_resource_type LIKE '%{oil_gas_resource_type}%'")
        if process1:
            conditions.append(f"process1 LIKE '%{process1}%'")
        if wellbore_type1:
            conditions.append(f"wellbore_type1 LIKE '%{wellbore_type1}%'")
        if wellbore_type2:
            conditions.append(f"wellbore_type2 LIKE '%{wellbore_type2}%'")
        if quality_control:
            conditions.append(f"quality_control LIKE '%{quality_control}%'")
        if hse_requirements:
            conditions.append(f"hse_requirements LIKE '%{hse_requirements}%'")

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        c.execute(
            f"SELECT DISTINCT process2 FROM standard_system WHERE process2 IS NOT NULL AND process2 != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_wellbore_type1(self, oil_gas_resource_type: str = "", process1: str = "", process2: str = "", wellbore_type2: str = "", quality_control: str = "", hse_requirements: str = ""):
        """获取井筒类型分类1非空distinct值，支持级联筛选"""
        c = self.conn.cursor()

        # 构建WHERE条件
        conditions = []
        if oil_gas_resource_type:
            conditions.append(f"oil_gas_resource_type LIKE '%{oil_gas_resource_type}%'")
        if process1:
            conditions.append(f"process1 LIKE '%{process1}%'")
        if process2:
            conditions.append(f"process2 LIKE '%{process2}%'")
        if wellbore_type2:
            conditions.append(f"wellbore_type2 LIKE '%{wellbore_type2}%'")
        if quality_control:
            conditions.append(f"quality_control LIKE '%{quality_control}%'")
        if hse_requirements:
            conditions.append(f"hse_requirements LIKE '%{hse_requirements}%'")

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        c.execute(
            f"SELECT DISTINCT wellbore_type1 FROM standard_system WHERE wellbore_type1 IS NOT NULL AND wellbore_type1 != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_wellbore_type2(self, oil_gas_resource_type: str = "", process1: str = "", process2: str = "", wellbore_type1: str = "", quality_control: str = "", hse_requirements: str = ""):
        """获取井筒类型分类2非空distinct值，支持级联筛选"""
        c = self.conn.cursor()

        # 构建WHERE条件
        conditions = []
        if oil_gas_resource_type:
            conditions.append(f"oil_gas_resource_type LIKE '%{oil_gas_resource_type}%'")
        if process1:
            conditions.append(f"process1 LIKE '%{process1}%'")
        if process2:
            conditions.append(f"process2 LIKE '%{process2}%'")
        if wellbore_type1:
            conditions.append(f"wellbore_type1 LIKE '%{wellbore_type1}%'")
        if quality_control:
            conditions.append(f"quality_control LIKE '%{quality_control}%'")
        if hse_requirements:
            conditions.append(f"hse_requirements LIKE '%{hse_requirements}%'")

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        c.execute(
            f"SELECT DISTINCT wellbore_type2 FROM standard_system WHERE wellbore_type2 IS NOT NULL AND wellbore_type2 != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_quality_control(self, oil_gas_resource_type: str = "", process1: str = "", process2: str = "", wellbore_type1: str = "", wellbore_type2: str = "", hse_requirements: str = ""):
        """获取质量控制(施工方)非空distinct值，支持级联筛选"""
        c = self.conn.cursor()

        # 构建WHERE条件
        conditions = []
        if oil_gas_resource_type:
            conditions.append(f"oil_gas_resource_type LIKE '%{oil_gas_resource_type}%'")
        if process1:
            conditions.append(f"process1 LIKE '%{process1}%'")
        if process2:
            conditions.append(f"process2 LIKE '%{process2}%'")
        if wellbore_type1:
            conditions.append(f"wellbore_type1 LIKE '%{wellbore_type1}%'")
        if wellbore_type2:
            conditions.append(f"wellbore_type2 LIKE '%{wellbore_type2}%'")
        if hse_requirements:
            conditions.append(f"hse_requirements LIKE '%{hse_requirements}%'")

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        c.execute(
            f"SELECT DISTINCT quality_control FROM standard_system WHERE quality_control IS NOT NULL AND quality_control != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels

    def query_hse_requirements(self, oil_gas_resource_type: str = "", process1: str = "", process2: str = "", wellbore_type1: str = "", wellbore_type2: str = "", quality_control: str = ""):
        """获取健康、安全与环境控制要求非空distinct值，支持级联筛选"""
        c = self.conn.cursor()

        # 构建WHERE条件
        conditions = []
        if oil_gas_resource_type:
            conditions.append(f"oil_gas_resource_type LIKE '%{oil_gas_resource_type}%'")
        if process1:
            conditions.append(f"process1 LIKE '%{process1}%'")
        if process2:
            conditions.append(f"process2 LIKE '%{process2}%'")
        if wellbore_type1:
            conditions.append(f"wellbore_type1 LIKE '%{wellbore_type1}%'")
        if wellbore_type2:
            conditions.append(f"wellbore_type2 LIKE '%{wellbore_type2}%'")
        if quality_control:
            conditions.append(f"quality_control LIKE '%{quality_control}%'")

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        c.execute(
            f"SELECT DISTINCT hse_requirements FROM standard_system WHERE hse_requirements IS NOT NULL AND hse_requirements != ''{where_clause}"
        )
        levels = [row[0] for row in c.fetchall()]
        return levels


@st.cache_resource
def init_standard_db():
    print("init standard_db")
    return StandardDB()
