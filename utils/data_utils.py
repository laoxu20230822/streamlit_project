"""
数据工具模块
提供处理 DataFrame 和字典列表的通用函数
"""
import pandas as pd
from typing import Union, Optional, List, Dict, Any


def count_unique_standard_codes(df: pd.DataFrame) -> int:
    """
    计算 DataFrame 中 standard_code 列的去重数量

    Args:
        df (pd.DataFrame): 包含数据的 DataFrame

    Returns:
        int: 去重后的 standard_code 数量，如果列不存在则返回 0
    """
    if df is None or df.empty:
        return 0

    if 'standard_code' not in df.columns:
        return 0

    # 去除空值后计算唯一值数量
    return df['standard_code'].dropna().nunique()


def get_unique_standard_codes(df: pd.DataFrame) -> List[str]:
    """
    获取 DataFrame 中所有唯一的 standard_code 值

    Args:
        df (pd.DataFrame): 包含数据的 DataFrame

    Returns:
        List[str]: 唯一的 standard_code 值列表
    """
    if df is None or df.empty:
        return []

    if 'standard_code' not in df.columns:
        return []

    # 返回排序后的唯一值列表
    unique_codes = df['standard_code'].dropna().unique()
    return sorted([str(code) for code in unique_codes if pd.notna(code)])


def get_standard_code_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    获取 DataFrame 中 standard_code 的完整统计信息

    Args:
        df (pd.DataFrame): 包含数据的 DataFrame

    Returns:
        Dict[str, Any]: 包含统计信息的字典
        - unique_count: 唯一值数量
        - total_count: 总记录数（包含空值）
        - non_null_count: 非空记录数
        - unique_codes: 唯一值列表
        - top_codes: 出现频率最高的前5个代码及其计数
    """
    if df is None or df.empty:
        return {
            'unique_count': 0,
            'total_count': 0,
            'non_null_count': 0,
            'unique_codes': [],
            'top_codes': []
        }

    if 'standard_code' not in df.columns:
        return {
            'unique_count': 0,
            'total_count': len(df),
            'non_null_count': 0,
            'unique_codes': [],
            'top_codes': []
        }

    # 获取非空的 standard_code 系列
    code_series = df['standard_code'].dropna()

    # 统计信息
    stats = {
        'unique_count': code_series.nunique(),
        'total_count': len(df),
        'non_null_count': len(code_series),
        'unique_codes': get_unique_standard_codes(df),
        'top_codes': []
    }

    # 获取出现频率最高的前5个代码
    if not code_series.empty:
        value_counts = code_series.value_counts().head(5)
        stats['top_codes'] = [
            {'code': str(code), 'count': int(count)}
            for code, count in value_counts.items()
        ]

    return stats


def count_unique_values_by_column(df: pd.DataFrame, column_name: str) -> int:
    """
    计算 DataFrame 中指定列的去重数量（通用版本）

    Args:
        df (pd.DataFrame): 包含数据的 DataFrame
        column_name (str): 要计算去重数量的列名

    Returns:
        int: 去重后的数量，如果列不存在则返回 0
    """
    if df is None or df.empty:
        return 0

    if column_name not in df.columns:
        return 0

    return df[column_name].dropna().nunique()


def display_standard_code_metrics(df: pd.DataFrame, location: str = 'above'):
    """
    生成用于显示 standard_code 统计信息的 HTML/Markdown 内容

    Args:
        df (pd.DataFrame): 包含数据的 DataFrame
        location (str): 显示位置 ('above', 'sidebar', 'inline')

    Returns:
        str: 格式化的统计信息字符串
    """
    stats = get_standard_code_statistics(df)

    if location == 'sidebar':
        return f"""
        📊 **标准代码统计**
        - 唯一数量: {stats['unique_count']}
        - 总记录数: {stats['total_count']}
        - 非空记录: {stats['non_null_count']}
        """
    elif location == 'inline':
        return f"（共 {stats['total_count']} 条记录，{stats['unique_count']} 个唯一标准代码）"
    else:  # above
        return f"""
        ## 📊 标准代码统计信息

        | 指标 | 数量 |
        |------|------|
        | 唯一标准代码数 | {stats['unique_count']} |
        | 总记录数 | {stats['total_count']} |
        | 非空记录数 | {stats['non_null_count']} |
        """


def display_aggrid_metrics(df: pd.DataFrame, position: str = 'left', show_divider: bool = True):
    """
    在 AgGrid 表格上方显示统计信息

    Args:
        df (pd.DataFrame): 包含数据的 DataFrame
        position (str): 显示位置 ('left', 'center', 'right')
        show_divider (bool): 是否在统计信息下方显示分隔线
    """
    import streamlit as st

    # 获取统计信息
    stats = get_standard_code_statistics(df)

    if position == 'left':
        # 左侧显示，右侧留空
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(f"**📊 唯一标准代码数：{stats['unique_count']}**")
        with col2:
            st.empty()
    elif position == 'center':
        # 居中显示
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.markdown(f"**📊 唯一标准代码数：{stats['unique_count']}**")
    elif position == 'right':
        # 右侧显示，左侧留空
        col1, col2 = st.columns([5, 1])
        with col1:
            st.empty()
        with col2:
            st.markdown(f"**📊 唯一标准代码数：{stats['unique_count']}**")

    # 添加分隔线
    if show_divider:
        st.markdown("---")


def display_aggrid_metrics_enhanced(df: pd.DataFrame, metrics_config: dict = None):
    """
    增强版 AgGrid 统计信息显示，可自定义显示的指标

    Args:
        df (pd.DataFrame): 包含数据的 DataFrame
        metrics_config (dict): 配置要显示的指标
            示例:
            {
                'position': 'left',  # 'left', 'center', 'right'
                'show_divider': True,
                'metrics': [
                    {'label': '唯一标准代码', 'value': 'unique_count'},
                    {'label': '总记录数', 'value': 'total_count'}
                ],
                'title': '📊 统计信息'
            }
    """
    import streamlit as st

    # 默认配置
    if metrics_config is None:
        metrics_config = {
            'position': 'left',
            'show_divider': True,
            'metrics': [
                {'label': '唯一标准代码', 'value': 'unique_count'}
            ],
            'title': '📊 唯一标准代码数'
        }

    # 获取统计信息
    stats = get_standard_code_statistics(df)

    # 根据配置生成显示内容
    if 'title' in metrics_config:
        display_text = f"**{metrics_config['title']}：**"
    elif len(metrics_config['metrics']) == 1:
        # 单个指标
        metric = metrics_config['metrics'][0]
        value = stats[metric['value']]
        display_text = f"**📊 {metric['label']}：{value}**"
    else:
        # 多个指标
        lines = ["**📊 统计信息**"]
        for metric in metrics_config['metrics']:
            value = stats[metric['value']]
            lines.append(f"- {metric['label']}：{value}")
        display_text = "\n".join(lines)

    # 根据位置显示
    position = metrics_config.get('position', 'left')
    if position == 'left':
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(display_text)
        with col2:
            st.empty()
    elif position == 'center':
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.markdown(display_text)
    elif position == 'right':
        col1, col2 = st.columns([5, 1])
        with col1:
            st.empty()
        with col2:
            st.markdown(display_text)

    # 添加分隔线
    if metrics_config.get('show_divider', True):
        st.markdown("---")


def get_selectbox_index(options: List[Any], key: str) -> int:
    """
    根据 session_state 中的值获取其在 options 列表中的索引

    Args:
        options: 选项列表
        key: session_state 中的键名

    Returns:
        int: 值在 options 中的索引，如果值不存在或为 None 则返回 0
    """
    import streamlit as st

    value = st.session_state.get(key)
    print(key,value)
    if value is not None and value in options:
        return options.index(value)
    return 0


# 示例用法和测试
if __name__ == "__main__":
    # 创建测试数据
    test_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6],
        'name': ['张三', '李四', '王五', '赵六', '钱七', '孙八'],
        'standard_code': ['SC001', 'SC002', 'SC001', 'SC003', None, 'SC002'],
        'address': ['北京', '上海', '广州', '深圳', '杭州', '南京']
    })

    # 测试函数
    print("测试数据:")
    print(test_data)
    print("\n")

    # 测试去重计数
    unique_count = count_unique_standard_codes(test_data)
    print(f"唯一标准代码数量: {unique_count}")

    # 测试获取唯一值列表
    unique_codes = get_unique_standard_codes(test_data)
    print(f"唯一标准代码列表: {unique_codes}")

    # 测试统计信息
    stats = get_standard_code_statistics(test_data)
    print("\n完整统计信息:")
    for key, value in stats.items():
        print(f"{key}: {value}")

    # 测试不同位置的显示格式
    print("\n表格上方显示格式:")
    print(display_standard_code_metrics(test_data, 'above'))

    print("\n侧边栏显示格式:")
    print(display_standard_code_metrics(test_data, 'sidebar'))

    print("\n内联显示格式:")
    print(display_standard_code_metrics(test_data, 'inline'))