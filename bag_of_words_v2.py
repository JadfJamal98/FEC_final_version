import numpy as np 
from collections import Counter
from Wordlist_Import import *
from Selection import *
from Text_Writer import *
import os

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

    all_wordsl = [word.lower() for word in all_words]
    
    return all_wordsl

def score_c_t(topic,tick,typ,nolist):
    """
    Function that computes the ESG-score using the bag-of-words method for a given company and type.
    ==============================================================================================================

    Input:
    ------
    topic: Environmental, Social or Governance.
    tick: the ticker of the company.
    typ: the type, 10-K or DEF 14A
    nolist: the list of words to not be considered when computing the score.

    Output:
    ------
    Final score as single value. 
    """
    
    listtop = get_words(topic) #list of words from a topic
    
    df_tick = {} 

    for word in listtop:
        df_tick.update({word: 0}) # dictionary with keys that are the words in the list
    
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
   
    for name in file_names: # looping through all file names
       
        text = open(pathf+"/"+name+".txt",encoding= 'utf-8') # opening
        tokens = tokenize(text,nolist) # tokenizing

        for key in df_tick.keys(): # looping through all words of the topic

            if key in tokens:
                df_tick[key]+=1 # if exist in the document, add 1
                df_tick

    N = len(listyear) # Total Number of Files
    
    w_idf = {} # initializing the weights of the inverse document frequency

    for key in df_tick.keys():

        if df_tick[key] == 0:

            continue # so remove non appearing words and to avoid dividing by 0

        else:

            w_idf.update({key: np.log(N/df_tick[key])}) # applying the formula
    
    score = {}

    for filen in file_names: # looping through all file names
        
        w = {} # the normal weight

        text = open(pathf + "/"+filen+".txt",encoding= 'utf-8') # opening file
        tokens = tokenize(text,nolist) # tokenising
        freq = Counter(tokens) # dictionary containing as keys the words of tokenisation and as values the frequency 
        sum = 0 
        for word in w_idf.keys(): # looping through the words were we got some w
            
            if freq[word] == 0: # if the freq is 0 to avoid log(0)
                continue
            
            else:
                w.update({word:max(0.0,1.0 + np.log(freq[word]) * w_idf[word])}) # updating with the correct weight
                sum += w[word] # adding to the sum
        
        a = len(tokens) #length of the document
        si = 1/(1+np.log(a))*sum # the score for that year
        score.update({filen:si}) # updating the dictionary

    return score

def complete(given):
    """
    This function fills the gap in a streamline of years
    """

    score = given # avoid calling the function multiple times

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

def merge(rep10K,Proxy,wP,wK):
    """
    merges 10-K scores and Proxy scores given specific weights
    """
    
    s10_K = complete(rep10K) # checking for no missing years
    sproxy = complete(Proxy)


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

""" def plotting(merger):

    X = [int("20"+str(i[0][-2:])) for i in merger.items()]
    Y = [i[1] for i in merger.items()]

    return X , Y

nonotext = open(os.getcwd().replace("\\","/") +"/nonosquare.txt","r",encoding='utf-8')
nonolist = nonotext.readlines()[0].split(" ")

ws = load_workbook(filename="ESG_word_list.xlsx")
sheetns = ws.sheetnames

Governance = importing(ws[sheetns[0]])

Environmental = importing(ws[sheetns[1]])

Social = importing(ws[sheetns[2]])

topics = [Governance, Environmental, Social]
topic_names = ['Governance', 'Environmental', 'Social']


rep10K = score_c_t(Environmental,"BAC","10-K",nonolist)
#Proxy = score_c_t(Environmental,"BAC","DEF 14A",nonolist)
#merger= merge(rep10K,Proxy,wP=0.5,wK=0.5)

 """