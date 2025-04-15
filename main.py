#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program reads in an input, triples it and then writes the result
to a file.   
"""

import sys 
import os
import numpy as np
from src.sim import sim

def main(s):
    

    # Open the config file service_*.txt to obtain the 
    # maximum number of sub-jobs per job
    config_folder = 'config'
    service_file = os.path.join(config_folder,'service_'+s+'.txt')
    
    service_times = np.loadtxt(service_file)

    para_file = os.path.join(config_folder, 'para_'+s+'.txt')
    paras = np.loadtxt(para_file)

    interarrival_file = os.path.join(config_folder, 'interarrival_'+s+'.txt')
    interarrival_times = np.loadtxt(interarrival_file)

    mrt_string, dep_string = sim(paras[0], paras[1], interarrival_times, service_times)


    # Maximum number of sub-jobs per job
    J = service_times.shape[1]
    

    out_folder = 'output'
    mrt_file = os.path.join(out_folder,'mrt_'+s+'.txt')
    with open(mrt_file,'w') as file:
        file.writelines(mrt_string)

    out_folder = 'output'
    dep_file = os.path.join(out_folder,'dep_'+s+'.txt')
    with open(dep_file,'w') as file:
        file.writelines(dep_string)

    
if __name__ == "__main__":
   main(sys.argv[1])