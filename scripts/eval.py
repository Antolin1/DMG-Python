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
import torch
import numpy as np
import random

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
    
    samples = [sampleGraph(getPallete(dataset).initialGraphs[0], 
                           getPallete(dataset), model, 
                           max_size, getSeparator(dataset)) 
           for i in range(number_models)]
    
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
    
    iso_prop = len(iso)*100/len(samples)
    
    clean_new_models = [g for g in samples if (not g in inconsistents) and (not g in iso)]
    clean_pr = len(clean_new_models)*100/len(samples)
    
    print(clean_pr,'% consistent novel models')
    print(iso_prop,'% isomorfic models')
    print(inco_prop,'% inconsistent models')
if __name__ == "__main__":
    main()
