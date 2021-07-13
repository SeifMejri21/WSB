# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 13:44:44 2021

@author: Administrator
"""




import pandas as pd
import datetime as dt
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import string
import re
from reddit import wsb_thread_scraper,comment_extract


############################################################################################################
############################################################################################################
# function that gets the type of a cerain word
def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

# function that cleans comments
def clean_text(text):
    # lower text
    text = text.lower()
    # tokenize text and remove puncutation
    text = [word.strip(string.punctuation) for word in text.split(" ")]
     # remove words that contain numbers
    text = [word for word in text if not any(c.isdigit() for c in word)]
    # remove stop words
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    # remove empty tokens
    text = [t for t in text if len(t) > 0]
    # pos tag text
    pos_tags = pos_tag(text)
    # lemmatize text
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    # remove words with only one letter
    text = [t for t in text if len(t) > 1]
    # join all
    text = " ".join(text)
    return text

############################################################################################################
############################################################################################################
# function that returns a list  of tickers listed on a certain market  ex:NYSE 
def ticker_getter(market):
    if (market == 'Nasdaq 100') :
        ticker_data = pd.read_excel(r'C:\Users\Administrator\Desktop\NASDAQ100.xlsx')
    elif (market == 'NYSE'):
        ticker_data = pd.read_excel(r'C:\Users\Administrator\Desktop\NYSE.xlsx')
    elif (market == 'Nasdaq'):
        ticker_data =  pd.read_excel(r'C:\Users\Administrator\Desktop\nasdaq.xlsx')
    else : 
        raise TypeError("Market must be NYSE, Nasdaq or Nasdaq 100 ")     
    symbols = ticker_data['Symbol'].tolist()
    symbols_lower=['']*len(symbols)
    
    for i in range(len(symbols)):
        symbols[i]=str(symbols[i])
        symbols[i]= symbols[i].upper()
        symbols_lower[i]=symbols[i].lower()    
    
    return(symbols_lower)

############################################################################################################
############################################################################################################
#function that returns a list of company names listed on a certain market
def company_getter(market):
    if (market == 'Nasdaq 100') :
        ticker_data = pd.read_excel(r'C:\Users\Administrator\Desktop\NASDAQ100.xlsx')
    elif (market == 'NYSE'):
        ticker_data = pd.read_excel(r'C:\Users\Administrator\Desktop\NYSE.xlsx')
    elif (market == 'Nasdaq'):
        ticker_data =  pd.read_excel(r'C:\Users\Administrator\Desktop\nasdaq.xlsx')
    else : 
        raise TypeError("Market must be NYSE, Nasdaq or Nasdaq 100 ")         
    
    comapny = ticker_data['Company'].tolist()
    return(comapny)


############################################################################################################
############################################################################################################
#function that returns a dataframe of coments analysed sentiments   
def sentiment_df(comments_list,market):
    sia = SIA()
    results = []
    for comment in comments_list :
        pol_score = sia.polarity_scores(comment)
        results.append(pol_score)
    sentiments_dataset = pd.DataFrame(results)
    sentiment_df=pd.DataFrame({'comment': comments_list , 'stock' : ['']*len(results) , 'company' : ['']*len(results) })
    symbols_lower_ND100 = ticker_getter(market)
    companies_ND100 = company_getter(market)
    final_df=sentiment_df.join(sentiments_dataset)
    for ticker in symbols_lower_ND100 :
        for com in comments_list :
            if re.search(r'\s+\$?' + ticker + r'\$?\s+' , com) :
                final_df.iloc[comments_list.index(com), final_df.columns.get_loc('stock')] = ticker.upper()
                final_df.iloc[comments_list.index(com), final_df.columns.get_loc('company')] = companies_ND100[symbols_lower_ND100.index(ticker)]
            
    return(final_df)

############################################################################################################
############################################################################################################
#function that returns a the name of the daily thread for today
def daily_thread_name():
    mydate = dt.datetime.now()
    day = mydate.strftime("%d")
    month = mydate.strftime("%B")
    year =  mydate.strftime("%Y")
    date = str(month+' '+ day +', '+year) 
    daily_thread = 'Daily Discussion Thread for '+date
    return(daily_thread)


############################################################################################################
############################################################################################################
#function that scrapes, cleans and analyzes thr daily discussuion thread
def daily_thread_analysis(thread_df,market):
    thread_of_the_day = thread_df[thread_df['title']==daily_thread_name()]
    daily_thread_comments=[]
    daily_thread_comments= comment_extract(thread_of_the_day)
    daily_thread_comments_flat= [item for sublist in daily_thread_comments for item in sublist]
    daily_thread_comments_flat_clean=[]
    for subred in  daily_thread_comments_flat:
        daily_thread_comments_flat_clean.append(clean_text(subred))
    
    sentiment_df_final = sentiment_df(daily_thread_comments_flat_clean,market)
    return(sentiment_df_final)
   

############################################################################################################
############################################################################################################











