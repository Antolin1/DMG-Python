#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 10:08:29 2021

@author: Jose Antonio
"""

import unittest
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
from dmg.rds.rdsPreprocess import removeTypes
import tests.graphs4test as g4t
import dmg.graphUtils as gu
from networkx.algorithms.isomorphism import is_isomorphic


class TestRDS(unittest.TestCase):
    
    def test_rds(self):
        metafilter_refs = ['Database.elements', 
                           'Table.indexes',
                           'Table.columns',
                           'Index.indexColumns',
                           'IndexColumn.column',
                           'Reference.primaryKeyColumns',
                           'Reference.foreignKeyColumns',
                           'Column.primaryReferences',
                           'Column.foreignReferences']
        metafilter_cla = ['Database', 'Column','Table',
                          'Index', 'IndexColumn','Reference']
        
        metafilter_atts = ['Database.name', 'Type.name', 'Column.name']
        
        metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                 attributes = metafilter_atts,
                 classes = metafilter_cla)
        
        meta_models = ['data/metamodels/rds_manual.ecore']
        
        removeTypes('data/testmodels/testRDS.xmi', 
                     'data/testmodels/outRDS.xmi')
        
        #now parse the graph
        G1 = m2g.getGraphFromModel('data/testmodels/outRDS.xmi', 
                              meta_models, metafilterobj,
                              consider_atts = True)
        
        #print(G1.nodes(data=True))
        self.assertTrue(is_isomorphic(G1, g4t.G_rds, 
                                      gu.node_match_type_atts, 
                                      gu.edge_match_type))

