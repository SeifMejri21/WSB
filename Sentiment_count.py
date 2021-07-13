# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 13:58:24 2021

@author: Administrator
"""






import pandas as pd
from Data_cleaning import ticker_getter



############################################################################################################
############################################################################################################
#function that filterns the data frame f
def filter_stocks(df, market):
    symbols_lower_ND100 = ticker_getter(market)
    ND_100 = []
    for ticker in symbols_lower_ND100 :
        stock_df=df[df['stock']==ticker.upper()]
        ND_100.append(stock_df)
    final_df= pd.concat(ND_100) 
    final_df.reset_index(inplace = True, drop = True)
    return(final_df)


############################################################################################################
############################################################################################################
#function that counts the type of a given stock
def sentiment_count(df):
    scores= df['compound'].tolist()
    pos_count=0
    neg_count=0
    neut_count=0
    for score in scores : 
        if(score>0):
            pos_count=pos_count+1    
        elif(score<0):
            neg_count=neg_count+1
        else:
            neut_count = neut_count+1 
    test_count = pos_count + neg_count + neut_count
    if((test_count != len(scores))):
        raise TypeError('you have a huge problem !!! ')
    scores_list = [pos_count , neg_count , neut_count]
    return(scores_list)
        

############################################################################################################
############################################################################################################
#function that counts mentions and mentions type for each stock
def count_stocks(df):
    count_sentiment_dict ={'stock' :[] , 'company':[] , 'all_count' :[] ,'positive_count':[] ,
                           'negative_count':[] , 'neutral_count':[] ,'mean_score':[] }
    stocks = df['stock'].unique().tolist()
    stocks_list=[]
    for stock in stocks:
        stock_df=df[df['stock']==stock] 
        count_sentiment_dict['stock'].append(stock)
        count_sentiment_dict['company'].append(stock_df.iloc[0,stock_df.columns.get_loc('company')])
        count_sentiment_dict['all_count'].append(len(stock_df['stock']))
        count_sentiment_dict['mean_score'].append(stock_df['compound'].mean( skipna = True))
        
        scores_list = sentiment_count(stock_df)
        count_sentiment_dict['positive_count'].append(scores_list[0])
        count_sentiment_dict['negative_count'].append(scores_list[1])
        count_sentiment_dict['neutral_count'].append(scores_list[2])
        stocks_list.append(stock_df)       
    count_sentiment_df = pd.DataFrame(count_sentiment_dict)    
    return (count_sentiment_df)
    

############################################################################################################
############################################################################################################









