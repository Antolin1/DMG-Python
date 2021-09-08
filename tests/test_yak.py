#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 15:40:23 2021

@author: Jose Antonio
"""

import unittest
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
import tests.graphs4test as g4t
from networkx.algorithms.isomorphism import is_isomorphic
import dmg.graphUtils as gu
import glob
from dmg.yakindu.yakinduPreprocess import removeLayout
import dmg.yakindu.yakinduPallete as yp 
import random
random.seed(123)

class TestYakindu(unittest.TestCase):
    
    def test_yakinduComplete(self):
        metafilter_refs = ['Region.vertices', 
                           'CompositeElement.regions',
                           'Vertex.outgoingTransitions',
                           'Transition.target']
        metafilter_cla = ['Region', 'CompositeElement','Vertex','Transition']
        
        metafilter_atts = None
        
        metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                 attributes = metafilter_atts,
                 classes = metafilter_cla)
        
        meta_models = glob.glob("data/metamodels/yakinduComplete/*")
        
        removeLayout('data/testmodels/yakinduFullTest.xmi', 
                     'data/testmodels/outYak.xmi')
        
        #now parse the graph
        G1 = m2g.getGraphFromModel('data/testmodels/outYak.xmi', 
                              meta_models, metafilterobj,
                              consider_atts = False)
        
        self.assertTrue(is_isomorphic(G1, g4t.G_yak_meta, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
                
    def test_yakinduPallete(self):
        metafilter_refs = ['Region.vertices', 
                           'CompositeElement.regions',
                           'Vertex.outgoingTransitions',
                           'Vertex.incomingTransitions',
                           'Transition.target',
                           'Transition.source']
        metafilter_cla = list(yp.dic_nodes_yak.keys())
        
        metafilter_atts = None
        
        metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                 attributes = metafilter_atts,
                 classes = metafilter_cla)
        
        meta_models = glob.glob("data/metamodels/yakinduComplete/*")
        
        removeLayout('data/testmodels/yakinduFullTest.xmi', 
                     'data/testmodels/outYak.xmi')
        
        #now parse the graph
        G1 = m2g.getGraphFromModel('data/testmodels/outYak.xmi', 
                              meta_models, metafilterobj,
                              consider_atts = False)
        
        sequence = yp.yakindu_pallete.graphToSequence(G1)
        
        self.assertTrue(is_isomorphic(yp.G_initial_yak, 
                                      sequence[-1][0], 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        
        for j, (graph, idd) in enumerate(sequence):
            #print(graph.nodes(data = True))
            #print('Edit nº', idd)
            applied = yp.yakindu_pallete.applyEdit(graph, idd)
            if j == 0:
                self.assertTrue(is_isomorphic(G1, 
                                      applied, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
            else:
                self.assertTrue(is_isomorphic(sequence[j-1][0], 
                                      applied, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
