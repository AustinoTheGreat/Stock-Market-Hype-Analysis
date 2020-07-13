import praw
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import yfinance as yf
import re

from ftplib import FTP
import csv

filename = "nasdaqlisted.txt"
ftp = FTP('ftp.nasdaqtrader.com')
print("Welcome: ", ftp.getwelcome())
ftp.login()
ftp.cwd('/symboldirectory/')
ftp.retrbinary("RETR " + filename, open(filename, "wb").write)
ftp.quit

with open(filename) as f:
    content = f.readlines()

content = [x.split("|", 1)[0] for x in content]
content.pop(0)
content.remove("HUGE")
content.remove("AMCIW")
content.remove("ROSEW")
content.remove("KBLMW")

class stock:
  def __init__(self, ticker, r, averageDailyVolume10Day, volume, fiftyDayAverage, ask, open, dayLow, dayHigh):
    self.ticker = ticker
    self.r = r
    self.averageDailyVolume10Day = averageDailyVolume10Day
    self.volume = volume
    self.fiftyDayAverage = fiftyDayAverage
    self.ask = ask
    self.open = open
    self.dayLow = dayLow
    self.dayHigh = dayHigh

pennys = []
existingPennys = ""



# Rurl = ["https://api.pushshift.io/reddit/search/submission/?subreddit=pennystocks&after=1d&before=0d&limit=1000",
#         "https://api.pushshift.io/reddit/search/submission/?subreddit=pennystocks&after=2d&before=1d&limit=1000",
#         "https://api.pushshift.io/reddit/search/submission/?subreddit=pennystocks&after=3d&before=2d&limit=1000",
#         "https://api.pushshift.io/reddit/search/submission/?subreddit=pennystocks&after=4d&before=3d&limit=1000",
#         "https://api.pushshift.io/reddit/search/submission/?subreddit=pennystocks&after=5d&before=4d&limit=1000",
#         "https://api.pushshift.io/reddit/search/submission/?subreddit=pennystocks&after=6d&before=5d&limit=1000",
#         "https://api.pushshift.io/reddit/search/submission/?subreddit=pennystocks&after=7d&before=6d&limit=1000"]

Rurl = ["https://api.pushshift.io/reddit/search/submission/?subreddit=pennystocks&after=1d&before=0d&limit=1000"]

for u in Rurl:
    r = requests.get(u)
    data = r.json()
    # data["data"][0]["title"]
    print(u)
    for i in range(0, len(data["data"])):
        for x in content:
            if re.search(rf"(\b(?=\w)|$){x}\b(?!\w)", data["data"][i]["title"], re.IGNORECASE):
            # if r"[$]|^|\s" + x.lower() + r"$|\s" in data["data"][i]["title"].lower():
                if x in existingPennys:
                    for y in pennys:
                        if x == y.ticker:
                            y.r = y.r + 1
                            break
                else:
                    existingPennys = existingPennys + " " + x
                    cur = yf.Ticker(x)
                    print(x)
                    print(i)
                    if cur.info["dayLow"] < 7:
                        pennys.append(stock(x, 1, cur.info["averageDailyVolume10Day"], cur.info["volume"], 
                            cur.info["fiftyDayAverage"], cur.info["ask"], cur.info["open"], cur.info["dayLow"], 
                            cur.info["dayHigh"]))
                    print("a")

for x in pennys:
    print(x.ticker + ": " + str(x.r))

with open('data.csv', mode='w') as dataFile:
    dataFileWriter = csv.writer(dataFile)
    dataFileWriter.writerow(["Ticker", "Pennystocks Mentions", "averageDailyVolume10Day", "volume", "fiftyDayAverage", "ask", "open", "dayLow", "dayHigh"])

    for x in pennys:
        dataFileWriter.writerow([x.ticker, x.r, x.averageDailyVolume10Day, x.volume, x.fiftyDayAverage, x.ask, x.open, x.dayLow, x.dayHigh])





# for i in range(1, len(content)):
#     print(content[i])
#     Rurl = "https://api.pushshift.io/reddit/search/submission/?q=" + content[i] + "&subreddit=pennystocks&after=1d&before=0d&limit=5000"
#     r = requests.get(Rurl)
#     data = r.json()
#     if (len(data["data"]) > 0):
#         cur = yf.Ticker(content[i])
#         pennys.append(stock(content[i], len(data["data"]), cur.info["averageDailyVolume10Day"], cur.info["volume"], 
#         cur.info["fiftyDayAverage"], cur.info["ask"], cur.info["open"], cur.info["dayLow"], 
#         cur.info["dayHigh"]))
# print(pennys)



# content.pop(0)
# for i in range(0, 10):
#     print(content[i])

#reddit = praw.Reddit(client_id='zlO7ERl3_9rQeg', client_secret='71fDz7-Bw8KhyxnystcSNHRRWgw', user_agent='pennystocks scrapping')
# contentAll = ""

# for i in range(1, len(content)):
#     contentAll = contentAll + " " + content[i]

# data = yf.download(  # or pdr.get_data_yahoo(...
#     # tickers list or string as well
#     tickers = "AAPL MSFT",

#     # use "period" instead of start/end
#     # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
#     # (optional, default is '1mo')
#     period = "1mo",

#     # fetch data by interval (including intraday if period < 60 days)
#     # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#     # (optional, default is '1d')
#     interval = "1d",

#     # group by ticker (to access via data['SPY'])
#     # (optional, default is 'column')
#     group_by = 'ticker',

#     # adjust all OHLC automatically
#     # (optional, default is False)
#     auto_adjust = True,

#     # download pre/post regular market hours data
#     # (optional, default is False)
#     prepost = True,

#     # use threads for mass downloading? (True/False/Integer)
#     # (optional, default is True)
#     threads = True,

#     # proxy URL scheme use use when downloading?
#     # (optional, default is None)
#     proxy = None
# )
# print(data)


# Rurl = "https://api.pushshift.io/reddit/search/submission/?q=IDEX&subreddit=pennystocks&after=1d&before=0d&limit=5000"
# r = requests.get(Rurl)
# data = r.json()
# print(len(data["data"]))

# First time set up the data file
# dataFile = open("data.csv", "w")
# writer = csv.writer(dataFile)
# for x in content:
#     writer.writerow([x])


