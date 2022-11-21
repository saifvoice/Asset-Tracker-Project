from dash_extensions.enrich import  DashProxy, Output, Input, State, ServersideOutput, html, dcc, Trigger, FileSystemStore, ServersideOutputTransform, FileSystemCache
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from home import home_layout
from enrol import form_layout
from urllib.parse import unquote
import configparser
from sqlalchemy import create_engine, engine_from_config
import mysql.connector
import pandas as pd
import random
import plotly.express as px
from records import customer_records
from flask_caching import Cache


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
                    dbc.Col([
                        html.Img(src='assets/tbcn-logo.png', width=200, height=100,className='navbar-brand rounded float-start'),
                    ]),
                    dbc.Col(html.Img(src='assets/atmosfair.png', width=200, height=100,className='navbar-brand rounded float-start'))
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


app = DashProxy(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], transforms=[ServersideOutputTransform()])
app.title = "Save-80"
server = app.server
# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'filesystem',
#     'CACHE_DIR': 'cache-directory',
#     # should be equal to maximum number of users on the app at a single time
#     # higher numbers will store more data in the filesystem / redis cache
#     'CACHE_THRESHOLD': 5})
fss = FileSystemStore(threshold=5)

main_layout = dbc.Container([
    dcc.Store(id='cached_data'),
    dcc.Location(id='location'),
    dcc.Interval(id='query_data', interval=10*1000),
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


app.validation_layout = html.Div([main_layout, home_layout, form_layout, customer_records])

app.layout = main_layout

@app.callback(
    ServersideOutput('cached_data', 'data', backend=fss),
    Input('query_data', 'n_intervals')
, memoize=True)
def query_data(n):
    config = {'db.url': f'mysql+pymysql://{username}:{password}@{hostname}/{database}'}
    engine = engine_from_config(config, prefix='db.')

    df = pd.read_sql_table('customer_profile', engine)
    engine.dispose()
    return df


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
        if page == 'records':
            return customer_records, False, False, True, False
    else:
        return home_layout, True, False, False, False


@app.callback(
    Output('customer_map', 'figure'),
    Input('cached_data', 'data'),
    Input('customer_map', 'clickData')
)
def plot_map_points(data, clickdata):
    if clickdata == None:
        customer_map = px.scatter_mapbox(
            data, lat='latitude', lon='longitude',
            hover_name='name', custom_data=['id', 'name', 'address', 'phone', 'nin', 'asset_count', 'latitude', 'longitude'],
            hover_data={'name': False, 'latitude':False, 'longitude':False, 'asset_count':True},
            zoom=6, center=dict(lat=9.0765, lon=8),
            mapbox_style = 'carto-positron', height=800, )
        customer_map.update_traces(marker=dict(size=15, color='#fe6b6b'))
        customer_map.update_layout(
            legend =dict(title_text = '', orientation='h', x=0.4, font_size=15, font_color='#FFFFFF'), paper_bgcolor='#E5ECF6',
            margin = dict(l = 0, r = 0, t = 0, b = 0)
        )
    else:
        customer_map = px.scatter_mapbox(
            data, lat='latitude', lon='longitude',
            hover_name='name', custom_data=['id', 'name', 'address', 'phone', 'nin', 'asset_count', 'latitude', 'longitude'],
            hover_data={'name': False, 'latitude':False, 'longitude':False, 'asset_count':True},
            zoom=10, center=dict(lat=clickdata['points'][0]['lat'], lon=clickdata['points'][0]['lon']),
            mapbox_style = 'carto-positron', height=800 )
        customer_map.update_traces(marker=dict(size=15, color='#fe6b6b'))
        customer_map.update_layout(
            legend =dict(title_text = '', orientation='h', x=0.4, font_size=15, font_color='#FFFFFF'), paper_bgcolor='#E5ECF6',
            margin = dict(l = 0, r = 0, t = 0, b = 0)
        )


    return customer_map





@app.callback(
    Output('customer_dd', 'options'),
    Output('customer_dd', 'disabled'),
    Output('customer_dd', 'placeholder'),
    Input('search_by', 'value'),
    Input('cached_data', 'data')
)
def dropdown_items(value, data):
    labels = {'name': 'Name', 'phone': 'Phone No.', 'nin':'National ID.'}
    if value == None:
        raise PreventUpdate
    options = [{'label':value, 'value':value} for value in data[value].tolist()]
    disabled = False
    placeholder = f'Search by {labels[value]}'


    return options, disabled, placeholder





@app.callback(
    Output('enrolment_alert', 'color'),
    Output('enrolment_alert', 'is_open'),
    Output('enrolment_alert', 'children'),
    Input('enrol_button', 'n_clicks'),
    State('customer_name', 'value'),
    State('form_address', 'value'),
    State('form_phone', 'value'),
    State('form_nin', 'value'),
    State('form_lat', 'value'),
    State('form_lon', 'value'),
    State('asset_dropdown', 'value'),
    prevent_initial_call=True
)
def enrolment_form(n, name, address, phone, nin, lat, lon, asset):
    data = {'name': name, 'address': address, 'phone': phone, 'nin': nin, 'latitude':lat, 'longitude':lon, 'asset':asset}
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



@app.callback(
    Output('customer_map', 'clickData'),
    Input('search_button', 'n_clicks')
)
def clear_clickdata(n):
    return None
    


@app.callback(
    Output('info_markdown', 'children'),
    Input('search_button', 'n_clicks'),
    Input('customer_map', 'clickData'),
    Input('cached_data', 'data'),
    State('search_by', 'value'),
    State('customer_dd', 'value')
)
def customer_info(n, clickdata, data, by, value):
    if clickdata != None and value != None:
        df = data[data[by]==value]
        df = df.iloc[[0]]
        markdown_1 = f'''
            * **Name:** {df['name'].item()}
            * **Address:** {df['address'].item()}
            * **Phone No.:** {df['phone'].item()}
            * **National ID: ** {df['nin'].item()}
            * **No of assets in posession: ** {df['asset_count'].item()}
            '''
    
    elif clickdata != None and value == None:
        id = clickdata['points'][0]['customdata'][0]
        df = data[data['id']==id]
        markdown_1 = f'''
            * **Name:** {df['name'].item()}
            * **Address:** {df['address'].item()}
            * **Phone No.:** {df['phone'].item()}
            * **National ID: ** {df['nin'].item()}
            * **No of assets in posession: ** {df['asset_count'].item()}
            '''
    elif clickdata == None and value != None:
        df = data[data[by]==value]
        df = df.iloc[[0]]
        markdown_1 = f'''
            * **Name:** {df['name'].item()}
            * **Address:** {df['address'].item()}
            * **Phone No.:** {df['phone'].item()}
            * **National ID: ** {df['nin'].item()}
            * **No of assets in posession: ** {df['asset_count'].item()}
            '''
    else:
        id = random.randint(1, len(data['id'].tolist())+1)
        df = data[data['id']==id]
        markdown_1 = f'''
            * **Name:** 
            * **Address:** 
            * **Phone No.:** 
            * **National ID: ** 
            * **No of assets in posession: ** 
            '''

    return markdown_1


    

    


if __name__ =='__main__':
    app.run_server(debug=True)