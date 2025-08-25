# #展示pdf
# pdf_path = "*.pdf"

# # 读取PDF并转base64
# with open(pdf_path, "rb") as f:
#     base64_pdf = b64encode(f.read()).decode("utf-8")


# @st.dialog("标准内容",width="large")
# def show_pdf(base64_pdf):
#     pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#     st.markdown(pdf_display, unsafe_allow_html=True)

# # # 按钮点击后显示PDF
# if st.button("打开 PDF"):
#     show_pdf(base64_pdf)
