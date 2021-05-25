from sys import path
from sec_edgar_downloader import Downloader
import os, re
import numpy as np

"""
if not os.path.isdir(os.getcwd().replace('\\', '/') +'/sec-edgar-filings'):
    os.makedirs(os.getcwd().replace('\\', '/') +'/sec-edgar-filings')

def exec(pa,tickers,types):
    
    dl = Downloader() # the SEC_edgar_downloader package  

    for typ in types: # looping over different types        

        for tick in tickers: 

            dl.get(typ, tick, amount = 10, download_details=True)

        assert os.path.isdir(pa),'Wrong File Directory Check Again' # assert the SEC edgar folder is created 
"""
pa = os.getcwd().replace("\\","/") + "/Top 40"
types = ['10-K', 'DEF 14A']

tickers = ["AAPL","MSFT","AMZN","GOOGL","FB","TSLA",
        "JNJ","WMT","JPM","MA","PG",
        "UNH","NVDA","DIS","HD","PYPL","BAC","VZ","CMCSA",
        "ADBE","NFLX","KO","NKE","MRK","T","PFE","PEP","CRM",
        "INTC","ORCL","ABT","CSCO","ABBV","TMO","AVGO","XOM","QCOM","TMUS"]

def find_good(pa):
    good_ones = []
    all_years = {}
    years = []
    tick = None
    typ = None

    maximlength = max([len(r.replace("\\","/").split("/")) for r,d,f in os.walk(pa)])

    for root, dirs, files in os.walk(pa):
        filing_code = root.replace("\\","/").split('/')
        
        if len(filing_code) == maximlength:
            tick = filing_code[-3]
            
            typ = filing_code[-2]
            
            year = filing_code[-1].split('-')[1]
            
            years.append(int(year))
        else:
            y = np.array(years)
            y.sort()
            y = np.unique(y)
            if len(y) >= 10:
                good_ones.append(tick)
                all_years.update({tick + '_' + typ : y})
            years = []
    doubles = []
    for l in tickers:
        numbers = good_ones.count(l)
        if numbers == 2:
            doubles.append(l)

    return doubles, all_years

#to_keep_tick, to_keep_years = find_good(pa)
