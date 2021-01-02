#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 09:41:13 2021

@author: pemawangmo
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time




# =============================================================================
# weekly = "https://finance.yahoo.com/quote/AAPL/history?period1=1387305000&period2=1545071400&interval=1wk&filter=history&frequency=1wk"
# monthly = "https://finance.yahoo.com/quote/AAPL/history?period1=1387305000&period2=1545071400&interval=1mo&filter=history&frequency=1mo"
# daily = "https://finance.yahoo.com/quote/"+ele+"/history?period1=1387305000&period2=1545071400&interval=1d&filter=history&frequency=1d"
# 
# =============================================================================

def scroll2(driver):
    arr = ["window.scrollTo(0,508);","window.scrollTo(0,3811.199951171875);","window.scrollTo(0,7573.60009765625);","window.scrollTo(0,11355.2001953125);","window.scrollTo(0,15122.400390625);","window.scrollTo(0,18894.400390625);","window.scrollTo(0,22667.19921875);","window.scrollTo(0,26431.19921875);","window.scrollTo(0,30195.19921875);","window.scrollTo(0,33976.80078125);","window.scrollTo(0,37733.6015625);","window.scrollTo(0,41507.19921875);","window.scrollTo(0,45293.6015625);"]
    
    for x in arr:
        print("scr: "+ x )
        driver.execute_script(x)

def scroll(driver):
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        print("scrolling")
        # Scroll down to bottom
        for _ in range(20):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height



option = webdriver.ChromeOptions()
option.add_argument("--incognito")
#browser = webdriver.Chrome("D:\chromedriver\chromedriver.exe")
data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
table = data[0]
#print(table.head())

sliced_table = table[1:]
#print(sliced_table)
#header = table.iloc[0]
#print(header)


#corrected_table = sliced_table.rename(columns=header)
#print(corrected_table)

tickers = sliced_table['Symbol'].tolist()
#print(tickers)
gics = sliced_table['GICS Sector'].tolist()
#print(gics)

gics[:10]
#print(gics)
companies_list = pd.concat([pd.DataFrame(tickers), pd.DataFrame(gics)], axis=1, sort=False)
#companies_list.to_csv("Company_gics.csv")
#print (tickers)

com_name = []
gain_daily = []
gain_weekly = []
gain_monthly = []

close_daily = []
close_weekly = []
close_monthly = []
gic=[]
i=0
for ele in tickers[:10]:
    print(i)
    print(ele)
    try:
        #day wise
        browser_driver_array = webdriver.Chrome(executable_path='/Users/pemawangmo/Desktop/DS_Notes/DADV/assignments/IMDB/chromedriver')
        browser_driver_array.get("https://finance.yahoo.com/quote/"+ele+"/history?period1=1387305000&period2=1545071400&interval=1d&filter=history&frequency=1d")
        titles_element = browser_driver_array.find_elements_by_xpath(".//span[@class='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)']")
        #scroll2(browser_driver_array)
        #browser_driver_array.execute_script("window.scrollTo(0,3811.199951171875);")
        #browser_driver_array.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        x = browser_driver_array.find_elements_by_xpath(".//tr[@class='BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)']")
        data = [y.text for y in x]
        
        data2 =  []
        
        for a in data:
            if "Dividend" not in a:
                data2.append(a)
        dates = [[z[:12]] for z in data2]
        data = [z[12:].strip().split(" ") for z in data2]

        result = pd.concat([pd.DataFrame(dates), pd.DataFrame(data)], axis=1, sort=False)
        result.columns = ["Date","Open", "High"	,"Low"	,"Close",	"Adj Close",	"Volume"]
        result.head(10)
        result.to_csv(ele + "_daily.csv")
        gain_daily.append((float(result['Close'][0]) - float(result['Close'][len(result)-1]))/len(result))
        close_daily.append(result['Close'])
        
        browser_driver_array.quit()


        #week wise
        browser_driver_array = webdriver.Chrome(executable_path='/Users/pemawangmo/Desktop/DS_Notes/DADV/assignments/IMDB/chromedriver')
        browser_driver_array.get("https://finance.yahoo.com/quote/"+ele+"/history?period1=1387305000&period2=1545071400&interval=1wk&filter=history&frequency=1wk")
        titles_element = browser_driver_array.find_elements_by_xpath(".//span[@class='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)']")
        #scroll2(browser_driver_array)
        #browser_driver_array.execute_script("window.scrollTo(0,3811.199951171875);")
        #browser_driver_array.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        x = browser_driver_array.find_elements_by_xpath(".//tr[@class='BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)']")
        data = [y.text for y in x]
        
        data2 =  []
        
        for a in data:
            if "Dividend" not in a:
                data2.append(a)
        dates = [[z[:12]] for z in data2]
        data = [z[12:].strip().split(" ") for z in data2]

        result = pd.concat([pd.DataFrame(dates), pd.DataFrame(data)], axis=1, sort=False)
        result.columns = ["Date","Open","	High"	,"Low"	,"Close",	"Adj Close",	"Volume"]
        result.head(10)
        gain_weekly.append((float(result['Close'][0]) - float(result['Close'][len(result)-1]))/len(result))
        close_weekly.append(result['Close'])
        result.to_csv(ele + "_weekly.csv")
        
        browser_driver_array.quit()



        #monthly wise
        browser_driver_array = webdriver.Chrome(executable_path='/Users/pemawangmo/Desktop/DS_Notes/DADV/assignments/IMDB/chromedriver')
        browser_driver_array.get("https://finance.yahoo.com/quote/"+ele+"/history?period1=1387305000&period2=1545071400&interval=1mo&filter=history&frequency=1mo")
        titles_element = browser_driver_array.find_elements_by_xpath(".//span[@class='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)']")
        #scroll2(browser_driver_array)
        #browser_driver_array.execute_script("window.scrollTo(0,3811.199951171875);")
        #browser_driver_array.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        x = browser_driver_array.find_elements_by_xpath(".//tr[@class='BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)']")
        data = [y.text for y in x]
        
        data2 =  []
        
        for a in data:
            if "Dividend" not in a:
                data2.append(a)
        dates = [[z[:12]] for z in data2]
        data = [z[12:].strip().split(" ") for z in data2]

        result = pd.concat([pd.DataFrame(dates), pd.DataFrame(data)], axis=1, sort=False)
        result.columns = ["Date","Open","	High"	,"Low"	,"Close",	"Adj Close",	"Volume"]
        result.head(10)
        result.to_csv(ele + "_monthly.csv")
        try:
            gain_monthly.append((float(result['Close'][0]) - float(result['Close'][len(result)-1]))/len(result))
        except:
            pass
        close_monthly.append(result['Close'])
        
        browser_driver_array.quit()

        com_name.append(ele)
        gic.append(gics[i])
        i=i+1
        time.sleep(2)
    except Exception as e:
        print(e)



comp = pd.DataFrame({'com_name': com_name,
                              'gic': gic,
                              'gain_daily' : gain_daily,
                                'gain_weekly' : gain_weekly,
                                
                                'close_daily' : close_daily,
                                'close_weekly' : close_weekly,
                                'close_monthly' : close_monthly})
'''
comp = pd.DataFrame({'com_name': com_name,
                              'gic': gic,
                              'gain_daily' : gain_daily,
                                'gain_weekly' : gain_weekly,
                                'gain_monthly' : gain_monthly,
                                
                                'close_daily' : close_daily,
                                'close_weekly' : close_weekly,
                                'close_monthly' : close_monthly})
'''    
comp.to_csv('gain_company.csv')  






  