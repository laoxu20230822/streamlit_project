import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
df = pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")



gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection(
    selection_mode='single',     # Enable multiple row selection
    use_checkbox=False             # Show checkboxes for selection
)

#需要修复
grid_options = {
    'columnDefs': [
    { 'field': "athlete", 'minWidth': 150,},
    # First group by by country
    { 'field': "athlete", 'minWidth': 150, }
  ],
}
grid_response = AgGrid(df, gridOptions=grid_options)
selected_rows = grid_response['selected_rows']

# st.write(grid_response.selected_data['athlete'])
