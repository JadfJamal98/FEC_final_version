from sys import path
import numpy as np
from bs4 import BeautifulSoup as bsoup 
from sec_edgar_downloader import Downloader

import os


########################

#NOT USED 

########################
def writingtxt(pathf,ticker,nb,typ):
    """
    This function takes location of the .html files, takes out the tables and html coding from the file, and writes only
    the text in .txt file
    ----------------------------------------------------------------------------------------------------
    Input:
    ------

    pathf: list, list of paths containing the approriate .html file to proccess
    ticker: string, the ticker of the Company whose report we are treating
    nb: int, no of reports treated for that company
    typ: string, the type of reports we are treating ex. 10-K or proxy (DEF 14A)

    Output:
    -------

    None
    """

    assert len(pathf) == nb, 'the number of issues does not match' # an assert to check that the number of paths parsed is equal nb
    
    
    filename = [typ+ticker.lower()+str(2020-i)+'.txt' for i in reversed(range(0,nb))] # loop to create list of filenames
    
    for p,n in zip(pathf,filename): # looping through files and filesname

        raw_html = open(p,encoding = 'utf-8') # opening the html given the path
    
        soup = bsoup(raw_html, 'lxml')# decoding the html

        ltables = soup.find_all('table') # locating the tables
    
        for z in ltables: # removing the table
            z.decompose()
        
        bla = open(n,"w+", encoding = 'utf-8') #opening a new .txt file with filename
        bla.write(soup.text) # writing the text of the report in the .txt file
        

    return None


def findhtml(pathused,ticker,typ):
    """
    This function given the directory of the folder will search for .html files, append and return the list containing these
    directories.
    ============================================================================================
    Input:
    ------
    pathused: string, path of the folder you we working in
    ticker: string, the ticker here is used as the name of folder in which SEC_edgar stores the files
    typ: string, type of folder we are searching for either 10-K or DEF 14A, also the way SEC_edgar stores the files
    
    Output:
    -------

    allfiles: list of directory of a specific type and company (ex AAPL 10-K) that will be used to data scrapping
    """

    allfiles = [] # initializing the return list
    pathused += "/"+ticker.upper()+"/"+typ # since SEC_edgar has a standard way to store files as its the Ticker and inside 
                                           # sec-edgar-filings ==> AAPL ==> 10-K 
    
    for r,d,f in os.walk(pathused): # os.walk will return all the files inside the directory (with absolute path)
                                    # r is the absolute path
                                    # f is list of files in the folders
        
        if 'filing-details.html' in f: # if filing.html (SEC-edgar convention to name html files) is in this folder 
            pathfol = r.replace("\\","/") # we modify it 
            allfiles.append(pathfol+'/filing-details.html') # we append the absolute path
        else:
            continue
    return allfiles #and return it


def exec(nb,tickers,pa,typ,First):
    """
    this function is to download and process all data and have an end product as a .txt file ready to use
    ========================================================================================================
    Input:
    ------

    nb = int, number of issuance required to download
    tickers: list, list of company's tickers to donwload and process
    pa: string, path of main directory
    typ: string, type of document 10-K or DEF 14A
    First: Boolean, if its the first time and you haven't downloaded all anythoing you put it as True
                    if you already have the Edgar folder and only need to convert .txt put it as False
    """
    dl = Downloader() # the SEC_edgar_downloader package
    if First: # if First == True
    # loading the data
        for t in tickers: # looping over all tickers
            dl.get(typ, t,amount=nb, download_details=True)

    assert os.path.isdir(pa),'Wrong File Directory Check Again' # assert the SEC edgar folder is created 

    # proccesing it
    for t in tickers:
        writingtxt(findhtml(pa,t,typ),t,nb,typ)

def import_data(nb, tickers, types, First = True):
    """
    This function downloads and pre-processes the request data from EDGAR database
    ============================================================================================
    Input:
    ------
    nb: int, number of years of data to download for each company
    tickers: list, list of the stock tickers for which the data is downloaded
    types: list, list of types of files downloaded from EDGAR database
    First: Boolean, if its the first time and you haven't downloaded all anythoing you put it as True
                    if you already have the Edgar folder and only need to convert .txt put it as False
    Output:
    -------
    """
    pa = os.getcwd().replace("\\","/") + "/sec-edgar-filings"
    for i in types: # looping over different types
        exec(nb,tickers,pa,i,First)


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
    if len(clr) == 1:
        final_list = clr[0].split(' ')
    else:
        for l in clr:
            final_list += l.replace('\n',' ').split(' ')

    fl = np.array(final_list).squeeze()
    filtered = []
    for word in fl:
        if word.lower() in sw or len(word)>25 or not word.isalpha():
            continue
        else:
            filtered.append(word.lower())
    
    return filtered
