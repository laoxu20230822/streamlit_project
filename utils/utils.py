import re


def build_single_column_search(search_term, column):
    """为单个列构建搜索条件，将搜索词按空格分割后生成OR连接的LIKE条件"""
    # 检查输入是否有效
    if not search_term or not column:
        return ""

    # 按空格分割搜索词，并过滤掉空字符串
    search_parts = [part for part in re.split(r"\s+", search_term.strip()) if part]

    if not search_parts:
        return ""

    # 为每个搜索部分构建同一列的LIKE条件
    conditions = [f"{column} LIKE '%{part}%'" for part in search_parts]

    # 用OR连接所有条件，并添加括号包裹
    where_clause = f"({' OR '.join(conditions)})"

    return where_clause


if __name__ == "__main__":
    # 测试新函数
    search_term = "标准内容 标准内容2"
    column = "standard_content"
    where_clause = build_single_column_search(search_term, column)
    print(f"生成的SQL条件: {where_clause}")
