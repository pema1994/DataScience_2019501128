#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 22:48:10 2020

@author: pemawangmo
"""


import pandas as pd
import seaborn as sns



data =  pd.read_csv('/Users/pemawangmo/Desktop/DS_Notes/DADV/assignments/task3/rank_votes.csv')
final_data = data[data['numVotes'] >= 10000 ]


sns_plot  = sns.jointplot(x = final_data["averageRating"], y = final_data["numVotes"], kind = 'scatter')
sns_plot.savefig("scatterplot.svg")