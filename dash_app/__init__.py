from dash_extensions.enrich import  DashProxy, html, dcc, ServersideOutputTransform
import dash_bootstrap_components as dbc
from dash_app.callbacks import register_callbacks
from dash_app.home import home_layout
from dash_app.enrol import form_layout
from dash_app.records import customer_records
from dash_app.search import search_layout
from flask_login import login_required




style_2 = {
}
nav = dbc.Nav([
        dbc.NavItem(dbc.NavLink("Home", id='home', href='/home', style=style_2),  class_name='me-1'),
        dbc.NavItem(dbc.NavLink("Register", id='register', href='/register', style=style_2),  class_name='me-1'),
        dbc.NavItem(dbc.NavLink("Records", id='records', href='/records', style=style_2),  class_name='me-1'),
        dbc.NavItem(dbc.NavLink("Search", id='search', href='/search', style=style_2), class_name='me-1'),
        dbc.NavItem(dbc.NavLink("Logout", id='logout', href='/logout', style=style_2, external_link=True), class_name='me-1')
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
            html.H2('Save-80 Geo-locator'), #style={'color':'#B8E1E9'}
            dbc.NavbarToggler(id='nav-toggler', n_clicks=0),
            dbc.Collapse(nav, id='navbar-collapse', is_open=False, navbar=True)
        ],class_name='col-6 text-center header-text'),
        dbc.Col(html.Img(src='assets/atmosfair.png', width=200, height=100,className='navbar-brand rounded float-end'))
    ], fluid=True, class_name='d-flex justify-content-center')
,id='navbar', class_name='navbar')


FOOTER_STYLE = {
    "position": "fixed",
    "bottom": 0,
    "left": 0,
    "right": 0,
    'height':'80px',
    # 'background': '#bdc3c7',
    # 'background': '-webkit-linear-gradient(to top, #2c3e50, #bdc3c7)',
    # 'background': 'linear-gradient(to top, #2c3e50, #bdc3c7)',


}
content_con = {
    # 'backround-color': '#606c88',
    # 'background': '-webkit-linear-gradient(0deg, #606c88 0%, #3f4c6b 100%)',
    # 'background': 'linear-gradient(0deg, #606c88 0%, #3f4c6b 100%)',
    'background-image': 'url(assets/background.jpg)'
}

main_layout = dbc.Container([
    dcc.Store(id='cached_data'),
    dcc.Location(id='location'),
    dcc.Interval(id='query_data', interval=15*1000),
    dbc.Row(navbar, class_name='sticky-top'),
    dbc.Row(
            dbc.Col(id='content_container', lg={'size':12}, class_name='content-con') #content_con
        ),
    dbc.Row([
        dbc.Col([
            html.Small('13a, Mambila Street, Aso Drive, Abuja.', className='m-info'), #, style={'color':'#B8E1E9'}
            html.A('www.tbcn.com.ng', href='http://tbcn.com.ng') #style={'color':'#B8E1E9'}
        ], class_name='me-auto info_footer'),
        dbc.Col([
            html.H3('Powered by Metaverse®', className='footer_text mt-2')
        ], class_name='text-center footer mt-0'),
        dbc.Col([
            html.Small('To Be Connected Nigeria®', className='m-info ms-auto'), #, style={'color':'#B8E1E9'}
            html.Small('2022©', className='ms-auto') #, style={'color':'#B8E1E9'}
        ], class_name='text-center info_footer')
    ], class_name='d-flex justify-content-center bg-light',  style=FOOTER_STYLE)    
], fluid=True, class_name='main_content')

















def create_dash_app(server):
    dash_app = DashProxy(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], transforms=[ServersideOutputTransform()], server=server, url_base_pathname='/')
    dash_app.title = "Save-80"
    dash_app.validation_layout = html.Div([main_layout, home_layout, form_layout, customer_records, search_layout])
    dash_app.layout = main_layout

    register_callbacks(dash_app)
    _protect_dashviews(dash_app)
    return dash_app


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func])
