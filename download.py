from sec_edgar_downloader import Downloader
import os

#listticks = ["AAPL","MSFT","AMZN","GOOGL","FB","TSLA","BRK.A","V","JNJ","WMT","JPM","MA","PG","UNH","NVDA","DIS","HD","PYPL","BAC","VZ","CMCSA","ADBE","NFLX","KO","NKE","MRK","T","PFE","PEP","CRM","INTC","ORCL","ABT","CSCO","ABBV","TMO","AVGO","XOM","QCOM","TMUS"]
#listicks = ['C','BLK']
ll = 'WFC'
dl = Downloader(os.getcwd().replace("\\","/"))
#print(os.getcwd().replace("\\","/"))
#for tick in listicks:
dl.get("10-K",ll, amount = 11,download_details=True)
dl.get("DEF 14A",ll, amount = 11,download_details=True)

"""
directory = os.getcwd().replace("\\","/")

for root, dirs, files in os.walk(directory):
    if 'full-submission.txt' in files:
        direct = root.replace("\\","/")+"/full-submission.txt"
        os.remove(direct)
"""