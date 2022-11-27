from dash import dash_table
import dash_bootstrap_components as dbc

style_1 = {
    "background": "rgba(255,255,255,0.5)",
   " -webkit-backdrop-filter": 'blur(10px)',
   ' backdrop-filter':' blur(10px)',
   ' border': '1px solid rgba(255,255,255,0.25)'
}


customer_records = dbc.Container(
    dbc.Row([
        dbc.Col([
            dbc.Spinner(dash_table.DataTable(
                id='customer_table',
                style_cell = {'minWidth' :95, 'maxWidth':130, 'border': '#D3D3D3'},
                style_data = {'whiteSpace': 'normal', 'height':'auto', 'color': 'whitesmoke', 'backgroundColor': 'rgba(0,0,0,0.5)'},
                style_data_conditional = [{'if': {'row_index': 'odd'},'backgroundColor': 'rgba(171,174,197,0.5)', 'color':'#000000'}],
                style_header = {'textAlign': 'center', 'whiteSpace': 'normal', 'height': 'auto', 'fontWeight': 'bold', 'color': 'white', 'backgroundColor': '#303030'},
                style_filter = {'color': 'white', 'backgroundColor': '#606368'},
                filter_action='native',
                sort_action='native',
                sort_mode='single',
                page_action= 'native',
                page_current=0,
                page_size=30,
                export_format='xlsx',
                style_cell_conditional=(
                    [
                        {
                            'if': {'column_id': c}, 'textAlign':'left' 
                        } for c in ['Name', 'Address']
                    ] +
                    [
                        {
                            'if': {'column_id': c}, 'textAlign':'right' 
                        } for c in ['Phone No.', 'Product ID.']
                    ] 
                ),
            ))
        ], class_name='col-xs-12 col-lg-10 shadow rounded', style=style_1)
    ],class_name='justify-content-center align-items-center gx-1')
, fluid=True)


