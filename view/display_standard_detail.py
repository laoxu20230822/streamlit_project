import streamlit as st
from database.standard_index import init_standard_index_db

def display_standard_detail(standard_code:str):
    standard_index=init_standard_index_db()
    detail=standard_index.detail(standard_code)
    
    if not detail:
        st.error(f"未找到标准详情: {standard_code}")
        return

    html_stype="<hr style='margin: 0.5rem 0; border-color: grey;'></hr>"
    # st.html(
    # "<hr style='border: 1px solid #eee; margin: 1rem 0;'></hr>")
    st.markdown(f"""**标准英文名称：** {detail['english_name']}  
    {html_stype}""",unsafe_allow_html=True)
    #st.write(detail['english_name'])
    #st.markdown("---")
    
# ... existing code ...
    col1,col2=st.columns(2)
    with col1:
        col1.markdown(f"""**标准分类：** {detail['standard_type'] if detail['standard_type'] else '无'}  
        {html_stype}""",unsafe_allow_html=True)
        
        col1.markdown(f"""**专业：** {detail['specialty']}  
        {html_stype}""",unsafe_allow_html=True)
        col1.markdown(f"""**ICS分类号：** {detail['ics_classification']}
        {html_stype}""",unsafe_allow_html=True)
        col1.markdown(f"""**发布日期：** {detail['release_date']}  
        {html_stype}""",unsafe_allow_html=True)
        
    with col2:
        # 根据状态值决定显示颜色
        status_color = "red" if detail['status'] != "现行" else "inherit"
        col2.markdown(f"""**标准状态：** <span style="color: {status_color}">{detail['status']}</span>
        {html_stype}""",unsafe_allow_html=True)
        col2.markdown(f"""**标准性质：** {detail['standard_nature']}  
        {html_stype}""",unsafe_allow_html=True)
        col2.markdown(f"""**CCS分类号：** {detail['ccs_classification']}  
        {html_stype}""",unsafe_allow_html=True)
        col2.markdown(f"""**实施日期：** {detail['implementation_date']}  
        {html_stype}""",unsafe_allow_html=True)
    #st.markdown("##### 起草单位及其他")
    st.markdown(f"""**起草单位：** {detail['drafting_unit']}  
    {html_stype}""",unsafe_allow_html=True)
    st.markdown(f"""**起草人：** {detail['drafters']}  
    {html_stype}""",unsafe_allow_html=True)
    st.markdown(f"""**技术委员会（或技术归口单位）：** {detail['responsible_unit']}  
    {html_stype}""",unsafe_allow_html=True)