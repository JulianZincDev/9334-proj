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
from src.RandomInterarrivalsIterator import RandomInterarrivalsIterator
from src.RandomServiceTimesIterator import RandomServiceTimesIterator

def write_output(mrt_string, dep_string, s):
    out_folder = 'output'
    mrt_file = os.path.join(out_folder,'mrt_'+s+'.txt')
    with open(mrt_file,'w') as file:
        file.writelines(mrt_string)

    dep_file = os.path.join(out_folder,'dep_'+s+'.txt')
    with open(dep_file,'w') as file:
        file.writelines(dep_string)

def main(s):
    # Open the config file service_*.txt to obtain the 
    # maximum number of sub-jobs per job
    config_folder = 'config'
    service_file = os.path.join(config_folder,'service_'+s+'.txt')
    
    service_times = np.loadtxt(service_file)

    para_file = os.path.join(config_folder, 'para_'+s+'.txt')
    paras = np.loadtxt(para_file)


    mode_file = os.path.join(config_folder, 'mode_'+s+'.txt')
    mode = ''
    with open(mode_file, 'r') as modes_file:
        mode = modes_file.readline().strip()
    
    n = paras[0]
    h = paras[1]


    interarrival_file = os.path.join(config_folder, 'interarrival_'+s+'.txt')
    if (mode == 'random'):
        time_end = paras[2]
        with open(interarrival_file) as ia_file:
            # If the mode is random, get all the different relevant arguments from all the files
            lam, a2l, a2u = ia_file.readline().strip().split(' ')
            ps = np.array(ia_file.readline().strip().split(' '), dtype=np.float64)
            [mu, alph] = np.loadtxt(service_file)

            # Use the appropriate values to create an Interarrivals iterator/iterable,
            # that just continually randomly generates the next interarrival time (until time_end is surpassed)
            interarrival_times = RandomInterarrivalsIterator(
                np.float64(lam), np.float64(a2l),
                np.float64(a2u), np.float64(time_end))
            
            # Use the appropriate values to create a ServiceTime iterator/iterable,
            # that just cotinually randomly generates lists of service times (randomly generates the number of subjobs
            # and then randomly generates that many service times and provides them to an array.)
            service_times = RandomServiceTimesIterator(
                np.float64(mu), np.float64(alph), ps)

            # Then provide the iterators inplace of pre-determined interarrival_times and service_times, then the sim
            # function will loop over these iterators randomly generating the interarrivals and service times as it goes
            mrt_string, dep_string = sim(n, h, interarrival_times, service_times)
            write_output(mrt_string, dep_string, s)
        
        return
    
    interarrival_times = np.loadtxt(interarrival_file)

    mrt_string, dep_string = sim(n, h, interarrival_times, service_times)
    write_output(mrt_string, dep_string, s)


    
if __name__ == "__main__":
    main(sys.argv[1])