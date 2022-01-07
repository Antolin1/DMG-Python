#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 16:48:37 2021

@author: Jose Antonio
"""


import sys
import os
import glob
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'/scripts/')

import warnings
warnings.filterwarnings('ignore')

import numpy as np
from KDEpy.bw_selection import improved_sheather_jones
import random
#from utils4scripts import getMetamodel, getPackage, getRoot
from argparse import ArgumentParser
from modelSet import datasets_supported
import seaborn as sns
import matplotlib.pyplot as plt
import subprocess

random.seed(1)
np.random.seed(1)
import pandas as pd


# add alloy, viatra option and number of samples option
def main():
    
    parser = ArgumentParser(description='Script for measure the time of randomInstantiator')


    parser.add_argument("-d", "--dataset", dest="dataset", 
                        choices=['ecore-github', 'rds-genmymodel', 
                                 'yakindu-github','yakindu-exercise'], 
                        help="dataset considered.",
                        required=True)
    parser.add_argument("-pd", "--pathdataset", dest="path_dataset",
                        help="folder of the dataset.", metavar="DIR", 
                        required=True)
    parser.add_argument("-emf", "--emf_backend", dest="emf",
                        choices=['python', 'java'],
                        help="backend to parse the models.",
                        required=True)
    
    parser.add_argument("-nm", "--numberModels", dest="number_models",
                        help="number of models to generate.", type=int, default = 600)
    
    args = parser.parse_args()
    dataset_path = args.path_dataset
    dataset = args.dataset
    backend = args.emf
    samples = args.number_models
    msetObject = datasets_supported[dataset]
    
    train_path = dataset_path + '/train'
    graphs_train = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(train_path + "/*")]

    
    numberObjects = np.array([[len([n for n in G])] for G in graphs_train])
    #degObjects =  np.array([[np.mean([G.out_degree(n) for n in G])] for G in graphs_train])
    #concat = np.concatenate((numberObjects, degObjects), axis = 1)
    #print(numberObjects.shape)
    
    kernel_std = improved_sheather_jones(numberObjects)  # Shape (obs, dims)

    resampled_data = np.random.choice(numberObjects.flatten(),
                                      size=samples, replace=True)
    resampled_data = resampled_data + np.random.randn(samples) * kernel_std
    
    rounded = []
    times = []
    lower, upper = msetObject.bounds
    #delete upperbound and lowerbound
    for i,n in enumerate(resampled_data):
        candidate = int(round(n))
        if candidate < lower or candidate > upper:
            continue
        print('Expected output size:', candidate)
        subprocess.call(['java', '-jar', 'java/randomInstantiator/instantiateStats.jar', 
                     '-m',msetObject.pathsSynMeta[0],
                    '-f','-n','2','-s',str(candidate),'-o',
                     '/tmp',
                    '-e',str(i),
                    '-k','/tmp/stats.csv','-p','0'])
        rounded.append(candidate)
        times.append(pd.read_csv('/tmp/stats.csv', names = ['size','time']).values[1,:])
    times = np.array(times)
    np.savetxt('stats/'+dataset+'/randomInstantiator/stats.csv',times, delimiter = ',')
    
if __name__ == "__main__":
    main()
