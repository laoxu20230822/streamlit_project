import streamlit as st

# 页面标题
st.title("🎧 我的音频播放器 Demo")

# 读取本地 mp3 文件
with open("audio/test.mp3", "rb") as f:
    audio_bytes = f.read()

# 在页面上显示播放器
st.audio(audio_bytes, format="audio/mp3")




