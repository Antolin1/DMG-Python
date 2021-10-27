#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 12:11:23 2021

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

def getSolver(generator):
    if (generator == 'viatra'):
        return 'ViatraSolver'
    elif (generator == 'alloy'):
        return 'AlloySolver'

# add alloy, viatra option and number of samples option
def main():
    
    parser = ArgumentParser(description='Script for generate modes using KDE+randomInstantiator')


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
    
    
    
    parser.add_argument("-ps", "--pathsyn", dest="path_syn",
                        help="output folder.", metavar="DIR", 
                        required=True)
    
    parser.add_argument("-p", "--plot", dest="plot", choices=['True', 'False'],
                        required=False, default="True",
                        help="if plot distributions.")
    
    
    args = parser.parse_args()
    
    dataset_path = args.path_dataset
    dataset = args.dataset
    backend = args.emf
    samples = args.number_models
    save_path = args.path_syn
    msetObject = datasets_supported[dataset]
    plot = (args.plot == 'True') #bool(args.plot)
    
    
    train_path = dataset_path + '/train'
    test_path = dataset_path + '/test'
    graphs_train = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(train_path + "/*")]
    graphs_test = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(test_path + "/*")]
    
    numberObjects = np.array([[len([n for n in G])] for G in graphs_train])
    #degObjects =  np.array([[np.mean([G.out_degree(n) for n in G])] for G in graphs_train])
    #concat = np.concatenate((numberObjects, degObjects), axis = 1)
    #print(numberObjects.shape)
    
    kernel_std = improved_sheather_jones(numberObjects)  # Shape (obs, dims)

    resampled_data = np.random.choice(numberObjects.flatten(),
                                      size=samples, replace=True)
    resampled_data = resampled_data + np.random.randn(samples) * kernel_std
    
    rounded = []
    lower, upper = msetObject.bounds
    #delete upperbound and lowerbound
    for i,n in enumerate(resampled_data):
        candidate = int(round(n))
        if candidate < lower or candidate > upper:
            continue
        subprocess.call(['java', '-jar', 'java/randomInstantiator/instantiate.jar', 
                     '-m',msetObject.pathsSynMeta[0],
                    '-f','-n','1','-s',str(candidate),'-o',
                     save_path+'/'+str(i),
                    '-e',str(i)])
        rounded.append(candidate)
    
    if plot:
        line_labels = ['Syn', 'Train', 'Test']
        fig, axs = plt.subplots(ncols=2)
        l1 = sns.histplot(rounded, stat = 'density', ax=axs[0], color = 'red', label = 'Syn')
        l2 = sns.histplot(np.array([len([n for n in G]) 
                               for G in graphs_train]), stat = 'density', ax=axs[0],
                     color = 'blue',  label = 'Train')
        l3 = sns.histplot(np.array([len([n for n in G]) 
                               for G in graphs_test]), stat = 'density', ax=axs[0],
                     color = 'green',  label = 'Test')
        l4 = sns.distplot(rounded, hist=False, kde=True, 
                color = 'red', label = 'Syn', ax=axs[1])
        l5 = sns.distplot(np.array([len([n for n in G]) 
                               for G in graphs_train]), hist=False, kde=True, 
                color = 'blue', label = 'Train', ax=axs[1])
        l6 = sns.distplot(np.array([len([n for n in G]) 
                               for G in graphs_test]), hist=False, kde=True, 
                color = 'green', label = 'Test', ax=axs[1])
        fig.legend([l1, l2, l3, l4, l5, l6],     # The line objects
           labels=line_labels,   # The labels for each line
           loc="center right",   # Position of legend
           borderaxespad=0.1    # Small spacing around legend box
           )
        #plt.title('Graph statistics')
        plt.show()
if __name__ == "__main__":
    main()

