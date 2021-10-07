#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 15:29:48 2021

@author: Jose Antonio
"""

import sys
import os
import glob
sys.path.append(os.getcwd())

#from utils4scripts import (getSeparator, getMaxLen, 
#                           getDicNodes, getDicEdges, 
#                           getDicOperations, getInconsistent,
#                           getGraph, getPallete)
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
from c2st_gnn import C2ST_GNN
from argparse import ArgumentParser
from modelSet import datasets_supported

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
    
    parser = ArgumentParser(description='Script for evaluating the generator')

    parser.add_argument("-m", "--model", dest="model",
                        help="path to the model file.", metavar="FILE", 
                        required=True)
    parser.add_argument("-d", "--dataset", dest="dataset", 
                        choices=['ecore-github', 'rds-genmymodel', 
                                 'yakindu-github','yakindu-exercise'], 
                        help="dataset considered.",
                        required=True)
    parser.add_argument("-pd", "--pathdataset", dest="path_dataset",
                        help="folder of the dataset.", metavar="DIR", 
                        required=True)
    parser.add_argument("-nm", "--numberModels", dest="number_models",
                        help="number of models to generate.", type=int, default = 123)
    parser.add_argument("-ms", "--maxSize", dest="maxSize",
                        help="max size of the output models", type=int,
                        required=True)
    parser.add_argument("-emf", "--emf_backend", dest="emf",
                        choices=['python', 'java'],
                        help="backend to parse the models.",
                        required=True)
    parser.add_argument("-hi", "--hidden", dest="hidden_dim", type=int, 
                        required=False, default=128,
                        help="hidden dim of the nn size.")
    
    args = parser.parse_args()
    
    dataset_path = args.path_dataset
    dataset = args.dataset
    model_path = args.model
    number_models = args.number_models
    backend = args.emf
    max_size = args.maxSize
    hidden_dim = args.hidden_dim
    
    test_path = dataset_path + '/test'
    train_path = dataset_path + '/train'

    msetObject = datasets_supported[dataset]
    
    graphs_train = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(train_path + "/*")]
    graphs_test = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(test_path + "/*")]
    
    model = GenerativeModel(hidden_dim, msetObject.dic_nodes, 
                        msetObject.dic_edges, 
                        msetObject.operations)
    checkpoint = torch.load(model_path,map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    start_time = time.monotonic()
    samples = [sampleGraph(msetObject.pallete.initialGraphs[0], 
                           msetObject.pallete, model, 
                           max_size, msetObject.pallete.separator) 
           for i in range(number_models)]
    inference_duration = time.monotonic() - start_time
    
    inconsistents = []
    for s in samples:
        if msetObject.inconsistency(s):
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
    
    dims = list(msetObject.dic_edges.keys())
    print(len(not_inconsistents), 'consistents')
    print(len(samples), 'total samples')
    print(clean_pr,'% consistent novel models')
    print(iso_prop,'% isomorfic models')
    print(inco_prop,'% inconsistent models')
    print(len(not_inconsistents)/len(samples) * 100, '% Validity among all')
    print(len(uniques(not_inconsistents))/len(not_inconsistents) * 100, '% Uniqueness among valid ones')
    print(len(uniques(clean_new_models))/len(uniques(samples)) * 100, '% Novelty among unique ones')
    
    C2ST_GNN(not_inconsistents, graphs_test, dataset)
    print('Degree:', wasserstein_distance([np.mean(mt.getListDegree(G)) for G in samples], 
                     [np.mean(mt.getListDegree(G)) for G in graphs_test]))
    print('MPC:', wasserstein_distance([np.mean(list(mt.MPC(G,dims).values())) for G in samples], 
                     [np.mean(list(mt.MPC(G,dims).values())) for G in graphs_test]))
    print('Node activity:', wasserstein_distance([np.mean(list(mt.nodeActivity(G,dims))) for G in samples], 
                     [np.mean(list(mt.nodeActivity(G,dims))) for G in graphs_test]))
    print('Inference duration:', inference_duration)
    
if __name__ == "__main__":
    main()
