#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 09:50:10 2021

@author: pemawangmo
"""


import pandas as pd
from pandas import DataFrame
import glob


#QUESTION 2
    
def calculateGain(df):
    df_sorted = df.sort_values(by="Date",ascending=True).set_index("Date")
    df = df_sorted['Close']
    #print(df)
    return df.pct_change()
    


def dailyGain():
    gainers = []
    gain_df = DataFrame()

    for filename in glob.glob('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/daily/*.csv'):
        daily_data = pd.read_csv(filename)
        
        daily_data['Date']= pd.to_datetime(daily_data['Date'])
        gainers = round(calculateGain(daily_data), 2).tolist()
        
    gain_df = DataFrame(gainers, columns=['daily_gain'])
    gain_df.to_csv('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/daily_gain.csv')
    
def weeklyGain():
    gainers = []
    gain_df = DataFrame()
    
    for filename in glob.glob('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/weekly/*.csv'):
        daily_data = pd.read_csv(filename)
        
        daily_data['Date']= pd.to_datetime(daily_data['Date'])
        gainers = round(calculateGain(daily_data), 2).tolist()
                
    gain_df = DataFrame(gainers, columns=['weekly_gain'])
    gain_df.to_csv('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/weekly_gain.csv')


def monthlyGain():
    gainers = []
    gain_df = DataFrame()
    
    for filename in glob.glob('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/monthly/*.csv'):
        daily_data = pd.read_csv(filename)
        
        daily_data['Date']= pd.to_datetime(daily_data['Date'])
        gainers = round(calculateGain(daily_data), 2).tolist()
        
    gain_df = DataFrame(gainers, columns=['monthly_gain'])
    gain_df.to_csv('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/monthly_gain.csv')

dailyGain()
weeklyGain()
monthlyGain()




