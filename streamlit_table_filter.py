import streamlit as st
import pandas as pd

# 创建示例数据
data = {
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 40],
    '城市': ['北京', '上海', '广州', '深圳'],
    '分数': [85, 90, 78, 92]
}
df = pd.DataFrame(data)

# 标题
st.title('表格过滤演示')

# 添加过滤条件
min_age = st.slider('最小年龄', min_value=20, max_value=50, value=20)
max_age = st.slider('最大年龄', min_value=20, max_value=50, value=50)
selected_city = st.multiselect('选择城市', options=df['城市'].unique(), default=df['城市'].unique())

# 应用过滤条件
filtered_df = df[
    (df['年龄'] >= min_age) & 
    (df['年龄'] <= max_age) & 
    (df['城市'].isin(selected_city))
]

if __name__ == "__main__":
    # 显示过滤后的表格
    st.dataframe(filtered_df)
