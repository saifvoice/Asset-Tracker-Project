from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc


markdown_1 = f'''
            * **Name:** 
            * **Address:** 
            * **Phone No.:** 
            * **Product ID.: ** 
            * **No of assets in posession: ** 
            '''

search_layout = html.Div(
    dbc.Col([
            dcc.Dropdown(
                options=[
                    {'label':'Name', 'value':'name'},
                    {'label':'Phone No.', 'value':'phone'},
                    {'label':'National ID.', 'value':'nin'}
                ],
                id='search_by', placeholder = 'Search by', className='dropdown my-3', searchable=False, clearable=False
            ),
            dcc.Dropdown(
                id = 'customer_dd', placeholder= 'Search customer', className='dropdown', optionHeight=50, disabled=True
            ),
            dbc.Button('Search', id='search_button', class_name='search_btn my-3', href=''),
            dbc.Card([
            dbc.CardBody([
                html.H4('Customer Info', className="fs-3 h4 fw-bold"),
                html.Hr(),
                html.Br(),
                dcc.Markdown(markdown_1, id='info_markdown', className='fs-5 text-start')
            ])
        ], class_name='card mt-5')
        ], align='center', class_name='text-center col-sm-6 col-lg-3 mx-auto mt-5')
)