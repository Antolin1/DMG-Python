#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 11:49:46 2021

@author: Jose Antonio
"""

import numpy as np
import networkx as nx

#TODO: test them
#degrees
def getListInDegree(G):
    return [G.in_degree(n) for n in G.nodes()]

def getListOutDegree(G):
    return [G.out_degree(n) for n in G.nodes()]

def getListDegree(G):
    return [G.out_degree(n) + G.in_degree(n) for n in G.nodes()]

#clustering coef, seems wrong
def getClustList(G):
    return list(nx.clustering(nx.Graph(G)).values())


#MPC Varro et al.
def degreeVectors(G, dims):
    vectors = {}
    for n in G.nodes():
        vectors[n] = ([0]*len(dims))
    for e in G.edges:
        dim_e = G[e[0]][e[1]][e[2]]['type']
        if (not dim_e in dims):
            continue
        vectors[e[0]][dims.index(dim_e)] += 1
        vectors[e[1]][dims.index(dim_e)] += 1
    return vectors

def MPC(G, dims):
    degreevecs = degreeVectors(G, dims)
    mpc = {}
    for n,vs in degreevecs.items():
        dim = len(vs)
        deg = np.sum(vs)
        summ = 0.
        for d in vs:
            summ = summ + ((d/deg)**2)
        mpc_v = (1 - summ)*dim/(dim-1)
        mpc[n]=mpc_v
    return mpc