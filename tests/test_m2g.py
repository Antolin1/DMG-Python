#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 10:22:58 2021

@author: Jose Antonio
"""


import unittest
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
import networkx as nx
from networkx.algorithms.isomorphism import is_isomorphic
from multiset import Multiset

def node_match(n1,n2):
    return n1['type'] == n2['type']

def edge_match(e1,e2):
    t1 = []
    t2 = []
    for e in e1:
        t1.append(e1[e]['type'])
    for e in e2:
        t2.append(e2[e]['type'])
    return Multiset(t1) == Multiset(t2)

def node_match_with_atts(n1,n2):
    typess = node_match(n1, n2)
    return typess and (n1['atts'] == n2['atts'])
    
class Testm2g(unittest.TestCase):

    def test_smallEcore(self):
        #load model and transform it into a graph
        G1 = m2g.getGraphFromModel('data/testmodels/smallecoretest.xmi', 
                              'data/metamodels/smallEcore.ecore')
        
        #theorical graph
        G2 = nx.MultiDiGraph()
        G2.add_node(0, type = 'EPackage', atts = {'name':'<none>'})
        G2.add_node(1, type = 'EClass', atts = {'name':'<none>',
                                                'abstract':False})
        G2.add_node(2, type = 'EDataType', atts = {'name':'<none>'})
        G2.add_node(3, type = 'EDataType', atts = {'name':'<none>'})
        G2.add_node(4, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':True,
                                                    'lowerBound':0,
                                                    'upperBound':0})
        G2.add_node(5, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':False,
                                                    'lowerBound':0,
                                                    'upperBound':0})
        G2.add_node(6, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':False,
                                                    'lowerBound':0,
                                                    'upperBound':0})
        
        G2.add_edge(0, 1, type = 'eClassifiers')
        G2.add_edge(0, 2, type = 'eClassifiers')
        G2.add_edge(0, 3, type = 'eClassifiers')
        G2.add_edge(1, 0, type = 'ePackage')
        G2.add_edge(2, 0, type = 'ePackage')
        G2.add_edge(3, 0, type = 'ePackage')
        
        G2.add_edge(1, 4, type = 'eStructuralFeatures')
        G2.add_edge(1, 5, type = 'eStructuralFeatures')
        G2.add_edge(1, 6, type = 'eStructuralFeatures')
        G2.add_edge(4, 1, type = 'eContainingClass')
        G2.add_edge(5, 1, type = 'eContainingClass')
        G2.add_edge(6, 1, type = 'eContainingClass')
        
        G2.add_edge(4, 1, type = 'eType')
        G2.add_edge(5, 1, type = 'eType')
        G2.add_edge(6, 1, type = 'eType')
        
        self.assertTrue(is_isomorphic(G1, G2, 
                                      node_match_with_atts, 
                                      edge_match))
    
    def test_smallEcore_metafilter(self):
        metafilter_refs = ['EPackage.eClassifiers', 
                           'EClass.eStructuralFeatures',
                           'ETypedElement.eType']
        metafilter_cla = ['EPackage', 'EClass','EReference']
        
        metafilter_atts = ['ENamedElement.name',
                           'EReference.containment',
                           'ETypedElement.lowerBound']
        
        metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                 attributes = metafilter_atts,
                 classes = metafilter_cla)
        
        #load model and transform it into a graph
        G1 = m2g.getGraphFromModel('data/testmodels/smallecoretest.xmi', 
                              'data/metamodels/smallEcore.ecore',
                              metafilterobj)
        
        #theorical graph
        G2 = nx.MultiDiGraph()
        G2.add_node(0, type = 'EPackage', atts = {'name':'<none>'})
        G2.add_node(1, type = 'EClass', atts = {'name':'<none>'})
        G2.add_node(4, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':True,
                                                    'lowerBound':0})
        G2.add_node(5, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':False,
                                                    'lowerBound':0})
        G2.add_node(6, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':False,
                                                    'lowerBound':0})
        
        G2.add_edge(0, 1, type = 'eClassifiers')
        
        G2.add_edge(1, 4, type = 'eStructuralFeatures')
        G2.add_edge(1, 5, type = 'eStructuralFeatures')
        G2.add_edge(1, 6, type = 'eStructuralFeatures')
        
        G2.add_edge(4, 1, type = 'eType')
        G2.add_edge(5, 1, type = 'eType')
        G2.add_edge(6, 1, type = 'eType')
        
        
        
        self.assertTrue(is_isomorphic(G1, G2, 
                                      node_match_with_atts,edge_match))
        
    
    
    
    def test_yakinduSimpl(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()