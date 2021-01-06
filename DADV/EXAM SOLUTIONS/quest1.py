#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 09:41:13 2021

@author: pemawangmo
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame


from selenium import webdriver
import time
import datetime



from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
    
from selenium.webdriver.chrome.options import Options




# =============================================================================
# weekly = "https://finance.yahoo.com/quote/AAPL/history?period1=1387305000&period2=1545071400&interval=1wk&filter=history&frequency=1wk"
# monthly = "https://finance.yahoo.com/quote/AAPL/history?period1=1387305000&period2=1545071400&interval=1mo&filter=history&frequency=1mo"
# daily = "https://finance.yahoo.com/quote/"+ele+"/history?period1=1387305000&period2=1545071400&interval=1d&filter=history&frequency=1d"
# 
# =============================================================================

#QUESTION1

#scrapes wikipedia page to get all tickers from s&p500 companies
companies = []

comp_df = DataFrame()
page = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find("table", id = "constituents")

rows = table.findAll('tr')
for row in rows:
    cols = row.findAll('td')
    if(len(cols) > 0):
        companies.append([cols[0].getText(), cols[3].getText()])
    #print(sp500)
    
comp_df = DataFrame(companies,columns=['tickers', 'sector'])

comp_df.to_csv("companies.csv")


#GET ALL THE DATA DAILY, WEEKLY AND MONTHLY

#start and end dates for historical data
start = datetime.datetime(2010, 1, 1)  # start date
end = datetime.datetime(2016, 12, 30) #end date

PATH = '/Users/pemawangmo/Desktop/DS_Notes/DADV/assignments/IMDB/chromedriver'

read_ticker = pd.read_csv("companies.csv")
comp_ticker = read_ticker['tickers']

for ticker in comp_ticker[:10]:
    
    #daily wise
    
    chromeOptions = Options()
    chromeOptions.add_experimental_option("prefs", {"download.default_directory": "/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/daily"})
    
    driver = webdriver.Chrome(executable_path = PATH, options = chromeOptions)
    
    url = "https://finance.yahoo.com/quote/"+ticker+"/history?period1="+str(int(time.mktime(start.timetuple())))+"&period2="+str(int(time.mktime(end.timetuple())))+"&interval=1d&filter=history&frequency=1d"
    
    driver.get(url)
    
    time.sleep(3)
    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    time.sleep(5)  
    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Col1-1-HistoricalDataTable-Proxy > section > div.Pt\(15px\) > div.C\(\$tertiaryColor\).Mt\(20px\).Mb\(15px\) > span.Fl\(end\).Pos\(r\).T\(-6px\) > a > span'))).click()
    time.sleep(10)
    
    driver.quit()
    
    #weekly wise
    
    chromeOptions = Options()
    chromeOptions.add_experimental_option("prefs", {"download.default_directory": "/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/weekly"})
    
    driver = webdriver.Chrome(executable_path = PATH, options = chromeOptions)
    
    url = "https://finance.yahoo.com/quote/"+ticker+"/history?period1="+str(int(time.mktime(start.timetuple())))+"&period2="+str(int(time.mktime(end.timetuple())))+"&interval=1wk&filter=history&frequency=1wk"
    
    driver.get(url)
    
    time.sleep(3)
    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    time.sleep(5)    
    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Col1-1-HistoricalDataTable-Proxy > section > div.Pt\(15px\) > div.C\(\$tertiaryColor\).Mt\(20px\).Mb\(15px\) > span.Fl\(end\).Pos\(r\).T\(-6px\) > a > span'))).click()
    time.sleep(10)
    
    driver.quit()
    
    
    #monthy wise
    chromeOptions = Options()
    chromeOptions.add_experimental_option("prefs", {"download.default_directory": "/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/monthly"})
    
    driver = webdriver.Chrome(executable_path = PATH, options = chromeOptions)
    
    url = "https://finance.yahoo.com/quote/"+ticker+"/history?period1="+str(int(time.mktime(start.timetuple())))+"&period2="+str(int(time.mktime(end.timetuple())))+"&interval=1mo&filter=history&frequency=1mo"
    
    driver.get(url)
    
    time.sleep(3)
    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    time.sleep(5)  
    
    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Col1-1-HistoricalDataTable-Proxy > section > div.Pt\(15px\) > div.C\(\$tertiaryColor\).Mt\(20px\).Mb\(15px\) > span.Fl\(end\).Pos\(r\).T\(-6px\) > a > span'))).click()
    time.sleep(10)
    
    driver.quit()
  
    time.sleep(2)
    




    
