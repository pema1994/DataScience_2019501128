#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 09:50:10 2021

@author: pemawangmo
"""

import pandas as pd
from pandas import DataFrame
import seaborn as sn
import matplotlib.pyplot as plt

import glob


#QUESTION 2
    
def calculateGain(df):
    df_sorted = df.sort_values(by="Date",ascending=True).set_index("Date")
    df = df_sorted['Close']
    #print(df)
    return df.pct_change()
    


def dailyGain():
    gainers = {}

    for filename in glob.glob('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/daily/*.csv'):
        data_df = pd.read_csv(filename)
        
        data_df['Date']= pd.to_datetime(data_df['Date'])
        df4 = round(calculateGain(data_df), 2).tolist()
        
        gainers[filename[filename.rfind('/')+1:filename.find('.')]] = df4
    return gainers
    
def weeklyGain():
    gainers = {}

    for filename in glob.glob('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/weekly/*.csv'):
        data_df = pd.read_csv(filename)
        
        data_df['Date']= pd.to_datetime(data_df['Date'])
        df4 = round(calculateGain(data_df), 2).tolist()
        
        gainers[filename[filename.rfind('/')+1:filename.find('.')]] = df4
    return gainers


def monthlyGain():
    gainers = {}

    for filename in glob.glob('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/weekly/*.csv'):
        data_df = pd.read_csv(filename)
        
        data_df['Date']= pd.to_datetime(data_df['Date'])
        df4 = round(calculateGain(data_df), 2).tolist()
        
        gainers[filename[filename.rfind('/')+1:filename.find('.')]] = df4
    return gainers


daily_gainers  = dailyGain()

weekly_gainers = weeklyGain()

monthly_gainers = monthlyGain()
# 
 


# ############################QUESTION 4 #################################
def daily_plot():
    daily_gains = DataFrame()
    daily_gains = pd.DataFrame.from_dict(daily_gainers, orient='index')
        
   

    daily_tickers = daily_gains.index

    daily_avg = pd.DataFrame(daily_gains.mean(axis=1), index=daily_tickers)
    daily_avg.sort_values(by=0,ascending=False, inplace=True)
    
    top_5= daily_avg.head(5) #top 5
    top_index = top_5.index
    
    bottom_5 = daily_avg.tail(5) #bottom 5
    bottom_index = bottom_5.index
    
    com_read = pd.read_csv('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/companies.csv')
    
    sectors = com_read['sector']
    sectors.drop_duplicates(inplace=True)
    
    
    new_df = DataFrame()
    sec_list = []
    
    dict1_top = {}
    dict1_bottom = {}
    for c in top_index:
        new_df = com_read[(com_read['tickers'] == str(c)+"\n")]
        for s in sectors:
            val = new_df['sector'] == str(s)
           
            if (val.bool()):
                if s not in sec_list:
                    sec_list.append(s)
                if s not in dict1_top:
                    dict1_top[s] = 1
                else:
                    dict1_top[s]+=1
        
    #print(dict1_top)
    
    for c in bottom_index:
        new_df = com_read[(com_read['tickers'] == str(c)+"\n")]
        
        for s in sectors:
            val = new_df['sector'] == str(s)
           
            if (val.bool()):
                if s not in sec_list:
                    sec_list.append(s)
                if s not in dict1_bottom:
                    dict1_bottom[s] = 1
                else:
                    dict1_bottom[s]+=1
        
   # print(dict1_bottom)
    
    data = []
    for sc in sec_list:
        tmp = []
        tmp.append(sc)
        if sc in dict1_top:
            tmp.append(dict1_top[sc])
        else:
            tmp.append(0)
        if sc in dict1_bottom:
            tmp.append(dict1_bottom[sc])
        else:
            tmp.append(0)
        data.append(tmp)
    new2_df = pd.DataFrame(data,columns=['sectors','top5', 'bottom5'])
    idx = new2_df['sectors']
    new2_df.set_index('sectors', inplace=True)    
    ax = new2_df.plot.bar(rot=30)
    
    
    
    
def weekly_plot():
    weekly_gains = DataFrame()
    weekly_gains = pd.DataFrame.from_dict(weekly_gainers, orient='index')
        
   

    weekly_tickers = weekly_gains.index

    weekly_avg = pd.DataFrame(weekly_gains.mean(axis=1), index=weekly_tickers)
    weekly_avg.sort_values(by=0,ascending=False, inplace=True)
    
    top_5= weekly_avg.head(5) #top 5
    top_index = top_5.index
    
    bottom_5 = weekly_avg.tail(5) #bottom 5
    bottom_index = bottom_5.index
    
    com_read = pd.read_csv('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/companies.csv')
    
    sectors = com_read['sector']
    sectors.drop_duplicates(inplace=True)
    
    
    new_df = DataFrame()
    sec_list = []
    
    dict1_top = {}
    dict1_bottom = {}
    for c in top_index:
        new_df = com_read[(com_read['tickers'] == str(c)+"\n")]
        for s in sectors:
            val = new_df['sector'] == str(s)
           
            if (val.bool()):
                if s not in sec_list:
                    sec_list.append(s)
                if s not in dict1_top:
                    dict1_top[s] = 1
                else:
                    dict1_top[s]+=1
        
    #print(dict1_top)
    
    for c in bottom_index:
        new_df = com_read[(com_read['tickers'] == str(c)+"\n")]
        
        for s in sectors:
            val = new_df['sector'] == str(s)
           
            if (val.bool()):
                if s not in sec_list:
                    sec_list.append(s)
                if s not in dict1_bottom:
                    dict1_bottom[s] = 1
                else:
                    dict1_bottom[s]+=1
        
   # print(dict1_bottom)
    
    data = []
    for sc in sec_list:
        tmp = []
        tmp.append(sc)
        if sc in dict1_top:
            tmp.append(dict1_top[sc])
        else:
            tmp.append(0)
        if sc in dict1_bottom:
            tmp.append(dict1_bottom[sc])
        else:
            tmp.append(0)
        data.append(tmp)
    new2_df = pd.DataFrame(data,columns=['sectors','top5', 'bottom5'])
    idx = new2_df['sectors']
    new2_df.set_index('sectors', inplace=True)    
    ax = new2_df.plot.bar(rot=30)    


def monthly_plot():
    monthly_gains = DataFrame()
    monthly_gains = pd.DataFrame.from_dict(monthly_gainers, orient='index')
        
   

    monthly_tickers =  monthly_gains.index

    monthly_avg = pd.DataFrame(monthly_gains.mean(axis=1), index=monthly_tickers)
    monthly_avg.sort_values(by=0,ascending=False, inplace=True)
    
    top_5= monthly_avg.head(5) #top 5
    top_index = top_5.index
    
    bottom_5 = monthly_avg.tail(5) #bottom 5
    bottom_index = bottom_5.index
    
    com_read = pd.read_csv('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/companies.csv')
    
    sectors = com_read['sector']
    sectors.drop_duplicates(inplace=True)
    
    
    new_df = DataFrame()
    sec_list = []
    
    dict1_top = {}
    dict1_bottom = {}
    for c in top_index:
        new_df = com_read[(com_read['tickers'] == str(c)+"\n")]
        for s in sectors:
            val = new_df['sector'] == str(s)
           
            if (val.bool()):
                if s not in sec_list:
                    sec_list.append(s)
                if s not in dict1_top:
                    dict1_top[s] = 1
                else:
                    dict1_top[s]+=1
        
    #print(dict1_top)
    
    for c in bottom_index:
        new_df = com_read[(com_read['tickers'] == str(c)+"\n")]
        
        for s in sectors:
            val = new_df['sector'] == str(s)
           
            if (val.bool()):
                if s not in sec_list:
                    sec_list.append(s)
                if s not in dict1_bottom:
                    dict1_bottom[s] = 1
                else:
                    dict1_bottom[s]+=1
        
   # print(dict1_bottom)
    
    data = []
    for sc in sec_list:
        tmp = []
        tmp.append(sc)
        if sc in dict1_top:
            tmp.append(dict1_top[sc])
        else:
            tmp.append(0)
        if sc in dict1_bottom:
            tmp.append(dict1_bottom[sc])
        else:
            tmp.append(0)
        data.append(tmp)
    new2_df = pd.DataFrame(data,columns=['sectors','top5', 'bottom5'])
    idx = new2_df['sectors']
    new2_df.set_index('sectors', inplace=True)    
    ax = new2_df.plot.bar(rot=30) 




#daily_plot()
#weekly_plot()
monthly_plot()



    



