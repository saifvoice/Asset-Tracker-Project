from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import configparser
from sqlalchemy import create_engine, engine_from_config


##### Database Configuration ######
config = configparser.ConfigParser()
config.read('cloud_db.ini')
hostname = config['HOST_DATA']['hostname']
username = config['USER_DATA']['username']
password = config['USER_DATA']['password']
database = config['USER_DATA']['database']

#### Connection ####
config = {'db.url': f'mysql+pymysql://{username}:{password}@{hostname}/{database}'}
engine = engine_from_config(config, prefix='db.')

df = pd.read_sql_table('customer_profile', engine)
df.drop(columns=['id', 'asset_count'], inplace=True)
engine.dispose()

df.columns = ['Name', 'Address', 'Phone No.', 'Product ID.', 'Latitude', 'Longitude']

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
                id='genco_table',
                data = df.to_dict('records'),
                style_cell = {'minWidth' :95, 'maxWidth':130, 'border': '#D3D3D3'},
                style_data = {'whiteSpace': 'normal', 'height':'auto', 'color': 'whitesmoke', 'backgroundColor': 'rgba(0,0,0,0.5)'},
                style_data_conditional = [{'if': {'row_index': 'odd'},'backgroundColor': 'rgba(171,174,197,0.5)', 'color':'#000000'}],
                style_header = {'textAlign': 'center', 'whiteSpace': 'normal', 'height': 'auto', 'fontWeight': 'bold', 'color': 'white', 'backgroundColor': '#303030'},
                style_filter = {'color': 'white', 'backgroundColor': '#606368'},  
                columns=[{'name':i, 'id':i} for i in df.columns],
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


