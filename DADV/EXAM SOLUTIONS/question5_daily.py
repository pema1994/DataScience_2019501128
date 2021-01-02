#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 12:56:47 2021

@author: pemawangmo
"""

from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import os
from fpdf import FPDF
import numpy



my_path = os.path.abspath(__file__)
my_path = my_path.split("\\")
my_path = "\\".join(my_path[:-1])

#mypath = '/Users/pemawangmo/Desktop/DS_Notes/DADV/assignments/task4/sparklines/'


app = Flask(__name__)  
csv_files_weekly = []
path = '/Users/pemawangmo/Desktop/DS_Notes/DADV/FINAL_EXAM/datasets/'

directory = os.path.join(path)
for root,dirs,files in os.walk(directory):
    for file in files:
       if file.endswith("_daily.csv"):
           csv_files_weekly.append(file)



p =[]
for file in csv_files_weekly:
    data =  pd.read_csv(path+file, index_col=0, parse_dates=True)
    a =str(file).split("_")[0]
    b= (data['Close'][0] - data['Close'][len(data)-1])/data['Close'][len(data)-1]
    c = list(-(data['Close'].pct_change())[1:98])
    
    p.append([a,b,c])




final = sorted(p, key = lambda x: float(x[1]))






@app.route('/')
def first():
    max1 = final[len(final)-1][2]
    max2 = final[len(final)-2][2]
    
    min1 = final[0][2]
    min2 = final[1][2]
    
    corr1 = []
    corr2 = []
    corr3 = []
    corr4 = []
    for x in range(len(final)):
        corr1.append(numpy.corrcoef(max1, final[x][2])[0][1])
        corr2.append(numpy.corrcoef(max2, final[x][2])[0][1])
        corr3.append(numpy.corrcoef(min1, final[x][2])[0][1])
        corr4.append(numpy.corrcoef(min2, final[x][2])[0][1])
    
    
        
    high1 = corr1.index(min(corr1))
    high2 = corr2.index(min(corr2))
    high3 = corr3.index(min(corr3))
    high4 = corr4.index(min(corr4))
    
    
    #-----------------sparkline------------------#
    
    spark_path = '/Users/pemawangmo/Desktop/DS_Notes/DADV/FINAL_EXAM/'
    
    fig = plt.figure()
    ax1 = fig.add_subplot(411) # nrows, ncols, plot_number, top sparkline
    ax1.plot(final[len(final)-1][2], 'b-')
    ax1.axhline(c='grey', alpha=0.5)
    
    ax2 = fig.add_subplot(412, sharex=ax1) 
    ax2.plot(final[len(final)-2][2], 'g-')
    ax2.axhline(c='grey', alpha=0.5)
    
    ax3 = fig.add_subplot(413, sharex=ax1)
    ax3.plot(final[high1][2], 'y-')
    ax3.axhline(c='grey', alpha=0.5)
    
    ax4 = fig.add_subplot(414, sharex=ax1) # bottom sparkline
    ax4.plot(final[high2][2], 'r-')
    ax4.axhline(c='grey', alpha=0.5)
    
    
    for axes in [ax1, ax2, ax3, ax4]: # remove all borders
        plt.setp(axes.get_xticklabels(), visible=False)
        plt.setp(axes.get_yticklabels(), visible=False)
        plt.setp(axes.get_xticklines(), visible=False)
        plt.setp(axes.get_yticklines(), visible=False)
        plt.setp(axes.spines.values(), visible=False)
    
    # bottom sparkline
    plt.setp(ax4.get_xticklabels(), visible=True)
    plt.setp(ax4.get_xticklines(), visible=True)
    ax4.xaxis.tick_bottom() # but onlyt the lower x ticks not x ticks at the top
    
    plt.tight_layout()
    
    plt.savefig(spark_path + "spark_daily.png")

   
    #---------------------------------------------------#

    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 13.0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt= 'Sparklines', border=0)
    pdf.image(spark_path + 'spark_daily.png', x = None, y = None, w = 200, h = 150, type = '', link = '')
    pdf.output(spark_path+ 'sparkline_daily.pdf', 'F')

    
    return render_template('test.html', hist_url = 'spark_weekly.png')



if __name__ == "__main__":
    app.run(debug = True)
    
    
    