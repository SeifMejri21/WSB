# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 21:06:42 2021

@author: Administrator
"""



import praw
import pandas as pd
import datetime as dt


# Reddit api application to access submission

reddit = praw.Reddit(client_id='YfzlHC9H72ts2A', \
                     client_secret='t2XVjxcGhRG04hmfVB84WP7v-0ETNg', \
                     user_agent='Seif_Mejri', \
                     username='MrSifon98 ', \
                     password='01041998')
    
############################################################################################################
############################################################################################################    
#converts creation date & time to datetime    
def get_date(created):
    return dt.datetime.fromtimestamp(created)

############################################################################################################
############################################################################################################
#scpaes all wsb threads by type
def wsb_thread_scraper(thread_type):
    if(thread_type=='hot'):
        subreddit = reddit.subreddit('wallstreetbets')
        top_subreddit = subreddit.hot(limit=1000)
    elif(thread_type == 'new'):
        subreddit = reddit.subreddit('wallstreetbets')
        top_subreddit = subreddit.new(limit=1000)
    elif(thread_type == 'top'):
        subreddit = reddit.subreddit('wallstreetbets')
        top_subreddit = subreddit.top(limit=1000)
    else:
        subreddit = reddit.subreddit('wallstreetbets')
        top_subreddit = subreddit.rising(limit=1000)
        
    threads_dict = { "title":[] , "score":[] , "id":[], "url":[] , "comms_num": []  , "created": [] , "body":[]}
    for submission in top_subreddit:
        threads_dict["title"].append(submission.title)
        threads_dict["score"].append(submission.score)
        threads_dict["id"].append(submission.id)
        threads_dict["url"].append(submission.url)
        threads_dict["comms_num"].append(submission.num_comments)
        threads_dict["created"].append(submission.created)
        threads_dict["body"].append(submission.selftext)
    
    threads_df = pd.DataFrame(threads_dict)
    _timestamp = threads_df["created"].apply(get_date)
    threads_df = threads_df.assign(timestamp = _timestamp)
    return(threads_df)


############################################################################################################
############################################################################################################
#extracts all the comments of certain thread category
def comment_extract(threads_df):
    id_list=threads_df['id'].tolist()
    comments_list=[]
    for thread_id in id_list : 
        submission = reddit.submission(id=thread_id)
        submission.comments.replace_more(limit=1000)
        a=[]
        for comment in submission.comments.list():
                a.append(comment.body)
        comments_list.append(a)
    return(comments_list)
        
############################################################################################################
############################################################################################################
def list_flatter(big_list):
    flat_list =[]
    for a in  big_list :
        for b in a :
            flat_list.append(b)
    return(flat_list)
            
############################################################################################################
############################################################################################################
#returs all the comments for threads that  was created on wsb on a given day
def last_comments(df,period): 
    #day must be in this form dd/mm/yyyy   ex : 02/07/2021
    periods=['1h','2h','4h','6h','12h','24h']
    if period in periods:
        if(period == '1h'):
            lower_end = dt.datetime.now()- dt.timedelta(hours=1)
        elif(period == '2h'):
            lower_end = dt.datetime.now()- dt.timedelta(hours=2)
        elif(period == '4h'):
            lower_end = dt.datetime.now()- dt.timedelta(hours=4)
        elif(period == '6h'):
            lower_end = dt.datetime.now()- dt.timedelta(hours=6)
        elif(period == '12h'):
            lower_end = dt.datetime.now()- dt.timedelta(hours=12)    
        elif(period == '24h'):
            lower_end = dt.datetime.now()- dt.timedelta(hours=24) 
    else:
        raise TypeError("period must be in  ['1h','2h','4h','6h','12h','24h']")    
    
    cond_last_24 = df['timestamp'] >= lower_end   
    df1=df[cond_last_24]
    
    
    id_list=df1['id'].tolist()
    comments_list=[]
    for thread_id in id_list : 
        submission = reddit.submission(id=thread_id)
        submission.comments.replace_more(limit=1000)
        a=[]
        for comment in submission.comments.list():
                a.append(comment.body)
        comments_list.append(a)
    comments_list_final =list_flatter(comments_list)
    return(comments_list_final)

############################################################################################################
############################################################################################################
#returs all the comments for threads that  was created on wsb on a given day
def hot_comments(df): 
    #day must be in this form dd/mm/yyyy   ex : 02/07/2021
    lower_end = dt.datetime.now()- dt.timedelta(hours=24)   
    cond_last_48 = df['timestamp'] >= lower_end   
    cond_hot  = df['score'] >= 10000 
    df1=df[cond_hot & cond_last_48]
    
    
    id_list=df1['id'].tolist()
    comments_list=[]
    for thread_id in id_list : 
        submission = reddit.submission(id=thread_id)
        submission.comments.replace_more(limit=1000)
        a=[]
        for comment in submission.comments.list():
                a.append(comment.body)
        comments_list.append(a)
    comments_list_final =list_flatter(comments_list)
    return(comments_list_final)




