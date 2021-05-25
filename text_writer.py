from sys import path
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bsoup 
import os, re
from selection import *
#from SP500_companies import get_ticker

if not os.path.isdir(os.getcwd().replace('\\', '/') +'/Top 40/statements'):
    os.makedirs(os.getcwd().replace('\\', '/') +'/Top 40/statements')

def writingtxt(pathf,ticker,typ,save_path):

    filing_code = pathf.split('/')

    year = re.findall(r'\d+',filing_code[-2])[1] # extracts the year in the filing code name, e.g. 0001193125-17-310951

    file_name = save_path + "/"  + typ + "_" + ticker.upper() + "_" +  str(year) + ".txt"
    print(file_name)
    
    raw_html = open(pathf,encoding = 'utf-8') # opening the html given the path

    soup = bsoup(raw_html, 'lxml')# decoding the html

    ltables = soup.find_all('table') # locating the tables

    for table in ltables: # removing the table

        table.decompose()
    
    new_text_file = open(file_name, "w+", encoding = 'utf-8') #opening a new .txt file with filename

    new_text_file.write(soup.text) # writing the text of the report in the .txt file

    new_text_file.close()

def findhtml(pathused,ticker,types): # function that finds all html files in given path

    for tick in ticker:

        for typ in types:

            curr_path = pathused + "/" + tick.upper() + "/" + typ # sec-edgar-filings ==> AAPL ==> 10-K 
           
            for root, dirs, files in os.walk(curr_path): # os.walk returns all  files inside  directory (with absolute path r); f is list of  files in folder
            
                if 'filing-details.html' in files: # if filing.html (SEC-edgar convention to name html files) is in this folder 

                    pathfol = root.replace("\\","/") 

                    html_path = pathfol + '/filing-details.html'

                    save_path = pathused + '/statements'

                    writingtxt(html_path,tick,typ,save_path)

                else:
                     continue

pa = os.getcwd().replace('\\', '/') +'/Top 40'
tickers,years_for_each = find_good(pa)
types = ["10-K","DEF 14A"]

findhtml(pa,tickers,types)



