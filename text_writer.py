import numpy as np
from bs4 import BeautifulSoup as bsoup 
import os, re
from selection import *

if not os.path.isdir(os.getcwd().replace('\\', '/') +'/Top 40/statements'):
    os.makedirs(os.getcwd().replace('\\', '/') +'/Top 40/statements')

def tokenize(text, sw):
    """
    This function tokenizes the given text in a list of single words
    ============================================================================================
    Input:
    ------
    text: file object, path to opened txt file with encoding ='utf-8'
    sw: list, list of stop words
    Output:
    -------
    filtered: list, list of words presents in the input text
    """
    
    #get lines from text
    lines = text.readlines() 

    #tokenize text
    clr = []
    for i in lines:
        
        if ' ' in i:
            clr.append(i)
        else:
            continue
    final_list = []
    
    if len(clr) <= 10:
        index = 0
        for i,line in enumerate(clr):
            if len(line) > 10000:
                index = i
        final_list = clr[index].split(' ')
    else:
        for l in clr:
            final_list += l.replace('\n',' ').split(' ')
<<<<<<< HEAD
    
    fl = np.array(final_list).squeeze()
    filtered = []
    
    for word in fl:
=======

    #fl = np.array(final_list).squeeze()
    filtered = []
    for word in final_list:
>>>>>>> 261ccd6852fd01662bb45067e8c618aad279bc5b
        if word.lower() in sw or len(word)>25 or not word.isalpha():
            continue
        else:
            filtered.append(word.lower())
    
    return filtered    

def writingtxt(pathf,ticker,typ,save_path):
    """
    This function eliminates all the html code from the file and writes it into a text file.
    ============================================================================================
    Input:
    ------
    pathf: the path where the html file is located.
    ticker: the ticker of the company that.
    typ: the type, i.e. 10-K or DEF 14A proxy.
    save_path: the path where the final text file should be saved.    

    Output:
    -------
    None. 
    """
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
    """
    This function locates the html and calls the writingtext function for further process.
    ============================================================================================
    Input:
    ------
    pathused: the path of the directory that is being used.
    ticker: the ticker of the company. 
    types: the types, i.e. 10-K or DEF 14A proxy.

    Output:
    -------
    None.
    """
    for tick in ticker:
        print(tick)
        for typ in types:

            curr_path = pathused + "/" + tick.upper() + "/" + typ # sec-edgar-filings ==> AAPL ==> 10-K 
           
            for root, dirs, files in os.walk(curr_path): # os.walk returns all  files inside  directory (with absolute path r); f is list of  files in folder
                print(files)
                if 'filing-details.html' in files: # if filing.html (SEC-edgar convention to name html files) is in this folder 
                    
                    pathfol = root.replace("\\","/") 
                    print(pathfol)
                    html_path = pathfol + '/filing-details.html'

                    save_path = pathused + '/statements'

                    writingtxt(html_path,tick,typ,save_path)

                else:
                     continue

# Setting the path where all the needed files are located.
pa = os.getcwd().replace('\\', '/') +'/Top 40'




