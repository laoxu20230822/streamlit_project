from PyInstaller.utils.hooks import collect_data_files, copy_metadata, collect_submodules

# 收集st_aggrid的所有子模块
hiddenimports = collect_submodules('st_aggrid')

# 收集st_aggrid的前端资源
datas = collect_data_files('st_aggrid')

# 复制streamlit-aggrid的元数据
datas += copy_metadata('streamlit-aggrid')