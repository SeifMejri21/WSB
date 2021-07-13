# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 14:11:52 2021

@author: Administrator
"""

from reddit import wsb_thread_scraper,comment_extract,last_24_comments,list_flatter
from Data_cleaning import  sentiment_df,daily_thread_analysis
from Sentiment_count import count_stocks,filter_stocks
from Data_viz import  pie_plotly,tree_plotly,h_barplot_plotly,scatter_plotly,mean_bar_plotly

#### All comments
all_threads = wsb_thread_scraper('new')
all_comments = list_flatter(comment_extract(all_threads))
comments_sentiments_df = sentiment_df(all_comments,'Nasdaq 100')
filtered_all_comments_df = filter_stocks(comments_sentiments_df ,'Nasdaq 100')
counting_all_comments = count_stocks(filtered_all_comments_df)
pie_plotly(counting_all_comments)
tree_plotly(counting_all_comments)
h_barplot_plotly(counting_all_comments)
scatter_plotly(counting_all_comments)
mean_bar_plotly(counting_all_comments)


#### last 24
last_24_comments_flat = last_24_comments(all_threads,)
comments_sentiments_df_24 = sentiment_df(last_24_comments_flat,'Nasdaq')
filtered_all_comments_df_24 = filter_stocks(comments_sentiments_df_24 ,'Nasdaq 100')
counting_all_comments_24 = count_stocks(filtered_all_comments_df_24)
pie_plotly(counting_all_comments_24)
tree_plotly(counting_all_comments_24)
h_barplot_plotly(counting_all_comments_24)
scatter_plotly(counting_all_comments_24)
mean_bar_plotly(counting_all_comments_24)





#### daily discussion thread 
daily_thread_comments_sentimennts_df =daily_thread_analysis(all_threads,'Nasdaq')
filtered_daily_thread_comments_df = filter_stocks(daily_thread_comments_sentimennts_df,'Nasdaq 100')
counting_daily_thread_comments = count_stocks(filtered_daily_thread_comments_df)
pie_plotly(counting_daily_thread_comments)
tree_plotly(counting_daily_thread_comments)
h_barplot_plotly(counting_daily_thread_comments)
scatter_plotly(counting_daily_thread_comments)
mean_bar_plotly(counting_daily_thread_comments)































