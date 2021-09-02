# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:00:06 2021

@author: Jose Antonio
"""

import networkx as nx
from multiset import Multiset

def node_match(n1,n2):
    return n1['type'] == n2['type']

def edge_match(e1,e2):
    t1 = []
    t2 = []
    for e in e1:
        t1.append(e1[e]['type'])
    for e in e2:
        t2.append(e2[e]['type'])
    return Multiset(t1) == Multiset(t2)

def node_match_with_atts(n1,n2):
    typess = node_match(n1, n2)
    return typess and (n1['atts'] == n2['atts'])


#G for test small ecore
G_test_small_ecore = nx.MultiDiGraph()
G_test_small_ecore.add_node(0, type = 'EPackage', atts = {'name':'<none>'})
G_test_small_ecore.add_node(1, type = 'EClass', atts = {'name':'<none>',
                                        'abstract':False})
G_test_small_ecore.add_node(2, type = 'EDataType', atts = {'name':'<none>'})
G_test_small_ecore.add_node(3, type = 'EDataType', atts = {'name':'<none>'})
G_test_small_ecore.add_node(4, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':True,
                                                    'lowerBound':0,
                                                    'upperBound':0})
G_test_small_ecore.add_node(5, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':False,
                                                    'lowerBound':0,
                                                    'upperBound':0})
G_test_small_ecore.add_node(6, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':False,
                                                    'lowerBound':0,
                                                    'upperBound':0})
        
G_test_small_ecore.add_edge(0, 1, type = 'eClassifiers')
G_test_small_ecore.add_edge(0, 2, type = 'eClassifiers')
G_test_small_ecore.add_edge(0, 3, type = 'eClassifiers')
G_test_small_ecore.add_edge(1, 0, type = 'ePackage')
G_test_small_ecore.add_edge(2, 0, type = 'ePackage')
G_test_small_ecore.add_edge(3, 0, type = 'ePackage')
        
G_test_small_ecore.add_edge(1, 4, type = 'eStructuralFeatures')
G_test_small_ecore.add_edge(1, 5, type = 'eStructuralFeatures')
G_test_small_ecore.add_edge(1, 6, type = 'eStructuralFeatures')
G_test_small_ecore.add_edge(4, 1, type = 'eContainingClass')
G_test_small_ecore.add_edge(5, 1, type = 'eContainingClass')
G_test_small_ecore.add_edge(6, 1, type = 'eContainingClass')

G_test_small_ecore.add_edge(4, 1, type = 'eType')
G_test_small_ecore.add_edge(5, 1, type = 'eType')
G_test_small_ecore.add_edge(6, 1, type = 'eType')



#G for test metafilter in small ecore
G_test_small_ecore_mf = nx.MultiDiGraph()
G_test_small_ecore_mf.add_node(0, type = 'EPackage', atts = {'name':'<none>'})
G_test_small_ecore_mf.add_node(1, type = 'EClass', atts = {'name':'<none>'})
G_test_small_ecore_mf.add_node(4, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':True,
                                                    'lowerBound':0})
G_test_small_ecore_mf.add_node(5, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':False,
                                                    'lowerBound':0})
G_test_small_ecore_mf.add_node(6, type = 'EReference', atts = {'name':'<none>',
                                                    'containment':False,
                                                    'lowerBound':0})
        
G_test_small_ecore_mf.add_edge(0, 1, type = 'eClassifiers')
        
G_test_small_ecore_mf.add_edge(1, 4, type = 'eStructuralFeatures')
G_test_small_ecore_mf.add_edge(1, 5, type = 'eStructuralFeatures')
G_test_small_ecore_mf.add_edge(1, 6, type = 'eStructuralFeatures')
        
G_test_small_ecore_mf.add_edge(4, 1, type = 'eType')
G_test_small_ecore_mf.add_edge(5, 1, type = 'eType')
G_test_small_ecore_mf.add_edge(6, 1, type = 'eType')




##### graphs for test edits

##########################graph2 - add a refernece in the same class
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

############################ add a reference that connects two classes
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

############################ to check false
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
G5.add_node(7, type = 'EReference')
        
G5.add_edge(0, 1, type = 'eClassifiers')
G5.add_edge(1, 0, type = 'ePackage')
        
G5.add_edge(1, 4, type = 'eStructuralFeatures')
G5.add_edge(1, 5, type = 'eStructuralFeatures')
G5.add_edge(1, 6, type = 'eStructuralFeatures')
G5.add_edge(1, 7, type = 'eStructuralFeatures')
G5.add_edge(4, 1, type = 'eContainingClass')
G5.add_edge(5, 1, type = 'eContainingClass')
G5.add_edge(6, 1, type = 'eContainingClass')
G5.add_edge(7, 1, type = 'eContainingClass')
        
G5.add_edge(4, 1, type = 'eType')
G5.add_edge(5, 1, type = 'eType')
G5.add_edge(6, 1, type = 'eType')
G5.add_edge(7, 1, type = 'eType')

############################ add a reference that connects two classes
G6 = nx.MultiDiGraph()
G6.add_node(0, type = 'EPackage')
G6.add_node(1, type = 'EClass', ids = {1})
G6.add_node(2, type = 'EClass', ids = {2})
G6.add_node(4, type = 'EReference')
G6.add_node(5, type = 'EReference')
G6.add_node(6, type = 'EReference')
G6.add_node(7, type = 'EReference')
        
G6.add_edge(0, 1, type = 'eClassifiers')
G6.add_edge(1, 0, type = 'ePackage')
G6.add_edge(0, 2, type = 'eClassifiers')
G6.add_edge(2, 0, type = 'ePackage')
        
G6.add_edge(1, 4, type = 'eStructuralFeatures')
G6.add_edge(1, 5, type = 'eStructuralFeatures')
G6.add_edge(1, 6, type = 'eStructuralFeatures')
G6.add_edge(1, 7, type = 'eStructuralFeatures')
G6.add_edge(4, 1, type = 'eContainingClass')
G6.add_edge(5, 1, type = 'eContainingClass')
G6.add_edge(6, 1, type = 'eContainingClass')
G6.add_edge(7, 1, type = 'eContainingClass')
        
G6.add_edge(4, 1, type = 'eType')
G6.add_edge(5, 1, type = 'eType')
G6.add_edge(6, 1, type = 'eType')
G6.add_edge(7, 2, type = 'eType')

################ patterns for add a reference
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

