# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 21:47:45 2021

@author: Administrator
"""


import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
    return(fig2)

##########################################################################################################################
##########################################################################################################################


def h_barplot_plotly(df):
    df2 = df.sort_values(by=['all_count'])
    df2=df2[df2['all_count']>=5]
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
                      yaxis_title="Positive mentions"
                       ,xaxis_title="Negative mentions")
    plot(fig4)
    
    
##########################################################################################################################
##########################################################################################################################    

def mean_bar_plotly(df):
    df2 = df.sort_values(by=['mean_score'])
    df2=df2[df2['all_count']>=5]
    fig5 = px.bar(df2, x='stock', y='mean_score' , color = 'stock' ,
                  hover_data =['stock','company'],text = 'stock' )
    fig5.update_layout(title="General feeling about the Stock",
                      xaxis_title="Stock",
                      yaxis_title="average mention score")
    plot(fig5)



##########################################################################################################################
##########################################################################################################################    


def sent_score(df):
    df2 = df.sort_values(by=['sum_score'])    
    fig6 = px.strip(df2, x="sum_score", y="stock")
    fig6.update_layout(title="Sentiment score",
                      xaxis_title="Score",
                      yaxis_title="Stock")
    plot(fig6)
    


############################################################################################################
############################################################################################################



def count_ev_viz(stock,df_1):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
    go.Scatter(x=df_1['date'], y=df_1['all_count'], name="All Mentions"), secondary_y=False, )
    fig.add_trace(go.Scatter(x=df_1['date'], y=df_1['negative_count'],name="Negative Mentions"),secondary_y=False)    
    fig.add_trace(go.Scatter(x=df_1['date'], y=df_1['positive_count'],name="Positive Mentions"),secondary_y=False)  
    fig.add_trace(go.Candlestick(x=df_1['date'],open=df_1['Open'], high=df_1['High'],
    low=df_1['Low'], close=df_1['Close'],increasing_line_color= 'cyan', decreasing_line_color= 'gray',
    showlegend = True , name="Candle Stick"), secondary_y=True)    
    fig.update_layout(title_text= "<b>"+stock+"</b>  Mentions/Price  Evolution ")
    fig.update_xaxes(title_text="Date")  
    fig.update_yaxes(title_text="<b>Mentions number</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Stock Price</b>", secondary_y=True)      
    plot(fig)
        
    
    
############################################################################################################
############################################################################################################
  
def puts_calls_bar(my_df):
    df6 = my_df[(my_df['puts']>=1) | (my_df['calls']>=1)].sort_values(by=['calls'])
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(
    x= df6['stock'].tolist(),
    y= df6['calls'].tolist(),
    name=' Calls',
    orientation='v',
    marker=dict(
        color='rgba(0, 255, 130, 0.6)',
        line=dict(color='rgba(0, 255, 130, 1.0)', width = 1 ))))

    fig6.add_trace(go.Bar(
        x= df6['stock'].tolist(),
        y= df6['puts'].tolist(),
        name=' Puts',
        orientation='v',
        marker=dict(
            color='rgba(255, 0, 0, 0.6)',
            line=dict(color='rgba(255, 0, 0, 1.0)', width = 1 ))))
    
    fig6.update_layout(title="Calls/Puts Distribution ",
                      xaxis_title="Stock",
                      yaxis_title="Puts/Calls",
                      height =500)
    fig6.update_layout(barmode='stack')
    plot(fig6)


############################################################################################################
############################################################################################################

def candle_stick(my_list, stock):
    df_1=my_list [0]
    stock_data_df=my_list[1]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df_1['date'], y=df_1['negative_count'],name="Negative Mentions"),secondary_y=False)    
    fig.add_trace(go.Scatter(x=df_1['date'], y=df_1['positive_count'],name="Positive Mentions"),secondary_y=False) 
    fig.add_trace(go.Scatter(x=df_1['date'], y=df_1['Close'],name="Close Price"),secondary_y=True) 
    
    fig.add_trace(go.Candlestick(x=stock_data_df.index.tolist(),open=stock_data_df['Open'], high=stock_data_df['High'],
    low=stock_data_df['Low'], close=stock_data_df['Close'],increasing_line_color= 'cyan', decreasing_line_color= 'gray',
    showlegend = True , name="Candle Stick"), secondary_y=True)    
    
    
    fig.update_layout(title_text= "<b>"+stock+"</b>  Mentions/Price  Evolution ")
    
    fig.update_xaxes(title_text="Date")  
    fig.update_yaxes(title_text="<b>Mentions number</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Stock Price</b>", secondary_y=True)   
    plot(fig)








