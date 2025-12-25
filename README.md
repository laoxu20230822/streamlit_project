# 储层改造标准知识服务系统

一个基于 Streamlit 的标准文档查询系统，专门用于管理和查询石油天然气行业的标准文档。

## 功能特性

- **多维度查询**：支持标准名称、条款、术语、指标、试验方法、图表公式、体系等多维度查询
- **数据管理**：提供 Excel 文件上传和解析功能，支持分模块加载不同类型的数据
- **知识展示**：标准详情展示、产品标准、工艺标准、术语词库、性能指标等多类型内容展示
- **高级表格**：使用 AgGrid 实现高级表格功能，支持排序、筛选、分页
- **PDF/图片展示**：内置 PDF 和图片查看功能

## 技术栈

- **前端框架**：Streamlit 1.51+
- **数据库**：SQLite
- **ORM**：SQLAlchemy 2.0+
- **数据处理**：Pandas
- **Excel 处理**：OpenPyXL
- **表格组件**：Streamlit AgGrid
- **多页面**：Stream Pages
- **PDF 生成**：ReportLab

## 项目结构

```
streamlit_project/
├── database/              # 数据库模型层
│   ├── standard_db.py     # 标准文档数据模型
│   ├── standard_index.py  # 标准索引数据模型
│   ├── standard_structure.py # 标准结构数据模型
│   ├── glossary.py        # 术语词库数据模型
│   ├── metric.py          # 性能指标数据模型
│   ├── reference_standards.py # 引用标准数据模型
│   ├── standard_category.py    # 标准分类数据模型
│   ├── chart.py           # 图表数据模型
│   └── page.py            # 分页查询工具类
├── view/                  # 视图层
│   ├── display_standard_query_list.py    # 标准查询列表
│   ├── display_standard_detail.py        # 标准详情展示
│   ├── display_product_standard.py       # 产品标准展示
│   ├── display_craft_standard.py         # 工艺标准展示
│   ├── display_glossary_query_list.py    # 术语查询展示
│   ├── display_metric_query_list.py      # 性能指标查询展示
│   ├── display_method_query_list.py      # 方法查询展示
│   ├── display_chart_query_list.py       # 图表查询展示
│   ├── display_ccgz_query_list.py        # 储层改造相关查询展示
│   ├── display_navigator_tab.py          # 导航标签页
│   ├── showpdf.py                         # PDF 展示功能
│   └── showimg.py                         # 图片展示功能
├── utils/                 # 工具层
│   ├── data_utils.py      # DataFrame 处理工具
│   └── utils.py           # SQL 构建工具
├── audio/                 # 音频模块
│   ├── audio.py           # 音频播放演示功能
│   ├── static_html.py     # 静态 HTML 展示
│   └── testpdf.py         # PDF 测试功能
├── pages/                 # 多页面应用
│   └── load_data.py       # 数据加载页面
├── hello.py               # 主应用入口
├── home.py                # 首页
├── run_app.py             # 生产环境启动脚本
├── pyproject.toml         # 项目配置和依赖
└── standard.db            # SQLite 数据库
```

## 安装和运行

### 使用 uv（推荐）

1. **安装 uv**（如果尚未安装）：
```bash
pip install uv
```

2. **运行应用**（自动创建虚拟环境并安装依赖）：
```bash
uv run run_app.py
```

### 手动安装

1. **创建虚拟环境**：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

2. **安装依赖**：
```bash
pip install -e .
```

3. **运行应用**：
```bash
# 开发模式
streamlit run hello.py

# 生产模式
python run_app.py
```

## 使用指南

### 数据加载

1. 启动应用后，点击侧边栏的"加载数据"进入数据加载页面
2. 上传 Excel 文件（支持 .xlsx 格式）
3. 选择要加载的数据类型（标准文档、术语词库、性能指标等）
4. 点击加载按钮，系统会自动解析并导入数据库

### 查询操作

1. **标准查询**：在搜索框输入标准名称，点击"标准"按钮
2. **条款查询**：输入关键词，点击"条款"按钮查看相关条款内容
3. **术语查询**：输入术语，点击"术语"按钮查看定义和解释
4. **指标查询**：点击"指标"按钮，使用下拉筛选框选择指标类别
5. **试验方法查询**：点击"试验方法"按钮，筛选相关试验方法
6. **图表公式查询**：点击"图表公式"按钮查看相关图表和公式
7. **体系查询**：使用体系导航功能，按层级查看标准体系

### 查看详情

- 在查询结果列表中点击任意条目查看详细信息
- 标准详情页面包含左侧章节导航和右侧内容展示
- 支持图片和 PDF 文件的在线预览

## 开发注意事项

1. **页面依赖**：页面的 context 值依赖于 DataFrame 的加载，注意其他输入组件变动时的依赖关系
2. **数据库操作**：使用提供的数据库模型类，避免直接编写 SQL 语句
3. **缓存策略**：应用使用缓存机制提高性能，大数据量查询时注意分页使用
4. **函数规范**：编写函数时注意单一职责原则，避免副作用

## 配置说明

### 静态文件配置

静态文件（图片、CSS 等）通过 `.streamlit/config.toml` 配置服务。

### 数据库配置

默认使用 SQLite 数据库 `standard.db`，数据库文件在项目根目录。

## 依赖说明

主要依赖项：

- `streamlit[pdf]`: Web 框架及 PDF 支持
- `sqlalchemy`: ORM 工具
- `pandas`: 数据处理
- `openpyxl`: Excel 文件处理
- `streamlit-aggrid`: 高级表格组件
- `st-pages`: 多页面支持
- `reportlab`: PDF 生成
- `streamlit-extras`: 额外的 Streamlit 组件
- `streamlit-tree-select`: 树形选择组件

## 部署

### 开发部署

```bash
streamlit run hello.py --server.port 8501
```

### 生产部署

使用 PyInstaller 打包：

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包应用
pyinstaller run_app.spec

# 运行打包后的应用
dist/run_app
```

## 许可证

本项目仅供内部使用。

此文档仅用于团队内部，试用阶段