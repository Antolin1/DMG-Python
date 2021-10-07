#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:30:15 2021

@author: Jose Antonio
"""

import sys
import glob
from utils4scripts import (getSeparator, getMaxLen, 
                           getDicNodes, getDicEdges, 
                           getDicOperations, getInconsistent,
                           getGraph, getPallete)
from dmg.deeplearning.generativeModel import GenerativeModel
from dmg.deeplearning.generativeModel import sampleGraph
from networkx.algorithms.isomorphism import is_isomorphic
import dmg.graphUtils as gu
import dmg.realism.metrics as mt
import torch
import numpy as np
import random
from scipy.stats import wasserstein_distance
import time
import seaborn as sns
from c2st_gnn import C2ST_GNN
def uniques(Gs):
    dic = set([])
    for G1 in Gs:
        iso = False
        for G2 in dic:
            if is_isomorphic(G1, G2, gu.node_match_type, gu.edge_match_type):
                iso = True
        if not iso:
            dic.add(G1)
    return dic


torch.manual_seed(123)
random.seed(123)
np.random.seed(123)
import matplotlib.pyplot as plt
def main():
    dataset_path = sys.argv[1]
    dataset = sys.argv[2]
    backend = sys.argv[3]
    generator = sys.argv[4]
    syn_path = sys.argv[5]
    
    test_path = dataset_path + '/test'

    graphs_test = [getGraph(f,dataset,backend) 
                for f in glob.glob(test_path + "/*")]
    
    samples = []
    for filename in glob.iglob(syn_path + '/**/*.xmi', recursive=True):
        #change this
        samples.append(getGraph(filename,'yakindu-exercise',backend))
    

    
    inconsistents = []
    for s in samples:
        if getInconsistent(dataset)(s):
            inconsistents.append(s)
    inco_prop = len(inconsistents)*100/len(samples)
    

    not_inconsistents = [g for g in samples if not g in inconsistents]    

    
    
    dims = list(getDicEdges(dataset).keys())
    print(inco_prop,'% inconsistent models')
    print(len(not_inconsistents)/len(samples) * 100, '% Validity among all')
    print(len(uniques(not_inconsistents))/len(not_inconsistents) * 100, '% Uniqueness among valid ones')
    print('Degree:', wasserstein_distance([np.mean(mt.getListDegree(G)) for G in samples], 
                     [np.mean(mt.getListDegree(G)) for G in graphs_test]))
    print('MPC:', wasserstein_distance([np.mean(list(mt.MPC(G,dims).values())) for G in samples], 
                     [np.mean(list(mt.MPC(G,dims).values())) for G in graphs_test]))
    print('Node activity:', wasserstein_distance([np.mean(list(mt.nodeActivity(G,dims))) for G in samples], 
                     [np.mean(list(mt.nodeActivity(G,dims))) for G in graphs_test]))
    print('Node:', wasserstein_distance([len(G) for G in samples], 
                     [len(G) for G in graphs_test]))
    C2ST_GNN(not_inconsistents, graphs_test, dataset)
    #plt.hist([len(G) for G in samples], bins = 10, density=True, alpha=0.6)
    #plt.hist([len(G) for G in graphs_test],  bins = 10, density=True, alpha=0.6)
    #plt.savefig('foo.png', bbox_inches='tight')
if __name__ == "__main__":
    main()


