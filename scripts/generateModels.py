#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 15:45:07 2021

@author: Jose Antonio
"""

import sys
import os
sys.path.append(os.getcwd())

import glob
from pathlib import Path
from shutil import copyfile
from sklearn.model_selection import train_test_split
import ntpath
import dmg.graphUtils as gu
from networkx.algorithms.isomorphism import is_isomorphic
from modelSet import datasets_supported
from argparse import ArgumentParser
from eval import uniques
from assessment import getModelPath
import torch
from dmg.deeplearning.generativeModel import GenerativeModel
from dmg.deeplearning.generativeModel import sampleGraph
from networkx.algorithms.isomorphism import is_isomorphic
from dmg.model2graph.shapes import (getShapesDP, 
                                    internalDiversityShapes, computeMD, 
                                    getCategoricalDistribution)

import dmg.model2graph.model2graph as m2g

import random
import numpy as np
torch.manual_seed(123)
random.seed(123)
np.random.seed(123)

def main():
    
    
    parser = ArgumentParser(description='Script for generating model using DMG')
    
    parser.add_argument("-d", "--dataset", dest="dataset", 
                    choices=['ecore-github', 'rds-genmymodel', 
                             'yakindu-github','yakindu-exercise'], 
                    help="dataset considered.",
                    required=True)
    parser.add_argument("-hi", "--hidden", dest="hidden_dim", type=int, 
                        required=False, default=128,
                        help="hidden dim of the nn size.")
    parser.add_argument("-nm", "--numberModels", dest="number_models",
                        help="number of models to generate.", type=int, default = 500)
    parser.add_argument("-ms", "--maxSize", dest="maxSize",
                        help="max size of the output models", type=int,
                        required=True)
    parser.add_argument("-ps", "--pathsyn", dest="path_syn",
                        help="folder of the syn dataset.", metavar="DIR", 
                        required=True)
    
    #parse args
    args = parser.parse_args()
    
    dataset = args.dataset
    model_path = getModelPath(dataset)
    number_models = args.number_models
    max_size = args.maxSize
    hidden_dim = args.hidden_dim
    msetObject = datasets_supported[dataset]
    pathSave = args.path_syn
    
    model = GenerativeModel(hidden_dim, msetObject.dic_nodes, 
                        msetObject.dic_edges, 
                        msetObject.operations)
    checkpoint = torch.load(model_path,map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    samples = []
    while (len(samples) < number_models):
        G = sampleGraph(msetObject.pallete.initialGraphs[0], 
                           msetObject.pallete, model, 
                           max_size, msetObject.pallete.separator)
        if not msetObject.inconsistency(G):
            samples.append(G)
    
    print('Max elements:', np.max([len(G) for G in samples]))
    print('Min elements:', np.min([len(G) for G in samples]))
    
    for j,G in enumerate(samples):
        m2g.serializeGraphModel(pathSave+'/'+str(j)+'.xmi',msetObject.pathsSynMeta, 
                                msetObject.rootSyn, G)

if __name__ == "__main__":
    main()
