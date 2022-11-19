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
config = {'db.url': f'mysql+pymysql://{username}:{password}@{hostname}/{database}'}
engine = engine_from_config(config, prefix='db.')

###### DataFrames #####
customer_profile_df = pd.read_sql_table('customer_profile', engine) 

customer_map = px.scatter_mapbox(
    customer_profile_df, lat='latitude', lon='longitude',
    hover_name='name', custom_data=['asset_count'],
    hover_data={'name': False, 'latitude':False, 'longitude':False, 'asset_count':True},
    zoom=5, center=dict(lat=9.0765, lon=8),
    mapbox_style = 'carto-positron', height=800)
customer_map.update_traces(marker=dict(size=25))
customer_map.update_layout(
    legend =dict(title_text = '', orientation='h', x=0.4, font_size=15, font_color='#FFFFFF'), paper_bgcolor='#E5ECF6',
    margin = dict(l = 0, r = 0, t = 0, b = 0)
)
#title=dict(font=dict(size=30, color='#FFFFFF'), text='<b>Customer Locations</b>', x=0.5, y=0.97)



home_layout = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Graph(figure=customer_map, id='map'), class_name='map col-sm-12 col-lg-10 rounded h-auto'),
        dbc.Col([
            dbc.Card([
            dbc.CardBody([
                html.H4('Remarks', className="fs-4 h4 fw-bold"),
                html.H5(id='genco_remarks', className="fs-5 h5"),
                html.Hr(),
                dcc.Markdown(id='remarks', className='fw-bold')
            ])
        ])
        ], align='center', class_name='text-center')
    ], class_name='align-top')
], fluid=True, class_name='my-4 py-4 rounded')

engine.dispose()

    