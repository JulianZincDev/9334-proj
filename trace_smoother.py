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
m = 3000    # number of data points in each simulation

test_number = sys.argv[1]
test_iteration_start = int(sys.argv[2])
test_iteration_end = int(sys.argv[3])
h = np.loadtxt(os.path.join('config', f'para_{test_number}.txt'))[1]

nsim = test_iteration_end - test_iteration_start + 1     # number of simulation
response_time_traces = np.zeros((nsim,m))

# load the traces 
for i in range(test_iteration_end - test_iteration_start):

    response_time_traces[i,:] = np.loadtxt(os.path.join('jrt_traces', f'jrts_{str(test_number)}-{str(i+test_iteration_start)}.txt'))[:m]

# Compute the mean over the all the replications
mt = np.mean(response_time_traces,axis = 0)

# smooth it out with different values of w
# vary the value of w here 
w = 50
mt_smooth = np.zeros((m-w,))

for i in range(m-w):
    if (i < w):
        mt_smooth[i] = np.mean(mt[:(2*i+1)])
    else:
        mt_smooth[i] = np.mean(mt[(i-w):(i+w)])

plt.plot(np.arange(m-w),mt_smooth)
plt.title('window size w = ' + str(w))
plt.savefig(f'response time plot: h={h}'+f', w={w}'+'.pdf')

