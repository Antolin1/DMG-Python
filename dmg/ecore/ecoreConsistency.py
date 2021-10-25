#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 10:56:27 2021

@author: Jose Antonio
"""

import networkx as nx
import dmg.graphUtils as gu
from networkx.algorithms.isomorphism import GraphMatcher

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

def doesNotHaveType(G,n):
    for n2 in G[n]:
        for e in G[n][n2]:
            if G[n][n2][e]['type'] == 'eType':
                return False
    return True

def wrongAttributeType(G, n):
    for n2 in G[n]:
        for e in G[n][n2]:
            if G[n][n2][e]['type'] == 'eType' and G.nodes[n2]['type']=='EClass':
                return True
    return False

def wrongEReferenceType(G, n):
    for n2 in G[n]:
        for e in G[n][n2]:
            if G[n][n2][e]['type'] == 'eType' and G.nodes[n2]['type']!='EClass':
                return True
    return False

def referenceDoesNotHaveType(G):
    for n in G:
        if G.nodes[n]['type'] == 'EReference' and (doesNotHaveType(G,n) or 
                                                   wrongEReferenceType(G,n)):
            return True
    return False

def attributeDoesNotHaveType(G):
    for n in G:
        if G.nodes[n]['type'] == 'EAttribute' and (doesNotHaveType(G,n) or 
                                                   wrongAttributeType(G,n)):
            return True
    return False


#def oppositeOfItself(G):
oppItself = nx.MultiDiGraph()
oppItself.add_node(0, type = 'EReference')
oppItself.add_edge(0, 0, type = 'eOpposite')

def opositeOfItself(G):
    GM = GraphMatcher(G, oppItself, node_match = gu.node_match_type, 
                                  edge_match = gu.edge_match_type)
    for subgraph in GM.subgraph_isomorphisms_iter():
        return True
    return False

## end opposites oppositeRestriction, oppositeRestrictionSameClasses
def areTheyOpposite(G, n1, n2):
    try:
        for e in G[n1][n2]:
            if G[n1][n2][e]['type'] == 'eOpposite':
                return True
        return False
    except:
        return False

def restrictionOpposite(G):
    for n1 in G:
        for n2 in G:
            if (n1!=n2 and G.nodes[n1]['type'] == 'EReference' 
                and G.nodes[n2]['type'] == 'EReference' and areTheyOpposite(G,n1,n2)):
                if (not areTheyOpposite(G,n2,n1)):
                    return True
    return False

def getType(G, n):
    for n2 in G[n]:
        for e in G[n][n2]:
            if G[n][n2][e]['type'] == 'eType':
                return n2

def getContaining(G, n):
    for n2 in G[n]:
        for e in G[n][n2]:
            if G[n][n2][e]['type'] == 'eContainingClass':
                return n2

def restrictionSameClasses(G):
    for n1 in G:
        for n2 in G:
            if (n1!=n2 and G.nodes[n1]['type'] == 'EReference' 
                and G.nodes[n2]['type'] == 'EReference' and areTheyOpposite(G,n1,n2)
                and areTheyOpposite(G,n2,n1)):
                if (getType(G,n1)!=getContaining(G,n2)):
                    return True
    return False

def inconsistent(G):
    return (hasCycles(G) or 
            referenceDoesNotHaveType(G) or 
            attributeDoesNotHaveType(G) or 
            opositeOfItself(G) or restrictionOpposite(G) 
            or restrictionSameClasses(G))