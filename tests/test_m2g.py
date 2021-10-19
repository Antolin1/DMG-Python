#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 10:22:58 2021

@author: Jose Antonio
"""


import unittest
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
from dmg.model2graph.shapes import (internalDiversityDP, 
                                    getShapesDP, externalDiversity)
import tests.graphs4test as g4t
from networkx.algorithms.isomorphism import is_isomorphic
import dmg.graphUtils as gu



    
class Testm2g(unittest.TestCase):

    def test_smallEcore(self):
        #load model and transform it into a graph with atts
        G1 = m2g.getGraphFromModel('data/testmodels/smallecoretest.xmi', 
                              ['data/metamodels/smallEcore.ecore'])
        #check if it is isomorfic considering atts
        self.assertTrue(is_isomorphic(G1, g4t.G_test_small_ecore, 
                                      gu.node_match_type_atts, 
                                      gu.edge_match_type))
        
        #load model and transform it into a graph without atts
        G1_wAtt = m2g.getGraphFromModel('data/testmodels/smallecoretest.xmi', 
                              ['data/metamodels/smallEcore.ecore'], 
                              consider_atts = False)
        #check no atts
        for n in G1_wAtt:
             self.assertFalse('atts' in G1_wAtt.nodes[n])
        
        #check if it is isomorfic without considering atts
        self.assertTrue(is_isomorphic(G1_wAtt, g4t.G_test_small_ecore, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
    
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
                              ['data/metamodels/smallEcore.ecore'],
                              metafilterobj)
        
        self.assertTrue(is_isomorphic(G1, g4t.G_test_small_ecore_mf, 
                                      gu.node_match_type_atts,
                                      gu.edge_match_type))
        
    
    

    def test_yakinduSimpl(self):
        #load model and transform it into a graph with atts
        G1 = m2g.getGraphFromModel('data/testmodels/yakindutest.xmi', 
                              ['data/metamodels/yakinduSimplified.ecore'])
        #check if it is isomorfic without considering atts
        self.assertTrue(is_isomorphic(G1, g4t.G_yak, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
    
    def test_yakinduSimpl_metafiter(self):
        metafilter_refs = ['Region.vertices', 
                           'CompositeElement.regions',
                           'Vertex.outgoingTransitions',
                           'Transition.target']
        metafilter_cla = None
        
        metafilter_atts = None
        
        metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                 attributes = metafilter_atts,
                 classes = metafilter_cla)
        
        #load model and transform it into a graph withput atts
        G1 = m2g.getGraphFromModel('data/testmodels/yakindutest.xmi', 
                              ['data/metamodels/yakinduSimplified.ecore'],
                              metafilterobj,
                              consider_atts = False)
        #check if it is isomorfic without considering atts
        self.assertTrue(is_isomorphic(G1, g4t.G_yak_meta, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        
    def test_getModelFromGraph(self):
        #load model and transform it into a graph with atts
        G1 = m2g.getGraphFromModel('data/testmodels/smallecoretest.xmi', 
                              ['data/metamodels/smallEcore.ecore'])
        list_elements = m2g.getModelFromGraph(['data/metamodels/smallEcore.ecore'],
                                          G1)
        self.assertEqual(len(G1), len(list_elements))
        
        
        
        G2 = m2g.getGraphFromModelElements(list_elements.values())
        
        self.assertTrue(is_isomorphic(G1, G2, 
                                      gu.node_match_type_atts, 
                                      gu.edge_match_type))
    
    def test_serialization(self):
        #load model and transform it into a graph with atts
        G1 = m2g.getGraphFromModel('data/testmodels/smallecoretest.xmi', 
                              ['data/metamodels/smallEcore.ecore'])
        m2g.serializeGraphModel('data/testmodels/testSerialization.xmi', 
                            ['data/metamodels/smallEcore.ecore'], 'EPackage', 
                            G1)
        G2 = m2g.getGraphFromModel('data/testmodels/testSerialization.xmi', 
                              ['data/metamodels/smallEcore.ecore'])
        self.assertTrue(is_isomorphic(G1, G2, 
                                      gu.node_match_type_atts, 
                                      gu.edge_match_type))
    
    
    def test_shapes(self):
        metafilter_refs = ['Region.vertices', 
                           'CompositeElement.regions',
                           'Transition.target',
                           'Transition.source']
        metafilter_cla = None
        
        metafilter_atts = None
        
        metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                 attributes = metafilter_atts,
                 classes = metafilter_cla)
        
        #load model and transform it into a graph withput atts
        G1 = m2g.getGraphFromModel('data/testmodels/yakindutest.xmi', 
                              ['data/metamodels/yakinduSimplified.ecore'],
                              metafilterobj,
                              consider_atts = False)
        for i in range(5):
            shape_entry = getShapesDP(G1, i, ['data/metamodels/yakinduSimplified.ecore'])[2][-1]
            shape_statechart = getShapesDP(G1, i, ['data/metamodels/yakinduSimplified.ecore'])[0][-1]
            #self.assertTrue(compareShapes(shape_entry, shape_entry))
            #if i > 0:
            #    self.assertFalse(compareShapes(shape_entry, shape_statechart))
                
        
        G3 = g4t.G_yak_shape
        for i in range(5):
            #if i == 1:
            #    print(getShapesDP(G3,i,['data/metamodels/yakindu_simplified.ecore']))
            #print('i=',i,':', internalDiversity(G3,i,['data/metamodels/yakindu_simplified.ecore']))
            print('DP i=',i,":", internalDiversityDP(G3,i,['data/metamodels/yakindu_simplified.ecore']))
        
        #print(getShapesDP(G3,3,['data/metamodels/yakindu_simplified.ecore'])[2])
        print('External diversity', externalDiversity(G1,G3,i,['data/metamodels/yakindu_simplified.ecore']))
        self.assertAlmostEqual(externalDiversity(G3,G3,i,['data/metamodels/yakindu_simplified.ecore']), 0.0)
        self.assertAlmostEqual(externalDiversity(G1,G1,i,['data/metamodels/yakinduSimplified.ecore']), 0.0)
        print('External diversity', externalDiversity(G3,G3,i,['data/metamodels/yakindu_simplified.ecore']))
        
        
if __name__ == '__main__':
    unittest.main()