import sys
import os

# ----------------- PyInstaller 运行时路径修复：开始 -----------------
# 检查程序是否被 PyInstaller 打包
if hasattr(sys, '_MEIPASS'):
    # 如果是，则将当前工作目录更改为 PyInstaller 创建的临时目录
    os.chdir(sys._MEIPASS)
# ----------------- PyInstaller 运行时路径修复：结束 -----------------

import streamlit.web.cli as stcli
import os, sys

# 设置 Streamlit 环境变量
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "false"

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        current_dir = sys._MEIPASS
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "hello.py")

    sys.argv = ["streamlit", "run", file_path,
        "--server.enableCORS=true", "--server.enableXsrfProtection=false",
        "--global.developmentMode=false", "--client.toolbarMode=minimal"]
    sys.exit(stcli.main())