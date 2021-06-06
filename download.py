from sec_edgar_downloader import Downloader
import os

# Defining the initial list of companies for which filings are downloaded
listticks = ["AAPL","MSFT","AMZN","GOOGL","FB","TSLA","BRK.A","V","JNJ","WMT","JPM","MA","PG","UNH","NVDA","DIS","HD","PYPL","BAC","VZ","CMCSA","ADBE","NFLX","KO","NKE","MRK","T","PFE","PEP","CRM","INTC","ORCL","ABT","CSCO","ABBV","TMO","AVGO","XOM","QCOM","TMUS"]

def download():
    """
    Function that downloads 10-K and DEF 14A proxy statements using the sec_edgar_downloader API.
    ==============================================================================================================

    Input:
    ------
    None    

    Output:
    ------
    HTML files for each company and each ticker and each type are stores in the respective directory as follows: one
    folder per ticker, which contains one folder per type. Each type folder again has a folder for the respective year which contains
    html files and full-submission text files (latter removed as not used)
    """

    # Setting the downloader and giving the directory where the 

    dl = Downloader(os.getcwd().replace("\\","/"))
    print(os.getcwd().replace("\\","/"))
    for tick in listticks:
        dl.get("10-K",tick, amount = 11,download_details=True)
        dl.get("DEF 14A",tick, amount = 11,download_details=True)

    # Deleting the text files that are not used 
    directory = os.getcwd().replace("\\","/")

    for root, dirs, files in os.walk(directory):
        if 'full-submission.txt' in files:
            direct = root.replace("\\","/")+"/full-submission.txt"
            os.remove(direct)
