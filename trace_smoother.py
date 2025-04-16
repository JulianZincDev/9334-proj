#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMP9334 Capacity Planning 

Revision Problem Week 5B, Q1, Part (a): Transient removal 
"""

import numpy as np 
import matplotlib.pyplot as plt 
import os
import sys

# Put the traces in a numpy array
nsim = 5     # number of simulation
m = 20000    # number of data points in each simulation
response_time_traces = np.zeros((nsim,m))

test_number = sys.argv[1]

# load the traces 
for i in range(5):

    response_time_traces[i,:] = np.loadtxt(os.path.join('jrt_traces', f'jrts_{str(test_number)}-{str(i+1)}.txt'))[:20000]

# Compute the mean over the 5 replications
mt = np.mean(response_time_traces,axis = 0)

# smooth it out with different values of w
# vary the value of w here 
w = 500
mt_smooth = np.zeros((m-w,))

for i in range(m-w):
    if (i < w):
        mt_smooth[i] = np.mean(mt[:(2*i+1)])
    else:
        mt_smooth[i] = np.mean(mt[(i-w):(i+w)])

plt.plot(np.arange(m-w),mt_smooth)
plt.title('window size w = ' + str(w))
plt.savefig('week05B_q1_a_'+str(w)+'.pdf')

