# run_app.spec

# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        # --- Streamlit 核心静态文件 ---
        ("./.venv/Lib/site-packages/streamlit/static", "streamlit/static"),
        ("./.venv/Lib/site-packages/streamlit/runtime", "streamlit/runtime"),

        # --- 第三方库前端文件 ---
        ('./.venv/Lib/site-packages/st_aggrid/frontend', 'st_aggrid/frontend'),
        # 这是你之前动态添加的 st_pages，现在统一放在这里
        ('./.venv/Lib/site-packages/st_pages', 'st_pages'),

        # --- 你的应用文件夹 ---
        ('.streamlit', '.streamlit'), # 这一行已经包含了 .streamlit 文件夹下的所有内容
        # --- ('assets', 'assets'),
        # --- ('data', 'data'),
        ('database', 'database'),
        # --- ('doc', 'doc'),
        ('file', 'file'),
        ('hooks', 'hooks'),
        ('images', 'images'),
        ('pages', 'pages'),
        ('static', 'static'),
        ('view', 'view'),

        # --- 你的应用根目录文件 ---
        ('hello.py', '.'),
        ('home.py', '.'),
        # --- ('main.py', '.'),
        # --- ('test.py', '.'),
        ('standard.db', '.'),
        # --- ('customers.db', '.'),
        # --- ('requirements.txt', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'streamlit',
        'st_pages',
        'importlib_metadata',
        'zipp',
        'database',
        'database.customer',
        'database.db',
        'database.glossary',
        'database.page',
        'database.reference_standards',
        'database.sql',
        'database.standard_db',
        'database.standard_index',
        'database.standard_structure',
        'view',
        'view.display_craft_standard',
        'view.display_product_standard',
        'view.display_standard_detail',
        'view.display_standard_glossary',
        'view.display_standard_query_list',
        'view.display_standard_references',
        'view.display_standard_structure',
        'view.display_tiaokuan_query_list',
        'st_aggrid',
        'streamlit.web.cli'
    ],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

# options = [('v', None, 'OPTION')]
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
    console=False,
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
