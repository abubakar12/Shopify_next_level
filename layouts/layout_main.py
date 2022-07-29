import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, \
    ServersideOutputTransform,callback,FileSystemStore,callback_context,MATCH, ALL
selected_chart_template='simple_white'
import plotly.graph_objects as go
from dashboarding import dashboard_class
from calculations_main import main_dashboard_calc
from dateutil.relativedelta import relativedelta
import dash_mantine_components as dmc
# Usual DASH stuff
from datetime import datetime, timedelta, date
from dash.exceptions import PreventUpdate





precision=100


sample_file=pd.read_csv(r"C:\Users\hp\Desktop\Shopify_app\Shopify_next_level\sample_data.csv")
sample_file["Date"]=pd.to_datetime(sample_file["Date"],format="%Y-%m-%d")
sample_file=sample_file[~(sample_file["quantity"].isnull())]
sample_file=sample_file.sort_values(by="Date")
sample_file["Date"]=sample_file["Date"].astype(str)
    
dates=sample_file["Date"].unique()
min_val=np.min(dates)
max_val=np.max(dates)


date_picker=html.Div(
    [
        dmc.DateRangePicker(
            id="my-date-picker-range",
            label="Date Range",
            value=[min_val, max_val],
            style={"width": 330},
        ),
        dmc.Space(h=10),
        dmc.Text(id="selected-date-date-range-picker"),
    ]
)




option_selected = dbc.Container(
    
    
    dbc.Row([     
        
              dbc.Col(
                    date_picker
                ),
              
              dbc.Col(
                    html.Div([
                    html.H6("Product Type"),
                    dcc.Dropdown(
                    id='prod-type',
                    options=[""],
                    value=""
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=6,
                    ],),md=2
                ),
                
                dbc.Col(
                    html.Div([
                    html.H6("product_id"),
                    dcc.Dropdown(
                    id='prod-id',
                    options=[""],
                    value=""
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=6,
                    ],),md=2
                ),
                
                dbc.Col(
                    html.Div([
                    html.H6("variant id"),
                    dcc.Dropdown(
                    id='var-id',
                    options=[""],
                    value=""
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=6,
                    ],),md=2
                ),
                
                dbc.Col(
                    html.Div([
                    html.H6("SKU"),
                    dcc.Dropdown(
                    id='sku-id',
                    options=[""],
                    value=""
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=6,
                    ],),md=2
                ),

        
        ]),
    

    
    
        
   
)    
    
            
 

               
header = ['COGS','Discounts','Shipping Cost','Shipping Charged','Avg.Order Value','Avg Order Profit','LTV','CAC','Net Margin',\
          'Gross Margin','Ad Spend','Ad Speed/Order','Handling Fee','Transaction Fee','Disputed Revenue','Refunded',\
              'Unique Visitors','Conversion Rate','Revenue Visitor','Net Profit/Visitor']
    
card_title=[]

header_big = ['Number Of Orders','Number Of Refunds and Cancellations','Unique Visitors','Conversion Rate']
card_title=[]


expenses_df=pd.DataFrame({"Disputed Revenue":0,"Adspend":0,"Cost of Goods":0,"Shipping":0,
"Handling Fee":0,"Apps":0,"Transaction Fee":0,"Other Expenses":0},index=[0]) 
expenses_df=pd.melt(expenses_df,var_name="measure",value_name="value")
    

    
            

first_page=dashboard_class.dashboard(sample_file,user_style={"text-align": "auto",
                  'max-height': '20px',
                  'overflow': 'auto'})  

layout1 = html.Div([
    dbc.Spinner(dcc.Graph(id="graph1"),color="info")

])  
                            

expenses_table=dbc.Spinner(html.Div(dbc.Table(first_page.simple_table(expenses_df),id='simple_table'),style={"maxHeight": "400px", "overflow": "scroll"})),
table=dbc.Spinner(html.Div(dbc.Table(id='bordered_table'),style={"maxHeight": "400px", "overflow": "scroll"})),
check_list=html.Div([html.Div(id="check_list"),layout1,html.Hr()])      
kpi_small=dbc.Container(first_page.kpi_creator_smaller(20,5),fluid=True),
kpi_big=dbc.Container(first_page.kpi_creator_bigger(4,2),fluid=True),
                            
main_page_var = dbc.Container(
    [html.Hr(),
     option_selected,
     html.Hr(),
     dbc.Row([dbc.Col(expenses_table,md=4),dbc.Col(dbc.Container(first_page.kpi_creator_bigger(4,2),fluid=True))]),
     dbc.Row(check_list,class_name="g-0"),
     dbc.Row(dbc.Container(first_page.kpi_creator_smaller(20,5),fluid=True),class_name="g-0"),
     dbc.Row(table,)
    ],fluid=True,
)

    
    
header = ['COGS','Discounts','Shipping Cost','Shipping Charged','Avg.Order Value','Avg Order Profit','LTV','CAC','Net Margin',\
          'Gross Margin','Ad Spend','Ad Speed/Order','Handling Fee','Transaction Fee','Disputed Revenue','Refunded',\
              'Unique Visitors','Conversion Rate','Revenue Visitor','Net Profit/Visitor']

##############################################################################
@callback(
    Output('my-date-picker-range', 'childen'),
    Input("url", "pathname"),
)
def initial_slider(url):
    dates=sample_file["Date"].unique()
    min_val=np.min(dates)
    max_val=np.max(dates)
    slider=dmc.DateRangePicker(
                id="my-date-picker-range",
                label="Date Range",
                value=[min_val, max_val],
                style={"width": 330},
            )
    return slider


# @callback(
#     Output("sample_file", "data"),
#     Input('my-date-picker-range', 'start_date'),
#     Input('my-date-picker-range', 'end_date'),
#     Input("url", "pathname"))
# def update_output(start_date, end_date,URL):
#     print("start date :{} end_date  : {}".format(start_date,end_date))
#     return sample_file
                    
@callback(
    Output("selected-date-date-range-picker", "children"),
    ServersideOutput("sample_file", "data"),
    Input('my-date-picker-range', "value"),
)
def update_output(dates):
    print("dates :   ",dates)
    start_date=dates[0]
    end_date=dates[1]
    start_date=pd.to_datetime(start_date)
    end_date=pd.to_datetime(end_date)
    
    sam=sample_file.copy()
    sam["Date"]=pd.to_datetime(sam["Date"],format="%Y-%m-%d")
    
    sam=sam[(sam["Date"]>=start_date)&\
                    (sam["Date"]<=end_date)]
        
    sample_file["Date"]=sample_file["Date"].astype(str)
        
    prefix = "You have selected: "
    if dates:
        return prefix + "   -   ".join(dates),sam
    else:
        raise PreventUpdate


    
    
@callback(
    Output('prod-type', 'options'),
    Output('prod-type', 'value'),
    Input("sample_file", "data"),
)
def initial_prod_type_select(url):
    prod_types=sample_file["product_type"].unique()
    option_selected=prod_types[0]
    
    return prod_types,option_selected

@callback(
    Output('prod-id', 'options'),
    Output('prod-id', 'value'),
    Input('prod-type', 'value'),
)
def prod_id_select(prod_type):
    sam_file=sample_file[sample_file["product_type"]==prod_type]
    prod_types=sam_file["product_id"].unique()
    option_selected=prod_types[0]
    
    return prod_types,option_selected

@callback(
    Output('var-id', 'options'),
    Output('var-id', 'value'),
    Input('prod-id', 'value'),
    State('prod-type', 'value'),
)
def var_id_select(prod_id,prod_type):
    sam_file=sample_file[(sample_file["product_type"]==prod_type)&\
                         (sample_file["product_id"]==prod_id)]
    prod_types=sam_file["variant_id"].unique()
    option_selected=prod_types[0]
    
    return prod_types,option_selected

@callback(
    Output('sku-id', 'options'),
    Output('sku-id', 'value'),
    State('prod-id', 'value'),
    State('prod-type', 'value'),
    Input('var-id', 'value'),
)
def sku_id_select(prod_id,prod_type,var_id):
    sam_file=sample_file[(sample_file["product_type"]==prod_type)&\
                         (sample_file["product_id"]==prod_id)&\
                        (sample_file["variant_id"]==var_id)]
    prod_types=sam_file["sku"].unique()
    option_selected=prod_types[0]
    
    return prod_types,option_selected






#############################################################################
@callback(
    Output("small-kpi-vals", 'data'),
    ServersideOutput("filt_file", 'data'),
    Output("simple_table", 'children'),
    Input("sample_file", "data"),
    Input('sku-id', 'value'),
    Input('prod-type', 'value'),
    Input('prod-id', 'value'),
    Input('var-id', 'value'),
)
def calculate_values_kpis(sample_file,sku,prod_type,prod_id,var_id):
    
    sam_file=sample_file[(sample_file["product_type"]==prod_type)&\
                            (sample_file["product_id"]==prod_id)&\
                             (sample_file["variant_id"]==var_id)&\
                             (sample_file["sku"]==sku)]
        
    sam_file=sam_file[["Date",'product_type',"product_id",\
                              "variant_id",'variant_title',"sku","price","quantity","total_discount",\
                                'ClientID','TotalSpent','AddressID', \
                                    'City', 'Province', 'Country'  ]]
        
    sam_file["revenue"]=sam_file["price"]*sam_file["quantity"]
        
    price=sam_file['price']
    quantity=sam_file['quantity']
    discounts=sam_file['total_discount']
    
    
    
    calculations=main_dashboard_calc.calculations_main(revenue=0,taxes=0,shipping_cost=0,other_expenses=0,\
                                                  handling_fee=0,cogs=0,adspend=0,app_expenses=0,\
                 tax_rate=0,fb_adspend=0,goog_adspend=0,other_marketing_expenses=0,transaction_fees=0,miscellaneous_expense=0,\
                     price=price,quantity=quantity,sum_all_orders_per_customer=0)
        
    revenue=calculations.revenue_calc()
    taxes_calc=calculations.taxes_calc()
    other_expenses=calculations.other_expenses_calc()
    tot_expenses=calculations.tot_expenses_calc()
    gross_profit=calculations.gross_profit_calc()
    
    cogs=0
    shipping_cost=0
    shipping_charged=0
    avg_order_value=calculations.avg_order_value_calc()
    avg_order_profit=calculations.avg_order_profit_calc()
    ltv=calculations.ltv_calc()
    cac=calculations.cac_calc()
    net_margin=calculations.net_margin_calc()
    gross_margin=calculations.gross_margin_calc()
    adspend=calculations.adspend_calc()
    adspend_speed=0#?????
    handling_fee=0
    transaction_fee=0
    disputed_revenue=0
    refunded=0
    unique_visitors=0
    conversion_rate=0
    revenue_visitor=0
    net_profit=calculations.net_profit_calc()
    app_expenses=0
        
    
    expenses_df=pd.DataFrame({"Disputed Revenue":disputed_revenue,"Adspend":adspend,"Cost of Goods":cogs,"Shipping":shipping_cost,
    "Handling Fee":handling_fee,"Apps":app_expenses,"Transaction Fee":transaction_fee,"Other Expenses":other_expenses},index=[0]) 
    expenses_df=pd.melt(expenses_df,var_name="measure",value_name="value")
    expenses_table=first_page.simple_table(expenses_df)
    
    
    
    small_kpi_array=[cogs,discounts,shipping_cost,shipping_charged,avg_order_value,avg_order_profit,ltv,\
                     cac,net_margin,gross_margin,adspend,adspend_speed,handling_fee,transaction_fee,disputed_revenue,\
                       refunded, unique_visitors,conversion_rate,revenue_visitor,net_profit ]
       
    return small_kpi_array,sam_file,expenses_table
    

    

    
    
@callback(
    Output({'type': 'small-kpi', 'index': ALL}, 'children'),
    Input("small-kpi-vals", 'data'),
    Input("filt_file", 'data')
)
def fill_kpi_values_smaller(values,filtered_data):
    
    values=[np.sum(zz) for zz in values]
    
    tot_position=range(20)
    card_title=np.array(values)
    card_title=(card_title*precision)
    card_title=card_title.astype(int)
    card_title=card_title/precision
    card_title=card_title.astype(str)
    

    return [first_page.card_smaller_kpi(position=pos,header=head,card_title=card_tit,initial=False) \
            for head,pos,card_tit in zip(header,tot_position,card_title)
            ]
        
        
@callback(
    Output({'type': 'big-kpi', 'index': ALL}, 'children'),
    Input("small-kpi-vals", 'data'),
    Input("filt_file", 'data')
)
def fill_kpi_values_bigger(values,filtered_data):
    
    tot_position=range(4)
    card_title=np.repeat('$0',4)
    
    basic_layout=[first_page.card_bigger_kpi(position=pos,header=head,card_title=card_tit,initial=False) \
        for head,pos,card_tit in zip(header_big,tot_position,card_title)
        ]

    return basic_layout
        
        
        
  

    
@callback(
    Output('bordered_table','children'),
    Input("filt_file", 'data'),
    Input('sku-id', 'value'),
    Input('prod-type', 'value'),
    Input('prod-id', 'value'),
    Input('var-id', 'value'),
)
def table_detailed(sam,sku,prod_type,prod_id,var_id):
    
    
    sam_file=first_page.bordered_table(sam)
    print(sam_file)  
    return sam_file
    

    
        
##############################################################################        
        
     
@callback(
    Output('graph1', 'figure'),
    Input("check_list", "value"),
    Input("filt_file", 'data'),
)
def fill_graph(val,filt_file):
    
    return first_page.trace_graphs(val,filt_file) 
  
   
##############################################################################
@callback(
    Output("check_list", 'children'),
    Input("small-kpi-vals", 'data'),
)
def make_checkbox(path):
        
        return dcc.Checklist(
                id='check_list',
                options=['quantity','revenue',"total_discount"],
                value=['quantity']
            ),

