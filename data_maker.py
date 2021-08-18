# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 21:53:59 2021

@author: Administrator
"""


import praw
import pandas as pd
import datetime as dt
import yfinance as yf


from reddit_scraper import wsb_thread_scraper,comment_extract,last_comments,list_flatter
from data_cleaner import  sentiment_df,daily_thread_analysis,ticker_getter
from mention_count import count_stocks,filter_stocks
#from data_viz import  pie_plotly,tree_plotly,h_barplot_plotly,scatter_plotly,mean_bar_plotly,sent_score,count_ev_viz



reddit = praw.Reddit(client_id='YfzlHC9H72ts2A', \
                     client_secret='t2XVjxcGhRG04hmfVB84WP7v-0ETNg', \
                     user_agent='Seif_Mejri', \
                     username='MrSifon98 ', \
                     password='01041998')
    


#############################################################################################
#############################################################################################

#####  #     #  #   #   ###  ########  ########   ####   #   #   ####             
#      #     #  ##  #  #        ##        ##     #    #  ##  #  #
#####  #     #  # # #  #        ##        ##     #    #  # # #   ###
#      #     #  #  ##  #        ##        ##     #    #  #  ##      #
#      #######  #   #   ###     ##     ########   ####   #   #  ####

#############################################################################################

### functions that returns a string of the thread name
def daily_thread_name_2(thread_type,delta) :
    mydate = dt.date.today()- dt.timedelta(hours=24*delta)
    day = mydate.strftime("%d")
    month = mydate.strftime("%B")
    year =  mydate.strftime("%Y")
    date = str(month+' '+ day +', '+year) 
    if thread_type == 'daily thread' :
            thread = 'Daily Discussion Thread for '+date
    elif thread_type == 'tomorrow moves' :
            thread = 'What Are Your Moves Tomorrow, '+date
    elif thread_type == 'Weekend thread' :
            thread = 'Weekend Discussion Thread for the Weekend of '+date
    elif thread_type == 'DT sent_df' :
            thread = 'Daily threads sent_anal '+date
    elif thread_type == 'DT count_df' :
            thread = 'Daily threads mentions count '+date
    elif thread_type == 'TM sent_df' :
            thread = 'Tomorrow Moves sent_anal '+date
    elif thread_type == 'TM count_df' :
            thread = 'Tomorrow Moves mentions count '+date
    else:
        raise TypeError("the thread type must  be   tomorrow moves ,   daily thread or Weekend thread ") 
    listy=[thread, date, mydate]
    return(listy)


#############################################################################################
#############################################################################################
###Function that scrapes comments from a given thread
def DT_scraper(df,sub_name):
    thread_name = df['title'].tolist()
    thread_id = df['id'].tolist()
    for thread in thread_name:
        if (thread==sub_name):
            my_thread_id = thread_id[thread_name.index(thread)]
    my_sub = reddit.submission(id =my_thread_id)
    my_sub.comments.replace_more(limit=1000)
    comments_list=[]
    for comment in my_sub.comments.list():
        comments_list.append(comment.body)
    return(comments_list)


###################################################################################################
###################################################################################################

def getIndexes(df, value):
    listOfPos = []
    result = df.isin([value])
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    return (row)
###################################################################################################
###################################################################################################

###function that returns a dataframe of
def one_stock_mentions(ticker , dct):
    out_dict = {  'stock' :[] , 'company' :[] , 'all_count' :[] , 'positive_count' :[] ,'negative_count' :[] ,
        'neutral_count' :[] , 'mean_score' :[] , 'sum_score' :[] , 'puts' :[] , 'calls' :[] }    
    out_dataframe=pd.DataFrame(out_dict)
    my_dates=[]
    delta=dt.timedelta(hours=24)
    for  i in range(len(dct['count_df'])):
        df= dct['count_df'][i]
        all_tickers = df['stock'].tolist()         
        price_df = yf.Ticker(ticker).history(period='1d', end=delta+dct['date'][len(dct['date'])-1], start=delta+dct['date'][0])
        prices_dates = price_df.index.tolist()
        prices_dates = [x.date() for x in prices_dates]
        if ticker in all_tickers :
            my_dates.append(dct['date'][i])
            out_dataframe.loc[df.index[i]] = df.iloc[getIndexes(df,ticker)]   
    
    close_list=[]
    open_list=[]
    high_list=[]
    low_list=[]
    for j in range(len(my_dates)):
        if (my_dates[j] in prices_dates ): 
            close_list.append(price_df.iloc[prices_dates.index(my_dates[j]), price_df.columns.get_loc('Close')])    
            open_list.append(price_df.iloc[prices_dates.index(my_dates[j]), price_df.columns.get_loc('Open')])    
            high_list.append(price_df.iloc[prices_dates.index(my_dates[j]), price_df.columns.get_loc('High')])
            low_list.append(price_df.iloc[prices_dates.index(my_dates[j]), price_df.columns.get_loc('Low')])
            
    price_df_2 = yf.Ticker(ticker).history(interval='1h', end=delta+dct['date'][len(dct['date'])-1], start=dct['date'][0])
    out_dataframe['date']=my_dates
    out_dataframe['Close']=close_list
    out_dataframe['Open']=open_list
    out_dataframe['High']=high_list
    out_dataframe['Low']=low_list
    
    out_list=[out_dataframe,price_df_2]
    return(out_list)

###################################################################################################
###################################################################################################

def market_cap():    
    data= pd.read_csv('ALL_TICKERS.csv')
    market_cap_data=data[['Symbol','Name','Market Cap']]
    return(market_cap_data)

###################################################################################################
###################################################################################################

def MC_finder(ticker):
    market_cap_data=market_cap()
    tickers = market_cap_data['Symbol'].tolist()
    MC = market_cap_data['Market Cap'].tolist()
    
    if ticker in tickers :
        my_MC= MC[tickers.index(ticker)]
    return(my_MC)

###################################################################################################
###################################################################################################

def rev_MC_finder(MC_val):
    market_cap_data=market_cap()
    tickers = market_cap_data['Symbol'].tolist()
    MC = market_cap_data['Market Cap'].tolist()
    if MC_val in MC :
        my_ticker= tickers[MC.index(MC_val)]
    return(my_ticker)


###################################################################################################
###################################################################################################

### Function that returns a list for eligible trading days
def days_list(thread_type):
    h8_bar= dt.datetime(2021,8,5,20,00,00).time()
    my_days_list=[]
    now =dt.datetime.now().time()

    if thread_type == 'daily thread':
        days_delta = int((dt.date.today() - dt.date(2021,7,14)).days) 
        for i in range(days_delta):
            if  not (((i-3)%7 == 0) | ((i-3)%7 == 1)):
                my_days_list.append(days_delta-i)
        if(h8_bar<now):
            if not (((days_delta-2)%7 == 0) | ((days_delta-2)%7 == 1)):
                my_days_list.append(0)
    if thread_type == 'tomorrow moves':
        days_delta = int((dt.date.today() - dt.date(2021,7,15)).days)
        for i in range(days_delta):
            if  not (((i-2)%7 == 0) | ((i-2)%7 == 1)):
                my_days_list.append(days_delta-i)
        if not (((days_delta-2)%7 == 0) | ((days_delta-2)%7 == 1)):
                my_days_list.append(0)
        if(h8_bar<now):
            if not (((days_delta-2)%7 == 0) | ((days_delta-2)%7 == 1)):
                my_days_list.append(-1)
    return(my_days_list)

#############################################################################################
#############################################################################################



def DT_dict_maker():
    dct = {'date' : [] ,'name' : [] ,  'sent_df' :[] , 'count_df' : []}
    days=days_list('daily thread')

    for i in days:
        sent_df_list=daily_thread_name_2('DT sent_df',i)
        count_df_list=daily_thread_name_2('DT count_df',i)
        dct['date'].append(sent_df_list[2])
        dct['name'].append('Daily Discussion Thread for '+count_df_list[1])
        dct['count_df'].append(pd.read_csv(count_df_list[0]+'.csv'))
        dct['sent_df'].append(pd.read_csv(sent_df_list[0]+'.csv')) 
    return(dct)



###################################################################################################
#####
def TM_dict_maker():
    dct = {'date' : [] ,'name' : [] ,  'sent_df' :[] , 'count_df' : []}
    days=days_list('tomorrow moves')

    for i in days:
        sent_df_list=daily_thread_name_2('TM sent_df',i)
        count_df_list=daily_thread_name_2('TM count_df',i)
        dct['date'].append(sent_df_list[2])
        dct['name'].append('What Are Your Moves Tomorrow, '+count_df_list[1])
        dct['count_df'].append(pd.read_csv(count_df_list[0]+'.csv'))
        dct['sent_df'].append(pd.read_csv(sent_df_list[0]+'.csv')) 
    return(dct)
###########################################################################

def DT_maker(all_threads,day):
    sub_name =daily_thread_name_2('daily thread',day)[0]
    print(sub_name)
    comments_data = DT_scraper(all_threads,sub_name)
    comments_data_df=pd.DataFrame({'comments' : comments_data})
    comments_data_df.to_csv(sub_name+'.csv')
    sent_df= sentiment_df(comments_data)
    filtered_all_comments_df = filter_stocks(sent_df )
    counting_all_comments = count_stocks(filtered_all_comments_df)
    sent_df.to_csv(daily_thread_name_2('DT sent_df',day)[0] +'.csv')
    counting_all_comments.to_csv(daily_thread_name_2('DT count_df',day)[0] +'.csv')
    return(counting_all_comments)

###################################################################################################
###################################################################################################
  
def TM_maker(all_threads,day):
    sub_name =daily_thread_name_2('tomorrow moves',day)[0]
    print(sub_name)
    comments_data = DT_scraper(all_threads,sub_name)
    comments_data_df=pd.DataFrame({'comments' : comments_data})
    comments_data_df.to_csv(sub_name+'.csv')
    sent_df= sentiment_df(comments_data)
    filtered_all_comments_df = filter_stocks(sent_df )
    counting_all_comments = count_stocks(filtered_all_comments_df)
    sent_df.to_csv(daily_thread_name_2('TM sent_df',day)[0] +'.csv')
    counting_all_comments.to_csv(daily_thread_name_2('TM count_df',day)[0] +'.csv')
    return(counting_all_comments)

###################################################################################################
###################################################################################################



###################################################################################################
###################################################################################################








