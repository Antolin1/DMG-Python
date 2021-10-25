#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 16:16:40 2021

@author: Jose Antonio
"""

import networkx as nx
import dmg.graphUtils as gu
from networkx.algorithms.isomorphism import GraphMatcher

#TODO: tests !!!

#pattern for equalRefs
equalRefs = nx.MultiDiGraph()
equalRefs.add_node(0, type = 'Column')
equalRefs.add_node(1, type = 'Reference')
equalRefs.add_node(2, type = 'Column')
equalRefs.add_node(3, type = 'Reference')

equalRefs.add_edge(0, 1, type = 'primaryReferences')
equalRefs.add_edge(1, 2, type = 'foreignKeyColumns')
equalRefs.add_edge(1, 0, type = 'primaryKeyColumns')
equalRefs.add_edge(2, 1, type = 'foreignReferences')

equalRefs.add_edge(0, 3, type = 'primaryReferences')
equalRefs.add_edge(3, 2, type = 'foreignKeyColumns')
equalRefs.add_edge(3, 0, type = 'primaryKeyColumns')
equalRefs.add_edge(2, 3, type = 'foreignReferences')

#pattern for index

icCons = nx.MultiDiGraph()
icCons.add_node(0, type = 'Table')
icCons.add_node(1, type = 'Index')
icCons.add_node(2, type = 'IndexColumn')
icCons.add_node(3, type = 'Column')
icCons.add_node(4, type = 'Table')

icCons.add_edge(0, 1, type = 'indexes')
icCons.add_edge(1, 2, type = 'indexColumns')
icCons.add_edge(2, 3, type = 'column')
icCons.add_edge(4, 3, type = 'columns')

#ref2thesame
ref2thesame = nx.MultiDiGraph()
ref2thesame.add_node(0, type = 'Column')
ref2thesame.add_node(1, type = 'Reference')

ref2thesame.add_edge(0, 1, type = 'primaryReferences')
ref2thesame.add_edge(1, 0, type = 'foreignKeyColumns')
ref2thesame.add_edge(1, 0, type = 'primaryKeyColumns')
ref2thesame.add_edge(0, 1, type = 'foreignReferences')



def inconsistenceEqualRefs(G):
    GM = GraphMatcher(G, equalRefs, node_match = gu.node_match_type, 
                                  edge_match = gu.edge_match_type)
    for subgraph in GM.subgraph_isomorphisms_iter():
        return True
    return False

def inconsistenceIcCons(G):
    GM = GraphMatcher(G, icCons, node_match = gu.node_match_type, 
                                  edge_match = gu.edge_match_type)
    for subgraph in GM.subgraph_isomorphisms_iter():
        return True
    return False

def ref2thesameColumn(G):
    GM = GraphMatcher(G, ref2thesame, node_match = gu.node_match_type, 
                                  edge_match = gu.edge_match_type)
    for subgraph in GM.subgraph_isomorphisms_iter():
        return True
    return False

def inconsistent(G):
    return (inconsistenceEqualRefs(G) or inconsistenceIcCons(G) or ref2thesameColumn(G))

