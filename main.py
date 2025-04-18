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

def write_output(mrt_string, dep_string, s, job_response_times = None):
    out_folder = 'output'
    jrt_num = sys.argv[2] if len(sys.argv) > 2 else '0'
    mrt_file = os.path.join(out_folder,'mrt_'+s+'.txt')
    with open(mrt_file,'w') as file:
        file.writelines(mrt_string)

    dep_file = os.path.join(out_folder,'dep_'+s+'.txt')
    with open(dep_file,'w') as file:
        file.writelines(dep_string)

    if job_response_times and len(sys.argv) > 2:
        jrt_file = os.path.join('jrt_traces', 'jrts_'+s+f'-{jrt_num}.txt')
        with open(jrt_file, 'w') as traces_file:
            traces_file.writelines([f'{str(jrt)}\n' for jrt in job_response_times])

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
            (mrt_string, dep_string), job_response_times = sim(n, h, interarrival_times, service_times, time_end)

            write_output(mrt_string, dep_string, s, job_response_times)
        
        return
    
    interarrival_times = np.loadtxt(interarrival_file)

    (mrt_string, dep_string), _ = sim(n, h, interarrival_times, service_times)
    write_output(mrt_string, dep_string, s)


    
if __name__ == "__main__":
    main(sys.argv[1])