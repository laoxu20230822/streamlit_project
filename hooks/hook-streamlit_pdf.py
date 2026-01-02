from PyInstaller.utils.hooks import collect_data_files, copy_metadata

# 收集streamlit_pdf的前端资源
datas = collect_data_files('streamlit_pdf')

# 复制streamlit-pdf的元数据
copy_metadata('streamlit-pdf')
