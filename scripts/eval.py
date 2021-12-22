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
from scipy.stats import mannwhitneyu, ttest_ind, levene
from dmg.realism.emd import compute_mmd, gaussian_emd
import networkx as nx


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
    model_path = args.model
    number_models = args.number_models
    backend = args.emf
    max_size = args.maxSize
    hidden_dim = args.hidden_dim
    epochs = args.epochs
    plot = (args.plot == 'True')
    neighborhoods = args.neighborhoods
    
    #train and test paths
    test_path = dataset_path + '/test'
    train_path = dataset_path + '/train'
    msetObject = datasets_supported[dataset]
    
    #load graphs
    graphs_train = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(train_path + "/*")]
    graphs_test = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(test_path + "/*")]
    
    #load generative model
    model = GenerativeModel(hidden_dim, msetObject.dic_nodes, 
                        msetObject.dic_edges, 
                        msetObject.operations)
    checkpoint = torch.load(model_path,map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    #generate samples
    start_time = time.monotonic()
    samples = [sampleGraph(msetObject.pallete.initialGraphs[0], 
                           msetObject.pallete, model, 
                           max_size, msetObject.pallete.separator) 
           for i in range(number_models)]
    inference_duration = time.monotonic() - start_time
    
    #check inconsistents
    inconsistents = []
    for s in samples:
        if msetObject.inconsistency(s):
            inconsistents.append(s)
    inco_prop = len(inconsistents)*100/len(samples)
    not_inconsistents = [g for g in samples if not g in inconsistents]
    
    #check isomorf
    iso = []
    for s in samples:
        for g in graphs_train:
            if (is_isomorphic(s,g,gu.node_match_type, gu.edge_match_type)):
                iso.append(s)
                break
    iso_prop = len(iso)*100/len(samples)
    
    #clean models: (not iso and not inconsistents)
    clean_new_models = [g for g in samples if (not g in inconsistents) and (not g in iso)]
    clean_pr = len(clean_new_models)*100/len(samples)
    
    #dims for MPC and so on
    dims = list(msetObject.dic_edges.keys())
    
    #basic stats
    print(len(not_inconsistents), 'consistents')
    print(len(samples), 'total samples')
    print(clean_pr,'% consistent novel models')
    print(iso_prop,'% isomorfic models')
    print(inco_prop,'% inconsistent models')
    print(len(not_inconsistents)/len(samples) * 100, '% Validity among all')
    print(len(uniques(not_inconsistents))/len(not_inconsistents) * 100, '% Uniqueness among valid ones')
    print(len(uniques(clean_new_models))/len(uniques(samples)) * 100, '% Novelty among unique ones')
    
    print('For novelty, we remove inconsistent models:')
    print('P. models unique novel:', len(uniques(clean_new_models))/len(not_inconsistents))
    
    print('Inference duration:', inference_duration)
    print('Max nodes syn:', np.max([len(G) for G in not_inconsistents]))
    print('Min nodes syn:', np.min([len(G) for G in not_inconsistents]))
    print('Max nodes real:', np.max([len(G) for G in graphs_test]))
    
    #C2ST
    acc, p_val, test_samples = C2ST_GNN(not_inconsistents, graphs_test, 
                                        msetObject, epochs=epochs, verbose = False)
    print('Acc C2ST:', acc)
    print('p-value C2ST:', p_val)
    print('Test samples C2ST:', test_samples)
    
    
    #WS degree
    print('Degree WS:', wasserstein_distance([np.mean(mt.getListDegree(G)) for G in not_inconsistents], 
                     [np.mean(mt.getListDegree(G)) for G in graphs_test]))
    hist_degrees_syn = [nx.degree_histogram(G) for G in not_inconsistents]
    hist_degrees_real = [nx.degree_histogram(G) for G in graphs_test]
    #MMD degree
    mmd_dist_degree = compute_mmd(hist_degrees_real, hist_degrees_syn, kernel=gaussian_emd)
    print('Degree MMD:', mmd_dist_degree)
    
    #WS MPC
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
    
    #WS NA
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
    
    
    #plot of Degree, MPC, NA, Nodes
    if plot:
        fig, axs = plt.subplots(ncols=4, figsize=(10, 5))
        line_labels = ['DMG', 'Real']
        
        l1 = sns.distplot([np.mean(mt.getListDegree(G)) for G in not_inconsistents], hist=False, kde=True
                          , color = 'red', label = 'DMG', ax=axs[0])
        l2 = sns.distplot([np.mean(mt.getListDegree(G)) for G in graphs_test], hist=False, kde=True, 
                  color = 'blue', label = 'Real', ax=axs[0])
        axs[0].title.set_text('Degree')
        axs[0].set_ylabel('')
    
        l3 = sns.distplot([np.mean(list(mt.MPC(G,dims).values())) for G in not_inconsistents], hist=False, kde=True, 
             color = 'red', label = 'DMG', ax=axs[1])
        l4 = sns.distplot([np.mean(list(mt.MPC(G,dims).values())) for G in graphs_test], hist=False, kde=True, 
              color = 'blue', label = 'Real', ax=axs[1])
        axs[1].title.set_text('MPC')
        axs[1].set_ylabel('')

        l5 = sns.distplot([np.mean(list(mt.nodeActivity(G,dims))) for G in not_inconsistents], hist=False, kde=True, 
              color = 'red', label = 'DMG', ax=axs[2])
        l6 = sns.distplot([np.mean(list(mt.nodeActivity(G,dims))) for G in graphs_test], hist=False, kde=True, 
             color = 'blue', label = 'Real', ax=axs[2])
        axs[2].title.set_text('Node Activity')
        axs[2].set_ylabel('')

        l7 = sns.distplot([len(G) for G in not_inconsistents], hist=False, kde=True
                          , color = 'red', label = 'DMG', ax=axs[3])
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
    #int_div_real = [internalDiversity(G, i, msetObject.pathsRealMeta) for G in graphs_test]
    #int_div_syn = [internalDiversity(G, i, msetObject.pathsSynMeta) for G in samples]
    
    int_div_real = []
    int_div_syn = []
    with mp.Pool(10) as pool:
        int_div_real = pool.map(internalDiversityShapes, div_real)
    with mp.Pool(10) as pool:
        int_div_syn = pool.map(internalDiversityShapes, div_syn)
    
    print('Mean internal diversity of reals:', np.mean(int_div_real),'+-', np.std(int_div_real))
    print('Mean internal diversity of syn:', np.mean(int_div_syn),'+-', np.std(int_div_syn))
    
    print('Tests')
    p_val_eqvar = levene(int_div_real, int_div_syn).pvalue
    print(mannwhitneyu(int_div_real, int_div_syn))
    print(ttest_ind(int_div_real, int_div_syn,equal_var=(p_val_eqvar>0.01)))
    print(levene(int_div_real, int_div_syn))
    
    if plot:
        data = np.array([int_div_real, int_div_syn])
        plot2 = plt.figure(2)
        plt.boxplot(data)
        plt.show()
    
    if plot:
        fig, ax = plt.subplots(1,1)
        line_labels = ['DMG', 'Real']
        
        l1 = sns.distplot(int_div_syn, hist=False, kde=True
                          , color = 'red', label = 'DMG', ax=ax)
        l2 = sns.distplot(int_div_real, hist=False, kde=True, 
                  color = 'blue', label = 'Real', ax=ax)
        ax.title.set_text('Internal diversity')
        ax.set_ylabel('')
        fig.legend([l1, l2],     # The line objects
           labels=line_labels,   # The labels for each line
           loc="center right",   # Position of legend
           borderaxespad=0.1    # Small spacing around legend box
           )
        plt.show()
    
# =============================================================================
#     print('External diversity')
#     cat_real = []
#     cat_syn = []
#     with mp.Pool(10) as pool:
#         cat_real = pool.map(getCategoricalDistribution, div_real)
#     with mp.Pool(10) as pool:
#         cat_syn = pool.map(getCategoricalDistribution, div_syn)
# 
#     ext_div_real = []
#     pairs = []
#     for a,G1 in enumerate(cat_real):
#         for b,G2 in enumerate(cat_real):
#             if G1!=G2 and a < b:
#                 pairs.append((G1,G2))
#                 #ext_div_real.append(computeMD(G1,G2))
#     def compMD(p):
#         return computeMD(p[0],p[1])
#     with mp.Pool(10) as pool:
#         ext_div_real = pool.map(compMD, pairs)
# 
#     
#     ext_div_syn = []
#     pairs = []
#     for a,G1 in enumerate(cat_syn):
#         for b,G2 in enumerate(cat_syn):
#             if G1!=G2 and a < b:
#                 pairs.append((G1,G2))
#                 #ext_div_syn.append(computeMD(G1,G2))
#     with mp.Pool(10) as pool:
#         ext_div_syn = pool.map(compMD, pairs)
# 
#         
#     print('Mean external diversity of reals:', np.mean(ext_div_real))
#     print('Mean external diversity of syn:', np.mean(ext_div_syn))
#     print(mannwhitneyu(ext_div_real, ext_div_syn))
#     if plot:
#         data = np.array([ext_div_real, ext_div_syn])
#         plot3 = plt.figure(3)
#         plt.boxplot(data)
#         plt.show()
# =============================================================================
if __name__ == "__main__":
    main()
