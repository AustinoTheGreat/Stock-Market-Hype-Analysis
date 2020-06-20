import praw
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

from ftplib import FTP

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
for i in range(0, 10):
    print(content[i])

#reddit = praw.Reddit(client_id='zlO7ERl3_9rQeg', client_secret='71fDz7-Bw8KhyxnystcSNHRRWgw', user_agent='pennystocks scrapping')

Rurl = "https://api.pushshift.io/reddit/search/submission/?q=IDEX&subreddit=pennystocks&after=1d&before=0d&limit=1"
r = requests.get(Rurl)
data = r.json()
print(data)


# hot_posts = reddit.subreddit('pennystocks').hot(limit=10)
# for post in hot_posts:
#     print(post.title)
