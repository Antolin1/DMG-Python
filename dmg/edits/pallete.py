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
    
    def __init__(self, editOperations,
                 initialGraph):
        self.editOperations = editOperations
        self.initialGraph = initialGraph
        #TODO: check consistency
        
    def graphToSequence(self, G):
        list_ids = list(range(0,len(self.editOperations)))
        random.shuffle(list_ids)
        if (is_isomorphic(G,self.initialGraph,
                          node_match, edge_match)):
            return []
        else:
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
        
        
    