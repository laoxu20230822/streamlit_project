1. **Identify the Problem**: The error occurs because `st.session_state.quality_control` and `st.session_state.hse_requirements` are accessed directly without being initialized first.

2. **Correct Initialization Pattern**: Follow the same pattern used in `show_metric_select_boxes` function:

   * Use `st.session_state.get("variable_name", "全部")` to safely get values with default "全部"

   * Update session\_state with these values to ensure they're properly initialized

3. **Modify** **`show_method_select_boxes`** **function**:

   * Add initialization for all session\_state variables at the beginning of the function

   * Include `performance_indicator_level1`, `performance_indicator_level2`, `product_category1`, `product_category2`, `product_name`, `quality_control`, and `hse_requirements`

   * Update session\_state with these initialized values

4. **Fix Both Functions**: Apply the same fix to both `show_method_select_boxes` and `display_method_query_list_new` functions to ensure consistent initialization

5. **Testing**: The fix will ensure that all session\_state variables are properly initialized before being accessed, preventing the AttributeError

**Files to Modify**:

* `/Users/xuminghui/code/uv_project_install/streamlit_project/view/display_method_query_list.py`

