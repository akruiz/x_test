from selenium import webdriver
from bs4 import BeautifulSoup
import os
import pandas as pd
import time
import numpy as np

# load data for columns
driver = webdriver.Chrome('C:/Users/212775461/Documents/TPS/App Framework Repository/test/chromedriver')
sites_data = driver.get("https://te-data-test.herokuapp.com/api/sites?token=RUFTVEVSIEVHRyAjIDMuLi4KCnlvdXIgc2ljaw")
content_site = driver.page_source
soup_site = BeautifulSoup(content_site, features="html.parser")
find_site_text = soup_site.find('html').text
# formatting
d = find_site_text[find_site_text.find("[")+1:find_site_text.find("]")]

# get sites for link
sites=[]
for a in d.split(","):
    a = a.replace('"', '')
    sites.append(a)

df= pd.DataFrame([])
df_site = pd.DataFrame([])
# run every minute
starttime = time.time()
while True:
    print("tick")
    #load power data
    for s in sites:
        power_data = driver.get(
          "https://te-data-test.herokuapp.com/api/signals?token=RUFTVEVSIEVHRyAjIDMuLi4KCnlvdXIgc2ljaw&site={}".format(s))
        content_power = driver.page_source
        soup_power = BeautifulSoup(content_power, features="html.parser")
        find_power_txt = soup_power.find('html').text
        data = pd.read_json(find_power_txt)
        data['data_name'] = data.index
        if 'SITE_SM_solarInstPower' in data['data_name']:
            if data['site'][1] in sites:
                df = df.append([data])
    (print('data append'))
    df.to_csv('all_data.csv')
    time.sleep(50.0 - ((time.time() - starttime) % 50.0)) # reducing to 50 second to make up for next few lines for detection

    # PART 3: start setting up for 24 hour detection
    for i in df.site.unique():
        df_power = df[df.site == i]
        df_power = df_power.loc[df_power.data_name == 'SITE_SM_solarInstPower']
        if len(df_power) <= 24:
            condition = (df_power['signals'] < 0)
            df_power['Anomaly'] = np.where(condition, 'Yes', 'No')
            if 'Yes' in df_power['Anomaly'].tail(1440):
                print(i)
                print(df_power['timestamp'][0]) # print results for 24 hour anomaly detection