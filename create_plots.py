import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os

def create_df(path, accum):

    score_file = pd.read_table(path)
    score_file = score_file.iloc[:,0].str.split(expand=True)
    score_file.columns = ['Year', 'Governance', 'Environmental', 'Social']

    if not accum:
        return score_file

    else:
        accum = []

        for i in score_file.index:
            accum.append((float(score_file.iloc[i,1]) + float(score_file.iloc[i,2]) + float(score_file.iloc[i,3])))

        score_file['accum'] = accum

        return score_file

def topic_sectors(path,sec_tickers,sec_names,topic_names, method):

    """
    Function that creates plots for each topic showing the average score of all sectors in that topic.
    ============================================================================================
    Inputs:
    file_path: the path of the directory where all the score_files are saved
    sec_tickers: list of list of tickers for each sector / dictionary with keys according to the sector
    method: bag of words or word2vec
    ------
    Output: 

    """

    for topic in topic_names:

        for sec,sec_name in zip(sec_tickers,sec_names):
            
            all_score = {}
            for i in range(10,22):
                all_score.update({str(i):0.0}) 

            min_year = '0'
            max_year = '100'

            for tick in sec:
                
                file_path = path + '/' + tick + '.txt'

                if os.path.exists(file_path):

                    score_file = create_df(file_path,accum=False)
                    years = score_file[['Year']].values.squeeze()

                    if int(min(years)) > int(min_year):
                        min_year = min(years)

                    if int(max(years)) < int(max_year):
                        max_year = max(years)

                    for year in years:
                        all_score[year] += float(score_file[score_file['Year'] == year][topic].values)
                else:
                    continue
            avg_score = []
            N = len(sec)
            
            for n in np.arange(int(min_year), int(max_year)+1):
                avg_score.append(all_score[str(n)]/N)
            
            
            plt.plot(np.arange(int(min_year), int(max_year)+1), avg_score, label = sec_name)
        

        plt.xlabel('Years')
        plt.ylabel('Average Score')
        plt.title('Sector scores from ' + method + ' for ' + topic)
        plt.legend()
        plt.show()

def total_sectors(path,sec_tickers,sec_names,method):
    
    """
    Function that creates plots for each topic showing the average score of all sectors in that topic.
    ============================================================================================
    Inputs:
    file_path: the path of the directory where all the score_files are saved
    sec_tickers: list of list of tickers for each sector / dictionary with keys according to the sector
    method: bag of words or word2vec
    ------
    Output: 

    """

    for sec,sec_name in zip(sec_tickers,sec_names):
        
        all_score = {}
        for i in range(10,22):
            all_score.update({str(i):0.0}) 

        min_year = '0'
        max_year = '100'

        for tick in sec:
            
            file_path = path + '/' + tick + '.txt'

            if os.path.exists(file_path):

                score_file = create_df(file_path, accum = True)
                years = score_file[['Year']].values.squeeze()

                if int(min(years)) > int(min_year):
                    min_year = min(years)

                if int(max(years)) < int(max_year):
                    max_year = max(years)

                for year in years:
                    all_score[year] += float(score_file[score_file['Year'] == year]['accum'].values)
            else:
                continue
        avg_score = []
        N = len(sec)
        
        for n in np.arange(int(min_year), int(max_year)+1):
            avg_score.append(all_score[str(n)]/N)
        
        
        plt.plot(np.arange(int(min_year), int(max_year)+1), avg_score, label = sec_name)
    
    plt.xlabel('Years')
    plt.ylabel('Average Score')
    plt.title('Total sector scores from ' + method)
    plt.legend()
    plt.show()

def sectors_companies(path,sec_tickers,sec_names, method):
    
    """
    Function that creates plots for each topic showing the average score of all sectors in that topic.
    ============================================================================================
    Inputs:
    file_path: the path of the directory where all the score_files are saved
    sec_tickers: list of list of tickers for each sector / dictionary with keys according to the sector
    method: bag of words or word2vec
    ------
    Output: 

    """

    for sec,sec_name in zip(sec_tickers,sec_names):
        
        for tick in sec:
            
            file_path = path + '/' + tick + '.txt'

            if os.path.exists(file_path):

                score_file = create_df(file_path,accum=True)
                years = score_file[['Year']].values.squeeze()

                min_year = int(min(years))
                max_year = int(max(years))

                plt.plot(np.arange(int(min_year), int(max_year)+1), score_file.accum.values, label = tick)

            else:
                continue
        
        plt.xlabel('Years')
        plt.ylabel('Total Score')
        plt.title('Company scores from ' + method + ' for ' + sec_name + ' sector')
        plt.legend()
        plt.show()


Tech = ['AAPL','MSFT','NVDA','ADBE','INTC','ORCL','QCOM']
Telecom = ['VZ','CSCO','NFLX','TMUS']
Banking = ['BLK','WFC']
Retail = ['AMZN','WMT','NKE','KO']
Health = ['UNH','ABT','MRK','PFE','TMO', 'JNJ']
sect = [Tech,Telecom,Banking,Retail,Health]
sec_names = ['Tech', 'Telecom', 'Banking', 'Retail', 'Health']
topic_names = ['Governance', 'Environmental', 'Social']
path = os.getcwd().replace('\\', '/') + '/score_files'


# Replace method by 'Word2Vec' if needed
topic_sectors(path, sect, sec_names, topic_names, 'Bag of Words')
total_sectors(path, sect, sec_names, 'Bag of Words')
sectors_companies(path, sect, sec_names, 'Bag of Words')