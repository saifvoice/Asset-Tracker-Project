from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from home import home_layout
from enrol import form_layout
from urllib.parse import unquote
import configparser
from sqlalchemy import create_engine, engine_from_config
import mysql.connector
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
engine.dispose()
content = ['home', 'enrol']
nav = dbc.Nav([
        dbc.NavItem(dbc.NavLink("Home", id='home', href='/home'),  class_name='me-1'),
        dbc.NavItem(dbc.NavLink("Enrol", id='enrol', href='/enrol'),  class_name='me-1'),
        dbc.NavItem(dbc.NavLink("Records", id='records', href='/records'),  class_name='me-1'),
        dbc.NavItem(dbc.NavLink("Logout", id='logout', href='/login'), class_name='me-1')
],navbar=True, justified=True, class_name='ms-auto fs-5')

navbar = dbc.Navbar(
    dbc.Container([
        dbc.Col([
            html.A([
                dbc.Row([
                    dbc.Col(html.Img(src='assets/tbcn-logo2.png', width=200, height=100,className='navbar-brand rounded float-start')),
                    dbc.Col(dbc.NavbarBrand("TBCN", className="me-auto"), class_name='text-start')
                ], align='center', className='g-0'),
            ], href='/'),
        ], align='start', class_name='col-3'),
        dbc.Col(html.H1('Save-80 Asset Tracker'), class_name='col-6 text-center'),
        dbc.Col([
            dbc.NavbarToggler(id='nav-toggler', n_clicks=0),
            dbc.Collapse(nav, id='navbar-collapse', is_open=False, navbar=True)
        ])
    ], fluid=True, class_name='d-flex justify-content-center')
,id='navbar', class_name='navbar')


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Save-80"

app.layout = dbc.Container([
    dcc.Location(id='location'),
    dbc.Row(navbar, class_name='sticky-top'),
    dbc.Row(
            dbc.Col(id='content_container', xl={'size':10, 'offset':1}, lg={'size':10, 'offset':1})
        ),
    dbc.Row([
        dbc.Col([
            html.H3('Powered by TCBN')
        ], class_name='text-center')
    ], class_name='d-flex justify-content-center footer navbar')    
], fluid=True)


app.validation_layout = html.Div([home_layout, form_layout])


@app.callback(
    Output('content_container', 'children'),
    Output('home', 'active'),
    Output('enrol', 'active'),
    Output('records', 'active'),
    Output('logout', 'active'),
    Input('location', 'pathname')
)
def display_content(pathname):
    page = unquote(pathname[1:])
    if page in content:
        if page == 'home':
            return home_layout, True, False, False, False
        if page == 'enrol':
            return form_layout, False, True, False, False
    else:
        return home_layout, True, False, False, False

@app.callback(
    Output('enrolment_alert', 'color'),
    Output('enrolment_alert', 'is_open'),
    Output('enrolment_alert', 'children'),
    Input('enrol_button', 'n_clicks'),
    Input('customer_name', 'value'),
    Input('form_address', 'value'),
    Input('form_phone', 'value'),
    Input('form_nin', 'value'),
    Input('form_lat', 'value'),
    Input('form_lon', 'value'),
    Input('asset_dropdown', 'value')
)
def enrolment_form(n, name, address, phone, nin, lat, lon, asset):
    data = {'name': name, 'address': address, 'phone': phone, 'nin': nin, 'latitude':lat, 'longitude':lon, 'asset':asset}
    for i in data.values():
        print(type(i))
    for i in data.values():
        if not i:
            color = 'danger'
            is_open = True
            msg = 'Please fill all the given fields'
            return color, is_open, msg
    config = {'db.url': f'mysql+pymysql://{username}:{password}@{hostname}/{database}'}
    engine = engine_from_config(config, prefix='db.')
    query = "insert into customer_profile (name, address, phone, nin, asset_count, latitude, longitude) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    values = (name, address, phone, nin, 1, lat, lon)

    engine.execute(query, values)
    color = 'success'
    is_open = True
    msg = 'Customer enrolled successfully'

    # try:
    #     engine.execute(query, values)
    #     color = 'success'
    #     is_open = True
    #     msg = 'Customer enrolled successfully'
    # except:
    #     color = 'danger'
    #     is_open = True
    #     msg = 'Enrolment failed! Make sure you enter the correct values'
    engine.dispose()
    
    return color, is_open, msg

    


if __name__ =='__main__':
    app.run_server()