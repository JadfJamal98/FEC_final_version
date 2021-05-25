import numpy as np 
from data_mining import *
import re
from collections import Counter
from matplotlib import pyplot as plt
from importingEXCEL import *
from selection import *

def get_words(dictonary):
    # returns all words from a specific topic regardless of the categories and subcategories
    all_words = []
    categories = dictonary.keys()
    for category in categories:
        if category == 'self':
            all_words += dictonary[category]
        else:
            subcats = dictonary[category].keys()
            for subcat in subcats:
                all_words += dictonary[category][subcat]
    return all_words

def count_from_list(words, dictonary):
    #               ltopic freqof word from tokenization
    new_count = {}
    for word in words:
        if word in dictonary.keys():
            new_count.update({word:dictonary[word]})
        else:
            continue
    return new_count


def compute_score(topic, types, tickers, nb):

    #Create dictonary for computing words documents frequency
    df = {} #
    list_words = get_words(topic)#
    
    for word in list_words:#
        df.update({word: 0})#
    
    #Counting words from ESG word list

    #Get current path
    
    pa = os.getcwd().replace("\\","/") #
    


    #Get list of stop words to exclude
    stopwords = open(pa + '/nonosquare.txt',encoding ='utf-8') #
    stopwords_lines = stopwords.readlines()[0] #
    sw = stopwords_lines.split(' ') #this is the list or removed connection words #
    
    #tokenize all text files
    for tick in tickers:
        tick = tick.upper()
        for year in range(2021-nb, 2022):
            year = str(year)
            for file_type in types:
                if check(pa, tick, year, file_type):
                    text = open(pa + '/Top 40/statements/' + file_type +'_'+ tick+'_'+ year[-2:] +'.txt',"r",encoding ='utf-8')##########
                    tokenized = tokenize(text, sw)
                    #print(tokenized)
                    #create dictionary and count words
                    count_all = Counter(tokenized)
                    count_list = count_from_list(get_words(topic), count_all)
                    for word in count_list.keys():
                        df[word] += 1
    #print(df)
    #total number of documents
    tot_doc = nb*len(tickers)*len(types)

    #compute idf weights
    w_idf = {}
    for word in df.keys():
        if df[word] == 0:
            continue
        w_idf.update({word: np.log(tot_doc / df[word])})
    
    #Compute ESG Scores
    scores = {}
    #tokenize all text files
    for tick in tickers:
        tick = tick.lower()
        scores_years = []
        for year in range(2021-nb, 2022):
            year = str(year)
            tot_score = 0
            for file_type in types:
                if check(pa, tick, year, file_type):
                    text = open(pa + '/Top 40/statements/' + file_type +'_'+ tick+'_'+ year[-2:] +'.txt',encoding ='utf-8') ##############
                    tokenized = tokenize(text, sw)
                    #create dictionary and count words
                    count_all = Counter(tokenized)
                    count_list = count_from_list(get_words(topic), count_all)
                    sum_w = 0
                    for word in count_list.keys():
                        w = max(0, 1 + np.log(count_list[word])*w_idf[word])
                        sum_w += w
                    score = 1 / (1 + np.log(len(tokenized))) * sum_w
                    tot_score += 1 / len(types) * score
            scores_years.append(tot_score)
        scores.update({tick: scores_years})
    
    return scores
    #return list_words

def check(pa, tick, year, file_type):
    return os.path.exists(pa + '/Top 40/statements/' + file_type +'_'+ tick+'_'+ year[-2:] +'.txt')###########################



