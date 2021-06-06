from sys import path
import os, re
import numpy as np

# Setting the respective directory
pa = os.getcwd().replace("\\","/") + "/Top 40"
types = ['10-K', 'DEF 14A']

# Again the tickers of all the companies that are initially obtained
tickers = ["AAPL","MSFT","AMZN","GOOGL","FB","TSLA",
        "JNJ","WMT","JPM","MA","PG",
        "UNH","NVDA","DIS","HD","PYPL","BAC","VZ","CMCSA",
        "ADBE","NFLX","KO","NKE","MRK","T","PFE","PEP",
        "INTC","ORCL","ABT","CSCO","ABBV","TMO","AVGO","XOM","QCOM","TMUS", 'WFC', 'BLK']

def find_good(pa):
    """
    Function that selects the companies (tickers) for which sufficient amount of data is available: 10 consecutive years.
    ==============================================================================================================

    Input:
    ------
    path = path where the file is that should be read in.

    Output:
    ------
    List of the unique list of tickers for which for both types enough data is available.
    Dictionary of the actual list of years that are available for each ticker and the respective type  for each ticker.
    """
    good_ones = []
    all_years = {}
    years = []
    tick = None
    typ = None

    # Setting the max lenght such that ticker, year and type can be located
    max_length = max([len(r.replace("\\","/").split("/")) for r,d,f in os.walk(pa)])

    for root, dirs, files in os.walk(pa):

        filing_code = root.replace("\\","/").split('/')

        if len(filing_code) == max_length:
            
            years = []

            tick = filing_code[-3]

            if tick not in tickers:
                continue

            typ = filing_code[-2]
            year = filing_code[-1].split('-')[1]
            years.append(int(year))

            name = tick + '_' + typ

            if name not in all_years.keys():
                all_years.update({name:years})

            else:
                all_years[name].append(int(year))

    pop_keys = []

    for key in all_years.keys():

        curr_years = np.array(all_years[key])
        uniqe_years = np.unique(curr_years)
        uniqe_years.sort()

        # Checking if enough years are there
        if len(uniqe_years) >= 10:
            good_tick = key.split('_')[0]
            good_ones.append(good_tick)
            all_years[key] = list(uniqe_years)

        else:
            pop_keys.append(key)
    
    for pop_key in pop_keys:
        all_years.pop(pop_key)

    # Returning the unique tickers as well as the actual years that we have
    return np.unique(good_ones), all_years
