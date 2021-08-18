# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 22:00:59 2021

@author: Administrator
"""



import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt


from reddit_scraper import wsb_thread_scraper,last_comments,hot_comments
from data_cleaner import ticker_getter , company_getter,sentiment_df,market_getter
from data_maker import one_stock_mentions , DT_dict_maker, TM_dict_maker,market_cap,MC_finder,rev_MC_finder
from mention_count import  filter_stocks,count_stocks

#####################################################################################################################

### Data
DT_dict = DT_dict_maker()
TM_dict = TM_dict_maker()

stocks =  list(ticker_getter())
stocks = [x.upper() for x in stocks]

dates = list(DT_dict['date'])
dates.reverse()

dates_DT = list(DT_dict['date'])
dates_DT.reverse()

dates_TM = list(TM_dict['date'])
dates_TM.reverse()


merket_cap_list=market_cap()['Market Cap'].tolist()

sp500=market_getter('S&P 500')[0]
nasdaq100=market_getter('Nasdaq 100')[0]
dow30=market_getter('Dow Jones')[0]

all_threads = wsb_thread_scraper('new')

#####################################################################################################################

max_MC=max(merket_cap_list)
min_MC=min(merket_cap_list)
max_MC_1_5=max(merket_cap_list)*(1/5)
max_MC_2_5=max(merket_cap_list)*(2/5)
max_MC_3_5=max(merket_cap_list)*(3/5)
max_MC_4_5=max(merket_cap_list)*(4/5)



#####################################################################################################################

hot_comments_list = hot_comments(all_threads)
sent_df1= sentiment_df(hot_comments_list)
filtered_all_comments_df1 = filter_stocks(sent_df1 )
counting_all_comments1 = count_stocks(filtered_all_comments_df1)


DT_dict_hot = {'date' : dt.datetime.today() ,'name' : 'Hottest Comments' ,
                'sent_df' :sent_df1 , 'count_df' : counting_all_comments1}

#####################################################################################################################
#####################################################################################################################

last_comments_list = last_comments(all_threads,'1h')
sent_df= sentiment_df(last_comments_list)
filtered_all_comments_df = filter_stocks(sent_df )
counting_all_comments = count_stocks(filtered_all_comments_df)

DT_dict_late = {'date' : dt.datetime.today() ,'name' : 'Latest Comments' ,
                'sent_df' :sent_df , 'count_df' : counting_all_comments}


#####################################################################################################################
#####################################################################################################################



app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Dash-101', style={ 'font-size': '50px' , 'color':'#46BE52' , 
                               'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#1A2127'}),
    
    html.Div([
            html.Label(['Comments type'],
   style={'font-weight': 'bold', 'font-size': '20px' , 'color':'#1A2127' , 'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}),
            dcc.RadioItems(id='comment_type',
                options=[
                         {'label': 'Daily thread', 'value': 'Daily thread'},
                         {'label': 'Tomorrow Moves', 'value': 'Tomorrow Moves'},
                         {'label': 'Hottest Comments', 'value': 'Hottest Comments'},
                         {'label': 'Latest Comments', 'value': 'Latest Comments'},
                ],value='Daily thread',style={"width": "50%"}),]),
    
    html.Div([
        html.Label(['Dates'],   
           style={'font-weight': 'bold', 'font-size': '17px' , 'color':'#1A2127' , 'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}),
        dcc.Dropdown(id='my_dropdown',
            options= [{'label':x, 'value':x} for x in dates] ,
            value=dates[0],
            multi=False,
            clearable=False,
            style={"width": "50%"}),]),

    html.Div(html.H3(id='output_container', children=[]),
             style={ 'font-size': '23px' , 'color':'#1A2127' , 
                    'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}) ,

    html.Div([
            html.Label(['Filter by index'],
   style={'font-weight': 'bold', 'font-size': '17px' , 'color':'#1A2127' , 'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}),
            dcc.RadioItems(id='stock_filter',
                options=[
                         {'label': 'S&P 500', 'value': 'S&P 500'},
                         {'label': 'NASDAQ 100', 'value': 'NASDAQ 100'},
                         {'label': 'DOW 30', 'value': 'DOW 30'},
                         {'label': 'All stocks', 'value': 'All stocks'},
                ],style={"width": "50%"}),]),

     html.Div([
    html.Label(['Filter by Market Cap'],
                style={'font-weight': 'bold','font-size': '17px' , 'color':'#1A2127' , 
                    'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}),
   html.P(),
    dcc.RangeSlider(
        id='market_cap', # any name you'd like to give it
        marks={
            0: '0',     # key=position, value=what you see
            506000000000: '506 billion $',
            1012000000000: '1012 billion $',
            1518000000000: '1518 billion $',
            2024000000000: '2024 billion $',
            2530000000000: '2530 billion $',
        },
        step=max_MC/100,                # number of steps between values
        min=min_MC,
        max=max_MC,
        value=[min(merket_cap_list),max(merket_cap_list)],     # default value initially chosen
        dots=True,             # True, False - insert dots, only when step>1
        allowCross=False,      # True,False - Manage handle crossover
        disabled=False,        # True,False - disable handle
        pushable=2,            # any number, or True with multiple handles
        #updatemode='mouseup',  # 'mouseup', 'drag' - update value method
        included=True,         # True, False - highlight handle
        vertical=False,        # True, False - vertical, horizontal slider
        verticalHeight=900,    # hight of slider (pixels) when vertical=True
        className='None',
        tooltip={'always visible':False,  # show current slider values
                 'placement':'bottom'},
        ),
]),

    
    
    html.Div([dcc.Graph(id='the_graph')]),
    html.H1('Dash-101', style={ 'font-size': '15px' , 'color':'#46BE52' , 'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}),
    html.Div([dcc.Graph(id='the_graph2')]),
    html.H1('Dash-101', style={ 'font-size': '15px' , 'color':'#46BE52' , 'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}),
    html.Div([dcc.Graph(id='the_graph3')]),
    html.H1('Dash-101', style={ 'font-size': '15px' , 'color':'#46BE52' , 'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}),
    html.Div([dcc.Graph(id='the_graph4')]),
    html.H1('Dash-101', style={ 'font-size': '15px' , 'color':'#46BE52' , 'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}),    
    html.Div([dcc.Graph(id='the_graph6')]),
    
    html.H1('Individual Stock', style={ 'font-size': '30px' , 'color':'#46BE52' , 
                               'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#1A2127'}),
        
    html.Div([
        html.Label(['Stocks']),
        dcc.Dropdown(
            id='my_dropdown2',
            options= [{'label':x, 'value':x} for x in stocks] ,
            value='AAPL',
            multi=False,
            clearable=False,
            style={"width": "30%"}),]),
    
    html.Div(html.H3(id='output_container2', children=[]),
             style={ 'font-size': '20px' , 'color':'#1A2127' , 
                    'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}) ,
    html.Div([dcc.Graph(id='the_graph5')]),
    html.H1('Dash-101', style={ 'font-size': '15px' , 'color':'#46BE52' , 'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}),
    html.Div([dcc.Graph(id='the_graph7')]),

    html.H1('Dash-101', style={ 'font-size': '15px' , 'color':'#46BE52' , 'font-family' : 'Verdana', 'text-align': 'center','backgroundColor':'#46BE52'}),

    
])

#---------------------------------------------------------------
@app.callback(
    Output(component_id='output_container', component_property='children'),
    Output(component_id='the_graph', component_property='figure'),
    Output(component_id='the_graph2', component_property='figure'),
    Output(component_id='the_graph3', component_property='figure'),
    Output(component_id='the_graph4', component_property='figure'),
    Output(component_id='the_graph6', component_property='figure'),
    Output(component_id='output_container2', component_property='children'),
    Output(component_id='the_graph5', component_property='figure'),
    Output(component_id='the_graph7', component_property='figure'),
    Input(component_id='my_dropdown', component_property='value'),
    Input(component_id='my_dropdown2', component_property='value'),
    Input(component_id='comment_type', component_property='value'),
    Input(component_id='stock_filter', component_property='value'),
    Input(component_id='market_cap', component_property='value'),
)

def update_graph(my_dropdown,my_dropdown2, comment_type,stock_filter,market_cap):
    
    
    my_index=len(dates) - 1 - dates.index(dt.datetime.strptime(my_dropdown, '%Y-%m-%d').date())
    if(comment_type == 'Daily thread'):        
        my_df = DT_dict['count_df'][my_index]
        count_max=10
        count_max_2=5
        container = "The data from: {}".format(my_dropdown)
    if(comment_type == 'Tomorrow Moves'):        
        my_df = TM_dict['count_df'][my_index]
        count_max=10
        count_max_2=5
        container = "The data from: {}".format(my_dropdown)
    elif(comment_type == 'Hottest Comments'):
        my_df = DT_dict_hot['count_df']
        count_max=5
        count_max_2=3
        container = "Hottest Comments on WSB in the last 24 hours"
    elif(comment_type == 'Latest Comments'):
        my_df = DT_dict_late['count_df']
        count_max=1
        count_max_2=1
        container = "Latest Comments on WSB in the last 4 hours"
    
    if stock_filter == 'S&P 500':
        booli = my_df.stock.isin(sp500)
        my_df=my_df[booli]
        
    elif stock_filter == 'NASDAQ 100':
        booli = my_df.stock.isin(nasdaq100)
        my_df=my_df[booli]   
        
    elif stock_filter == 'DOW 30':
        booli = my_df.stock.isin(dow30)
        my_df=my_df[booli]
    elif stock_filter == 'All stocks':
        booli = my_df.stock.isin(stocks)
        my_df=my_df[booli]
    
    my_MCs=[]
    for tick in my_df['stock'].tolist() :
        my_MCs.append(MC_finder(tick))
    MC_filtered_tickers=[]    
    for j in range(len(my_MCs)):
        if ((my_MCs[j]<=market_cap[1] ) & (my_MCs[j]>=market_cap[0] )):
            MC_filtered_tickers.append(rev_MC_finder(my_MCs[j]))
     
    mc_filter=my_df.stock.isin(MC_filtered_tickers)
    my_df=my_df[mc_filter]


##############################################################################################
#### treeplot
    nb=len(my_df['stock'])
    
    fig2 = px.treemap(my_df,
    values = 'all_count' ,                  
    names = 'stock',
    parents= ['us market']*nb,
    hover_data= ['company']
    )
    fig2.update_traces(root_color="lightgrey")
    fig2.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig2.update_layout(title="Mentions Distribuion " )  
##############################################################################################
#### horizontal barplot   
    df2 = my_df[my_df['all_count']>=count_max].sort_values(by=['all_count'])
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
    y= df2['stock'].tolist(),
    x= df2['positive_count'].tolist(),
    name=' Positive',
    orientation='h',
    marker=dict(
        color='rgba(0, 255, 130, 0.6)',
        line=dict(color='rgba(0, 255, 130, 1.0)', width = 1 ))))

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
                      yaxis_title="Stock",
                      height =1000)
    fig3.update_layout(barmode='stack')
##############################################################################################
    fig4 = px.scatter(my_df, x="negative_count", y="positive_count", color = 'stock',
                 size='all_count', hover_data=['stock','company'],text = 'stock')
    
    fig4.add_shape(type="line",
    x0=0, y0=0, x1= max(my_df['negative_count'].max(),my_df['positive_count'].max()),
    y1= max(my_df['negative_count'].max(),my_df['positive_count'].max()),
    line=dict(
        color="lightpink",
        width=4,
        dash="dot",
    ))
    fig4.update_layout(title="Mentions type ", yaxis_title="Positive mentions",xaxis_title="Negative mentions")
##############################################################################################
    df3= my_df[my_df['all_count']>=count_max_2].sort_values(by=['mean_score'])   
    fig5 = px.bar(df3, x='stock', y='mean_score' , color= 'stock', 
                  hover_data =['stock','company','all_count'])
    fig5.update_layout(title="General feeling about the Stock",
                      xaxis_title="Stock",
                      yaxis_title="average mention score")
##############################################################################################    
    
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
    
##############################################################################################
    stocks_list=ticker_getter()
    companies_list=company_getter()
    the_company=companies_list[stocks_list.index(my_dropdown2.lower())]
    container2 = "Your stock is: {}".format(my_dropdown2+' ('+the_company+')')
##############################################################################################
    df_1=one_stock_mentions(my_dropdown2,DT_dict)[0]
    stock_data_df=one_stock_mentions(my_dropdown2,DT_dict)[1]
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df_1['date'], y=df_1['Close'],name="Close Price"),secondary_y=True) 
    fig.add_trace(go.Scatter(x=df_1['date'], y=df_1['negative_count'],name="Negative Mentions"),secondary_y=False)    
    fig.add_trace(go.Scatter(x=df_1['date'], y=df_1['positive_count'],name="Positive Mentions"),secondary_y=False) 
    
    fig.add_trace(go.Candlestick(x=stock_data_df.index.tolist(),open=stock_data_df['Open'], high=stock_data_df['High'],
    low=stock_data_df['Low'], close=stock_data_df['Close'],increasing_line_color= 'cyan', decreasing_line_color= 'gray',
    showlegend = True , name="Candle Stick"), secondary_y=True)    
    
    
    fig.update_layout(title_text= "<b>"+my_dropdown2+"</b>  Mentions/Price  Evolution ")
    
    fig.update_xaxes(title_text="Date")  
    fig.update_yaxes(title_text="<b>Mentions number</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Stock Price</b>", secondary_y=True)   
##############################################################################################
    df_2=df_1[['positive_count', 'negative_count', 'mean_score', 'sum_score','puts', 'calls', 'Close']]
    corr_df=df_2.corr()   
    fig7 = px.imshow(corr_df)
    fig7.update_layout(title="Correlation matrix for "+my_dropdown2,)
##############################################################################################

##############################################################################################
##############################################################################################


    return(container,fig2,fig3,fig4,fig5,fig6,container2,fig,fig7)


if __name__ == '__main__':
    app.run_server(debug=False)





    

