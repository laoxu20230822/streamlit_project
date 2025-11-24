import streamlit as st  # Streamlit Web应用框架
import pandas as pd  # 数据处理库
import numpy as np  # 数值计算库
import os  # 操作系统接口模块
import sys  # 系统参数和函数模块
from database import db  # 自定义数据库模块
from database.customer import CustomerWhereCause  # 客户查询条件类
from database.page import Pageable  # 分页查询类


# 处理文件上传的回调函数
def handle_upload_file():
    # 从session_state获取上传的文件
    uploaded_file=st.session_state.uploaded_file
    if uploaded_file is not None:
        try:
            # 读取Excel数据
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            # 批量插入数据到数据库
            db.batch_insert(df,conn)
            st.success('文件上传成功！')
        except Exception as e:
            st.error(f"文件解析失败: {str(e)}")

# 将当前项目目录添加到系统路径，确保模块导入正常
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 初始化数据库连接
conn=db.init_db()



# 在侧边栏创建过滤条件输入框
name=st.sidebar.text_input('姓名',key='name')

address=st.sidebar.text_input('地址',key='address')

phone=st.sidebar.text_input('手机号',key='phone')

# 创建客户查询过滤条件对象
filter=CustomerWhereCause(name,address,phone)

# 文件上传组件，支持Excel文件上传
uploaded_file = st.sidebar.file_uploader(
        "导入数据",
        type=['xlsx'],
        help="支持.xlsx格式文件",
        key='uploaded_file',
        on_change=handle_upload_file
    )
# 获取列名称映射（英文到中文）
def get_column_mapping():
    return {
        'id': 'ID',
        'name': '姓名',
        'address': '地址',
        'phone': '电话'
    }

# 查询客户数据（分页查询第1页，每页10条）
page_result=db.view_customers(conn=conn,filter=filter,pageable=Pageable(1,10))

# 显示数据表格
st.dataframe(
    pd.DataFrame(page_result.data if page_result.data else [],columns=get_column_mapping()),
    hide_index=True,  # 隐藏默认索引列
    use_container_width=True,
    column_config={
        "id": st.column_config.TextColumn(
            "ID",
             help="Streamlit **widget** commands 🎈",
            # default="st.",
            # max_chars=50,
            # validate=r"^st\.[a-z_]+$",
        ),
        "name": st.column_config.TextColumn(
            "姓名",
        ),
        "address": st.column_config.TextColumn(
            "地址",
        ),
        "phone": st.column_config.TextColumn(
            "手机号",
        )
    },  # 表格宽度自适应容器
)

# 分页控制区域
# 创建占位符
st.empty()

# 创建分页布局列（总宽度比例为: 0.6, 0.1, 0.1, 0.1, 0.1）
col1, col2,col3,col4,col5 = st.columns([0.6,0.1,0.1,0.1,0.1])

with col2:
    # 显示总页数
    st.write(f'共{page_result.total}页')
with col3:
    # 上一页按钮
    st.button('prev')
with col4:
    # 当前页码输入框
    st.number_input('current_page',label_visibility='collapsed',min_value=1,max_value=10)
with col5:
    # 下一页按钮
    st.button('next')




