#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 11:36:49 2021

@author: Jose Antonio
"""

import random
from networkx.algorithms.isomorphism import is_isomorphic
from dmg.graphUtils import edge_match_type as edge_match
from dmg.graphUtils import node_match_type as node_match
import networkx as nx

class Pallete:
    #editOperations: {x:y} x is id and y is object edit op
    #dic_nodes: {x:y} x is str and y is id (same to dic_edges)
    def __init__(self, editOperations,
                 dic_nodes,
                 dic_edges,
                 initialGraphs,
                 shuffle = True):
        self.editOperations = editOperations
        self.initialGraphs = initialGraphs
        self.dic_nodes = dic_nodes
        self.dic_edges = dic_edges
        self.shuffle = shuffle
        #TODO: check consistency
        
    def graphToSequence(self, G):
        list_ids = list(range(0,len(self.editOperations)))
        if self.shuffle:
            random.shuffle(list_ids)
        else:
            list_ids = sorted(list_ids, reverse=False)
        
        for intialGraph in self.initialGraphs:
            if is_isomorphic(G,intialGraph,
                          node_match, edge_match):
                return []

        for idd in list_ids:
            editOp = self.editOperations[idd]
            re = editOp.removeEdit(G)
            if re != None:
                re_new = nx.MultiDiGraph(re[0])
                for n in re_new:
                    if 'ids' in re_new.nodes[n]:
                        del re_new.nodes[n]['ids']
                return [(re[0], idd)] + self.graphToSequence(re_new)
        return []
    
    def applyEdit(self, G, idd):
        return self.editOperations[idd].applyEdit(G)
    
    def getSpecialNodes(self, idd):
        return self.editOperations[idd].ids
        
        
    