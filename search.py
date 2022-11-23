from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import configparser
from sqlalchemy import create_engine, engine_from_config
import pandas as pd


search_layout = html.Div(
    dbc.Col([
            dcc.Dropdown(
                options=[
                    {'label':'Name', 'value':'name'},
                    {'label':'Phone No.', 'value':'phone'},
                    {'label':'National ID.', 'value':'nin'}
                ],
                id='search_byx', placeholder = 'Search by', className='dropdown my-3', searchable=False, clearable=False
            ),
            dcc.Dropdown(
                id = 'customer_ddx', placeholder= 'Search customer', className='dropdown', optionHeight=50, disabled=True
            ),
            dbc.Button('Search', id='search_buttonx', class_name='search_btn my-3'),
            dbc.Card([
            dbc.CardBody([
                html.H4('Customer Info', className="fs-3 h4 fw-bold"),
                html.Hr(),
                html.Br(),
                dcc.Markdown(id='info_markdownx', className='fs-5 text-start')
            ])
        ], class_name='card')
        ], align='center', class_name='text-center col-sm-6 col-lg-3 mx-auto')
)