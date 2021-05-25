from sec_edgar_downloader import Downloader
import os

listticks = ["AAPL","MSFT","AMZN","GOOGL","FB","TSLA","BRK.A","V","JNJ","WMT","JPM","MA","PG","UNH","NVDA","DIS","HD","PYPL","BAC","VZ","CMCSA","ADBE","NFLX","KO","NKE","MRK","T","PFE","PEP","CRM","INTC","ORCL","ABT","CSCO","ABBV","TMO","AVGO","XOM","QCOM","TMUS"]
listticks += ['WFC','BLK']
 
dl = Downloader(os.getcwd().replace("\\","/"))
print(os.getcwd().replace("\\","/"))
for tick in listticks:
    dl.get("10-K",tick, amount = 11,download_details=True)
    dl.get("DEF 14A",tick, amount = 11,download_details=True)

#%% 
# To delete all text files... reducing the size of the file
directory = os.getcwd().replace("\\","/")

for root, dirs, files in os.walk(directory):
    if 'full-submission.txt' in files:
        direct = root.replace("\\","/")+"/full-submission.txt"
        os.remove(direct)
