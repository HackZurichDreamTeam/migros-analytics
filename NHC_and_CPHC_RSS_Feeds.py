#%%
# import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
NewsFeed = feedparser.parse("https://www.nhc.noaa.gov/gtwo.xml")
df_news_feed=pd.json_normalize(NewsFeed.entries)

#%%
##I started with the tropical cyclones data from: https://www.nhc.noaa.gov/aboutrss.shtml
df_news_feed.link

for link in df_news_feed.link:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())
    html = list(soup.children)[2]
    text = soup.find(class_="textbackground")
    print(text)