#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监听剪贴板，有新文本就追加到文件
"""
import os
import time
import pathlib
import subprocess

FILE = pathlib.Path.home() / "Desktop/voice-log.txt"   # 想写哪就改哪
LAST_HASH = ""

def get_clipboard() -> str:
    """通过 pbpaste 取文本，比 pyperclip 更轻"""
    return subprocess.check_output("pbpaste", text=True)

def append_line(text: str):
    """追加一行，带时间戳"""
    text = text.strip()
    if not text:
        return
    with FILE.open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%F %T')}  {text}\n")

if __name__ == "__main__":
    while True:
        try:
            
            txt = get_clipboard()
            h = hash(txt)
            if h != LAST_HASH:          # 内容变化才写
                LAST_HASH = h
                append_line(txt)
                print(f"append: {txt}")
        except Exception:
            pass
        time.sleep(1)                 # CPU 占用≈0