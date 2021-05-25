from sys import path
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bsoup 
from sec_edgar_downloader import Downloader
import os, re

if not os.path.isdir(os.getcwd().replace('\\', '/') +'/sec-edgar-filings/statements'):
    os.makedirs(os.getcwd().replace('\\', '/') +'/sec-edgar-filings/statements')


def writingtxt(pathf,ticker,typ,save_path):

    filing_code = pathf.split('/')

    year = re.findall(r'\d+',filing_code[-2])[1] # extracts the year in the filing code name, e.g. 0001193125-17-310951

    file_name = save_path + '/'  + typ + '_' + ticker.upper() + '_' +  str(year) + '.txt'
    
    raw_html = open(pathf,encoding = 'utf-8') # opening the html given the path

    soup = bsoup(raw_html, 'lxml')# decoding the html

    ltables = soup.find_all('table') # locating the tables

    for table in ltables: # removing the table

        table.decompose()
    
    new_text_file = open(file_name,"w+", encoding = 'utf-8') #opening a new .txt file with filename

    new_text_file.write(soup.text) # writing the text of the report in the .txt file

def findhtml(pathused,ticker,types): # function that finds all html files in given path

    for tick in ticker:

        for typ in types:

            curr_path = pathused + "/" + tick.upper() + "/" + typ # sec-edgar-filings ==> AAPL ==> 10-K 
           
            for root, dirs, files in os.walk(curr_path): # os.walk returns all  files inside  directory (with absolute path r); f is list of  files in folder
            
                if 'filing-details.html' in files: # if filing.html (SEC-edgar convention to name html files) is in this folder 

                    pathfol = root.replace("\\","/") 

                    html_path = pathfol + '/filing-details.html'

                    save_path = pathused + '/sec-edgar-filings/statements'

                    writingtxt(html_path,tick,typ,save_path)

                else:
                    continue


def exec(nb,tickers,types):

    pa = os.getcwd().replace("\\","/") + "/sec-edgar-filings" # create the path where html and other files are saved

    dl = Downloader() # the SEC_edgar_downloader package  

    for typ in types: # looping over different types        

        for tick in tickers: 

            dl.get(typ, tick,amount=nb, download_details=True)

        assert os.path.isdir(pa),'Wrong File Directory Check Again' # assert the SEC edgar folder is created 


#payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
#first_table = payload[0]
#second_table = payload[1]
#df = first_table
#tickers = df.iloc[26:126,0].values
tickers = ['TSLA', 'GOOGL', 'MSFT', 'AMZN', 'A', 'GM', 'F', 'PYPL', 'JPM']
types = ["10-K","DEF 14A"]
nb = 10


pa = os.getcwd().replace("\\","/") + "/sec-edgar-filings"


#exec(nb,tickers,types)
findhtml(pa,tickers,types)




