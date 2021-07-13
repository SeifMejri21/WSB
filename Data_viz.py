# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 13:57:39 2021

@author: Administrator
"""

import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go

##########################################################################################################################
##########################################################################################################################
#pie plot for all mentions
def pie_plotly(df):
    #Pie plot of total 
    fig1 = px.pie(df, values ='all_count', names='stock', title='Stocks nasdaq 100',
                  hover_data=['company'], labels={'company':'Comapny'})
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    fig1.update_layout(title="Mentions Distribuion " )
    plot(fig1)
    
##########################################################################################################################
##########################################################################################################################
#
def tree_plotly(df):    
    #Tree plot
    nb=len(df['stock'])
    fig2 = px.treemap(df,
    values = 'all_count' ,                  
    names = 'stock',
    parents= ['us market']*nb,
    hover_data= ['company']
    )
    fig2.update_traces(root_color="lightgrey")
    fig2.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig2.update_layout(title="Mentions Distribuion " )
    plot(fig2)

##########################################################################################################################
##########################################################################################################################


def h_barplot_plotly(df):
    df2 = df.sort_values(by=['all_count'])
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
    y= df2['stock'].tolist(),
    x= df2['positive_count'].tolist(),
    name=' Positive',
    orientation='h',
    marker=dict(
        color='rgba(10, 19, 255, 0.6)',
        line=dict(color='rgba(10, 19, 255, 1.0)', width = 1 ))))

    fig3.add_trace(go.Bar(
        y= df2['stock'].tolist(),
        x= df2['neutral_count'].tolist(),
        name=' Neutral',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80,  0.6)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width = 1 ))))
    
    fig3.add_trace(go.Bar(
        y= df2['stock'].tolist(),
        x= df2['negative_count'].tolist(),
        name=' Negative',
        orientation='h',
        marker=dict(
            color='rgba(255, 0, 0, 0.6)',
            line=dict(color='rgba(255, 0, 0, 1.0)', width = 1 ))))
    
    fig3.update_layout(title="Mentions Type Distribution ",
                      xaxis_title="Count",
                      yaxis_title="Stock")
    
    fig3.update_layout(barmode='stack')
    plot(fig3)
##########################################################################################################################
##########################################################################################################################
def scatter_plotly(df):
    fig4 = go.Figure()
    fig4 = px.scatter(df, x="negative_count", y="positive_count", color = 'stock',
                 size='all_count', hover_data=['stock','company'],text = 'stock')
    
    fig4.add_shape(type="line",
    x0=0, y0=0, x1= max(df['negative_count'].max(),df['positive_count'].max())
 , y1= max(df['negative_count'].max(),df['positive_count'].max())
,
    line=dict(
        color="lightpink",
        width=4,
        dash="dot",
    ))

    fig4.update_layout(title="Mentions type ",
                      xaxis_title="Negative mentions",
                      yaxis_title="Positive mentions")
    plot(fig4)
    
    
##########################################################################################################################
##########################################################################################################################    

def mean_bar_plotly(df):
    df2 = df.sort_values(by=['mean_score'])
    fig5 = px.bar(df2, x='stock', y='mean_score' , color= 'stock', 
                  hover_data =['stock','company'],text = 'stock' )
    fig5.update_layout(title="General feeling about the Stock",
                      xaxis_title="Stock",
                      yaxis_title="average mention score")
    plot(fig5)



##########################################################################################################################
##########################################################################################################################    



    

