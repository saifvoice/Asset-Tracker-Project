from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import configparser
from sqlalchemy import create_engine, engine_from_config
import pandas as pd


##### Database Configuration ######
config = configparser.ConfigParser()
config.read('local_db.ini')
hostname = config['HOST_DATA']['hostname']
username = config['USER_DATA']['username']
password = config['USER_DATA']['password']
database = config['USER_DATA']['database']

#### Connection ####
# config = {'db.url': f'mysql+pymysql://{username}:{password}@{hostname}/{database}'}
# engine = engine_from_config(config, prefix='db.')

###### DataFrames #####
# customer_profile_df = pd.read_sql_table('customer_profile', engine) 

# customer_map = px.scatter_mapbox(
#     customer_profile_df, lat='latitude', lon='longitude',
#     hover_name='name', custom_data=['id', 'name', 'address', 'phone', 'nin', 'asset_count', 'latitude', 'longitude'],
#     hover_data={'name': False, 'latitude':False, 'longitude':False, 'asset_count':True},
#     zoom=6, center=dict(lat=9.0765, lon=8),
#     mapbox_style = 'carto-positron', height=800, )
# customer_map.update_traces(marker=dict(size=15, color='#fe6b6b'))
# customer_map.update_layout(
#     legend =dict(title_text = '', orientation='h', x=0.4, font_size=15, font_color='#FFFFFF'), paper_bgcolor='#E5ECF6',
#     margin = dict(l = 0, r = 0, t = 0, b = 0)
# )


animation= {'frame': { 'redraw': False, }, 'transition': { 'duration': 1000, 'ease': 'linear', }}


home_layout = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Graph(id='customer_map', className='card', animate=True, animation_options=animation, style={'height': '75vh'}), class_name='map h-auto col-sm-12 col-lg-9 rounded h-auto'),
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
            dbc.Button('Search', id='search_button', class_name='search_btn my-3'),
            dbc.Card([
            dbc.CardBody([
                html.H4('Customer Info', className="fs-3 h4 fw-bold"),
                html.Hr(),
                html.Br(),
                dcc.Markdown(id='info_markdown', className='fs-5 text-start')
            ])
        ], class_name='card')
        ], align='center', class_name='text-center col-sm-6 col-lg-3')
    ], class_name='align-top')
], fluid=True, class_name='mt-3 py-4 rounded')

# engine.dispose()

    