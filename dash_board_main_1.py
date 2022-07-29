import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, \
    ServersideOutputTransform,callback,FileSystemStore,callback_context,MATCH, ALL

selected_chart_template='simple_white'
import plotly.graph_objects as go

    
from dashboarding import dashboard_class
from calculations_main import main_dashboard_calc
from layouts import layout_main

    
    

    
dash_app = DashProxy(__name__,transforms=[ServersideOutputTransform()],\
                external_stylesheets=[dbc.themes.SIMPLEX],suppress_callback_exceptions=True,\
                   )
    
    
    
    
app = dash_app.server
dash_app.title = "Shopify Data Analysis"
dash_app.layout = dbc.Container(
    [dcc.Store(id='dates_var',storage_type='session'),
     dcc.Store(id='small-kpi-vals',storage_type='session'),
     dcc.Store(id='sample_file',storage_type='session'),
     dcc.Store(id='filt_file',storage_type='session'),
     dcc.Location(id="url", refresh=True), 
     dbc.Row(dbc.Col(id="page-content",style={"padding":"0px"}))
     ],
   fluid=True
)




###############################################################################
# Multi-page selector callback - not really used, but left in for future use
@dash_app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):

    return layout_main.main_page_var


###################################################
# Server Run
###################################################
dash_app.config['suppress_callback_exceptions'] = True
if __name__ == '__main__':
    dash_app.run_server(debug=True)    