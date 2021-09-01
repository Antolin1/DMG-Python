# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 16:54:00 2021

@author: Usuario
"""

import unittest
import dmg.edits.editoperations as ed
import networkx as nx

##########################graph2
G2 = nx.MultiDiGraph()
G2.add_node(0, type = 'EPackage')
G2.add_node(1, type = 'EClass', ids = {1,2})
G2.add_node(4, type = 'EReference')
G2.add_node(5, type = 'EReference')
G2.add_node(6, type = 'EReference')
        
G2.add_edge(0, 1, type = 'eClassifiers')
G2.add_edge(1, 0, type = 'ePackage')
        
G2.add_edge(1, 4, type = 'eStructuralFeatures')
G2.add_edge(1, 5, type = 'eStructuralFeatures')
G2.add_edge(1, 6, type = 'eStructuralFeatures')
G2.add_edge(4, 1, type = 'eContainingClass')
G2.add_edge(5, 1, type = 'eContainingClass')
G2.add_edge(6, 1, type = 'eContainingClass')
        
G2.add_edge(4, 1, type = 'eType')
G2.add_edge(5, 1, type = 'eType')
G2.add_edge(6, 1, type = 'eType')
############################ graph3
G3 = nx.MultiDiGraph()
G3.add_node(0, type = 'EPackage')
G3.add_node(1, type = 'EClass', ids = {1})
G3.add_node(2, type = 'EClass', ids = {2})
G3.add_node(4, type = 'EReference')
G3.add_node(5, type = 'EReference')
G3.add_node(6, type = 'EReference')
        
G3.add_edge(0, 1, type = 'eClassifiers')
G3.add_edge(1, 0, type = 'ePackage')
G3.add_edge(0, 2, type = 'eClassifiers')
G3.add_edge(2, 0, type = 'ePackage')
        
G3.add_edge(1, 4, type = 'eStructuralFeatures')
G3.add_edge(1, 5, type = 'eStructuralFeatures')
G3.add_edge(1, 6, type = 'eStructuralFeatures')
G3.add_edge(4, 1, type = 'eContainingClass')
G3.add_edge(5, 1, type = 'eContainingClass')
G3.add_edge(6, 1, type = 'eContainingClass')
        
G3.add_edge(4, 1, type = 'eType')
G3.add_edge(5, 1, type = 'eType')
G3.add_edge(6, 1, type = 'eType')

############################ graph4
G4 = nx.MultiDiGraph()
G4.add_node(0, type = 'EPackage')
G4.add_node(1, type = 'EClass', ids = {1})
G4.add_node(2, type = 'EClass')
G4.add_node(4, type = 'EReference')
G4.add_node(5, type = 'EReference')
G4.add_node(6, type = 'EReference')
        
G4.add_edge(0, 1, type = 'eClassifiers')
G4.add_edge(1, 0, type = 'ePackage')
G4.add_edge(0, 2, type = 'eClassifiers')
G4.add_edge(2, 0, type = 'ePackage')
        
G4.add_edge(1, 4, type = 'eStructuralFeatures')
G4.add_edge(1, 5, type = 'eStructuralFeatures')
G4.add_edge(1, 6, type = 'eStructuralFeatures')
G4.add_edge(4, 1, type = 'eContainingClass')
G4.add_edge(5, 1, type = 'eContainingClass')
G4.add_edge(6, 1, type = 'eContainingClass')
        
G4.add_edge(4, 1, type = 'eType')
G4.add_edge(5, 1, type = 'eType')
G4.add_edge(6, 1, type = 'eType')

#########################graph5

G5 = nx.MultiDiGraph()
G5.add_node(0, type = 'EPackage')
G5.add_node(1, type = 'EClass', ids = {1,2})
G5.add_node(4, type = 'EReference')
G5.add_node(5, type = 'EReference')
G5.add_node(6, type = 'EReference')
        
G5.add_edge(0, 1, type = 'eClassifiers')
G5.add_edge(1, 0, type = 'ePackage')
        
G5.add_edge(1, 4, type = 'eStructuralFeatures')
G5.add_edge(1, 5, type = 'eStructuralFeatures')
G5.add_edge(1, 6, type = 'eStructuralFeatures')
G5.add_edge(4, 1, type = 'eContainingClass')
G5.add_edge(5, 1, type = 'eContainingClass')
G5.add_edge(6, 1, type = 'eContainingClass')
        
G5.add_edge(4, 1, type = 'eType')
G5.add_edge(5, 1, type = 'eType')
G5.add_edge(6, 1, type = 'eType')

################ patterns
pattern1 = nx.MultiDiGraph()
pattern1.add_node(0, type = 'EClass', ids = {1,2})
pattern1.add_node(1, type = 'EReference')
pattern1.add_edge(0, 1, type = 'eStructuralFeatures')
pattern1.add_edge(1, 0, type = 'eContainingClass')
pattern1.add_edge(1, 0, type = 'eType')
        
pattern2 = nx.MultiDiGraph()
pattern2.add_node(0, type = 'EClass', ids = {1})
pattern2.add_node(1, type = 'EReference')
pattern2.add_node(2, type = 'EClass', ids = {2})
pattern2.add_edge(0, 1, type = 'eStructuralFeatures')
pattern2.add_edge(1, 0, type = 'eContainingClass')
pattern2.add_edge(1, 2, type = 'eType')
        
addReference = ed.EditOperation([pattern1,pattern2],{1,2})

class TestEditOperations(unittest.TestCase):

    def test_typesId(self):
        expected = [[('EClass',{1,2})],[('EClass',{1}), ('EClass',{2})]]
        self.assertEqual(addReference.getPairTypeIds(), expected)
        
    def test_canApply(self):
        self.assertFalse(addReference.canApply(G4))
        self.assertTrue(addReference.canApply(G2))
        self.assertTrue(addReference.canApply(G3))
        
    #def test_applyEdit(self):
        #TODO, generate a py with all auxiliary graphs used in tests
        #generate applyEdit test
        
if __name__ == '__main__':
    unittest.main()