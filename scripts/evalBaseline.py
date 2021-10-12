#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:30:15 2021

@author: Jose Antonio
"""

import sys
import os
import glob
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'/scripts/')

import warnings
warnings.filterwarnings('ignore')

import dmg.graphUtils as gu
import dmg.realism.metrics as mt
import torch
import numpy as np
import random
from scipy.stats import wasserstein_distance

from c2st_gnn import C2ST_GNN
from argparse import ArgumentParser
from eval import uniques
from modelSet import datasets_supported

torch.manual_seed(123)
random.seed(123)
np.random.seed(123)
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    
    parser = ArgumentParser(description='Script for evaluating the baselines')


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
    
    parser.add_argument("-g", "--generator", dest="gen",
                        choices=['alloy', 'viatra'],
                        help="generator considered.",
                        required=True)
    
    parser.add_argument("-ps", "--pathsyn", dest="path_syn",
                        help="folder of the syn dataset.", metavar="DIR", 
                        required=True)
    
    parser.add_argument("-p", "--plot", dest="plot", choices=['True', 'False'],
                        required=False, default="True",
                        help="if plot distributions.")
    parser.add_argument("-e", "--epochs", dest="epochs",
                    help="max epochs.", type=int, default = 50,
                    required=False)

    args = parser.parse_args()
    dataset_path = args.path_dataset
    dataset = args.dataset
    backend = args.emf    
    generator = args.gen
    syn_path = args.path_syn
    plot = bool(args.plot)
    epochs = args.epochs
    
    msetObject = datasets_supported[dataset]

    
    test_path = dataset_path + '/test'

    graphs_test = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(test_path + "/*")]
    
    samples = []
    for filename in glob.iglob(syn_path + '/**/*.xmi', recursive=True):
        #change this
        samples.append(msetObject.getGraphSyn(filename,backend))
    

    
    inconsistents = []
    for s in samples:
        if msetObject.inconsistency(s):
            inconsistents.append(s)
    inco_prop = len(inconsistents)*100/len(samples)
    

    not_inconsistents = [g for g in samples if not g in inconsistents]    

    
    
    dims = list(msetObject.dic_edges.keys())
    print(inco_prop,'% inconsistent models')
    print(len(not_inconsistents)/len(samples) * 100, '% Validity among all')
    print(len(uniques(not_inconsistents))/len(not_inconsistents) * 100, '% Uniqueness among valid ones')
    print('Degree:', wasserstein_distance([np.mean(mt.getListDegree(G)) for G in samples], 
                     [np.mean(mt.getListDegree(G)) for G in graphs_test]))
    print('MPC:', wasserstein_distance([np.mean(list(mt.MPC(G,dims).values())) for G in samples], 
                     [np.mean(list(mt.MPC(G,dims).values())) for G in graphs_test]))
    print('Node activity:', wasserstein_distance([np.mean(list(mt.nodeActivity(G,dims))) for G in samples], 
                     [np.mean(list(mt.nodeActivity(G,dims))) for G in graphs_test]))
    #print('Node:', wasserstein_distance([len(G) for G in samples], 
    #                 [len(G) for G in graphs_test]))
    acc, p_val, test_samples = C2ST_GNN(not_inconsistents, graphs_test, dataset, epochs=epochs)
    print('Acc C2ST:', acc)
    print('p-value C2ST:', p_val)
    print('Test samples C2ST:', test_samples)
    
    fig, axs = plt.subplots(ncols=4, figsize=(10, 5))
    line_labels = [generator, 'Real']
    l1 = None
    l2 = None
    l3 = None
    l4 = None
    l5 = None
    l6 = None
    l7 = None
    l8 = None
    if plot:
        l1 = sns.distplot([np.mean(mt.getListDegree(G)) for G in samples], hist=False, kde=True
                          , color = 'red', label = generator, ax=axs[0])
        l2 = sns.distplot([np.mean(mt.getListDegree(G)) for G in graphs_test], hist=False, kde=True, 
                  color = 'blue', label = 'Real', ax=axs[0])
        axs[0].title.set_text('Degree')
        axs[0].set_ylabel('')
    
    if plot:
       l3 = sns.distplot([np.mean(list(mt.MPC(G,dims).values())) for G in samples], hist=False, kde=True, 
             color = 'red', label = generator, ax=axs[1])
       l4 = sns.distplot([np.mean(list(mt.MPC(G,dims).values())) for G in graphs_test], hist=False, kde=True, 
              color = 'blue', label = 'Real', ax=axs[1])
       axs[1].title.set_text('MPC')
       axs[1].set_ylabel('')
    
    if plot:
       l5 = sns.distplot([np.mean(list(mt.nodeActivity(G,dims))) for G in samples], hist=False, kde=True, 
              color = 'red', label = generator, ax=axs[2])
       l6 = sns.distplot([np.mean(list(mt.nodeActivity(G,dims))) for G in graphs_test], hist=False, kde=True, 
             color = 'blue', label = 'Real', ax=axs[2])
       axs[2].title.set_text('Node Activity')
       axs[2].set_ylabel('')
       
    if plot:
        l7 = sns.distplot([len(G) for G in samples], hist=False, kde=True
                          , color = 'red', label = generator, ax=axs[3])
        l8 = sns.distplot([len(G) for G in graphs_test], hist=False, kde=True, 
                  color = 'blue', label = 'Real', ax=axs[3])
        axs[3].title.set_text('Nodes')
        axs[3].set_ylabel('')
    if plot:
        #fig.legend()
        fig.legend([l1, l2, l3, l4, l5, l6, l7, l8],     # The line objects
           labels=line_labels,   # The labels for each line
           loc="center right",   # Position of legend
           borderaxespad=0.1    # Small spacing around legend box
           )
        #plt.title('Graph statistics')
        plt.show()
    
    #plt.hist([len(G) for G in samples], bins = 10, density=True, alpha=0.6)
    #plt.hist([len(G) for G in graphs_test],  bins = 10, density=True, alpha=0.6)
    #plt.savefig('foo.png', bbox_inches='tight')
if __name__ == "__main__":
    main()


