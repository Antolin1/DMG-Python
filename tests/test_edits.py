# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 16:54:00 2021

@author: Usuario
"""

import unittest
import dmg.edits.editoperations as ed
import tests.graphAux as ga
from networkx.algorithms.isomorphism import is_isomorphic

addReference = ed.EditOperation([ga.pattern1,ga.pattern2],{1,2})

class TestEditOperations(unittest.TestCase):

    def test_typesId(self):
        expected = [[('EClass',{1,2})],[('EClass',{1}), ('EClass',{2})]]
        self.assertEqual(addReference.getPairTypeIds(), expected)
        
    def test_canApply(self):
        self.assertFalse(addReference.canApply(ga.G4))
        self.assertTrue(addReference.canApply(ga.G2))
        self.assertTrue(addReference.canApply(ga.G3))
        
    def test_applyEdit(self):
        applied_edit_1 = addReference.applyEdit(ga.G2)
        applied_edit_2 = addReference.applyEdit(ga.G3)
        #print(applied_edit_2.nodes(data = True))
        #print(applied_edit_2.edges(data=True))
        self.assertTrue(is_isomorphic(applied_edit_1, ga.G5, 
                                      ga.node_match,ga.edge_match))
        self.assertTrue(is_isomorphic(applied_edit_2, ga.G6, 
                                      ga.node_match, ga.edge_match))
        self.assertFalse(is_isomorphic(applied_edit_1, ga.G2, 
                                      ga.node_match, ga.edge_match))
        
if __name__ == '__main__':
    unittest.main()