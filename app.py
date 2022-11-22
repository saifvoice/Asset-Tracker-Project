from dash_extensions.enrich import  DashProxy, Output, Input, State, ServersideOutput, html, dcc, Trigger, FileSystemStore, ServersideOutputTransform, FileSystemCache
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from home import home_layout
from enrol import form_layout
from urllib.parse import unquote
import configparser
from sqlalchemy import create_engine, engine_from_config
import pandas as pd
import random
import plotly.express as px
from records import customer_records
from flask_caching import Cache
import plotly.graph_objs as go


##### Database Configuration ######
config = configparser.ConfigParser()
config.read('cloud_db.ini')
hostname = config['HOST_DATA']['hostname']
username = config['USER_DATA']['username']
password = config['USER_DATA']['password']
database = config['USER_DATA']['database']

map_api = 'pk.eyJ1IjoieWF6aWlkIiwiYSI6ImNsYXI1a2xmczFxOWQzb3RhNWZnODBteTAifQ.tiRSI-AleU_c_m2tHWAP7Q'

# #### Connection ####
# config = {'db.url': f'mysql+pymysql://{username}:{password}@{hostname}/{database}'}
# engine = engine_from_config(config, prefix='db.')
# engine.dispose()
content = ['home', 'register', 'records']
nav = dbc.Nav([
        dbc.NavItem(dbc.NavLink("Home", id='home', href='/home'),  class_name='me-1'),
        dbc.NavItem(dbc.NavLink("Register", id='register', href='/register'),  class_name='me-1'),
        dbc.NavItem(dbc.NavLink("Records", id='records', href='/records'),  class_name='me-1'),
        dbc.NavItem(dbc.NavLink("Logout", id='logout', href='/login'), class_name='me-1')
],navbar=True, justified=True, class_name='mx-auto fs-4')

navbar = dbc.Navbar(
    dbc.Container([
        dbc.Col([
            html.A([
                dbc.Row([
                    dbc.Col([
                        html.Img(src='assets/tbcn-logo2.png', width=200, height=100,className='navbar-brand rounded float-start'),
                        html.Small('To Be Connected Nigeria', className='light')
                    ], class_name='col-3 align-center'),
                ], align='center', className='g-0'),
            ], href='/'),
        ], align='start', class_name='col-3'),
        dbc.Col([
            html.H2('Save-80 Geo-locator'),
            dbc.NavbarToggler(id='nav-toggler', n_clicks=0),
            dbc.Collapse(nav, id='navbar-collapse', is_open=False, navbar=True)
        ],class_name='col-6 text-center header-text'),
        dbc.Col(html.Img(src='assets/atmosfair.png', width=200, height=100,className='navbar-brand rounded float-end'))
        # dbc.Col([
        #     dbc.NavbarToggler(id='nav-toggler', n_clicks=0),
        #     dbc.Collapse(nav, id='navbar-collapse', is_open=False, navbar=True)
        # ])
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

FOOTER_STYLE = {
    "position": "fixed",
    "bottom": 0,
    "left": 0,
    "right": 0,
    "height": "6rem",
    "padding": "1rem 1rem",
    "background-color": "gray",
}

main_layout = dbc.Container([
    dcc.Store(id='cached_data'),
    dcc.Location(id='location'),
    dcc.Interval(id='query_data', interval=5*1000),
    dbc.Row(navbar, class_name='sticky-top'),
    dbc.Row(
            dbc.Col(id='content_container', lg={'size':12}, class_name='content-con')
        ),
    dbc.Row([
        dbc.Col([
            html.H3('Powered by Metaverse®', className='footer_text')
        ], class_name='text-center footer', style=FOOTER_STYLE)
    ], class_name='d-flex justify-content-center')    
], fluid=True)

#xl={'size':10, 'offset':1}, lg={'size':10, 'offset':1}
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
    Output('register', 'active'),
    Output('records', 'active'),
    Output('logout', 'active'),
    Input('location', 'pathname')
)
def display_content(pathname):
    page = unquote(pathname[1:])
    if page in content:
        if page == 'home':
            return home_layout, True, False, False, False
        if page == 'register':
            return form_layout, False, True, False, False
        if page == 'records':
            return customer_records, False, False, True, False
    else:
        return home_layout, True, False, False, False

hovertemplate = ('<b>Name: </b>: %{customdata[1]} <br>' +
                '<b>Address: </b>: %{customdata[2]}<br>' + 
                '<b>Phone No.: </b>: %{customdata[3]}<br>' +
                '<b>Product ID.: </b>: %{customdata[4]}<br>')



@app.callback(
    Output('customer_map', 'figure'),
    Input('search_button', 'n_clicks'),
    Input('cached_data', 'data'),
    Input('location', 'pathname'),
    State('search_by', 'value'),
    State('customer_dd', 'value'),
    prevent_initial_call=True
    # Input('customer_map', 'clickData')
)
def plot_map_points(n, data, pathname, by, value):
    page = unquote(pathname[1:])
    if by == None or value == None:
        raise PreventUpdate
    df = data[data[by] == value]
    df = df.iloc[[0]]
    lat = df['latitude'].item()
    lon = df['longitude'].item()
    customer_map = px.scatter_mapbox(
        data, lat='latitude', lon='longitude',
        hover_name='name', custom_data=['id', 'name', 'address', 'phone', 'nin', 'asset_count', 'latitude', 'longitude'],
        hover_data={'name': False, 'latitude':False, 'longitude':False, 'asset_count':True},
        zoom=9, center=dict(lat=lat, lon=lon),
        )
    customer_map.update_traces(marker=dict(size=15, color='#fe6b6b'), hovertemplate = hovertemplate)
    customer_map.update_layout(
        legend =dict(title_text = "", orientation='h', x=0.4, font_size=15, font_color='#FFFFFF'), paper_bgcolor='#E5ECF6',
        margin = dict(l = 0, r = 0, t = 0, b = 0), mapbox_style="streets", mapbox_accesstoken=map_api,
        hoverlabel = dict(bgcolor="#666DE9", font_size=15, font_color='whitesmoke')
    )
    customdata_trace = [df['name'].item(), df['address'].item(), df['phone'].item(), df['nin'].item()]

    hovertemplate_trace = ('<b>Name: ' + customdata_trace[0] + '<br>' +
                '<b>Address: </b>: ' + customdata_trace[1] + '<br>' + 
                '<b>Phone No.: </b>: ' + customdata_trace[2] + '<br>' +
                '<b>Product ID.: </b>: ' + str(customdata_trace[3]) + '<br>')
    customer_map.add_scattermapbox(
        below="", lat=[lat], lon=[lon], customdata=customdata_trace, hovertemplate=hovertemplate_trace,
        showlegend=False, name='',  hoverlabel = dict(bgcolor="#666DE9", font_size=15, font_color='whitesmoke'),
        marker=dict(size = 25, color='#666DE9')
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
    # State('form_lat', 'value'),
    # State('form_lon', 'value'),
    prevent_initial_call=True
)
def enrolment_form(n, name, address, phone, nin):
    data = {'name': name, 'address': address, 'phone': phone, 'nin': nin}
    for i in data.values():
        if not i:
            color = 'danger'
            is_open = True
            msg = 'Please fill all the given fields'
            return color, is_open, msg
    # config = {'db.url': f'mysql+pymysql://{username}:{password}@{hostname}/{database}'}
    # engine = engine_from_config(config, prefix='db.')
    # query = "insert into customer_profile (name, address, phone, nin, asset_count, latitude, longitude) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    # values = (name, address, phone, nin, 1, lat, lon)

    # engine.execute(query, values)
    color = 'success'
    is_open = True
    msg = 'Customer enrolled successfully'

    # try:
    #     engine.execute(query, values)
    #     engine.dispose()
    #     color = 'success'
    #     is_open = True
    #     msg = 'Customer enrolled successfully'
    # except:
    #     engine.dispose()
    #     color = 'danger'
    #     is_open = True
    #     msg = 'Enrolment failed! Make sure you enter the correct values'
    
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
            * **Product ID.: ** {df['nin'].item()}
            * **No of assets in posession: ** {df['asset_count'].item()}
            '''
    
    elif clickdata != None and value == None:
        id = clickdata['points'][0]['customdata'][0]
        df = data[data['id']==id]
        markdown_1 = f'''
            * **Name:** {df['name'].item()}
            * **Address:** {df['address'].item()}
            * **Phone No.:** {df['phone'].item()}
            * **Product ID.: ** {df['nin'].item()}
            * **No of assets in posession: ** {df['asset_count'].item()}
            '''
    elif clickdata == None and value != None:
        df = data[data[by]==value]
        df = df.iloc[[0]]
        markdown_1 = f'''
            * **Name:** {df['name'].item()}
            * **Address:** {df['address'].item()}
            * **Phone No.:** {df['phone'].item()}
            * **Product ID.: ** {df['nin'].item()}
            * **No of assets in posession: ** {df['asset_count'].item()}
            '''
    else:
        raise PreventUpdate

    return markdown_1


    

    


if __name__ =='__main__':
    app.run_server(debug=True)