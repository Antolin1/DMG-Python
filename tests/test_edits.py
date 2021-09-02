# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 16:54:00 2021

@author: Jose Antonio
"""

import unittest
import dmg.edits.editoperations as ed
import tests.graphAux as ga
from networkx.algorithms.isomorphism import is_isomorphic

addReference = ed.EditOperation([ga.pattern1_ref,ga.pattern2_ref])
addSuperType = ed.EditOperation([ga.pattern1_st])

class TestEditOperations(unittest.TestCase):

        
    def test_canApply(self):
        self.assertFalse(addReference.canApply(ga.G_with_one_id))
        self.assertTrue(addReference.canApply(ga.G_wo_ref_itself))
        self.assertTrue(addReference.canApply(ga.G_wo_ref))
        
    def test_applyEdit(self):
        applied_edit_1 = addReference.applyEdit(ga.G_wo_ref_itself)
        applied_edit_2 = addReference.applyEdit(ga.G_wo_ref)
        applied_edit_3 = addSuperType.applyEdit(ga.G_wo_ref)
        #print(applied_edit_2.nodes(data = True))
        #print(applied_edit_2.edges(data=True))
        self.assertTrue(is_isomorphic(applied_edit_1, 
                                      ga.G_expected_added_ref_itself, 
                                      ga.node_match,ga.edge_match))
        self.assertTrue(is_isomorphic(applied_edit_2, 
                                      ga.G_expected_added_ref, 
                                      ga.node_match, ga.edge_match))
        self.assertTrue(is_isomorphic(applied_edit_3, 
                                      ga.G_expected_added_super, 
                                      ga.node_match, ga.edge_match))
        self.assertFalse(is_isomorphic(applied_edit_1, ga.G_wo_ref_itself, 
                                      ga.node_match, ga.edge_match))
        
if __name__ == '__main__':
    unittest.main()