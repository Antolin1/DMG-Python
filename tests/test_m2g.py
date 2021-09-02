#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 10:22:58 2021

@author: Jose Antonio
"""


import unittest
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
import tests.graphAux as ga
from networkx.algorithms.isomorphism import is_isomorphic

    
class Testm2g(unittest.TestCase):

    def test_smallEcore(self):
        #load model and transform it into a graph with atts
        G1 = m2g.getGraphFromModel('data/testmodels/smallecoretest.xmi', 
                              'data/metamodels/smallEcore.ecore')
        #check if it is isomorfic considering atts
        self.assertTrue(is_isomorphic(G1, ga.G_test_small_ecore, 
                                      ga.node_match_with_atts, 
                                      ga.edge_match))
        
        #load model and transform it into a graph without atts
        G1_wAtt = m2g.getGraphFromModel('data/testmodels/smallecoretest.xmi', 
                              'data/metamodels/smallEcore.ecore', 
                              consider_atts = False)
        #check no atts
        for n in G1_wAtt:
             self.assertFalse('atts' in G1_wAtt.nodes[n])
        
        #check if it is isomorfic without considering atts
        self.assertTrue(is_isomorphic(G1_wAtt, ga.G_test_small_ecore, 
                                      ga.node_match, 
                                      ga.edge_match))
    
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
        
        self.assertTrue(is_isomorphic(G1, ga.G_test_small_ecore_mf, 
                                      ga.node_match_with_atts,ga.edge_match))
        
    
    
    
    def test_yakinduSimpl(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()