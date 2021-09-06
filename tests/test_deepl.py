#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 16:49:09 2021

@author: Jose Antonio
"""

import unittest
import dmg.edits.editoperations as ed
import tests.graphs4test as g4t
from networkx.algorithms.isomorphism import is_isomorphic
import dmg.graphUtils as gu
from dmg.edits.pallete import Pallete
from dmg.deeplearning.dataGeneration import sequence2data, data2graph

addReference = ed.EditOperation([g4t.pattern1_ref,g4t.pattern2_ref], [0,1])
addSuperType = ed.EditOperation([g4t.pattern1_st], [0,1])
addClass = ed.EditOperation([g4t.pattern1_ac], [0])

def node_match_type_ids(n1,n2):
    typess = gu.node_match_type(n1, n2)
    if ('ids' in n1) and ('ids' in n2):
        return typess and (n1['ids'] == n2['ids'])
    elif (not 'ids' in n1) and (not 'ids' in n2):
        return typess
    else:
        return False
        


class TestDeepLearning(unittest.TestCase):

        
    def test_sequence2data(self):
        
        dic_operations = {0 : addReference,
                          1: addSuperType,
                          2: addClass}
        
        dic_nodes = {'EClass' : 0,
                     'EReference' : 1,
                     'EPackage' : 2}
        
        dic_edges = {'eClassifiers': 0,
                     'ePackage': 1,
                     'eStructuralFeatures': 2,
                     'eContainingClass': 3,
                     'eType': 4,
                     'eSuperTypes': 5}
        
        pallete = Pallete(dic_operations, dic_nodes, dic_edges, g4t.G_initial)
        sequence = pallete.graphToSequence(g4t.G_g2s)
        max_len = 3
        listDatas = sequence2data(sequence, pallete, max_len)
        
        for j,data in enumerate(listDatas):
            self.assertEqual(data.x.shape[0], len(sequence[j][0]))
            self.assertEqual(data.edge_index.shape[1], 
                             len(sequence[j][0].edges))
            self.assertEqual(data.edge_attr.shape[0], 
                             len(sequence[j][0].edges))
            self.assertEqual(data.action.item(), 
                             sequence[j][1])
            self.assertEqual(data.sequence.shape[0], 
                             max_len)
            self.assertEqual(data.sequence.shape[1], 
                             len(sequence[j][0]))
            
            graph_inv = data2graph(data, pallete)
            self.assertTrue(is_isomorphic(graph_inv, 
                                      sequence[j][0], 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
            np_seq = data.sequence.numpy()
            for i,l in enumerate(np_seq):
                for t,c in enumerate(l):
                    if (c == 1):
                        if ('ids' in graph_inv.nodes[t]):
                            graph_inv.nodes[t]['ids'].add(i)
                        else:
                            graph_inv.nodes[t]['ids'] = set([i])
                            
            self.assertTrue(is_isomorphic(graph_inv, 
                                      sequence[j][0], 
                                      node_match_type_ids, 
                                      gu.edge_match_type))
            
            #print(data.x)
            #print(data.edge_index)
            #print(data.edge_attr)
            #print(data.action)
            #print(data.sequence)
            #print('-'*25)