# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 16:54:00 2021

@author: Jose Antonio
"""

import unittest
import dmg.edits.editoperations as ed
import tests.graphs4test as g4t
from networkx.algorithms.isomorphism import is_isomorphic
import dmg.graphUtils as gu
from dmg.edits.pallete import Pallete

addReference = ed.EditOperation([g4t.pattern1_ref,g4t.pattern2_ref])
addSuperType = ed.EditOperation([g4t.pattern1_st])
addClass = ed.EditOperation([g4t.pattern1_ac])

class TestEditOperations(unittest.TestCase):

        
    def test_canApply(self):
        self.assertFalse(addReference.canApply(g4t.G_with_one_id))
        self.assertFalse(addReference.canApply(g4t.G_with_nonsenseid))
        self.assertTrue(addReference.canApply(g4t.G_wo_ref_itself))
        self.assertTrue(addReference.canApply(g4t.G_wo_ref))
        
    def test_applyEdit(self):
        applied_edit_1 = addReference.applyEdit(g4t.G_wo_ref_itself)
        applied_edit_2 = addReference.applyEdit(g4t.G_wo_ref)
        applied_edit_3 = addSuperType.applyEdit(g4t.G_wo_ref)
        #print(applied_edit_2.nodes(data = True))
        #print(applied_edit_2.edges(data=True))
        self.assertTrue(is_isomorphic(applied_edit_1, 
                                      g4t.G_expected_added_ref_itself, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        self.assertTrue(is_isomorphic(applied_edit_2, 
                                      g4t.G_expected_added_ref, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        self.assertTrue(is_isomorphic(applied_edit_3, 
                                      g4t.G_expected_added_super, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        self.assertFalse(is_isomorphic(applied_edit_1, g4t.G_wo_ref_itself, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        
    def test_removeEdit(self):
        applied_edit = addSuperType.applyEdit(g4t.G_wo_ref)
        #(applied_edit_3.nodes(data= True))
        #print(applied_edit_3.edges(data= True))
        remove_edit,_ = addSuperType.removeEdit(applied_edit)
        
        applied_edit_1 = addReference.applyEdit(g4t.G_wo_ref_itself)
        remove_edit_1,_ = addReference.removeEdit(applied_edit_1)
        
        self.assertTrue(is_isomorphic(g4t.G_wo_ref, 
                                      remove_edit, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        self.assertTrue(is_isomorphic(g4t.G_wo_ref_itself, 
                                      remove_edit_1, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        
        self.assertTrue(addSuperType.removeEdit(applied_edit_1) == None)
    
    def test_pallete(self):
        dic_operations = {0 : addReference,
                          1: addSuperType,
                          2: addClass}
        
        pallete = Pallete(dic_operations, g4t.G_initial)
        
        sequence = pallete.graphToSequence(g4t.G_g2s)
        
        self.assertTrue(len(sequence)==3)
        self.assertTrue(is_isomorphic(g4t.G_initial, 
                                      sequence[-1][0], 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        
        for j, (graph, idd) in enumerate(sequence):
            #print(graph.nodes(data = True))
            #print('Edit nº', idd)
            applied = pallete.applyEdit(graph, idd)
            if j == 0:
                self.assertTrue(is_isomorphic(g4t.G_g2s, 
                                      applied, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
            else:
                self.assertTrue(is_isomorphic(sequence[j-1][0], 
                                      applied, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        
if __name__ == '__main__':
    unittest.main()