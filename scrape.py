import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

#!pip install webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from convert_to_coord import convert_to_coord

#get driver start
def scrapeWeather():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://severeweather.wmo.int/v2/list.html") #This is a dummy website URL
    try:
        elem = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "dataTables_scrollBody")) #This is a dummy element
    )
    finally:
        print('loaded')
        driver.find_element_by_xpath("//select/option[@value='60']").click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    """Scraper getting each row"""
    all = soup.findAll("tbody")[2]
    row = all.findAll('tr')

    rest_info = []

    for i in row:
        infos_row = i.findAll('td')
        for index,j in enumerate(infos_row):
            info = None
            if index == 0:
                info = j.find('span')
                event = info.text

            if index == 4:
                info = j.find('span')
                areas = info.text

            if index == 1:
                #issued time
                issued_time = j.text
            if index == 3:
                country = j.text

            if index == 5:
                regions = j.text

            if index == 2:
                continue
        #append to list for dataframe
        rest_info.append([event,issued_time,country,areas,regions,datetime.today().strftime('%Y-%m-%d %H:%M')])

    df = pd.DataFrame(rest_info, columns = ['Event_type','Issued_time','Country','Areas','Regions','Date'])
    df['Issued_time'] = df["Issued_time"].apply(lambda x: x.split("#")[0])
    df['coordinates'] = convert_to_coord(df['Regions'] +", "+ df["Areas"] + ", " + df["Country"])
    df.to_csv("scraped_weather.csv",mode='a', index=False,header=False)
    return