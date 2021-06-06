import numpy as np 
from Wordlist_Import import *
import Bag_of_Words as bow2
import os 
import Selection
from Text_Writer import *
import pandas as pd

# Import ESG word list
ws = load_workbook(filename="ESG_word_list.xlsx")
sheetns = ws.sheetnames

Governance = importing(ws[sheetns[0]])
Environmental = importing(ws[sheetns[1]])
Social = importing(ws[sheetns[2]])

# Defining topics and topic names
topics = [Governance, Environmental, Social]
topic_names = ['Governance', 'Environmental', 'Social']

# Choose type of data
types = ['10-K', 'DEF 14A']

# Choose path for company files
pa = os.getcwd().replace('\\', '/') +'/Top 40'

if not os.path.exists(pa):
    raise FileExistsError('The path does not exist')

# Get the 'good' ones, i.e. the ones with enough data
tickers,years_for_each = Selection.find_good(pa)

Tech = ['AAPL','MSFT','NVDA','ADBE','INTC','ORCL','QCOM']
Telecom = ['VZ','CSCO','CMCSA','NFLX','TMUS']
Banking = ['JPM','BAC','BLK','WFC']
Retail = ['AMZN','WMT','NKE','KO']
Health = ['UNH','ABT','MRK','PFE','TMO']
sect = [Tech,Telecom,Banking,Retail,Health]

nonotext = open(os.getcwd().replace("\\","/") +"/nonosquare.txt","r",encoding='utf-8')
nonolist = nonotext.readlines()[0].split(" ")
types = ['10-K', 'DEF 14A']

score_path = os.getcwd().replace('\\', '/') + '/score_files'

def create_score_files():
    """
    Function that creates file from the scores that can be accessed later on.
    ==============================================================================================================

    Input:
    ------
    None

    Output:
    ------
    None. Files are directly created in the specified directory. 
    """
    for tick in tickers:
        
        if os.path.exists(score_path + '/' + tick + '.txt'):
            print('File alredy exists at:')
            print(score_path + '/' + tick + '.txt')
        
        # If file does not yet exist, we compute the score and put it into file
        else:
            
            file_name = score_path + '/' + tick + '.txt'
            score_tick = pd.DataFrame()
            index = None
            for topic, topic_name in zip(topics, topic_names):

                # Computing the scores for 10-k and proxy using bag-of-words
                score_10K = bow2.score_c_t(topic,tick,"10-K",nonolist)
                score_proxy = bow2.score_c_t(topic,tick,"DEF 14A",nonolist)
                
                # Merging the two scores for the types
                merger = bow2.merge(score_10K,score_proxy,wP=0.5,wK=0.5)
                score_tick[topic_name] = [val for val in merger.values()]
                index = [key[-2:] for key in merger.keys()]

            score_tick.index = index   
            new_text_file = open(file_name, "w", encoding = 'utf-8') 
            new_text_file.write(score_tick.to_string()) 
            new_text_file.close()

# Executes the function and creates score files.
create_score_files()