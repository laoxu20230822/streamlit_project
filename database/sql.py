
CREATE_TABLE_STANDARD_STRUCTURE = """
CREATE TABLE IF NOT EXISTS standard_structure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_code TEXT NOT NULL,
    start_page INTEGER NOT NULL,
    title_order INTEGER NOT NULL,
    chapter_level INTEGER NULL,
    chapter_number TEXT  NULL,
    title_content TEXT  NULL,
    page_number INTEGER  NULL
);
"""

standard_system_table_schema="""
CREATE TABLE standard_system (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_serial TEXT NOT NULL,
    flow_number TEXT UNIQUE,
    serial TEXT NOT NULL,
    standard_code TEXT NOT NULL,
    standard_name TEXT NOT NULL,
    content_full TEXT,
    content_start_page INTEGER,
    page_start INTEGER,
    page_total INTEGER,
    line_start INTEGER,
    relevance_level INTEGER,
    min_chapter_id TEXT,
    content_element TEXT,
    content_element_sub TEXT,
    important_prompt TEXT,
    expression_form TEXT,
    expression_form_desc TEXT,
    paragraph_type TEXT,
    hierarchy_level INTEGER,
    formula_desc TEXT,
    item TEXT,
    item_id TEXT,
    unknown1 TEXT,
    performance_level1 TEXT,
    performance_level2 TEXT,
    method_name TEXT,
    sample_preparation TEXT,
    equipment_materials TEXT,
    product_cat1 TEXT,
    product_cat2 TEXT,
    product_name TEXT,
    resource_type TEXT,
    product TEXT,
    craft1 TEXT,
    craft2 TEXT)
"""

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


CREATE_TABLE_REFERENCE_STANDARDS = """
CREATE TABLE reference_standards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     -- 主键 
    standard_code TEXT ,  -- 标准号
    cited_standard_original TEXT  NULL,  -- 引用文件标准号（原文提取）
    citation_type TEXT,  -- 引用文件类型
    has_edition_year TEXT,  -- 是否带年代号引用
    cited_standard_normalized TEXT,  -- 引用文件标准号（规范后）
    standard_name_normalized TEXT,  -- 引用文件标准名称（规范后）
    standard_code_prefix TEXT,  -- 标准代号
    serial_number TEXT,  -- 标准序列号
    edition_year INTEGER,  -- 标准年代号
    statistical_code TEXT,  -- 标准代号（统计用）
    serial_number1 TEXT,  -- 标准序列号1
    serial_number2 TEXT,  -- 标准序列号2
    org_classification_code TEXT,  -- 标准组织分类编号
    unknown1 TEXT, -- 分割
    standard_category TEXT,  -- 标准类别
    is_referenced INTEGER CHECK(is_referenced IN (0, 1))  -- 是否引用文件
);
"""

reference_standards_insert_sql = """
INSERT INTO reference_standards (
    standard_code,
    cited_standard_original,
    citation_type,
    has_edition_year,
    cited_standard_normalized,
    standard_name_normalized,
    standard_code_prefix,
    serial_number,
    edition_year,
    statistical_code,
    serial_number1,
    serial_number2,
    org_classification_code,
    unknown1,
    standard_category,
    is_referenced
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
insert_standard_structure_sql="""
INSERT INTO standard_structure(
    standard_code,
    start_page,
    title_order,
    chapter_level,
    chapter_number,
    title_content,
    page_number
) VALUES (
    ?,?,?,?,?,?,?
)
"""

insert_standard_system_sql="""
INSERT INTO standard_system(
    system_serial,
    flow_number,
    serial,
    standard_code,
    standard_name,
    content_full,
    content_start_page,
    page_start,
    page_total,
    line_start,
    relevance_level,
    min_chapter_id,
    content_element,
    content_element_sub,
    important_prompt,
    expression_form,
    expression_form_desc,
    paragraph_type,
    hierarchy_level,
    formula_desc,
    item,
    item_id,
    unknown1,
    performance_level1,
    performance_level2,
    method_name,
    sample_preparation,
    equipment_materials,
    product_cat1,
    product_cat2,
    product_name,
    resource_type,
    product,
    craft1,
    craft2
) VALUES (
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?
)
"""

standard_system_select_sql="""
SELECT id,system_serial,flow_number,serial,standard_code, standard_name ,content_full FROM standard_system 
"""