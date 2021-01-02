#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 22:29:30 2020

@author: pemawangmo
"""

import matplotlib.pyplot as plt
import numpy as np

# create data
x = np.random.rand( 20 )
y = np.random.rand( 20 )
z = np.random.rand( 20 )
col = np.random.rand( 20 )

# Change global size varying with s
plt.scatter( x, y, s = z * 200, c = col )
plt.savefig( 'bubble_plot.svg', format="svg", dpi=96 )
plt.show()
plt.clf()