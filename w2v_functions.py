import numpy as np
import os
from text_writer import *
from bag_of_words_v2 import *

def score_w2v(model, topic_list, tick, typ, nolist):
    """
    Computes the yearly scores for a company using the w2v model given as input (for a specific kind of document and topic list)

    """
    
    topic_dict = {}
    for key in topic_list:
        topic_dict.update({key: 0})
    
    pa = os.getcwd().replace("\\","/")+'/Top 40' # path for for the .py folder

    pathf = os.getcwd().replace("\\","/")+"/Top 40/statements" # path for the .txt files

    _ , listyear = find_good(pa) # list of years for a specific company and type
    listyear = listyear[tick + "_" + typ] # we want only the list where the current typ and ticker is concerned
    
    file_names = []

    for year in listyear:
        y = str(year)
        if len(y) < 2:
            y = str(0) + y
        file_names.append(typ + "_" + tick + "_" + y)

    yearly_scores = {}
    for filen in file_names: # looping through all file names
        
        for key in topic_list:
            topic_dict[key] = 0 #reset count

        text = open(pathf + "/"+filen+".txt",encoding= 'utf-8') # opening file
        tokens = tokenize(text,nolist) # tokenising
        n = len(tokens)
        for word in tokens:
            for key in topic_dict.keys():
                if (word in model.index_to_key) and (key in model.index_to_key): #check if the word and the key are in the model vocabs
                    topic_dict[key] += model.similarity(word, key) / n
        
        values = list(topic_dict.values())
        score = sum(values) / len(values)
        yearly_scores.update({filen:score})


    return yearly_scores





def complete(score):
    """
    This function fills the gap in a streamline of years
    """

    score_keys = [key for key in score.keys()] # the list of keys
    
    base = score_keys[0][:-2] # getting the base of keys... ie. the DEF 14A_AAPL or 10-K_AMZN etc...
    
    first,last = int(score_keys[0][-2:]) , int(score_keys[-1][-2:]) # geting the time frame of the current score dict
    
    corr_key = [score_keys[0][:-2]+str(i) for i in range(first,last+1)] # comparing it to the correct time frame
    # by correct it is meant the true time frame without missing years


    # fiding the missing key:
    missing_key = None

    for key in corr_key: # looping through the correct time frame
        if key not in score_keys: #if a specific year is not in score's time frame we  mark it
            missing_key = key
    
    if missing_key == None: #if the document is not missing any date
        return score # return the original
    
    else:

        before= base + str(int(missing_key[-2:])-1) # the key of the year before
        after = base + str(int(missing_key[-2:])+1) # the key of the year after
        missing_val = 0.5*(score[before] + score[after]) # the average
        score.update({missing_key:missing_val}) # updating the orginal score

        comp = dict(sorted(score.items())) # sorting them increasingly ... later for plotting
        
        return comp







def merge_w2v(score_10K,score_proxy,wP,wK):
    """
    merges 10-K scores and Proxy scores given specific weights
    """
    
    s10_K = complete(score_10K) # checking for no missing years
    sproxy = complete(score_proxy)


    s10keys = [key for key in s10_K.keys()] # getting all keys
    baseK = s10keys[0][:-2] # the base of the key
    s10start ,s10end = s10keys[0][-2:] , s10keys[-1][-2:] # time frame of the 10-K score 

    ticker = baseK.split("_")[1] # getting the ticker for the return dictionary

    proxykeys = [key for key in sproxy.keys()] # same procedure for Proxy Statments
    baseP = proxykeys[0][:-2] 
    proxystart , proxyend = proxykeys[0][-2:] , proxykeys[-1][-2:]

    start = max(int(s10start),int(proxystart)) # truncating the max of begining time frames
    end = min(int(s10end),int(proxyend)) # and the min of the ending time frames
    
    merged = {} # return dictionary
    for i in range(start, end+1):
        value = wK*s10_K[baseK+str(i)] + wP*sproxy[baseP+str(i)] # weighted sum of each score
        key = ticker + "_" + str(i) # the key
        merged.update({key:value}) # updating the dictionary
    
    
    return merged


def plotting(merger):

    X = [int("20"+str(i[0][-2:])) for i in merger.items()]
    Y = [i[1] for i in merger.items()]

    return X , Y