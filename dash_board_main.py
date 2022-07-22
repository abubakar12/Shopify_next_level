import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, \
    ServersideOutputTransform,callback,FileSystemStore,callback_context,MATCH, ALL

class dashboard:
    def __init__(self, df, user_style,kpi_small="14rem",kpi_big="18rem"):
        self.df = df
        self.user_style = user_style
        self.kpi_small=kpi_small
        self.kpi_big=kpi_big


    def bordered_table(self):
        table = dbc.Table.from_dataframe(self.df, striped=True, bordered=True, hover=True,style=self.user_style)
        return table
    
    
    def simple_table(self):
        table = dbc.Table.from_dataframe(self.df, striped=True, bordered=False, hover=True,style=self.user_style)
        return table
    
    def card_bigger_kpi(self,header="",card_title="",paragraph="",footer="",):
        card = dbc.Card(
        [
            dbc.CardHeader(header),
            dbc.CardBody(
                [
                    html.H4(card_title, className="card-title"),
                    html.P(paragraph, className="card-text"),
                ]
            ),
            dbc.CardFooter(footer),
        ],
        style={"width": self.kpi_big},
                        )
        
        return card
    
    
    def card_smaller_kpi(self,position,header="",card_title="",paragraph="",footer=""):
        card = dbc.Card(

        [
            dbc.CardHeader(header),
            dbc.CardBody(
                [
                    html.H4(card_title, className="card-title"),
                    html.P(paragraph, className="card-text"),
                ]
            ),
            dbc.CardFooter(footer),
        ],
        style={"width": self.kpi_small},
        id={
                'type': 'small-kpi',
                'index': position
            },
                        )
        
        return card
    
    def kpi_creator(self,total,columns):
        rows=int(total/columns)
        if rows<1:
            rows=1
        position=0
        
        card_row=[]
        for row in range(rows):
            card_col=[]
            for column in range(columns):
                
                card=dbc.Col(self.card_smaller_kpi(position))
                position=position+1
                card_col.append(card)
            card_row.append(dbc.Row(card_col,className="g-0"))
        
        return card_row
            
            
                
header = ['COGS','Discounts','Shipping Cost','Shipping Charged','Avg.Order Value','Avg Order Profit','LTV','CAC','Net Margin',\
          'Gross Margin','Ad Spend','Ad Speed/Order','Handling Fee','Transaction Fee','Disputed Revenue','Refunded',\
              'Unique Visitors','Conversion Rate','Revenue Visitor','Net Profit/Visitor']
card_title=[]

            
            
    



    
    

first_page=dashboard("","")

                            
main_page_var = dbc.Container(
    [   
        
        html.Hr(),
        dbc.Container(first_page.kpi_creator(16,4))
    ],
)

    
dash_app = DashProxy(__name__,transforms=[ServersideOutputTransform()],\
                external_stylesheets=[dbc.themes.SIMPLEX],suppress_callback_exceptions=True,\
                   )
    
    
    
    
app = dash_app.server
dash_app.title = "Shopify Data Analysis"
dash_app.layout = dbc.Container(
    [dcc.Store(id='dates_var',storage_type='session'),
     dcc.Location(id="url", refresh=True), 
     dbc.Row(dbc.Col(id="page-content",style={"padding":"0px"},width=True))
     ],
   fluid=True
)

@dash_app.callback(
    Output({'type': 'small-kpi', 'index': ALL}, 'children'),
    Input("url", "pathname"),
    State({'type': 'small-kpi', 'index': ALL}, 'value')
)
def display_output(values,val):
    first_page=dashboard("","")
    tot_position=range(16)
    card_title=np.repeat('$0',16)
    

    return [first_page.card_smaller_kpi(position=pos,header=head,card_title=card_tit) \
            for head,pos,card_tit in zip(header,tot_position,card_title)
            ]
    




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