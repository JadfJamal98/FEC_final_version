import numpy as np 
from data_mining import *
import re
from collections import Counter
from matplotlib import pyplot as plt
from importingEXCEL import *
import bag_of_words_v2 as bow2
import time
import os 
import selection
import seaborn as sns
sns.set()
from text_writer import *
import pandas as pd

# Import ESG word list

ws = load_workbook(filename="ESG_word_list.xlsx")
sheetns = ws.sheetnames

Governance = importing(ws[sheetns[0]])

Environmental = importing(ws[sheetns[1]])

Social = importing(ws[sheetns[2]])

topics = [Governance, Environmental, Social]
topic_names = ['Governance', 'Environmental', 'Social']

#Choose type of data
types = ['10-K', 'DEF 14A']

#Choose Companies
pa = os.getcwd().replace('\\', '/') +'/Top 40'

if not os.path.exists(pa):
    raise FileExistsError('The path does not exist')

tickers,years_for_each = selection.find_good(pa)

nb = 10
Tech = ['AAPL','MSFT','NVDA','ADBE','INTC','ORCL','QCOM']
Telecom = ['VZ','CSCO','CMCSA','NFLX','TMUS']
Banking = ['JPM','BAC','BLK','WFC']
Retail = ['AMZN','WMT','NKE','KO']
Health = ['UNH','ABT','MRK','PFE','TMO']
sect = [Tech,Telecom,Banking,Retail,Health]

nonotext = open(os.getcwd().replace("\\","/") +"/nonosquare.txt","r",encoding='utf-8')
nonolist = nonotext.readlines()[0].split(" ")
types = ['10-K', 'DEF 14A']
done_ticks = ['AAPL', 'AMZN', 'JNJ', 'MSFT', 'NVDA', 'UNH', 'WMT']


score_path = os.getcwd().replace('\\', '/') + '/score_files'

def create_score_files():
    for tick in tickers:
        if tick in done_ticks:
            continue
        else:
            print(tick)
            file_name = score_path + '/' + tick + '.txt'
            score_tick = pd.DataFrame()
            index = None
            for topic, topic_name in zip(topics, topic_names):

                score_10K = bow2.score_c_t(topic,tick,"10-K",nonolist)
                score_proxy = bow2.score_c_t(topic,tick,"DEF 14A",nonolist)
                merger = bow2.merge(score_10K,score_proxy,wP=0.5,wK=0.5)
                score_tick[topic_name] = [val for val in merger.values()]
                index = [key[-2:] for key in merger.keys()]

            score_tick.index.name = 'Year'
            score_tick.index = index   
            new_text_file = open(file_name, "w", encoding = 'utf-8') 
            new_text_file.write(score_tick.to_string()) 
            new_text_file.close()

create_score_files()