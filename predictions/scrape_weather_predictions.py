import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys, os, json

# Set sys path to search first in the project root
project_root = sys.path[0]
while os.path.basename(project_root) != "data_science":
    project_root = os.path.dirname(project_root)
sys.path.insert(0, project_root)

os.chdir(project_root)

ggeocode = 'AIzaSyACn8ZsmhM9DjpK6MYUApfscEnQypC6LjY'

#location from google
def get_location_coordinates(location): # 4
    # pass for now
    # Define the base url
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={ggeocode}" # 6
    response = requests.get(geo_url) # 7
    content = response.content.decode("utf8") # 8
    geo_js = json.loads(content) # 9
    geo_status = geo_js["status"] # 10

    if geo_status == "OK": # 11
        geo_elements = geo_js["results"][0] # 12
        geometry = geo_elements["geometry"] # 13
        location_coordinates = geometry["location"] # 14
        location_lat = location_coordinates["lat"] # 15
        location_long = location_coordinates["lng"] # 16
        return (location_lat,location_long)
    else:
        return (None,None)

def get_tropical_cyclones_forcast():
    NewsFeed = feedparser.parse("https://www.nhc.noaa.gov/gtwo.xml")
    df_news_feed=pd.json_normalize(NewsFeed.entries)

    ##I started with the tropical cyclones data from: https://www.nhc.noaa.gov/aboutrss.shtml
    df_news_feed.link

    df_prediction = pd.DataFrame(columns = ['area','time_from_now (h)','likelihood (%)','information', 'geo_location'])
    for link in df_news_feed.link:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        html = list(soup.children)[2]
        text = soup.find(class_="textbackground")
        #print(text)
        output = text.string.split('\n')
        formation_info = []
        add_text = False
        for line in output:
            if line != "":
                if line[0].isdigit():
                    words = line.split()
                    if words[1] == "AM" or words[1] == "PM":
                        date = line
                    else:
                        last_loc = line[3:]
                        add_text = True 
                        text = ""
                if line[0]=="*":
                    add_text = False
                    formation_data = line
                    words = line.replace('.', ' ').split()
                    try:
                        i = words.index("days")
                        factor = 24
                    except:
                        i = words.index("hours")
                        factor = 1.0
                    predicted_time = int(words[i-1])*factor
                    percentage = int(words[-2])
                    if percentage >=20:
                        formation_info.append([last_loc, predicted_time, percentage, text])
                if add_text == True: 
                    text += line
            else:
                add_text = False
        df_pr = pd.DataFrame(formation_info, columns = ['area','time_from_now (h)','likelihood (%)','information'])
        df_pr["geo_location"] = df_pr["area"].apply(get_location_coordinates)
        df_prediction = pd.concat([df_prediction, df_pr], axis=0)
    df_prediction.to_csv("scraped_weather_predictions.csv",mode='a', index=False,header=True)

get_tropical_cyclones_forcast()
