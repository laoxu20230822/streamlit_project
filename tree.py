import streamlit as st
from streamlit_antd_components import tree

def  show_tree():

    # 树形数据
    tree_data = [
        {
            'label': '动物',
            'value': 'animal',
            'children': [
                {'label': '猫', 'value': 'cat', 'disabled': False},
                {'label': '狗', 'value': 'dog', 'disabled': False},
            ]
        },
        {
            'label': '植物',
            'value': 'plant',
            'children': [
                {'label': '玫瑰', 'value': 'rose', 'disabled': False},
                {'label': '松树', 'value': 'pine', 'disabled': False},
            ]
        }
    ]

    # 只允许选叶子节点（设置父节点 disabled=True）
    # for node in tree_data:
    #     node['disabled'] = True  # 禁用父节点选择，只允许选叶子

    # Sidebar 中选择
    with st.sidebar:
        selected = tree(
            label='选择一个叶子节点',
            items=tree_data,
            height=400
        )

    # # 内容展示区
    # if selected:
    #     st.success(f'你选择的是：{selected}')

    #     # 模拟内容映射
    #     content_map = {
    #         'cat': '🐱 猫是温顺的动物。',
    #         'dog': '🐶 狗是忠诚的伙伴。',
    #         'rose': '🌹 玫瑰象征爱情。',
    #         'pine': '🌲 松树代表长寿。'
    #     }

    #     st.markdown(f"### 内容展示：")
    #     st.info(content_map.get(selected, '暂无内容'))
    # else:
    #     st.info("请选择一个叶子节点。")
