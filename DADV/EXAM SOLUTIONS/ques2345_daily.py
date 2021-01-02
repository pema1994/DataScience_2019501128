#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 09:41:13 2021

@author: pemawangmo
"""



import os
import pandas as pd
import numpy


csv_files_daily = []
path = '/Users/pemawangmo/Desktop/DS_Notes/DADV/FINAL_EXAM/datasets/'

directory = os.path.join(path)
for root,dirs,files in os.walk(directory):
    for file in files:
       if file.endswith("_daily.csv"):
           csv_files_daily.append(file)


#-----daily gain---question2--------#
com_name=[]
gain = []
daily_gains = []
p =[]
for file in csv_files_daily:
    data =  pd.read_csv(path+file, index_col=0, parse_dates=True)
    a =str(file).split("_")[0]
    b= (data['Close'][0] - data['Close'][len(data)-1])/data['Close'][len(data)-1]
    c = list(-(data['Close'].pct_change())[1:98])
    com_name.append(str(file).split(".")[0])
    gain.append((data['Close'][0] - data['Close'][len(data)-1])/data['Close'][len(data)-1])
    daily_gains.append(list(-(data['Close'].pct_change())[1:98]))
    p.append([a,b,c])



#---find correlation----questin 3-----------------#

final = sorted(p, key = lambda x: float(x[1]))

final = final[:5] + final[5:]
pd.DataFrame(final).to_json("abcd.json")
corr = []
for x in range(len(final)):
    temp = []
    for y in range(len(final)):
        temp.append( numpy.corrcoef(final[x][2], final[y][2])[0][1])
    corr.append(temp)


#--plotting-------#



import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

# This dictionary defines the colormap
cdict = {'blue':  ((0.0, 0.0, 0.0),   # no red at 0
                  (0.5, 1.0, 1.0),   # all channels set to 1.0 at 0.5 to create white
                  (1.0, 0.8, 0.8)),  # set to 0.8 so its not too bright at 1

        'red': ((0.0, 0.8, 0.8),   # set to 0.8 so its not too bright at 0
                  (0.5, 1.0, 1.0),   # all channels set to 1.0 at 0.5 to create white
                  (1.0, 0.0, 0.0)),  # no green at 1

        'green':  ((0.0, 0.0, 0.0),   # no blue at 0
                  (0.5, 1.0, 1.0),   # all channels set to 1.0 at 0.5 to create white
                  (1.0, 0.0, 0.0))   # no blue at 1
       }

GnRdBe = colors.LinearSegmentedColormap('GnRdBe', cdict)
fig,ax = plt.subplots(1)
ax.set_xticklabels( com_name, rotation=90)
ax.set_yticklabels( com_name, rotation=0)
dummydata = corr
p=ax.pcolormesh(dummydata,cmap=GnRdBe,vmin=-1,vmax=1)
fig.colorbar(p,ax=ax)
plt.show()




#---------question4---------------------#

wiki =pd.read_csv(path+"company.csv", index_col=0, parse_dates=True)
d= {}
cc = wiki["com_name"]
gg = wiki["gic"]
for i in range(len(wiki)):
    d[cc[i]] = gg[i]


bar_dict = {}

final[0][0]

good_com = []
bad_com = []
cutoff = 5
i = 0
for x in final:
    if i < cutoff:
        bad_com.append(x[0])
    else:
        good_com.append(x[0])
    
    
    if x[0] in d.keys():
        
        if d[x[0]] in bar_dict.keys():
        
            bar_dict [ d[x[0]]].append(x[0])
        else:
            bar_dict [ d[x[0]]]= [x[0]]
    i+=1



import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import datetime

x = bar_dict.keys()

good_bar= []
bad_bar = []

for i in x:
    g_c=0
    b_c=0
    for k in bar_dict[i]:
        if k in good_com:
            g_c+=1
        elif k in bad_com:
            b_c+=1
    good_bar.append(g_c)
    bad_bar.append(b_c)






#------------bar plot-----------------#

import numpy as np
import matplotlib.pyplot as plt

N = 6
ind = np.arange(N)  # the x locations for the groups
width = 0.30       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)

yvals = bad_bar
rects1 = ax.bar(ind, yvals, width, color='r')
zvals = good_bar
rects2 = ax.bar(ind+width, zvals, width, color='g')
#kvals = [11,12,13]
#rects3 = ax.bar(ind+width*2, kvals, width, color='b')

ax.set_ylabel('Scores')
ax.set_xticks(ind+width)
ax.set_xticklabels( x, rotation=90)
ax.legend( (rects1[0], rects2[0]), ('Bottom 25', 'Top 25') )

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)


plt.show()





#------------question 5----------------------#

#finding the top2 max correlation

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

plt.show()

#--------------convert into pdf------------------#

from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_xy(0, 0)
pdf.set_font('arial', 'B', 13.0)
pdf.cell(ln=1, h=5.0, align='L', w=0, txt= 'Sparklines', border=0)
pdf.image(spark_path + 'spark_daily.png', x = None, y = None, w = 200, h = 150, type = '', link = '')
pdf.output(spark_path+ 'sparkline_daily.pdf', 'F')
