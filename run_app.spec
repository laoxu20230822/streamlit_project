# run_app.spec

# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, copy_metadata
import os

# 获取当前工作目录的绝对路径
current_dir = os.path.abspath('.')
site_packages_path = '.venv/Lib/site-packages'

a = Analysis(
    ['run_app.py'],
    pathex=[current_dir,site_packages_path],
    binaries=[],
    datas=[
        # --- Streamlit 核心静态文件 ---
        ("./.venv/Lib/site-packages/streamlit/static", "streamlit/static"),
        ("./.venv/Lib/site-packages/streamlit/runtime", "streamlit/runtime"),


        ("./.venv/Lib/site-packages/streamlit_extras/stylable_container", "streamlit_extras/stylable_container"),
        ("./.venv/Lib/site-packages/setuptools/_vendor", "setuptools/_vendor"),

        # --- 第三方库前端文件和元数据 ---
        # st_aggrid 由 hooks/hook-st_aggrid.py 自动收集
        ('./.venv/Lib/site-packages/st_pages', 'st_pages'),
        *collect_data_files('streamlit_extras', include_py_files=True),
        *copy_metadata('streamlit-extras'),
        *copy_metadata('streamlit'),

        # --- 添加streamlit_tree_select ---
        *collect_data_files('streamlit_tree_select', include_py_files=True),

        # --- 添加 streamlit-pdf ---
        *collect_data_files('streamlit_pdf', include_py_files=True),
        *copy_metadata('streamlit-pdf'),


        # --- 你的应用文件夹 ---
        ('.streamlit', '.streamlit'),
        ('database', 'database'),
        ('file', 'file'),
        ('hooks', 'hooks'),
        ('images', 'images'),
        ('pages', 'pages'),
        ('static', 'static'),
        ('view', 'view'),

        # --- 你的应用根目录文件 ---
        ('hello.py', '.'),
        ('home.py', '.'),
        ('standard.db', '.'),
        ('README.md', '.'),
        ('pyproject.toml', '.')
    ],
    hiddenimports=[
        'rpds',
        'rpds.rpds',
        'streamlit_extras',
        'streamlit_extras.stylable_container',
        'streamlit',
        'st_pages',
        'importlib_metadata',
        'zipp',
        'database',
        'database.chart',
        'database.glossary',
        'database.metric',
        'database.page',
        'database.reference_standards',
        'database.sql',
        'database.standard_category',
        'database.standard_db',
        'database.standard_index',
        'database.standard_structure',
        'view',
        'view.display_chart_query_list',
        'view.display_craft_standard',
        'view.display_glossary_query_list',
        'view.display_method_query_list',
        'view.display_metric_query_list',
        'view.display_product_standard',
        'view.display_standard_detail',
        'view.display_standard_glossary',
        'view.display_standard_query_list',
        'view.display_standard_references',
        'view.display_standard_structure',
        'view.display_tiaokuan_query_list',
        'view.display_tixi_query_list',
        'view.showimg',
        'st_aggrid',
        #'streamlit_extras',
        #'streamlit_extras.stylable_container',
        'streamlit_tree_select',
        'streamlit_pdf',
        'streamlit.web.cli',
        'setuptools._vendor.jaraco'
    ],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

options = []

exe = EXE(
    pyz,
    a.scripts,
    options,
    exclude_binaries=True,
    name='run_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run_app',
)