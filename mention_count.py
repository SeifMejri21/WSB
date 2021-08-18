# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 21:45:34 2021

@author: Administrator
"""


import pandas as pd
from data_cleaner import ticker_getter,company_getter
from numpy import nan


############################################################################################################
############################################################################################################
#function that filterns the data frame f
def filter_stocks(df):
    symbols_lower_ND100 = ticker_getter()
    ND_100 = []
    for ticker in symbols_lower_ND100 :
        stock_df=df[df['stock1']==ticker.upper()]
        ND_100.append(stock_df)
    final_df= pd.concat(ND_100) 
    final_df.reset_index(inplace = True, drop = True)
    return(final_df)


############################################################################################################
############################################################################################################
#function that counts the type of a given stock
def sentiment_count(scores):
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
def puts_calls_count(put_list,call_list):
    count_list=[]
    puts_count =0
    calls_count =0
    for bool_1 in put_list:
        if (bool_1== True):
            puts_count=puts_count+1
    for bool_2 in call_list:
        if (bool_2== True):
            calls_count=calls_count+1
    count_list.append(puts_count)
    count_list.append(calls_count)
    return(count_list)

############################################################################################################
############################################################################################################

def true_list(list_a , list_b, target):
    target_indexes=[]
    a_series=pd.Series(list_a)
    b_series=pd.Series(list_b)
    final_list_a=[]
    final_list_b=[]
    for i in range(len(list_a)):
        if list_a[i] == target:
            target_indexes.append(i)
    final_list_a=list(a_series[target_indexes])
    final_list_b=list(b_series[target_indexes])
#    final_list_a=list(itemgetter(*target_indexes)(list_a))
#    final_list_b=list(itemgetter(*target_indexes)(list_b))
#    for j in target_indexes:
#        final_list_a.append(list_a[j])
#        final_list_b.append(list_b[j])
    final_list = [final_list_a , final_list_b]
    return(final_list)


############################################################################################################
############################################################################################################
def companny_identifier(ticker):
    tick_list = ticker_getter()
    company_list =  company_getter()
    company = company_list[tick_list.index(ticker.lower())]
    return(company)
    
############################################################################################################
############################################################################################################
#function that counts mentions and mentions type for each stock
def count_stocks(df):
    count_sentiment_dict ={'stock' :[] , 'company':[] , 'all_count' :[] ,'positive_count':[] ,
                           'negative_count':[] , 'neutral_count':[] ,'mean_score':[],'sum_score':[]
                           ,'puts':[],'calls':[]}
    stocks1 = df['stock1'].tolist()
    stocks2 = df['stock2'].tolist()
    stocks3 = df['stock3'].tolist()
    stocks= stocks1 + stocks2 + stocks3
    stocks_uniq= list(set(stocks))
    stocks_uniq = [x for x in stocks_uniq if x is not nan]
    if '' in stocks_uniq:
        stocks_uniq.remove('')
  
    stocks_list=[]    
    for stock in stocks_uniq:
        stock_df=df[(df['stock1']==stock) | (df['stock2']==stock) | (df['stock3']==stock) ] 
        stock_list= list(stock_df['stock1'].tolist()) + (stock_df['stock2'].tolist()) + (stock_df['stock3'].tolist())
        
        scores_list_1stock= (stock_df['compound'].tolist()) + (stock_df['compound'].tolist()) + (stock_df['compound'].tolist())
        aux =true_list(stock_list,scores_list_1stock,stock)
        true_stock =aux[0]
        true_score =aux[1]
        
        
        puts_list_1stock= list((stock_df['put'].tolist()) + (stock_df['put'].tolist()) + (stock_df['put'].tolist()))
        aux2 =true_list(stock_list,puts_list_1stock,stock)
        true_puts =aux2[1]
        
        calls_list_1stock=list((stock_df['call'].tolist()) + (stock_df['call'].tolist()) + (stock_df['call'].tolist()))
        aux3 =true_list(stock_list,calls_list_1stock,stock)
        true_calls =aux3[1]
        
        puts_calls_list = puts_calls_count(true_puts,true_calls)

        count_sentiment_dict['stock'].append(stock)
        count_sentiment_dict['company'].append(companny_identifier(stock))
        count_sentiment_dict['all_count'].append(len(true_stock))
        count_sentiment_dict['mean_score'].append((sum(true_score))/(len(true_score)))
        count_sentiment_dict['sum_score'].append(sum(true_score))
        
        scores_list = sentiment_count(true_score)
        count_sentiment_dict['positive_count'].append(scores_list[0])
        count_sentiment_dict['negative_count'].append(scores_list[1])
        count_sentiment_dict['neutral_count'].append(scores_list[2])
        count_sentiment_dict['puts'].append(puts_calls_list[0])
        count_sentiment_dict['calls'].append(puts_calls_list[1])


        stocks_list.append(stock_df)       
    count_sentiment_df = pd.DataFrame(count_sentiment_dict)    
    return (count_sentiment_df)
    

############################################################################################################
############################################################################################################





