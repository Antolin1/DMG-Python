#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 12:15:01 2021

@author: Jose Antonio
"""

from multiset import Multiset
import graphviz
import networkx as nx

def node_match_type(n1,n2):
    return n1['type'] == n2['type']

def edge_match_type(e1,e2):
    t1 = []
    t2 = []
    for e in e1:
        t1.append(e1[e]['type'])
    for e in e2:
        t2.append(e2[e]['type'])
    return Multiset(t1) == Multiset(t2)

def node_match_type_atts(n1,n2):
    typess = node_match_type(n1, n2)
    return typess and (n1['atts'] == n2['atts'])


def plotGraphViz(G):
    g = graphviz.Digraph(filename='graph')
    for e in G.edges:
        g.node(str(e[0]), label = G.nodes[e[0]]['type'])
        g.node(str(e[1]), label = G.nodes[e[1]]['type'])
        g.edge(str(e[0]), str(e[1]),label=G[e[0]][e[1]][e[2]]['type'])
    return g

def fixDotGraph(G):
    G_new = nx.MultiDiGraph(G)
    for n in G_new:
        G_new.nodes[n]['type'] = G_new.nodes[n]['label']
        del G_new.nodes[n]['label']
    for e in list(G_new.edges(keys=True)):
        label = G_new[e[0]][e[1]][e[2]]['label']
        G_new.remove_edge(e[0],e[1],e[2])
        G_new.add_edge(e[0],e[1],e[2], type = label)
    new_map = {}
    j = 0
    for n in G_new:
        new_map[n] = j
        j = j + 1                                            
    G_new = nx.relabel_nodes(G_new, new_map)
    return G_new