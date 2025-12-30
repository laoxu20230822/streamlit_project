from calendar import c
import uuid
import streamlit as st
from database.chart import init_standard_chart_db
from database.standard_db import init_standard_db
from database.standard_index import init_standard_index_db
from database.page import Pageable
from database.standard_db import WhereCause
from st_aggrid import AgGrid, JsCode
import pandas as pd
from view.display_standard_detail import display_standard_detail
from view.display_standard_glossary import display_standard_glossary
from view.display_standard_references import display_standard_references
from view.display_standard_detail import display_standard_detail
from view.display_product_standard import display_product_standard
from view.display_craft_standard import display_craft_standard
from view.display_standard_structure import display_standard_structure
from view.display_standard_tab_info import display_standard_tab_info
import urllib.parse
from pathlib import Path
from utils.data_utils import count_unique_standard_codes
from view.display_ccgz_query_list import show_ccgz_select_boxes

imageRenderer = JsCode(
    """
    class ImageRenderer {
        init(params) {
            this.params = params;
            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '100');
            this.eGui.setAttribute('height', '100');
            this.eGui.style.objectFit = 'cover';
            this.eGui.style.cursor = 'pointer';
            
            // 添加点击事件监听器
            this.eGui.addEventListener('click', () => this.showImageModal());
        }
        
        getGui() {
            return this.eGui;
        }
        
        // 显示图片模态对话框
        showImageModal() {
            // 获取完整图片路径（大图）
            const fullImagePath = this.params.value;
            const imageName = this.params.data.in_text_name;
            
            // 创建模态对话框
            const modal = document.createElement('div');
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            modal.style.display = 'flex';
            modal.style.justifyContent = 'center';
            modal.style.alignItems = 'center';
            modal.style.zIndex = '9999';
            modal.style.cursor = 'pointer';
            
            // 创建图片容器
            const imageContainer = document.createElement('div');
            imageContainer.style.position = 'relative';
            imageContainer.style.maxWidth = '90%';
            imageContainer.style.maxHeight = '90%';
            imageContainer.style.backgroundColor = 'white';
            imageContainer.style.borderRadius = '8px';
            imageContainer.style.padding = '20px';
            imageContainer.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
            
            // 创建标题
            const title = document.createElement('h3');
            title.textContent = imageName;
            title.style.margin = '0 0 15px 0';
            title.style.textAlign = 'center';
            title.style.color = '#333';
            title.style.fontSize = '18px';
            
            // 创建大图
            const largeImage = document.createElement('img');
            largeImage.setAttribute('src', fullImagePath);
            largeImage.style.maxWidth = '100%';
            largeImage.style.maxHeight = '70vh';
            largeImage.style.objectFit = 'contain';
            largeImage.style.borderRadius = '4px';
            
            // 创建关闭按钮
            const closeButton = document.createElement('button');
            closeButton.innerHTML = '✕';
            closeButton.style.position = 'absolute';
            closeButton.style.top = '10px';
            closeButton.style.right = '10px';
            closeButton.style.backgroundColor = '#ff4444';
            closeButton.style.color = 'white';
            closeButton.style.border = 'none';
            closeButton.style.borderRadius = '50%';
            closeButton.style.width = '30px';
            closeButton.style.height = '30px';
            closeButton.style.cursor = 'pointer';
            closeButton.style.fontSize = '18px';
            closeButton.style.fontWeight = 'bold';
            closeButton.style.display = 'flex';
            closeButton.style.alignItems = 'center';
            closeButton.style.justifyContent = 'center';
            
            // 添加关闭事件
            const closeModal = () => {
                document.body.removeChild(modal);
            };
            
            closeButton.addEventListener('click', closeModal);
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    closeModal();
                }
            });
            
            // ESC键关闭
            document.addEventListener('keydown', function escHandler(e) {
                if (e.key === 'Escape') {
                    closeModal();
                    document.removeEventListener('keydown', escHandler);
                }
            });
            
            // 组装模态框
            imageContainer.appendChild(closeButton);
            imageContainer.appendChild(title);
            imageContainer.appendChild(largeImage);
            modal.appendChild(imageContainer);
            
            // 显示模态框
            document.body.appendChild(modal);
            
            console.log('Modal opened for image:', fullImagePath);
        }
    }
"""
)


def show_grid(data, key: str):
    df = pd.DataFrame(
        data if data else [],
        columns={
            "standard_code": "标准号",
            "standard_name": "标准名称",
            "in_text_number": "文中编号",
            "in_text_name": "文中名称",
            "image_file_name": "图文件名称",
        },
    )
    df.insert(0, "seq", range(1, len(df) + 1))
    df["standard_info"] = df["standard_code"] + " " + df["standard_name"] + ""

    # 使用下划线
    # df["image_file_name"]="Q_SY 01017-2018岩石物理分析成果数据存储文件结构"

    def get_safe_image_path(image_file_name):
        result = get_image_path_safe(image_file_name, base_path="static")
        return result["actual_path"] if result["exists"] else None

    df["image_info_path"] = "app/" + df["image_file_name"].apply(get_safe_image_path)
    # 过滤掉图片不存在的行
    # df = df[df["image_info_path"].notna()].copy()
    df["image_info"] = "/app/" + df["image_file_name"].apply(get_safe_image_path)
    df["in_text_name"] = df["in_text_number"] + " " + df["in_text_name"]
    grid_options = {
        "defaultColDef": {
            "filter": True,  # 开启过滤
            # "floatingFilter": True,   # 列头下方的小输入框
            "sortable": True,  # 可排序
            "resizable": True,  # 可拖动列宽
        },
        "enableCellTextSelection": True,
        "suppressNoRowsOverlay": True,
        "columnDefs": [
            {
                "field": "seq",
                "headerName": "序号",
                "width": 40,
                "suppressSizeToFit": True,
            },
            {
                "field": "standard_code",
                "headerName": "标准号",
                "hide": True,
            },
            {"field": "standard_name", "headerName": "标准名称", "hide": True},
            {
                "field": "in_text_number",
                "headerName": "文中编号",
                "width": 100,
                "hide": True,
            },
            {
                "field": "in_text_name",
                "headerName": "图片名称",
                "width": 250,
                "suppressSizeToFit": True,
            },
            {"field": "image_info_path", "headerName": "图片路径", "hide": True},
            {
                "field": "image_info",
                "headerName": "图片",
                "cellRenderer": imageRenderer,
                "width": 100,
                "autoHeight": True,
            },
            {"field": "standard_info", "headerName": "标准来源", "width": 400},
        ],
        "rowSelection": {
            "mode": "singleRow",
            "checkboxes": False,
            "enableClickSelection": True,
        },
        "autoSizeStrategy": {"type": "fitCellContents"},
        "pagination": True,
        ##"paginationAutoPageSize": True,
        "paginationPageSize": 50,
    }
    # 显示统计信息
    unique_count = count_unique_standard_codes(df)
    st.markdown(f"**查询标准总数: {unique_count}**")

    return AgGrid(
        df,
        gridOptions=grid_options,
        height=400,
        key=key,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
    )


#TODO 将查询放在一个数据层，返回元组
def display_chart_query_list(search_term: str,
                             imageData,tableData,formulaData):
    t1, t2, t3 = st.tabs(
        [
            "**图片**",
            "**表格**",
            "**公式**",
        ]
    )
    with t1:
        show_ccgz_select_boxes(prefix="chart", data=imageData)
        grid_response = show_grid(imageData, "image")
        selected_rows = grid_response["selected_rows"]
        if selected_rows is not None:
            st.session_state.selected_rows = [
                {
                    "standard_code": row["standard_code"],
                    "standard_name": row["standard_name"],
                    "image_info_path": row["image_info_path"],
                }
                for _, row in selected_rows.iterrows()
            ]
        if "selected_rows" in st.session_state:
            display_standard_tab_info()

    with t2:
        show_ccgz_select_boxes(prefix="chart", data=tableData)
        grid_response = show_grid(tableData, "table")
        selected_rows = grid_response["selected_rows"]
        if selected_rows is not None:
            st.session_state.selected_rows = [
                {
                    "standard_code": row["standard_code"],
                    "standard_name": row["standard_name"],
                    "image_info_path": row["image_info_path"],
                }
                for _, row in selected_rows.iterrows()
            ]
        if "selected_rows" in st.session_state:
            display_standard_tab_info()

    with t3:
        show_ccgz_select_boxes(prefix="chart", data=formulaData)
        grid_response = show_grid(formulaData, "formula")
        selected_rows = grid_response["selected_rows"]
        if selected_rows is not None:
            st.session_state.selected_rows = [
                {
                    "standard_code": row["standard_code"],
                    "standard_name": row["standard_name"],
                    "image_info_path": row["image_info_path"],
                }
                for _, row in selected_rows.iterrows()
            ]
        if "selected_rows" in st.session_state:
            display_standard_tab_info()



def get_image_path_safe(image_file_name, base_path="static"):
    """
    安全的图片路径获取函数，支持多种后缀名检查

    Args:
        image_file_name: 图片文件名（不含后缀）
        base_path: 基础路径，默认为"static"

    Returns:
        dict: 包含路径信息和状态的字典
        {
            'original_path': 原始构造路径,
            'actual_path': 实际存在的路径,
            'exists': 是否存在,
            'available_extensions': 可用的后缀名列表,
            'error': 错误信息（如果有）
        }
    """
    # 清理文件名，替换特殊字符
    clean_file_name = image_file_name.replace("/", "_").replace("\\", "_")

    # 支持的后缀名列表，按优先级排序
    supported_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"]

    # 基础路径处理
    base_path_obj = Path(base_path)

    # 构造原始路径（保持兼容性）
    original_path = f"{base_path}/{clean_file_name}.png"

    # 检查各种后缀的文件是否存在
    available_paths = []
    actual_path = None

    for ext in supported_extensions:
        test_path = base_path_obj / f"{clean_file_name}{ext}"
        if test_path.exists():
            available_paths.append(str(test_path))
            if actual_path is None:  # 优先使用第一个找到的
                actual_path = str(test_path)

    # 返回结果字典
    result = {
        "original_path": original_path,
        "actual_path": actual_path or original_path,  # 如果没有找到，使用原始路径
        "exists": actual_path is not None,
        "available_extensions": available_paths,
        "error": None if actual_path else f"未找到图片文件: {clean_file_name}",
    }

    return result
