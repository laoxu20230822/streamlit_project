
CREATE_TABLE_STANDARD_STRUCTURE = """
CREATE TABLE IF NOT EXISTS standard_structure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_code TEXT NOT NULL,
    start_page TEXT NOT NULL,
    title_order TEXT NOT NULL,
    chapter_level TEXT NULL,
    chapter_number TEXT  NULL,
    title_content TEXT  NULL,
    page_number TEXT  NULL
);
"""





CREATE_TABLE_REFERENCE_STANDARDS = """
CREATE TABLE reference_standards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     -- 主键 
    standard_code TEXT ,  -- 核心标准号
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
    is_referenced TEXT  -- 是否引用文件
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


standard_system_select_sql="""
SELECT standard_code, standard_name  FROM standard_system 
"""