import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from streamlit.elements.lib.layout_utils import Height
import os
##https://discuss.streamlit.io/t/display-images-in-aggrid-table/18434/10


def showimg():
    import streamlit as st
    import pandas as pd
    from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建images文件夹的绝对路径
    images_dir = os.path.join(current_dir, '..', 'images')
    if not os.path.exists(images_dir):
        st.error(f"图片文件夹不存在: {images_dir}")
        return
    # 获取images文件夹中的所有图片文件
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']


    # 示例数据
    data = {
        "Name": ["Cat", "Dog"],
        "Thumbnail": [
            "/app/static/logo2.png",
            "https://placedog.net/100/100"
        ],
        "Original": [
            "https://placedog.net/400/400",
            "https://placedog.net/400/400"
        ]
    }

    df = pd.DataFrame(data)
    # 自定义JS渲染器
    cell_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {
            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '100');
            this.eGui.setAttribute('height', '100');
            this.eGui.style.objectFit = 'cover';
            this.eGui.style.cursor = 'pointer';
            }
            getGui() {
                console.log(this.eGui);
                return this.eGui;
            }
        }
    """)
    cell_renderer_for_name = JsCode("""
        class NameRenderer {
            init(params) {
            this.eGui = document.createElement('div');
            this.eGui.innerText = params.value;
            this.eGui.style.fontWeight = 'bold';
            this.eGui.style.color = 'blue';
            }
            getGui() {
                console.log(this.eGui);
                return this.eGui;
            }
        }
    """)

    cell_renderer_for_img = JsCode("""
        class NameRenderer {
            init(params) {
            this.eGui = document.createElement('div');
            this.eGui.innerHTML = "<img src='/"+params.value+"' alt='logo' width='100' height='100'>";
            }
            getGui() {
                return this.eGui;
            }
        }
    """)

    # 配置AgGrid
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column("Thumbnail", cellRenderer=cell_renderer_for_img, header_name="Thumbnail",width=300,autoHeight=True)
    gb.configure_column("Name",cellRenderer=cell_renderer_for_name,header_name="Name",width=100)
    grid_options = gb.build()

    # 显示表格
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True
    )

    selected_rows = grid_response['selected_rows']
    # 如果有选中行，就弹出原图
    if selected_rows is not None:
        original_url = selected_rows[0]["Original"]
        with st.modal("原图预览"):
            st.image(original_url, use_column_width=True)

if __name__ == '__main__':
    showimg()
