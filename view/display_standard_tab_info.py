import uuid
import streamlit as st
from database.standard_db import init_standard_db
from database.standard_index import init_standard_index_db
from view.display_standard_detail import display_standard_detail
from view.display_standard_glossary import display_standard_glossary
from view.display_standard_references import display_standard_references
from view.display_product_standard import display_product_standard
from view.display_craft_standard import display_craft_standard
from view.display_standard_structure import display_standard_structure
import uuid
from streamlit_extras.stylable_container import stylable_container


def get_chapter_content(data_list, selected_chapter):
    # 初始化结果列表
    result = []
    # 遍历数据列表
    for item in data_list:
        chapter = item["min_chapter_code"]
        # 检查当前章节是否是选定章节或其子章节
        # 条件1：完全匹配（当前章节）
        # 条件2：以选定章节+点开头（子章节）
        if chapter == selected_chapter or chapter.startswith(f"{selected_chapter}."):
            result.append(item["standard_content"])

    return result


def display_standard_info(standard_code, standard_name):
    html_stype = "<hr style='margin: 0.5rem 0; border-color: grey;'></hr>"

    st.write(f"**标准号**：{standard_code}")
    # st.markdown(f"""
    # >:blue[{standard_code}]\n
    # >#### {standard_name}
    # """)


def display_standard_cotent(standard_code: str):
    standard_db = init_standard_db()
    standard_detail = standard_db.standard_detail(standard_code)
    t21, t22 = st.columns([4, 6])
    with t21.container(border=True, height=600):
        display_standard_structure(standard_code)
    with t22.container(border=True, height=600):
        if "chapter" in st.session_state and "chapter_content" in st.session_state:
            contents = get_chapter_content(standard_detail, st.session_state.chapter)
            st.markdown("\n\n".join(contents))
            # if st.session_state.chapter in st.session_state.chapter_content:
            #     content_arr=st.session_state.chapter_content[st.session_state.chapter]
            #     head=content_arr[0]
            #     st.markdown(head)
            #     for content in content_arr[1:]:
            #         st.markdown(content)


def display_standard_tab_info():
    if "selected_rows" in st.session_state:
        standard_code = st.session_state["selected_rows"][0]["standard_code"]
        standard_name = st.session_state["selected_rows"][0]["standard_name"]
        # 查询一级门类编号
        standard_db = init_standard_db()
        level1_code_data = standard_db.query_category_level1_code(standard_code)
        if level1_code_data is not None and level1_code_data[0] == "104":
            level1_code = level1_code_data[0]
            product_or_craft_tab_name = "相关产品"
            st.session_state.pc_type = "product"
        elif level1_code_data is not None and level1_code_data[0] in [
            "103",
            "106",
            "107",
        ]:
            product_or_craft_tab_name = "工业标准"
            st.session_state.pc_type = "craft"
        else:
            product_or_craft_tab_name = "其他"
            st.session_state.pc_type = "other"
        col1, col2 = st.columns([9, 1])

        t1, t2, t3, t4, t5 = col1.tabs(
            [
                "**基本信息**",
                "**目次及原文**",
                "**规范性引用清单**",
                "**术语**",
                "**" + product_or_craft_tab_name + "**",
            ]
        )
        # standard_code = df.iloc[selected_row]['standard_code']

        ## 显示标准详情
        with t1:
            display_standard_info(standard_code, standard_name)
            display_standard_detail(standard_code)

        # 显示目次信息
        with t2:
            display_standard_info(standard_code, standard_name)
            display_standard_cotent(standard_code)
        # st.markdown("---")

        # 引用文件
        with t3:
            display_standard_info(standard_code, standard_name)
            display_standard_references(standard_code)

        # 术语信息
        with t4:
            display_standard_info(standard_code, standard_name)
            display_standard_glossary(standard_code)

        # 工艺标准 or 产品标准
        with t5:
            display_standard_info(standard_code, standard_name)
            if st.session_state.pc_type == "product":
                display_product_standard(standard_code)
            elif st.session_state.pc_type == "craft":
                display_craft_standard(standard_code)
            else:
                st.write("other")

        with col2:
            # 处理PDF文件名：将standard_code中的"/"替换为下划线
            pdf_filename = standard_code.replace("/", "_") + ".pdf"
            pdf_path = f"static/{pdf_filename}"
            # 检查PDF文件是否存在，如果存在则将标准号显示为可点击的链接
            import os

            if os.path.exists(pdf_path):
                # 创建对话框来显示PDF
                @st.dialog(f"{standard_code}", width="large")
                def show_pdf_dialog():
                    st.pdf(pdf_path, height=400)

                if st.button(f"PDF"):
                    show_pdf_dialog()
            else:
                st.markdown(f"**文件不存在**", unsafe_allow_html=True)
                    
