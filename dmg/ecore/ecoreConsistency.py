#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 10:56:27 2021

@author: Jose Antonio
"""

import networkx as nx

def hasCycles(G):
    eclasses = []
    for n in G:
        if (G.nodes[n]['type']=='EClass'):
            eclasses.append(n)
    
    remove = []
    G_eclasses = G.subgraph(eclasses).copy()
    for e in G_eclasses.edges:
        if G[e[0]][e[1]][e[2]]['type'] != 'eSuperTypes':
            remove.append((e[0],e[1], e[2]))
    for s, t, k in remove:
        G_eclasses.remove_edge(s, t, k)
    
    try:
        nx.find_cycle(G_eclasses, orientation="original")
    except nx.exception.NetworkXNoCycle:
        return False
    return True

def inconsistent(G):
    return hasCycles(G)