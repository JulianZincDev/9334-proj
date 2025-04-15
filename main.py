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
from src.random_sim import random_sim

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

        with open(interarrival_file) as ia_file:
            lam, a2l, a2u = ia_file.readline().strip().split(' ')
            ps = np.array(ia_file.readline().strip().split(' '), dtype=np.float64)
            J = len(ps)

            [mu, alph] = np.loadtxt(service_file)

            random_sim(np.float64(lam), np.float64(a2l), np.float64(a2u), ps, np.float64(mu), np.float64(alph))

            # print(f'lam: {lam}, a2l: {a2l}, a2u: {a2u}\nps: {" ".join([p for p in ps])}\nJ: {J}\nmu: {mu}, alph: {alph}')
        
        return
    
    interarrival_times = np.loadtxt(interarrival_file)

    mrt_string, dep_string = sim(n, h, interarrival_times, service_times)


    

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