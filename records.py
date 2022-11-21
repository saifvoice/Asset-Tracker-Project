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
engine.dispose()

df.columns = ['ID', 'Name', 'Address', 'Phone No.', 'National ID.', 'Asset(s)', 'Latitude', 'Longitude']


customer_records = dbc.Container(
    dbc.Row([
        dbc.Col([
            dbc.Spinner(dash_table.DataTable(
                id='genco_table',
                data = df.to_dict('records'),
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
                        } for c in ['Phone No.', 'National ID.', 'Asset(s)']
                    ] +
                    [
                        {
                            'if': {'column_id': 'ID'}, 'textAlign':'center'
                        }
                    ]
                ),
            ))
        ], class_name='col-xs-12 col-lg-10 shadow rounded')
    ],class_name='justify-content-center align-items-center gx-1')
, fluid=True)


