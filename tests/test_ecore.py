#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 15:18:35 2021

@author: Jose Antonio
"""

import unittest
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
import tests.graphs4test as g4t
import dmg.graphUtils as gu
from networkx.algorithms.isomorphism import is_isomorphic

class TestEcore(unittest.TestCase):
    
    def test_m2g_ecore(self):
        metafilter_refs = ['EClass.eSuperTypes', 
                           'EPackage.eClassifiers']
        metafilter_cla = ['EPackage', 'EClass']
        
        metafilter_atts = ['ENamedElement.name']
        
        metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                 attributes = metafilter_atts,
                 classes = metafilter_cla)
        
        meta_models = []
        
        
        #now parse the graph
        G1 = m2g.getGraphFromModel('data/testmodels/testEcore.ecore', 
                              meta_models, metafilterobj,
                              consider_atts = True)
        #to small ecore
        list_elements = m2g.getModelFromGraph(['data/metamodels/smallEcore.ecore'],
                                          G1)
        
        G2 = m2g.getGraphFromModelElements(list_elements.values(), 
                                           metaFiler = metafilterobj)
        
        self.assertTrue(is_isomorphic(G1, G2, 
                                      gu.node_match_type_atts, 
                                      gu.edge_match_type))
