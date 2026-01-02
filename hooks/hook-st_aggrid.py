from PyInstaller.utils.hooks import collect_data_files, copy_metadata

# 收集st_aggrid的前端资源
datas = collect_data_files('st_aggrid')

# 复制streamlit-aggrid的元数据
copy_metadata('streamlit-aggrid')