from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import configparser
from sqlalchemy import create_engine, engine_from_config
import pandas as pd


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

# enrol_form = dbc.



name_input = html.Div(
    [
        dbc.Label("Name", html_for="customer_name"),
        dbc.Input(type="text", id="customer_name", placeholder="Enter customer name"),
    ],
    className="mb-3")

address_input = html.Div(
    [
        dbc.Label("Address", html_for="form_address"),
        dbc.Input(type="text", id="form_address", placeholder="Enter customer address"),
    ],
    className="mb-3")

phone_input = html.Div(
    [
        dbc.Label("Phone No.", html_for="form_phone"),
        dbc.Input(type="tel", id="form_phone", placeholder="Enter customer phone no."),
    ],
    className="mb-3")

nin_input = html.Div(
    [
        dbc.Label("National ID No.", html_for="form_nin"),
        dbc.Input(type="number", id="form_nin", placeholder="Enter customer NIN")
    ],
    className="mb-3")

coordinates_input = html.Div(
    [
        dbc.Row([
            dbc.Label("Latitude", html_for="form_lat"),
            dbc.Col([dbc.Input(type="number", id="form_lat", placeholder="Enter latitude")]),
            dbc.Label("Longitude", html_for="form_lon"),
            dbc.Col([dbc.Input(type="number", id="form_lon", placeholder="Enter longitude")])
        ], class_name="row")
    ],
    className="mb-3")

assets = html.Div(
    [
        dbc.Label("Asset Given", html_for="asset_dropdown"),
        dcc.Dropdown(
            id="asset_dropdown",
            options=[
                {"label": "asset 1", "value": "asset 1"},
                {"label": "asset 2", "value": "asset 2"},
            ],
        ),
    ],
    className="mb-3",
)

form = dbc.Form([
    html.H3('Customer Enrolment Form', className='text-center'),
    name_input, address_input, phone_input, nin_input, coordinates_input, assets,
    html.Br(),
    html.Br(),
    dbc.Col(dbc.Button(id='enrol_button', children='Enrol', class_name='search_btn'), class_name='d-flex justify-content-center'),
    dbc.Col(dbc.Alert(id='enrolment_alert', fade=True, color='success', duration=3000, is_open=False)),
    html.Br(),
], id='enrol_form')



form_layout = dbc.Container([
    dbc.Col(form, class_name='col-sm-10 col-lg-8 p-4 container-shadow'),
], class_name='my-4 py-4 rounded d-flex justify-content-center')