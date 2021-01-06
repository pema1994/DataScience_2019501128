#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:01:37 2021

@author: pemawangmo
"""

import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

import os




csv_files = []
path = '/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/daily/'
directory = os.path.join(path)
for root,dirs,files in os.walk(directory):
    for file in files:
        csv_files.append(file)


com_name=[]

for file in csv_files:
    com_name.append(str(file).split(".")[0])
 
#print(com_name)


def correlationMatrix():
    daily_gain = pd.read_csv('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/daily_gain.csv')
    #columns= ['daily_gain']
    #
    corrMatrix = daily_gain.corr()   
    #print(corrMatrix)
    sn.heatmap(corrMatrix, annot=True,vmin = -1, vmax = 1, center = 0, cmap=['red','blue'])
    #ax.set_xticklabels( com_name, rotation=90)
    #ax.set_yticklabels( com_name, rotation=0)

    plt.show()
    
    weekly_gain = pd.read_csv('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/weekly_gain.csv')
    #columns= ['weekly_gain']
    
    corrMatrix = weekly_gain.corr()     
    sn.heatmap(corrMatrix, annot=True, vmin = -1, vmax = 1, center = 0,cmap=['red','blue'])
    plt.show()
    
    monthly_gain = pd.read_csv('/Users/pemawangmo/Desktop/DS_Notes/DADV/dadv_exam/monthly_gain.csv')
    #columns= ['monthly_gain']
    
    corrMatrix = monthly_gain.corr()  
    
    sn.heatmap(corrMatrix, annot=True, vmin = -1, vmax = 1, center = 0,cmap=['red','blue'])
    plt.show()
    
correlationMatrix()



