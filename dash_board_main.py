import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, \
    ServersideOutputTransform,callback,FileSystemStore,callback_context,MATCH, ALL
selected_chart_template='simple_white'
import plotly.graph_objects as go

sample_file=pd.read_csv(r"C:\Users\hp\Desktop\Shopify_app\Shopify_next_level\sample_file.csv")
sample_file=sample_file.drop_duplicates(subset=["TYear","TMonth"])
sample_file["Date"]=pd.to_datetime(sample_file["TYear"].astype(str)+"-"\
                                   +sample_file["TMonth"].astype(str),format="%Y-%m")
    
from dashboarding import dashboard_class
from calculation_main import main_dashboard_calc

    
    
            
 

               
header = ['COGS','Discounts','Shipping Cost','Shipping Charged','Avg.Order Value','Avg Order Profit','LTV','CAC','Net Margin',\
          'Gross Margin','Ad Spend','Ad Speed/Order','Handling Fee','Transaction Fee','Disputed Revenue','Refunded',\
              'Unique Visitors','Conversion Rate','Revenue Visitor','Net Profit/Visitor']
    
card_title=[]

header_big = ['Number Of Orders','Number Of Refunds and Cancellations','Unique Visitors','Conversion Rate']
card_title=[]

# def calculate_values_kipis():
#     calculations=main_dashboard_calc.calculations(revenue=0,taxes=0,shipping_cost=0,other_expenses=0,\
#                                                   handling_fee=0,cogs=0,adspend=0,app_expenses=0,\
#                  tax_rate=0,fb_adspend=0,goog_adspend=0,other_marketing_expenses=0,transaction_fees=0,miscellaneous_expense=0)
#     revenue=calculations.revenue()
#     adspend=calculations.adspend()
#     taxes_calc=calculations.taxes_calc()
#     other_expenses=calculations.other_expenses()
#     tot_expenses=calculations.tot_expenses()
#     net_profit=calculations.net_profit()
#     avg_order_value=calculations.avg_order_value()
#     avg_order_profit=calculations.avg_order_profit()
#     ltv=calculations.ltv()
#     cac=calculations.cac()
#     net_margin=calculations.net_margin()
#     gross_margin=calculations.gross_margin()
#     gross_profit=calculations.gross_profit()
    
    
        
    
            

first_page=dashboard_class.dashboard(sample_file,user_style={"text-align": "auto",
                  'max-height': '20px',
                  'overflow': 'auto'})  

layout1 = html.Div([
    dbc.Spinner(dcc.Graph(id="graph1"),color="info")

])  
                            

expenses_table=dbc.Spinner(html.Div(dbc.Table(id='simple_table'),style={"maxHeight": "400px", "overflow": "scroll"})),
table=dbc.Spinner(html.Div(dbc.Table(id='bordered_table'),style={"maxHeight": "400px", "overflow": "scroll"})),
check_list=html.Div([html.Div(id="check_list"),layout1,html.Hr()])      
kpi_small=dbc.Container(first_page.kpi_creator_smaller(16,4),fluid=True),
kpi_big=dbc.Container(first_page.kpi_creator_bigger(4,2),fluid=True),
                            
main_page_var = dbc.Container(
    [html.Hr(),   
     dbc.Row([dbc.Col(expenses_table,md=4),dbc.Col(kpi_big)]),
     dbc.Row(check_list,class_name="g-0"),
     dbc.Row(kpi_small,class_name="g-0"),
     dbc.Row(table,)
    ],fluid=True,
)

    
dash_app = DashProxy(__name__,transforms=[ServersideOutputTransform()],\
                external_stylesheets=[dbc.themes.SIMPLEX],suppress_callback_exceptions=True,\
                   )
    
    
    
    
app = dash_app.server
dash_app.title = "Shopify Data Analysis"
dash_app.layout = dbc.Container(
    [dcc.Store(id='dates_var',storage_type='session'),
     dcc.Location(id="url", refresh=True), 
     dbc.Row(dbc.Col(id="page-content",style={"padding":"0px"}))
     ],
   fluid=True
)


##############################################################################
@dash_app.callback(
    Output({'type': 'small-kpi', 'index': ALL}, 'children'),
    Input("url", "pathname"),
    State({'type': 'small-kpi', 'index': ALL}, 'value')
)
def fill_kpi_values_smaller(values,val):
    
    

    first_page=dashboard_class.dashboard(sample_file,user_style={"text-align": "auto",
                      'max-height': '200px',
                      'overflow': 'auto'})
    tot_position=range(16)
    card_title=np.repeat('$0',16)
    

    return [first_page.card_smaller_kpi(position=pos,header=head,card_title=card_tit) \
            for head,pos,card_tit in zip(header,tot_position,card_title)
            ]
        
        
@dash_app.callback(
    Output({'type': 'big-kpi', 'index': ALL}, 'children'),
    Input("url", "pathname"),
    State({'type': 'big-kpi', 'index': ALL}, 'value')
)
def fill_kpi_values_bigger(values,val):
    
    first_page=dashboard_class.dashboard(sample_file,user_style={"text-align": "auto",
                      'max-height': '200px',
                      'overflow': 'auto'})
    tot_position=range(4)
    card_title=np.repeat('$0',4)
    

    return [first_page.card_bigger_kpi(position=pos,header=head,card_title=card_tit) \
            for head,pos,card_tit in zip(header_big,tot_position,card_title)
            ]
        
        
        
@dash_app.callback(
    Output('simple_table','children'),
    Input("url", "pathname"),
)
def simple_table(val):
    return first_page.simple_table()     

    
@dash_app.callback(
    Output('bordered_table','children'),
    Input("url", "pathname"),
)
def bordered_table(val):
    return first_page.bordered_table()   

    
        
##############################################################################        
        
     
@dash_app.callback(
    Output('graph1', 'figure'),
    Input("check_list", "value"),
)
def fill_graph(val):
    
    return first_page.trace_graphs(val) 
  
   
##############################################################################
@dash_app.callback(
    Output("check_list", 'children'),
    Input("url", "pathname"),
)
def make_checkbox(path):
        
        return dcc.Checklist(
                id='check_list',
                options=['Actual Sales', 'Projected Sales'],
                value=['Actual Sales']
            ),

###############################################################################
# Multi-page selector callback - not really used, but left in for future use
@dash_app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):

    return main_page_var


###################################################
# Server Run
###################################################
dash_app.config['suppress_callback_exceptions'] = True
if __name__ == '__main__':
    dash_app.run_server(debug=True)    