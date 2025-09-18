# hooks/hook-rpds.py
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files

# 收集 rpds 包内的所有动态库文件 (最重要的就是那个 .pyd)
binaries = collect_dynamic_libs('rpds')

# 如果 rpds 包还有其他数据文件，也可以一并收集（作为保险）
datas = collect_data_files('rpds')