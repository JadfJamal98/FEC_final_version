import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os
import seaborn as sns
sns.set()
from PIL import Image  
  
def create_df(path, bloomberg):
    """
    Function that creates a data frame from the file that is read from a path.
    ==============================================================================================================

    Input:
    ------
    path = path where the file is that should be read in.
    bloomberg = boolean whether or not the scores come from the Bloomberg file.

    Output:
    ------
    data frame with the computed scores as well as accumulated and indexed scores for all years. 
    """
    score_file = pd.read_table(path)
    score_file = score_file.iloc[:,0].str.split(expand=True)

    #Reading bloomberg file and dropping NA' as well as too early observations.
    if bloomberg:
        score_file.columns = ['Year', 'Environmental', 'Social', 'Governance', 'ESG_combined', 'ESG_controvesies', 'ESG_score']
        rows = score_file.shape[0]
        index = [0]
        for row in range(0,rows):
            curr_row = score_file.iloc[row,:].values
            if 'NA' in curr_row:
                index.append(score_file.index[row])
        score_file.drop(index,axis = 0,inplace = True)

        # Deleting the ESG combined and other not needed columns
        score_file.drop(['ESG_combined','ESG_controvesies'],axis=1,inplace=True)

    else:
        score_file.columns = ['Year', 'Governance', 'Environmental', 'Social']

        ESG_Score = []

        for i in range(score_file.shape[0]):
            ESG_Score.append((float(score_file.Environmental.values[i]) + float(score_file.Governance.values[i]) + float(score_file.Social.values[i])))

        score_file['ESG_score'] = ESG_Score

    # Getting indexed scores as well 
    indexed = []

    for i in range(score_file.shape[0]):
        indexed.append(float(score_file.ESG_score.values[i])/float(score_file.ESG_score.values[0]) - 1)

    score_file['indexed'] = indexed

    return score_file

def check_years(min_year, max_year, years):

    # Function that helps keeping track of which years can be used as some companies have more and some less years available

    if int(min(years)) > int(min_year):
        min_year = min(years)

    if int(max(years)) < int(max_year):
        max_year = max(years)

    return min_year, max_year

def topic_sectors(path, sec_tickers, sec_names, topic_names, method, bloomberg, total):

    """
    Function that creates plots for each topic showing the average score of all sectors in that topic.
    ============================================================================================
    Inputs:
    ------
    path: the path of the directory where all the score_files are saved
    sec_tickers: list of list of tickers for each sector / dictionary with keys according to the sector
    sec_names: the names of the sectors as strings.
    topic_names: the names of all topics as strings.
    method: bag of words or word2vec
    bloomberg: boolean, whether bloomberg scores should be used.
    total: boolean whether topic scores or total scores should be used.
    
    Output: 
    if #plt.show enabled -> graphs will be shown, otherwise saved into the current working directory.
    ------

    """
    # Taking the total score if boolean set to true
    if total:
        topic_names = ['ESG_score']

    for topic in topic_names:

        fig = plt.figure(figsize=(10,5))

        for sec,sec_name in zip(sec_tickers,sec_names):
            
            all_score = {}
            for i in range(10,22):
                all_score.update({str(i):0.0})

            min_year = '10'
            max_year = '21'

            for tick in sec:

                path_tick = path + tick + '.txt'

                if bloomberg:
                    scores = create_df(path_tick,bloomberg=True)
                    years = scores.Year.values

                else:
                    scores = create_df(path_tick,bloomberg=False)
                    years = scores.Year.values
                
                min_year, max_year = check_years(min_year,max_year,years)

                for year in years:
        
                    all_score[year] += float(scores[scores['Year'] == year][topic].values)

            avg_score = []
            N = len(sec)
            
            for n in range(int(min_year), int(max_year)+1):
                avg_score.append(all_score[str(n)]/N)
            
            plt.plot(np.arange(int(min_year), int(max_year)+1), avg_score, label = sec_name)
        

        plt.xlabel('Years')
        plt.ylabel('Score')
        plt.title('Scores for ' + topic + ' from ' + method)
        plt.legend()
        fig.savefig(topic + '_' + method + '.jpg', bbox_inches='tight', dpi=150)
        #plt.show()

def total_sectors(path, sec_tickers, sec_names):
    """
    Function that creates plots for each sector with the total scores.
    ============================================================================================
    Inputs:
    ------
    path: the path of the directory where all the score_files are saved
    sec_tickers: list of list of tickers for each sector / dictionary with keys according to the sector
    sec_names: the names of the sectors as strings.

    Output: 
    if #plt.show enabled -> graphs will be shown, otherwise saved into the current working directory.
    ------

    """
    for sec,sec_name in zip(sec_tickers,sec_names):

        # Creating a plot that will be saved later on.
        fig = plt.figure(figsize=(10,5))
        all_bow = {}
        for i in range(10,22):
            all_bow.update({str(i):0.0})

        all_bloom = {}
        for i in range(10,22):
            all_bloom.update({str(i):0.0}) 

        all_w2v = {}
        for i in range(10,22):
            all_w2v.update({str(i):0.0}) 

        min_year_bloom = '10'
        max_year_bloom = '21'
        min_year_bow = '10'
        max_year_bow = '21'
        min_year_w2v = '10'
        max_year_w2v = '21'

        for tick in sec:
            
            path_bloomberg = path + '/Bloomberg_Score/Bs_' + tick + '.txt'
            path_bow = path + '/score_files_bow/' + tick + '.txt'
            path_w2v = path + '/score_files_w2v/' + tick + '.txt'
            
            score_bloomberg = create_df(path_bloomberg,bloomberg=True)
            years_bloom = score_bloomberg.Year.values

            # Resetting the min and max years for bloomberg
            min_year_bloom, max_year_bloom = check_years(min_year_bloom,max_year_bloom,years_bloom)

            score_bow = create_df(path_bow,bloomberg=False)
            years_bow = score_bow.Year.values               
           
            # Resetting the min and max years for bag of words
            min_year_bow, max_year_bow = check_years(min_year_bow,max_year_bow,years_bow)

            score_w2v = create_df(path_w2v,bloomberg=False)
            years_w2v = score_w2v.Year.values 

            # Resetting the min and max years for word2vec
            min_year_w2v, max_year_w2v = check_years(min_year_w2v,max_year_w2v,years_w2v)
            
            for year in years_bloom:
                all_bloom[year] += float(score_bloomberg[score_bloomberg['Year'] == year]['ESG_score'].values)

            for year in years_bow:
                all_bow[year] += float(score_bow[score_bow['Year'] == year]['ESG_score'].values)

            for year in years_w2v:
                all_w2v[year] += float(score_w2v[score_w2v['Year'] == year]['ESG_score'].values)

        bloomberg = [ all_bloom[year]/len(sec) for year in years_bloom ]
        bow = [ all_bow[year]/len(sec) for year in years_bow ]
        w2v = [ all_w2v[year]/len(sec) for year in years_w2v ]
        
        # Re-indexing the total scores to make sure that all of them start at the correct date
        bloomberg_indexed = [i/bloomberg[0] - 1 for i in bloomberg]
        bow_indexed = [i/bow[0] - 1 for i in bow]
        w2v_indexed = [i/w2v[0] - 1 for i in w2v]

        plt.plot([int(i) for i in years_bloom], bloomberg_indexed, label = 'Bloomberg')
        plt.plot([int(i) for i in years_bow], bow_indexed, label = 'Bag of Words')
        plt.plot([int(i) for i in years_w2v], w2v_indexed, label = 'Word2Vec')
        
        plt.xlabel('Years')
        plt.ylabel('Score indexed')
        plt.title('Scores for ' + sec_name)
        plt.legend()
        fig.savefig(sec_name + '_indexed' + '.jpg', bbox_inches='tight', dpi=150)
        #plt.show()

def sectors_companies(path, sec_tickers, sec_names, method, bloomberg):
    """
    Function that creates plots for each sector with all companies and with the total scores.
    ============================================================================================
    Inputs:
    ------
    path: the path of the directory where all the score_files are saved
    sec_tickers: list of list of tickers for each sector / dictionary with keys according to the sector
    sec_names: the names of the sectors as strings.
    method: word2vec or bag of words
    bloomberg: boolean if also plots for the bloomberg values should be created.
    Output: 
    if #plt.show enabled -> graphs will be shown, otherwise saved into the current working directory.
    ------

    """

    for sec,sec_name in zip(sec_tickers,sec_names):

        fig = plt.figure(figsize=(10,5))

        for tick in sec:
            
            file_path = path + tick + '.txt'

            score_file = create_df(file_path, bloomberg)
            years = score_file.Year.values
            min_year = int(min(years))
            max_year = int(max(years))

            score_float = []
            for i in score_file.ESG_score.values:
                score_float.append(float(i))

            plt.plot(np.arange(int(min_year), int(max_year)+1), score_float, label = tick)
            
        plt.xlabel('Years')
        plt.ylabel('Total Score')
        plt.title('Company scores from ' + method + ' for ' + sec_name + ' sector')
        plt.legend()
        fig.savefig(sec_name + '_' + method + '.jpg', bbox_inches='tight', dpi=150)
        #plt.show()

# The list of tickers for which enough data was available
Tech = ['AAPL','MSFT','NVDA','ADBE','INTC','ORCL','QCOM']
Telecom = ['VZ','CSCO','NFLX','TMUS', 'CMCSA'] 
Banking = ['JPM','BAC'] 
Retail = ['AMZN','WMT','NKE', 'KO'] 
Health = ['UNH','ABT','MRK','PFE','TMO']
sect = [Tech,Telecom,Banking,Retail,Health]

sec_names = ['Tech', 'Telecom', 'Banking', 'Retail', 'Health']
topic_names = ['Governance', 'Environmental', 'Social']
path = os.getcwd().replace('\\', '/')

path_bow = os.getcwd().replace('\\', '/') + '/score_files_bow/'
path_w2v = os.getcwd().replace('\\', '/') + '/score_files_w2v/'
path_bloom = os.getcwd().replace('\\', '/') + '/Bloomberg_Score/Bs_'

# Creating all the plots
topic_sectors(path_bow,sect,sec_names,topic_names,'Bag of Words',bloomberg=False, total=False)
topic_sectors(path_w2v,sect,sec_names,topic_names,'Word2Vec',bloomberg=False, total=False)
topic_sectors(path_bloom,sect,sec_names,topic_names,'Bloomberg',bloomberg=True, total=False)

topic_sectors(path_bow,sect,sec_names,topic_names,'Bag of Words',bloomberg=False, total=True)
topic_sectors(path_w2v,sect,sec_names,topic_names,'Word2Vec',bloomberg=False, total=True)
topic_sectors(path_bloom,sect,sec_names,topic_names,'Bloomberg',bloomberg=True, total=True)

sectors_companies(path_bow,sect,sec_names,'Bag of Words',bloomberg=False)
sectors_companies(path_w2v,sect,sec_names,'Word2Vec',bloomberg=False)
sectors_companies(path_bloom,sect,sec_names,'Bloomberg',bloomberg=True)

total_sectors(path,sect,sec_names)

