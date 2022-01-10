#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 11:15:35 2022

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

def getTimeViatra(pathStats):
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
    # parser.add_argument("-ps", "--pathsyn", dest="path_syn",
    #                     help="Path of stats.", metavar="DIR", 
    #                     required=True)
    parser.add_argument("-emf", "--emf_backend", dest="emf",
                        choices=['python', 'java'],
                        help="backend to parse the models.",
                        required=True)
    parser.add_argument("-nm", "--numberModels", dest="number_models",
                        help="number of models to generate.", type=int, default = 500)
    parser.add_argument("-pd", "--pathdataset", dest="path_dataset",
                        help="folder of the dataset.", metavar="DIR", 
                        required=True)
    
    #parse args
    args = parser.parse_args()
    dataset = args.dataset
    model_path = args.model
    hidden_dim = args.hidden_dim
    max_size = args.maxSize
    dataset_path = args.path_dataset
    #save_path = args.path_syn
    backend = args.emf
    number_models = args.number_models

    msetObject = datasets_supported[dataset]
    
    
     # dmg
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
    times = np.array(times)
    lens_M2 = times[:,0]
    #viatra
    times_baseline = []

    for root, subFolder, files in os.walk('./stats/'+dataset+'/viatra/'):
        for item in files:
            if item.endswith(".xmi") :
                fileNamePath = str(os.path.join(root,item))
                path = Path(fileNamePath)    
                statsFile = str(path.parent.parent.absolute()) + '/stats.csv'
                time_ms = getTimeViatra(statsFile)/1000.
                #print(fileNamePath)
                G = msetObject.getGraphSyn(fileNamePath,backend)
                
                lower, upper = msetObject.bounds
                if len(G) < lower: #or len(G1) > upper:
                    continue
                
                times_baseline.append([len(G), time_ms])
                
    if len(times_baseline) > number_models:
        times_baseline = random.sample(times_baseline, number_models)
    times_baseline = np.array(times_baseline)
    lens_baseline = times_baseline[:,0]
    
    ## randomEMF
    df = pd.read_csv('./stats/'+dataset+'/randomEMF/stats.csv', names = ['size','time'])
    times_randomEMF = df.values
    new_times_randomEMF = []
    for r in times_randomEMF:
        lower, upper = msetObject.bounds
        if r[0]<lower:
            continue
        new_times_randomEMF.append((r[0],r[1]/1000.))
    
    if len(new_times_randomEMF) > number_models:
        times_randomEMF = random.sample(new_times_randomEMF, number_models)
    else:
        times_randomEMF = new_times_randomEMF
    
    times_randomEMF = np.array(times_randomEMF)
    lens_randomEMF = times_randomEMF[:,0]
    
    ##randomInstantiator
    df = pd.read_csv('./stats/'+dataset+'/randomInstantiator/stats.csv', names = ['size','time'])
    times_randomInstantiator = df.values
    new_times_randomInstantiator = []
    for r in times_randomInstantiator:
        lower, upper = msetObject.bounds
        if r[0]<lower:
            continue
        new_times_randomInstantiator.append((r[0],r[1]/1000.))
        
    if len(new_times_randomInstantiator) > number_models:
         times_randomInstantiator = random.sample(new_times_randomInstantiator, number_models)
    else:
         times_randomInstantiator = new_times_randomInstantiator
    times_randomInstantiator = np.array(times_randomInstantiator)
    lens_random = times_randomInstantiator[:,0]
    
    #train and test paths
    test_path = dataset_path + '/test'
    train_path = dataset_path + '/train'
    msetObject = datasets_supported[dataset]
    
    #load graphs
    graphs_test = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(test_path + "/*")]
    
    #match the bounds
    min_bound = int(np.min([len(G) for G in graphs_test]))
    max_bound = int(np.max([len(G) for G in graphs_test]))
    
    times = times[np.array([(row[0] <=max_bound) and (row[0]>=min_bound) for row in times])]
    times_randomInstantiator = times_randomInstantiator[np.array([(row[0] <=max_bound) and (row[0]>=min_bound) 
                                                                  for row in times_randomInstantiator])]
    times_randomEMF = times_randomEMF[np.array([(row[0] <=max_bound) and (row[0]>=min_bound) 
                                                                  for row in times_randomEMF])]
    times_baseline = times_baseline[np.array([(row[0] <=max_bound) and (row[0]>=min_bound) 
                                                                  for row in times_baseline])]
    
    #quantiles
    a1 = np.quantile(np.array(list(range(min_bound,max_bound + 1))),0.333)
    a2 = np.quantile(np.array(list(range(min_bound,max_bound + 1))),0.666)
    
    print('Q1',min_bound,a1)
    print('Q2',a1,a2)
    print('Q3',a2,max_bound)
    #print('Q4',a3,max_bound)
    
    times_q1 = times[np.array([(row[0] <=a1)for row in times])]
    times_q2 = times[np.array([(row[0] <=a2) and (row[0]>a1) for row in times])]
    times_q3 = times[np.array([(row[0] >a2)for row in times])]
    
    print('Q1 M2:',np.mean(times_q1[:,1]),'+-',np.std(times_q1[:,1]))
    print('Q2 M2:',np.mean(times_q2[:,1]),'+-',np.std(times_q2[:,1]))
    print('Q3 M2:',np.mean(times_q3[:,1]),'+-',np.std(times_q3[:,1]))
# =============================================================================
#     print('Q1 M2:',times_q1.shape)
#     print('Q2 M2:',times_q2.shape)
#     print('Q3 M2:',times_q3.shape)
# =============================================================================
    
    #print('Q4 M2:',np.mean(times_q4[:,1]),'+-',np.std(times_q4[:,1]))
    
    times_baseline_q1 = times_baseline[np.array([(row[0] <=a1)for row in times_baseline])]
    times_baseline_q2 = times_baseline[np.array([(row[0] <=a2) and (row[0]>a1) for row in times_baseline])]
    times_baseline_q3 = times_baseline[np.array([(row[0] >a2)for row in times_baseline])]
    
    print('Q1 VIATRA:',np.mean(times_baseline_q1[:,1]),'+-',np.std(times_baseline_q1[:,1]))
    print('Q2 VIATRA:',np.mean(times_baseline_q2[:,1]),'+-',np.std(times_baseline_q2[:,1]))
    print('Q3 VIATRA:',np.mean(times_baseline_q3[:,1]),'+-',np.std(times_baseline_q3[:,1]))
# =============================================================================
#     print('Q1 VIATRA:',times_baseline_q1.shape)
#     print('Q2 VIATRA:',times_baseline_q2.shape)
#     print('Q3 VIATRA:',times_baseline_q3.shape)
# =============================================================================
    #print('Q4 VIATRA:',np.mean(times_baseline_q4[:,1]),'+-',np.std(times_baseline_q4[:,1]))
    
    times_randomInstantiator_q1 = times_randomInstantiator[np.array([(row[0] <=a1)for row in times_randomInstantiator])]
    times_randomInstantiator_q2 = times_randomInstantiator[np.array([(row[0] <=a2) and (row[0]>a1) for row in times_randomInstantiator])]
    times_randomInstantiator_q3 = times_randomInstantiator[np.array([(row[0] >a2)for row in times_randomInstantiator])]
    #times_randomInstantiator_q4 = times_randomInstantiator[np.array([(row[0] >a3)for row in times_randomInstantiator])]
    
    print('Q1 random:',np.mean(times_randomInstantiator_q1[:,1]),'+-',np.std(times_randomInstantiator_q1[:,1]))
    print('Q2 random:',np.mean(times_randomInstantiator_q2[:,1]),'+-',np.std(times_randomInstantiator_q2[:,1]))
    print('Q3 random:',np.mean(times_randomInstantiator_q3[:,1]),'+-',np.std(times_randomInstantiator_q3[:,1]))
# =============================================================================
#     print('Q1 random:',times_randomInstantiator_q1.shape)
#     print('Q2 random:',times_randomInstantiator_q2.shape)
#     print('Q3 random:',times_randomInstantiator_q3.shape)
# =============================================================================
    #print('Q4 random:',np.mean(times_randomInstantiator_q4[:,1]),'+-',np.std(times_randomInstantiator_q4[:,1]))
    
    times_randomEMF_q1 = times_randomEMF[np.array([(row[0] <=a1)for row in times_randomEMF])]
    times_randomEMF_q2 = times_randomEMF[np.array([(row[0] <=a2) and (row[0]>a1) for row in times_randomEMF])]
    times_randomEMF_q3 = times_randomEMF[np.array([(row[0] >a2)for row in times_randomEMF])]
    #times_randomEMF_q4 = times_randomEMF[np.array([(row[0] >a3)for row in times_randomEMF])]
    
    print('Q1 RANDOMEMF:',np.mean(times_randomEMF_q1[:,1]),'+-',np.std(times_randomEMF_q1[:,1]))
    print('Q2 RANDOMEMF:',np.mean(times_randomEMF_q2[:,1]),'+-',np.std(times_randomEMF_q2[:,1]))
    print('Q3 RANDOMEMF:',np.mean(times_randomEMF_q3[:,1]),'+-',np.std(times_randomEMF_q3[:,1]))
# =============================================================================
#     print('Q1 RANDOMEMF:',times_randomEMF_q1.shape)
#     print('Q2 RANDOMEMF:',times_randomEMF_q2.shape)
#     print('Q3 RANDOMEMF:',times_randomEMF_q3.shape)
# =============================================================================
    #print('Q4 RANDOMEMF:',np.mean(times_randomEMF_q4[:,1]),'+-',np.std(times_randomEMF_q4[:,1]))
    

    fig, ax = plt.subplots(1,1)
    line_labels = ['M2', 'VIATRA', 'RANDOM','rEMF']
        
    l1 = sns.distplot(times[:,0], hist=False, kde=True
                          , color = 'red', label = 'M2', ax=ax)
    l2 = sns.distplot(times_baseline[:,0], hist=False, kde=True, 
                  color = 'blue', label = 'VIATRA', ax=ax)
    l3 = sns.distplot(times_randomInstantiator[:,0], hist=False, kde=True, 
                  color = 'green', label = 'RANDOM', ax=ax)
    l4 = sns.distplot(times_randomEMF[:,0], hist=False, kde=True, 
                  color = 'black', label = 'rEMF', ax=ax)
    ax.title.set_text('Sizes')
    ax.set_ylabel('')
    fig.legend([l1,l2,l3,l4],     # The line objects
           labels=line_labels,   # The labels for each line
           loc="center right",   # Position of legend
           borderaxespad=0.1    # Small spacing around legend box
           )
    plt.show()
    
if __name__ == "__main__":
    main()
