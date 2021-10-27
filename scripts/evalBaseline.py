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
                        choices=['alloy', 'viatra', 'randomEMF'],
                        help="generator considered.",
                        required=True)
    parser.add_argument("-nm", "--numberModels", dest="number_models",
                        help="number of models to generate.", type=int, default = 500,
                        required=False)
    parser.add_argument("-ps", "--pathsyn", dest="path_syn",
                        help="folder of the syn dataset.", metavar="DIR", 
                        required=True)
    
    parser.add_argument("-p", "--plot", dest="plot", choices=['True', 'False'],
                        required=False, default="True",
                        help="if plot distributions.")
    parser.add_argument("-e", "--epochs", dest="epochs",
                    help="max epochs.", type=int, default = 100,
                    required=False)
    parser.add_argument("-ne", "--neighborhoods", dest="neighborhoods", type=int, 
                        required=False, default=5,
                        help="Neighborhoods to compute the diversity.")
    #parse args
    args = parser.parse_args()
    dataset_path = args.path_dataset
    dataset = args.dataset
    backend = args.emf    
    generator = args.gen
    syn_path = args.path_syn
    plot = (args.plot == 'True')
    epochs = args.epochs
    neighborhoods = args.neighborhoods
    number_models = args.number_models
    msetObject = datasets_supported[dataset]

    #load graphs    
    test_path = dataset_path + '/test'
    graphs_test = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(test_path + "/*")]
    samples = []
    for filename in glob.iglob(syn_path + '/**/*.xmi', recursive=True):
        G1 = msetObject.getGraphSyn(filename,backend)
        lower, upper = msetObject.bounds
        if len(G1) < lower or len(G1) > upper:
            continue
        samples.append(G1)
    samples = random.sample(samples, number_models)
    
    #inconsistency
    inconsistents = []
    for s in samples:
        if msetObject.inconsistency(s):
            inconsistents.append(s)
    inco_prop = len(inconsistents)*100/len(samples)
    not_inconsistents = [g for g in samples if not g in inconsistents]    

    
    #basic stats
    dims = list(msetObject.dic_edges.keys())
    print(inco_prop,'% inconsistent models')
    print(len(not_inconsistents)/len(samples) * 100, '% Validity among all')
    print(len(uniques(not_inconsistents))/len(not_inconsistents) * 100, '% Uniqueness among valid ones')
    
    
    #Degree
    print('Degree:', wasserstein_distance([np.mean(mt.getListDegree(G)) for G in not_inconsistents], 
                     [np.mean(mt.getListDegree(G)) for G in graphs_test]))
    hist_degrees_syn = [nx.degree_histogram(G) for G in not_inconsistents]
    hist_degrees_real = [nx.degree_histogram(G) for G in graphs_test]
    #MMD degree
    mmd_dist_degree = compute_mmd(hist_degrees_real, hist_degrees_syn, kernel=gaussian_emd)
    print('Degree MMD:', mmd_dist_degree)
    
    #MPC
    print('MPC:', wasserstein_distance([np.mean(list(mt.MPC(G,dims).values())) for G in not_inconsistents], 
                     [np.mean(list(mt.MPC(G,dims).values())) for G in graphs_test]))
    
    hist_mpc_syn = [np.histogram(list(mt.MPC(G,dims).values()), bins=100, range=(0.0, 1.0), density=False)[0]
                    for G in not_inconsistents]
    hist_mpc_real = [np.histogram(list(mt.MPC(G,dims).values()), bins=100, range=(0.0, 1.0), density=False)[0]
                    for G in graphs_test]
    #MMD MPC
    mmd_dist_mpc = compute_mmd(hist_mpc_real, hist_mpc_syn, kernel=gaussian_emd, 
                                sigma=1.0/10, distance_scaling=100)
    print('MPC MMD:', mmd_dist_mpc)
    
    #NA
    print('Node activity:', wasserstein_distance([np.mean(list(mt.nodeActivity(G,dims))) for G in not_inconsistents], 
                     [np.mean(list(mt.nodeActivity(G,dims))) for G in graphs_test]))
    
    hist_na_syn = [np.histogram(list(mt.nodeActivity(G,dims)), bins=100, range=(0.0, 1.0), density=False)[0]
                    for G in not_inconsistents]
    hist_na_real = [np.histogram(list(mt.nodeActivity(G,dims)), bins=100, range=(0.0, 1.0), density=False)[0]
                    for G in graphs_test]
    #MMD MPC
    mmd_dist_na = compute_mmd(hist_na_real, hist_na_syn, kernel=gaussian_emd,
                              sigma=1.0/10, distance_scaling=100)
    print('NA MMD:', mmd_dist_na)

    #C2ST
    acc, p_val, test_samples = C2ST_GNN(not_inconsistents, graphs_test, msetObject, epochs=epochs, verbose = True)
    print('Acc C2ST:', acc)
    print('p-value C2ST:', p_val)
    print('Test samples C2ST:', test_samples)
    
    
    #plots
    if plot:
        fig, axs = plt.subplots(ncols=4, figsize=(10, 5))
        line_labels = [generator, 'Real']

        l1 = sns.distplot([np.mean(mt.getListDegree(G)) for G in not_inconsistents], hist=False, kde=True
                          , color = 'red', label = generator, ax=axs[0])
        l2 = sns.distplot([np.mean(mt.getListDegree(G)) for G in graphs_test], hist=False, kde=True, 
                  color = 'blue', label = 'Real', ax=axs[0])
        axs[0].title.set_text('Degree')
        axs[0].set_ylabel('')
    
        l3 = sns.distplot([np.mean(list(mt.MPC(G,dims).values())) for G in not_inconsistents], hist=False, kde=True, 
             color = 'red', label = generator, ax=axs[1])
        l4 = sns.distplot([np.mean(list(mt.MPC(G,dims).values())) for G in graphs_test], hist=False, kde=True, 
              color = 'blue', label = 'Real', ax=axs[1])
        axs[1].title.set_text('MPC')
        axs[1].set_ylabel('')
    
        l5 = sns.distplot([np.mean(list(mt.nodeActivity(G,dims))) for G in not_inconsistents], hist=False, kde=True, 
              color = 'red', label = generator, ax=axs[2])
        l6 = sns.distplot([np.mean(list(mt.nodeActivity(G,dims))) for G in graphs_test], hist=False, kde=True, 
             color = 'blue', label = 'Real', ax=axs[2])
        axs[2].title.set_text('Node Activity')
        axs[2].set_ylabel('')
       
        l7 = sns.distplot([len(G) for G in not_inconsistents], hist=False, kde=True
                          , color = 'red', label = generator, ax=axs[3])
        l8 = sns.distplot([len(G) for G in graphs_test], hist=False, kde=True, 
                  color = 'blue', label = 'Real', ax=axs[3])
        axs[3].title.set_text('Nodes')
        axs[3].set_ylabel('')
        
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
    
    ##diversity
    i = neighborhoods
    def map_f(G):
        return getShapesDP(G, i, msetObject.pathsSynMeta)
    
    print('Internal Diversity')
    div_real = []
    div_syn = []
    with mp.Pool(10) as pool: #careeeeee
        div_real = pool.map(map_f, graphs_test)
    with mp.Pool(10) as pool:
        div_syn = pool.map(map_f, not_inconsistents)
    
    div_real = [[r[-1] for r in d.values()] for d in div_real]
    div_syn = [[r[-1] for r in d.values()] for d in div_syn]
    
    int_div_real = []
    int_div_syn = []
    with mp.Pool(10) as pool:
        int_div_real = pool.map(internalDiversityShapes, div_real)
    with mp.Pool(10) as pool:
        int_div_syn = pool.map(internalDiversityShapes, div_syn)
    
    print('Mean internal diversity of reals:', np.mean(int_div_real))
    print('Mean internal diversity of syn:', np.mean(int_div_syn))
    print(mannwhitneyu(int_div_real, int_div_syn))
    
    if plot:
        data = np.array([int_div_real, int_div_syn])
        plot2 = plt.figure(2)
        plt.boxplot(data)
        plt.show()
    
    print('External diversity')
    cat_real = []
    cat_syn = []
    with mp.Pool(10) as pool:
        cat_real = pool.map(getCategoricalDistribution, div_real)
    with mp.Pool(10) as pool:
        cat_syn = pool.map(getCategoricalDistribution, div_syn)

    ext_div_real = []
    pairs = []
    for a,G1 in enumerate(cat_real):
        for b,G2 in enumerate(cat_real):
            if G1!=G2 and a < b:
                pairs.append((G1,G2))
    def compMD(p):
        return computeMD(p[0],p[1])
    with mp.Pool(10) as pool:
        ext_div_real = pool.map(compMD, pairs)

    ext_div_syn = []
    pairs = []
    for a,G1 in enumerate(cat_syn):
        for b,G2 in enumerate(cat_syn):
            if G1!=G2 and a < b:
                pairs.append((G1,G2))
    with mp.Pool(10) as pool:
        ext_div_syn = pool.map(compMD, pairs)

    print('Mean external diversity of reals:', np.mean(ext_div_real))
    print('Mean external diversity of syn:', np.mean(ext_div_syn))
    print(mannwhitneyu(ext_div_real, ext_div_syn))
    
    if plot:
        data = np.array([ext_div_real, ext_div_syn])
        plot3 = plt.figure(3)
        plt.boxplot(data)
        plt.show()
if __name__ == "__main__":
    main()


