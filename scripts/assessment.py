#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 15:16:20 2021

@author: Jose Antonio
"""
import sys
import os
import glob
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'/scripts/')

import warnings
warnings.filterwarnings('ignore')

import dmg.realism.metrics as mt
import torch
import numpy as np
import random
from scipy.stats import wasserstein_distance

from c2st_gnn import C2ST_GNN
from argparse import ArgumentParser
from eval import uniques
from modelSet import datasets_supported
from dmg.model2graph.shapes import (getShapesDP, 
                                    internalDiversityShapes, computeMD, 
                                    getCategoricalDistribution)
from scipy.stats import mannwhitneyu
import multiprocess as mp
from dmg.realism.emd import compute_mmd, gaussian_emd
import networkx as nx


torch.manual_seed(123)
random.seed(123)
np.random.seed(123)
import matplotlib.pyplot as plt
import seaborn as sns

from dmg.deeplearning.generativeModel import GenerativeModel
from dmg.deeplearning.generativeModel import sampleGraph

def getModelPath(dataset):
    if dataset == 'ecore-github':
        return 'models/ecore-github-finalModel-cuda.m'
    elif dataset == 'yakindu-github':
        return 'models/yakindu-github-finalModel-cuda.m'
    elif dataset == 'yakindu-exercise':
        return 'models/yakindu-exercise-finalModel-cuda.m'
    elif dataset == 'rds-genmymodel':
        return 'models/rds-genmymodel-finalModel-cuda.m'
    




def getSynPath(generator, dataset):
    return 'baselines/' + dataset +'/' + generator

def main():
    
    generators = ['DMG', 'viatra', 'randomEMF', 'randomInstantiator']
    #parser
    
    parser = ArgumentParser(description='Script for evaluating all the generators')

    parser.add_argument("-d", "--dataset", dest="dataset", 
                        choices=['ecore-github', 'rds-genmymodel', 
                                 'yakindu-github','yakindu-exercise'], 
                        help="dataset considered.",
                        required=True)
    parser.add_argument("-pd", "--pathdataset", dest="path_dataset",
                        help="folder of the dataset.", metavar="DIR", 
                        required=True)
    parser.add_argument("-nm", "--numberModels", dest="number_models",
                        help="number of models to generate.", type=int, default = 500)
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
    parser.add_argument("-p", "--plot", dest="plot", choices=['True', 'False'],
                        required=False, default="True",
                        help="if plot distributions.")
    parser.add_argument("-e", "--epochs", dest="epochs",
                    help="max epochs.", type=int, 
                    required=False, default=100)
    
    parser.add_argument("-ne", "--neighborhoods", dest="neighborhoods", type=int, 
                        required=False, default=5,
                        help="Neighborhoods to compute the diversity.")
    
    #parse args
    args = parser.parse_args()
    dataset_path = args.path_dataset
    dataset = args.dataset
    model_path = getModelPath(dataset)
    number_models = args.number_models
    backend = args.emf
    max_size = args.maxSize
    hidden_dim = args.hidden_dim
    epochs = args.epochs
    plot = (args.plot == 'True')
    neighborhoods = args.neighborhoods
    msetObject = datasets_supported[dataset]
    
    
    test_path = dataset_path + '/test'
    graphs_test = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(test_path + "/*")]
    
    
    generators_samples = {}
    
    ##obtaining samples
    for gen in generators:
        print('Obtaining samples for', gen)
        if gen == 'DMG':
            model = GenerativeModel(hidden_dim, msetObject.dic_nodes, 
                        msetObject.dic_edges, 
                        msetObject.operations)
            checkpoint = torch.load(model_path,map_location=torch.device('cpu'))
            model.load_state_dict(checkpoint['model_state_dict'])
            model.eval()
            generators_samples[gen] = [sampleGraph(msetObject.pallete.initialGraphs[0], 
                           msetObject.pallete, model, 
                           max_size, msetObject.pallete.separator) 
                       for i in range(number_models)]
        else:
            samples = []
            for filename in glob.iglob(getSynPath(gen, dataset) + '/**/*.xmi', recursive=True):
                G1 = msetObject.getGraphSyn(filename,backend)
                lower, upper = msetObject.bounds
                if len(G1) < lower: #or len(G1) > upper:
                    continue
                samples.append(G1)
            samples = random.sample(samples, number_models)
            generators_samples[gen] = samples
    
    print('--'*10)
    for gen in generators:
        print('Samples generated by',gen,':',len(generators_samples[gen]))
    
    ##check inconsistent
    generators_not_inconsistents = {}
    for gen in generators:
        inconsistents = []
        for s in generators_samples[gen]:
            if msetObject.inconsistency(s):
                inconsistents.append(s)
        #inco_prop = len(inconsistents)*100/len(samples)
        not_inconsistents = [g for g in generators_samples[gen] if not g in inconsistents]
        generators_not_inconsistents[gen] = not_inconsistents
    
    print('--'*10)
    for gen in generators:
        print('Consistency',gen,':',(len(generators_not_inconsistents[gen])*100/len(samples)))
        
    generators = [gen for gen in generators if len(generators_not_inconsistents[gen]) > 0]
    
    mmds_degree = {}
    hist_degrees_real = [nx.degree_histogram(G) for G in graphs_test]
    for gen in generators:
        if len(generators_not_inconsistents[gen]) > 0:
            hist_degrees_syn = [nx.degree_histogram(G) for G in generators_not_inconsistents[gen]]
            mmds_degree[gen] = compute_mmd(hist_degrees_real, hist_degrees_syn, kernel=gaussian_emd)
        else:
            mmds_degree[gen] = 'Not enough consistents'
    
    print('--'*10)
    for gen in generators:
        print('MMD degree',gen,':',mmds_degree[gen])
    
    dims = list(msetObject.dic_edges.keys())
    hist_mpc_real = [np.histogram(list(mt.MPC(G,dims).values()), bins=100, range=(0.0, 1.0), density=False)[0]
                        for G in graphs_test]
    mmds_mpc = {}
    for gen in generators:
        if len(generators_not_inconsistents[gen]) > 0:
            hist_mpc_syn = [np.histogram(list(mt.MPC(G,dims).values()), bins=100, range=(0.0, 1.0), density=False)[0]
                            for G in generators_not_inconsistents[gen]]
            #MMD MPC
            mmds_mpc[gen] = compute_mmd(hist_mpc_real, hist_mpc_syn, kernel=gaussian_emd, 
                                        sigma=1.0/10, distance_scaling=100)
        else:
            mmds_mpc[gen] = 'Not enough consistents'
    
    print('--'*10)
    for gen in generators:
        print('MMD MPC',gen,':',mmds_mpc[gen])
        
        
    hist_na_real = [np.histogram(list(mt.nodeActivity(G,dims)), bins=100, range=(0.0, 1.0), density=False)[0]
                        for G in graphs_test]
    mmds_na = {}
    for gen in generators:
        if len(generators_not_inconsistents[gen]) > 0:
            hist_na_syn = [np.histogram(list(mt.nodeActivity(G,dims)), bins=100, range=(0.0, 1.0), density=False)[0]
                            for G in generators_not_inconsistents[gen]]
            #MMD MPC
            mmds_na[gen] = compute_mmd(hist_na_real, hist_na_syn, kernel=gaussian_emd,
                                      sigma=1.0/10, distance_scaling=100)
        else:
            mmds_na[gen] = 'Not enough consistents'
    
    print('--'*10)
    for gen in generators:
        print('MMD NA',gen,':',mmds_na[gen])
        
    c2st_generators = {}
    for gen in generators:
        if len(generators_not_inconsistents[gen]) > 0:
            acc, p_val, test_samples = C2ST_GNN(generators_not_inconsistents[gen], graphs_test, 
                                                msetObject, epochs=epochs, verbose = False)
            c2st_generators[gen] = (acc, p_val, test_samples)
        else:
            c2st_generators[gen] = ('NEC', 'NEC', 'NEC')
    
    print('--'*10)
    for gen in generators:
        print('C2ST',gen,': acc',c2st_generators[gen][0], 'p-value', 
              c2st_generators[gen][1], 
              'samples in test set', c2st_generators[gen][2])
    
    ##plots
    if plot:
        fig, axs = plt.subplots(ncols=4, figsize=(10, 5))
        colors = ['red', 'blue', 'green', 'yellow']
        lines_degree_generators = []
        lines_mpc_generators = []
        lines_na_generators = []
        lines_nodes_generators = []
        for j,gen in enumerate(generators):
            if len(generators_not_inconsistents[gen]) > 0: 
                lines_degree_generators.append(sns.distplot([np.mean(mt.getListDegree(G)) for G in generators_not_inconsistents[gen]], hist=False, kde=True
                              , color = colors[j], label = gen, ax=axs[0]))
                axs[0].title.set_text('Degree')
                axs[0].set_ylabel('')
            
                lines_mpc_generators.append(sns.distplot([np.mean(list(mt.MPC(G,dims).values())) for G in generators_not_inconsistents[gen]], hist=False, kde=True, 
                     color = colors[j], label = gen, ax=axs[1]))
                axs[1].title.set_text('MPC')
                axs[1].set_ylabel('')
            
                lines_na_generators.append(sns.distplot([np.mean(list(mt.nodeActivity(G,dims))) for G in generators_not_inconsistents[gen]], hist=False, kde=True, 
                      color = colors[j], label = gen, ax=axs[2]))
                axs[2].title.set_text('Node Activity')
                axs[2].set_ylabel('')
               
                lines_nodes_generators.append(sns.distplot([len(G) for G in generators_not_inconsistents[gen]], hist=False, kde=True
                                  , color = colors[j], label = gen, ax=axs[3]))
                axs[3].title.set_text('Nodes')
                axs[3].set_ylabel('')
        
        l2 = sns.distplot([np.mean(mt.getListDegree(G)) for G in graphs_test], hist=False, kde=True, 
                  color = 'black', label = 'real', ax=axs[0])
        l4 = sns.distplot([np.mean(list(mt.MPC(G,dims).values())) for G in graphs_test], hist=False, kde=True, 
              color = 'black', label = 'real', ax=axs[1])
        l6 = sns.distplot([np.mean(list(mt.nodeActivity(G,dims))) for G in graphs_test], hist=False, kde=True, 
             color = 'black', label = 'real', ax=axs[2])
        l8 = sns.distplot([len(G) for G in graphs_test], hist=False, kde=True, 
                  color = 'black', label = 'real', ax=axs[3])
        
        fig.legend(lines_degree_generators + lines_mpc_generators + lines_na_generators + lines_nodes_generators
                   + [l2,l4,l6,l8],     # The line objects
           labels=generators + ['real'],   # The labels for each line
           loc="center right",   # Position of legend
           borderaxespad=0.1    # Small spacing around legend box
           )
        #plt.title('Graph statistics')
        plt.show()
    
    ## diversity
    i = neighborhoods
    def map_f(G):
        return getShapesDP(G, i, msetObject.pathsSynMeta)
    
    div_real = []
    with mp.Pool(10) as pool: #careeeeee
        div_real = pool.map(map_f, graphs_test)
    div_real = [[r[-1] for r in d.values()] for d in div_real]
    
    int_div_real = []
    with mp.Pool(10) as pool:
        int_div_real = pool.map(internalDiversityShapes, div_real)
    
    int_div_generators = {}
    div_generators = {}
    for gen in generators:
        with mp.Pool(10) as pool:
            div_generators[gen] = pool.map(map_f, generators_not_inconsistents[gen])
        div_generators[gen] = [[r[-1] for r in d.values()] 
                                   for d in div_generators[gen]]
        with mp.Pool(10) as pool:
            int_div_generators[gen] = pool.map(internalDiversityShapes, div_generators[gen])
    
    print('--'*10)
    for gen in generators:
        print('Internal diversity',gen,':',np.mean(int_div_generators[gen]), '+-', np.std(int_div_generators[gen]))
    print('Internal diversity real:', np.mean(int_div_real),'+-', np.std(int_div_real))
    
    if plot:
        data = [int_div_generators[gen] for gen in generators] + [int_div_real]
        plot2 = plt.figure(2)
        plt.boxplot(data ,labels = generators + ['real'])
        plt.show()

if __name__ == "__main__":
    main()
    