#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 10:57:34 2021

@author: Jose Antonio
"""


import sys
import os
import glob
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'/scripts/')

import warnings
warnings.filterwarnings('ignore')


from dmg.deeplearning.generativeModel import GenerativeModel
from dmg.deeplearning.generativeModel import sampleGraph
from networkx.algorithms.isomorphism import is_isomorphic
from dmg.model2graph.shapes import (getShapesDP, 
                                    internalDiversityShapes, computeMD, 
                                    getCategoricalDistribution)
import dmg.graphUtils as gu
import dmg.realism.metrics as mt
import torch
import numpy as np
import random
from scipy.stats import wasserstein_distance
import time
from c2st_gnn import C2ST_GNN
from argparse import ArgumentParser
from modelSet import datasets_supported
import seaborn as sns
import matplotlib.pyplot as plt
import multiprocess as mp
from scipy.stats import mannwhitneyu, linregress
from dmg.realism.emd import compute_mmd, gaussian_emd
import networkx as nx
import math
from pathlib import Path
#import lmfit


torch.manual_seed(123)
random.seed(123)
np.random.seed(123)

import pandas as pd

def getTime(pathStats):
    df = pd.read_csv(pathStats)
    columns = list(df.columns)
    columns_time = [c for c in columns if 'time' in c.lower()]
    columns_time = ['Solver time']
    return np.sum(df[columns_time].values)

def main():
    
    #parser
    parser = ArgumentParser(description='Script for evaluating the generator')

    parser.add_argument("-m", "--model", dest="model",
                        help="path to the model file.", metavar="FILE", 
                        required=True)
    parser.add_argument("-d", "--dataset", dest="dataset", 
                        choices=['ecore-github', 'rds-genmymodel', 
                                 'yakindu-github','yakindu-exercise'], 
                        help="dataset considered.",
                        required=True)
    parser.add_argument("-hi", "--hidden", dest="hidden_dim", type=int, 
                        required=False, default=128,
                        help="hidden dim of the nn size.")
    parser.add_argument("-ms", "--maxSize", dest="maxSize",
                        help="max size of the output models", type=int,
                        required=True)
    parser.add_argument("-nm", "--numberModels", dest="number_models",
                        help="number of models to generate.", type=int, default = 500)
    parser.add_argument("-ps", "--pathsyn", dest="path_syn",
                        help="Path of stats.", metavar="DIR", 
                        required=True)
    parser.add_argument("-emf", "--emf_backend", dest="emf",
                        choices=['python', 'java'],
                        help="backend to parse the models.",
                        required=True)
    
    #parse args
    args = parser.parse_args()
    dataset = args.dataset
    model_path = args.model
    hidden_dim = args.hidden_dim
    max_size = args.maxSize
    number_models = args.number_models
    save_path = args.path_syn
    backend = args.emf

    msetObject = datasets_supported[dataset]
    
    times_baseline = []
    lens_baseline = []
    for root, subFolder, files in os.walk(save_path):
        for item in files:
            if item.endswith(".xmi") :
                fileNamePath = str(os.path.join(root,item))
                path = Path(fileNamePath)    
                statsFile = str(path.parent.parent.absolute()) + '/stats.csv'
                time_ms = getTime(statsFile)/1000.
                #print(fileNamePath)
                G = msetObject.getGraphSyn(fileNamePath,backend)
                times_baseline.append([len(G), time_ms])
                lens_baseline.append(len(G))
    
    times_baseline = np.array(times_baseline)
    
    #load generative model
    model = GenerativeModel(hidden_dim, msetObject.dic_nodes, 
                        msetObject.dic_edges, 
                        msetObject.operations)
    checkpoint = torch.load(model_path,map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    times = []
    lens = []
    for k in range(number_models):
        start_time = time.monotonic()
        G = sampleGraph(msetObject.pallete.initialGraphs[0], 
                           msetObject.pallete, model, 
                           max_size, msetObject.pallete.separator)
        duration = time.monotonic() - start_time
        times.append([len(G),duration])
        lens.append(len(G))
        if k%100 == 0:
            print('Generated',k+1)
    #print(times)
    times = np.array(times)
    #linregress
    slope, intercept, r, p, se = linregress(np.log10(times[:,0]),np.log10(times[:,1]))
    print('Slope', slope)
    print('Intercept', intercept)
    print('R^2',r**2)
    
    slope_v, intercept_v, r_v, p_v, se_v = linregress(times_baseline[:,0],np.log10(times_baseline[:,1]))
    print('Slope', slope_v)
    print('Intercept', intercept_v)
    print('R^2',r_v**2)
    
    minn = np.min(lens + lens_baseline)
    maxx = np.max(lens + lens_baseline)
    domain = np.array(list(range(minn,maxx)))
    plot2 = plt.figure(2)
    ax = plt.gca()
    ax.scatter(times[:,0],times[:,1])
    ax.scatter(times_baseline[:,0], times_baseline[:,1], color = 'green')
    plt.plot(domain, np.power(domain,slope) * (10**intercept), color='red')
    plt.plot(domain, np.power(10, domain * slope_v) * (10**intercept_v), color='red')
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlabel('Number of elements')
    ax.set_ylabel('Time (seconds)')
    #ax.set_title('Log-Log plot of the p')
    plt.show()
    
# =============================================================================
#     minn = np.min(lens)
#     maxx = np.max(lens)
#     plot2 = plt.figure(3)
#     ax = plt.gca()
#     ax.scatter(times[:,0],times[:,1])
#     ax.scatter(times_baseline[:,0], times_baseline[:,1], color = 'green')
#     #plt.plot(list(range(minn,maxx)), np.power(np.array(list(range(minn,maxx))),slope) * (math.e**intercept), color='red')
#     ax.set_xlabel('Number of elements')
#     ax.set_ylabel('Time (seconds)')
#     plt.show()
#     
#     plot2 = plt.figure(3)
#     ax = plt.gca()
#     ax.scatter(times[:,0],times[:,1])
#     ax.scatter(times_baseline[:,0], times_baseline[:,1], color = 'green')
#     #plt.plot(times[:,0], np.power(times[:,0],slope) * (math.e**intercept), color='red')
#     ax.set_yscale('log')
#     #ax.set_xscale('log')
#     ax.set_xlabel('Number of elements')
#     ax.set_ylabel('Time (seconds)')
#     #ax.set_title('Log-Log plot of the p')
#     plt.show()
# =============================================================================

if __name__ == "__main__":
    main()