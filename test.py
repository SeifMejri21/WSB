# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 11:10:47 2021

@author: Administrator
"""



import pandas as pd


from reddit_scraper import wsb_thread_scraper
from data_cleaner import  sentiment_df
from mention_count import count_stocks,filter_stocks
from data_viz import tree_plotly,h_barplot_plotly,scatter_plotly,mean_bar_plotly,count_ev_viz,puts_calls_bar
from data_maker import  daily_thread_name_2,DT_scraper,days_list,DT_maker,TM_maker




### Scraping threads names,id, urls ....
all_threads = wsb_thread_scraper('new')



a=DT_maker(all_threads,0)
TM_maker(all_threads,0)


### Scraping todays thread (Daily discussion thread , what are your moves for tommorrow, )

#Daily discussion thread 
sub_name =daily_thread_name_2('daily thread',1)[0]
print(sub_name)

comments_data = DT_scraper(all_threads,sub_name)
comments_data_df=pd.DataFrame({'comments' : comments_data})
comments_data_df.to_csv(sub_name+'.csv')


#what are your moves for tommorrow

sub_name =daily_thread_name_2('tomorrow moves',0)[0]
print(sub_name)

comments_data = DT_scraper(all_threads,sub_name)
comments_data_df=pd.DataFrame({'comments' : comments_data})
comments_data_df.to_csv(sub_name+'.csv')

###################################################################################################
###################################################################################################



###################################################################################################
### reading, analysing and exporting comment for a given thread

#Daily discussion thread  
sub_name =daily_thread_name_2('daily thread',1)[0]
sub_name
comments_data = pd.read_csv(sub_name+'.csv')
comments_list= comments_data['comments'].tolist()
sent_df= sentiment_df(comments_list)
filtered_all_comments_df = filter_stocks(sent_df )
counting_all_comments = count_stocks(filtered_all_comments_df)

daily_thread_name_2('daily thread',1)[1]

sent_df.to_csv('Daily threads sent_anal '+ daily_thread_name_2('daily thread',1)[1] +'.csv')
counting_all_comments.to_csv('Daily threads mentions count '+ daily_thread_name_2('daily thread',1)[1] +'.csv')


###################################################################
#What are your moves tommorw thread  
sub_name =daily_thread_name_2('tomorrow moves',0)[0]
sub_name
comments_data = pd.read_csv(sub_name+'.csv')
comments_list= comments_data['comments'].tolist()
sent_df= sentiment_df(comments_list)
filtered_all_comments_df = filter_stocks(sent_df )
counting_all_comments = count_stocks(filtered_all_comments_df)

daily_thread_name_2('tomorrow moves',0)[1]

sent_df.to_csv('Tomorrow Moves sent_anal '+ daily_thread_name_2('tomorrow moves',0)[1] +'.csv')
counting_all_comments.to_csv('Tomorrow Moves mentions count '+ daily_thread_name_2('tomorrow moves',0)[1] +'.csv')


##############################################################



###fresh data

DT_dict = {'date' : [] ,'name' : [] ,  'sent_df' :[] , 'count_df' : []}
days=days_list('daily thread')


for i in days:
    listy=daily_thread_name_2('daily thread',24*i)[0]
    comments_data = pd.read_excel(listy[0]+'.xlsx')
    comments_list= comments_data['comments'].tolist()
    sent_df= sentiment_df(comments_list,'Nasdaq')
    filtered_all_comments_df = filter_stocks(sent_df ,'Nasdaq')
    counting_all_comments = count_stocks(filtered_all_comments_df)
    DT_dict['date'].append(listy[1])
    DT_dict['name'].append(listy[0])
    DT_dict['sent_df'].append(sent_df)
    DT_dict['count_df'].append(counting_all_comments)    
    
##############################################################
###saved data

DT_dict = {'date' : [] ,'name' : [] ,  'sent_df' :[] , 'count_df' : []}
days=days_list('daily thread')

for i in days:
    sent_df_list=daily_thread_name_2('sent_df',24*i)
    count_df_list=daily_thread_name_2('count_df',24*i)
    DT_dict['date'].append(sent_df_list[2])
    DT_dict['name'].append('Daily Discussion Thread for '+count_df_list[1])
    DT_dict['count_df'].append(pd.read_excel(count_df_list[0]+'.xlsx'))
    DT_dict['sent_df'].append(pd.read_excel(sent_df_list[0]+'.xlsx'))  

###################################################################################################
###################################################################################################
  


###################################################################################################
###################################################################################################




############### TEST ZONE ###############



