import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, \
    ServersideOutputTransform,callback,FileSystemStore,callback_context,MATCH, ALL
selected_chart_template='simple_white'
import plotly.graph_objects as go


class dashboard:
    
    def __init__(self, df, user_style={"text-align": "auto",
                      'max-height': '200px',
                      'overflow': 'auto'},kpi_small="14rem",kpi_big="18rem"):
        self.df = df
        self.user_style = user_style
        self.kpi_small=kpi_small
        self.kpi_big=kpi_big


    def bordered_table(self,expenses_df_datewise):
        table = dbc.Table.from_dataframe(expenses_df_datewise, striped=True, bordered=True, hover=True,style=self.user_style)
        return table
    
    
    def simple_table(self,expenses_df):
        # self.expenses_df = expenses_df
        table = dbc.Table.from_dataframe(expenses_df, striped=True, bordered=False, hover=True,style=self.user_style)
        return table
    
    def card_bigger_kpi(self,position,header="",card_title="",paragraph="",footer="",initial=True):
        if initial==True:
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
            id={
                    'type': 'big-kpi',
                    'index': position
                },
            
                            )
        else:
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
    
    
    def card_smaller_kpi(self,position,header="",card_title="",paragraph="",footer="",initial=True):
        if initial==True:
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
        else:
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
                            )
            
        
        return card
    
    def kpi_creator_smaller(self,total,columns):
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
    
    def kpi_creator_bigger(self,total,columns):
        rows=int(total/columns)
        if rows<1:
            rows=1
        position=0
        
        card_row=[]
        for row in range(rows):
            card_col=[]
            for column in range(columns):
                
                card=dbc.Col(self.card_bigger_kpi(position))
                position=position+1
                card_col.append(card)
            card_row.append(dbc.Row(card_col,className="g-0"))
        
        return card_row
     
    def trace_graphs(self,columns_used,filt_file,name_date_columns="Date"):

        df=filt_file.copy()

        
        fig = go.Figure()
        try:
            for col in columns_used:
                fig.add_trace(go.Scatter(x=df[name_date_columns], y=df[col],
                                    mode='lines+markers',
                                    name=col,customdata=df['Date'],
                                    # marker_color=ai_green
                                    ))
        except:
            for col in columns_used:
                fig.add_trace(go.Scatter(x=df[name_date_columns], y=df[col],
                                    mode='lines+markers',
                                    name=col,customdata=df['Date'],
                                    # marker_color=ai_green
                                    ))
            

            
        fig=fig.update_layout(template=selected_chart_template)
        fig=fig.update_layout(margin={'t': 30, 'b': 0,'l':0,'r':0})
        return fig   