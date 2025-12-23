"""
储层改造层级字典表

用于存储储层改造业务的5级分类数据，支持从Excel或standard_system表初始化。
"""

import sqlite3
from pathlib import Path
from typing import List, Tuple
import streamlit as st
import pandas as pd

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS ccgz_level_dict (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level1 TEXT NOT NULL,
    level2 TEXT,
    level3 TEXT,
    level4 TEXT,
    level5 TEXT,
    UNIQUE(level1, level2, level3, level4, level5)
)
"""

CREATE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_ccgz_level1 ON ccgz_level_dict(level1);
CREATE INDEX IF NOT EXISTS idx_ccgz_level2 ON ccgz_level_dict(level2);
CREATE INDEX IF NOT EXISTS idx_ccgz_level3 ON ccgz_level_dict(level3);
CREATE INDEX IF NOT EXISTS idx_ccgz_level4 ON ccgz_level_dict(level4);
CREATE INDEX IF NOT EXISTS idx_ccgz_level5 ON ccgz_level_dict(level5);
"""


class CcgzLevelDictDB:
    """储层改造层级字典表数据库操作类"""

    conn: sqlite3.Connection

    def __init__(self):
        db_path = Path(__file__).parent.parent / "standard.db"
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_table()
        self._load_data_on_init()

    def _init_table(self):
        """初始化表结构和索引"""
        c = self.conn.cursor()
        c.execute(CREATE_TABLE_SQL)
        c.executescript(CREATE_INDEX_SQL)
        self.conn.commit()

    def create_table(self):
        """创建表（供外部调用）"""
        c = self.conn.cursor()
        c.execute(CREATE_TABLE_SQL)
        c.executescript(CREATE_INDEX_SQL)
        self.conn.commit()

    def drop(self):
        """删除表"""
        c = self.conn.cursor()
        c.execute("DROP TABLE IF EXISTS ccgz_level_dict")
        self.conn.commit()

    def clear(self):
        """清空表数据"""
        c = self.conn.cursor()
        c.execute("DELETE FROM ccgz_level_dict")
        self.conn.commit()

    def insert(self, level1: str, level2: str = "", level3: str = "", level4: str = "", level5: str = ""):
        """
        插入单条数据

        Args:
            level1: 1级分类
            level2: 2级分类（可选）
            level3: 3级分类（可选）
            level4: 4级分类（可选）
            level5: 5级分类（可选）
        """
        c = self.conn.cursor()
        # 处理空字符串转为None
        level2 = level2 if level2 else None
        level3 = level3 if level3 else None
        level4 = level4 if level4 else None
        level5 = level5 if level5 else None

        c.execute(
            """
            INSERT OR IGNORE INTO ccgz_level_dict (level1, level2, level3, level4, level5)
            VALUES (?, ?, ?, ?, ?)
            """,
            (level1, level2, level3, level4, level5)
        )
        self.conn.commit()

    def batch_insert(self, data_list: List[Tuple[str, str, str, str, str]]):
        """
        批量插入数据

        Args:
            data_list: 元组列表，每个元组格式为 (level1, level2, level3, level4, level5)
        """
        c = self.conn.cursor()
        # 处理空字符串转为None
        processed_data = []
        for row in data_list:
            processed_row = tuple(
                (val if val else None) for val in row
            )
            processed_data.append(processed_row)

        c.executemany(
            """
            INSERT OR IGNORE INTO ccgz_level_dict (level1, level2, level3, level4, level5)
            VALUES (?, ?, ?, ?, ?)
            """,
            processed_data
        )
        self.conn.commit()

    def count(self) -> int:
        """获取记录数"""
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM ccgz_level_dict")
        return c.fetchone()[0]

    def query_level1(self) -> List[str]:
        """
        查询所有1级分类

        Returns:
            1级分类列表
        """
        c = self.conn.cursor()
        c.execute(
            """
            SELECT DISTINCT level1
            FROM ccgz_level_dict
            WHERE level1 IS NOT NULL AND level1 != ''
            ORDER BY level1
            """
        )
        return [row[0] for row in c.fetchall()]

    def query_level2(self, level1: str = "") -> List[str]:
        """
        根据level1查询2级分类

        Args:
            level1: 1级分类（为空时返回所有2级分类）

        Returns:
            2级分类列表
        """
        c = self.conn.cursor()
        if level1:
            c.execute(
                """
                SELECT DISTINCT level2
                FROM ccgz_level_dict
                WHERE level1 = ?
                  AND level2 IS NOT NULL AND level2 != ''
                ORDER BY level2
                """,
                (level1,)
            )
        else:
            c.execute(
                """
                SELECT DISTINCT level2
                FROM ccgz_level_dict
                WHERE level2 IS NOT NULL AND level2 != ''
                ORDER BY level2
                """
            )
        return [row[0] for row in c.fetchall()]

    def query_level3(self, level1: str = "", level2: str = "") -> List[str]:
        """
        根据level1和level2查询3级分类

        Args:
            level1: 1级分类（为空时不作为筛选条件）
            level2: 2级分类（为空时不作为筛选条件）

        Returns:
            3级分类列表
        """
        c = self.conn.cursor()
        conditions = []
        params = []

        if level1:
            conditions.append("level1 = ?")
            params.append(level1)
        if level2:
            conditions.append("level2 = ?")
            params.append(level2)

        conditions.append("level3 IS NOT NULL AND level3 != ''")

        where_clause = " AND ".join(conditions)
        sql = f"""
            SELECT DISTINCT level3
            FROM ccgz_level_dict
            WHERE {where_clause}
            ORDER BY level3
        """

        c.execute(sql, params)
        return [row[0] for row in c.fetchall()]

    def query_level4(self, level1: str = "", level2: str = "", level3: str = "") -> List[str]:
        """
        根据level1/level2/level3查询4级分类

        Args:
            level1: 1级分类（为空时不作为筛选条件）
            level2: 2级分类（为空时不作为筛选条件）
            level3: 3级分类（为空时不作为筛选条件）

        Returns:
            4级分类列表
        """
        c = self.conn.cursor()
        conditions = []
        params = []

        if level1:
            conditions.append("level1 = ?")
            params.append(level1)
        if level2:
            conditions.append("level2 = ?")
            params.append(level2)
        if level3:
            conditions.append("level3 = ?")
            params.append(level3)

        conditions.append("level4 IS NOT NULL AND level4 != ''")

        where_clause = " AND ".join(conditions)
        sql = f"""
            SELECT DISTINCT level4
            FROM ccgz_level_dict
            WHERE {where_clause}
            ORDER BY level4
        """

        c.execute(sql, params)
        return [row[0] for row in c.fetchall()]

    def query_level5(self, level1: str = "", level2: str = "", level3: str = "", level4: str = "") -> List[str]:
        """
        根据level1/level2/level3/level4查询5级分类

        Args:
            level1: 1级分类（为空时不作为筛选条件）
            level2: 2级分类（为空时不作为筛选条件）
            level3: 3级分类（为空时不作为筛选条件）
            level4: 4级分类（为空时不作为筛选条件）

        Returns:
            5级分类列表
        """
        c = self.conn.cursor()
        conditions = []
        params = []

        if level1:
            conditions.append("level1 = ?")
            params.append(level1)
        if level2:
            conditions.append("level2 = ?")
            params.append(level2)
        if level3:
            conditions.append("level3 = ?")
            params.append(level3)
        if level4:
            conditions.append("level4 = ?")
            params.append(level4)

        conditions.append("level5 IS NOT NULL AND level5 != ''")

        where_clause = " AND ".join(conditions)
        sql = f"""
            SELECT DISTINCT level5
            FROM ccgz_level_dict
            WHERE {where_clause}
            ORDER BY level5
        """

        c.execute(sql, params)
        return [row[0] for row in c.fetchall()]

    def init_from_standard_system(self):
        """
        从standard_system表初始化数据

        执行操作：
        1. 清空当前表
        2. 从standard_system表提取5级分类数据
        3. 批量插入到当前表
        """
        c = self.conn.cursor()

        # 1. 清空表
        c.execute("DELETE FROM ccgz_level_dict")

        # 2. 从standard_system表提取数据并插入
        c.execute(
            """
            INSERT OR IGNORE INTO ccgz_level_dict (level1, level2, level3, level4, level5)
            SELECT DISTINCT
                NULLIF(stimulation_business_level1, ''),
                NULLIF(stimulation_business_level2, ''),
                NULLIF(stimulation_business_level3, ''),
                NULLIF(stimulation_business_level4, ''),
                NULLIF(stimulation_business_level5, '')
            FROM standard_system
            WHERE stimulation_business_level1 IS NOT NULL
              AND stimulation_business_level1 != ''
            """
        )
        self.conn.commit()

    def _get_excel_path(self) -> Path:
        """
        获取Excel数据文件的路径

        Returns:
            Excel文件的Path对象
        """
        path = Path(__file__).parent.parent / "static" / "ccgz_level_dict.xlsx"
        if not path.exists():
            print(f"警告: Excel文件不存在: {path}")
        return path

    def load_from_excel(self, file_path: str = None):
        """
        从Excel文件加载数据（清空重建）

        Excel表头列名映射：
        - 储层改造业务1级 → level1
        - 储层改造业务2级 → level2
        - 储层改造业务3级 → level3
        - 储层改造业务4级 → level4
        - 储层改造业务5级 → level5

        Args:
            file_path: Excel文件路径，为None时使用默认路径
        """
        if file_path is None:
            file_path = self._get_excel_path()
        else:
            file_path = Path(file_path)

        if not file_path.exists():
            print(f"Excel文件不存在: {file_path}")
            return

        # 读取Excel文件
        df = pd.read_excel(file_path, engine="openpyxl").fillna("")

        # 列名映射：中文表头 → 数据库列名
        column_mapping = {
            "储层改造业务1级": "level1",
            "储层改造业务2级": "level2",
            "储层改造业务3级": "level3",
            "储层改造业务4级": "level4",
            "储层改造业务5级": "level5",
        }
        df = df.rename(columns=column_mapping)

        # 清空当前表
        self.clear()

        # 批量插入数据
        data_list = [
            (row["level1"], row["level2"], row["level3"], row["level4"], row["level5"])
            for _, row in df.iterrows()
        ]
        self.batch_insert(data_list)
        print(f"从Excel加载数据完成，共{len(data_list)}条记录")

    def _load_data_on_init(self):
        """
        启动时的数据加载逻辑

        数据加载优先级：
        1. 如果Excel文件存在，清空表并从Excel加载
        2. 如果Excel不存在且表为空，从standard_system表初始化
        3. 否则保持现有数据不变
        """
        excel_path = self._get_excel_path()

        if excel_path.exists():
            # 情况1：Excel存在，清空并从Excel加载
            print(f"检测到Excel文件: {excel_path}，正在加载...")
            self.load_from_excel()
        else:
            # 情况2：Excel不存在
            if self.count() == 0:
                # 表为空，从standard_system初始化
                print("Excel文件不存在且表为空，从standard_system表初始化...")
                self.init_from_standard_system()
            else:
                # 表有数据，保持不变
                print(f"使用现有数据，共{self.count()}条记录")


@st.cache_resource
def init_ccgz_level_dict_db():
    """初始化储层改造层级字典表数据库实例（缓存）"""
    print("init ccgz_level_dict_db")
    return CcgzLevelDictDB()
