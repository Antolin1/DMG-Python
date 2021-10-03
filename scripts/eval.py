#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 15:29:48 2021

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

def main():
    dataset_path = sys.argv[1]
    dataset = sys.argv[2]
    model_path = sys.argv[3]
    number_models = int(sys.argv[4])
    backend = sys.argv[5]
    max_size = int(sys.argv[6])
    hidden_dim = int(sys.argv[7])
    
    test_path = dataset_path + '/test'
    train_path = dataset_path + '/train'
    graphs_test = [getGraph(f,dataset,backend) 
                for f in glob.glob(test_path + "/*")]
    graphs_train = [getGraph(f,dataset,backend) 
                for f in glob.glob(train_path + "/*")]
    
    model = GenerativeModel(hidden_dim, getDicNodes(dataset), 
                        getDicEdges(dataset), 
                        getDicOperations(dataset))
    checkpoint = torch.load(model_path,map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    start_time = time.monotonic()
    samples = [sampleGraph(getPallete(dataset).initialGraphs[0], 
                           getPallete(dataset), model, 
                           max_size, getSeparator(dataset)) 
           for i in range(number_models)]
    inference_duration = time.monotonic() - start_time
    
    inconsistents = []
    for s in samples:
        if getInconsistent(dataset)(s):
            inconsistents.append(s)
    inco_prop = len(inconsistents)*100/len(samples)
    
    iso = []
    for s in samples:
        for g in graphs_train:
            if (is_isomorphic(s,g,gu.node_match_type, gu.edge_match_type)):
                iso.append(s)
                break
    
    not_inconsistents = [g for g in samples if not g in inconsistents]    
    iso_prop = len(iso)*100/len(samples)
    
    clean_new_models = [g for g in samples if (not g in inconsistents) and (not g in iso)]
    clean_pr = len(clean_new_models)*100/len(samples)
    
    dims = list(getDicEdges(dataset).keys())
    print(clean_pr,'% consistent novel models')
    print(iso_prop,'% isomorfic models')
    print(inco_prop,'% inconsistent models')
    print(len(not_inconsistents)/len(samples) * 100, '% Validity among all')
    print(len(uniques(not_inconsistents))/len(not_inconsistents) * 100, '% Uniqueness among valid ones')
    print(len(uniques(clean_new_models))/len(uniques(samples)) * 100, '% Novelty among unique ones')
    print('Degree:', wasserstein_distance([np.mean(mt.getListDegree(G)) for G in samples], 
                     [np.mean(mt.getListDegree(G)) for G in graphs_test]))
    print('MPC:', wasserstein_distance([np.mean(list(mt.MPC(G,dims).values())) for G in samples], 
                     [np.mean(list(mt.MPC(G,dims).values())) for G in graphs_test]))
    print('Node activity:', wasserstein_distance([np.mean(list(mt.nodeActivity(G,dims))) for G in samples], 
                     [np.mean(list(mt.nodeActivity(G,dims))) for G in graphs_test]))
    print('Inference duration:', inference_duration)
if __name__ == "__main__":
    main()
