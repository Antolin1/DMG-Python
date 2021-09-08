# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:00:06 2021

@author: Jose Antonio
"""

import networkx as nx


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

#G for yakindu
G_yak = nx.MultiDiGraph()
G_yak.add_node(0, type = 'Statechart')
G_yak.add_node(1, type = 'Region')
G_yak.add_node(2, type = 'Entry')
G_yak.add_node(3, type = 'State')
G_yak.add_node(4, type = 'Transition')
        
G_yak.add_edge(0, 1, type = 'regions')
G_yak.add_edge(1, 2, type = 'vertices')
G_yak.add_edge(1, 3, type = 'vertices')
G_yak.add_edge(2, 4, type = 'outgoingTransitions')
G_yak.add_edge(4, 2, type = 'source')
G_yak.add_edge(4, 3, type = 'target')
G_yak.add_edge(3, 4, type = 'incomingTransitions')

#G for yakindu metafiler
G_yak_meta = nx.MultiDiGraph()
G_yak_meta.add_node(0, type = 'Statechart')
G_yak_meta.add_node(1, type = 'Region')
G_yak_meta.add_node(2, type = 'Entry')
G_yak_meta.add_node(3, type = 'State')
G_yak_meta.add_node(4, type = 'Transition')
        
G_yak_meta.add_edge(0, 1, type = 'regions')
G_yak_meta.add_edge(1, 2, type = 'vertices')
G_yak_meta.add_edge(1, 3, type = 'vertices')
G_yak_meta.add_edge(2, 4, type = 'outgoingTransitions')
G_yak_meta.add_edge(4, 3, type = 'target')


##### graphs for test edits

##########################graph2 - add a refernece in the same class
G_wo_ref_itself = nx.MultiDiGraph()
G_wo_ref_itself.add_node(0, type = 'EPackage')
G_wo_ref_itself.add_node(1, type = 'EClass', ids = {0,1})
G_wo_ref_itself.add_node(4, type = 'EReference')
G_wo_ref_itself.add_node(5, type = 'EReference')
G_wo_ref_itself.add_node(6, type = 'EReference')
        
G_wo_ref_itself.add_edge(0, 1, type = 'eClassifiers')
G_wo_ref_itself.add_edge(1, 0, type = 'ePackage')
        
G_wo_ref_itself.add_edge(1, 4, type = 'eStructuralFeatures')
G_wo_ref_itself.add_edge(1, 5, type = 'eStructuralFeatures')
G_wo_ref_itself.add_edge(1, 6, type = 'eStructuralFeatures')
G_wo_ref_itself.add_edge(4, 1, type = 'eContainingClass')
G_wo_ref_itself.add_edge(5, 1, type = 'eContainingClass')
G_wo_ref_itself.add_edge(6, 1, type = 'eContainingClass')
        
G_wo_ref_itself.add_edge(4, 1, type = 'eType')
G_wo_ref_itself.add_edge(5, 1, type = 'eType')
G_wo_ref_itself.add_edge(6, 1, type = 'eType')

############################ add a reference that connects two classes
G_wo_ref = nx.MultiDiGraph()
G_wo_ref.add_node(0, type = 'EPackage')
G_wo_ref.add_node(1, type = 'EClass', ids = {0})
G_wo_ref.add_node(2, type = 'EClass', ids = {1})
G_wo_ref.add_node(4, type = 'EReference')
G_wo_ref.add_node(5, type = 'EReference')
G_wo_ref.add_node(6, type = 'EReference')
        
G_wo_ref.add_edge(0, 1, type = 'eClassifiers')
G_wo_ref.add_edge(1, 0, type = 'ePackage')
G_wo_ref.add_edge(0, 2, type = 'eClassifiers')
G_wo_ref.add_edge(2, 0, type = 'ePackage')
        
G_wo_ref.add_edge(1, 4, type = 'eStructuralFeatures')
G_wo_ref.add_edge(1, 5, type = 'eStructuralFeatures')
G_wo_ref.add_edge(1, 6, type = 'eStructuralFeatures')
G_wo_ref.add_edge(4, 1, type = 'eContainingClass')
G_wo_ref.add_edge(5, 1, type = 'eContainingClass')
G_wo_ref.add_edge(6, 1, type = 'eContainingClass')
        
G_wo_ref.add_edge(4, 1, type = 'eType')
G_wo_ref.add_edge(5, 1, type = 'eType')
G_wo_ref.add_edge(6, 1, type = 'eType')

############################ to check false
G_with_one_id = nx.MultiDiGraph()
G_with_one_id.add_node(0, type = 'EPackage')
G_with_one_id.add_node(1, type = 'EClass', ids = {0})
G_with_one_id.add_node(2, type = 'EClass')
G_with_one_id.add_node(4, type = 'EReference')
G_with_one_id.add_node(5, type = 'EReference')
G_with_one_id.add_node(6, type = 'EReference')
        
G_with_one_id.add_edge(0, 1, type = 'eClassifiers')
G_with_one_id.add_edge(1, 0, type = 'ePackage')
G_with_one_id.add_edge(0, 2, type = 'eClassifiers')
G_with_one_id.add_edge(2, 0, type = 'ePackage')
        
G_with_one_id.add_edge(1, 4, type = 'eStructuralFeatures')
G_with_one_id.add_edge(1, 5, type = 'eStructuralFeatures')
G_with_one_id.add_edge(1, 6, type = 'eStructuralFeatures')
G_with_one_id.add_edge(4, 1, type = 'eContainingClass')
G_with_one_id.add_edge(5, 1, type = 'eContainingClass')
G_with_one_id.add_edge(6, 1, type = 'eContainingClass')
        
G_with_one_id.add_edge(4, 1, type = 'eType')
G_with_one_id.add_edge(5, 1, type = 'eType')
G_with_one_id.add_edge(6, 1, type = 'eType')

############################ to check false
G_with_nonsenseid = nx.MultiDiGraph()
G_with_nonsenseid.add_node(0, type = 'EPackage')
G_with_nonsenseid.add_node(1, type = 'EClass', ids = {0})
G_with_nonsenseid.add_node(2, type = 'EClass')
G_with_nonsenseid.add_node(4, type = 'EReference', ids = {1})
G_with_nonsenseid.add_node(5, type = 'EReference')
G_with_nonsenseid.add_node(6, type = 'EReference')
        
G_with_nonsenseid.add_edge(0, 1, type = 'eClassifiers')
G_with_nonsenseid.add_edge(1, 0, type = 'ePackage')
G_with_nonsenseid.add_edge(0, 2, type = 'eClassifiers')
G_with_nonsenseid.add_edge(2, 0, type = 'ePackage')
        
G_with_nonsenseid.add_edge(1, 4, type = 'eStructuralFeatures')
G_with_nonsenseid.add_edge(1, 5, type = 'eStructuralFeatures')
G_with_nonsenseid.add_edge(1, 6, type = 'eStructuralFeatures')
G_with_nonsenseid.add_edge(4, 1, type = 'eContainingClass')
G_with_nonsenseid.add_edge(5, 1, type = 'eContainingClass')
G_with_nonsenseid.add_edge(6, 1, type = 'eContainingClass')
        
G_with_nonsenseid.add_edge(4, 1, type = 'eType')
G_with_nonsenseid.add_edge(5, 1, type = 'eType')
G_with_nonsenseid.add_edge(6, 1, type = 'eType')

#########################graph5

G_expected_added_ref_itself = nx.MultiDiGraph()
G_expected_added_ref_itself.add_node(0, type = 'EPackage')
G_expected_added_ref_itself.add_node(1, type = 'EClass')
G_expected_added_ref_itself.add_node(4, type = 'EReference')
G_expected_added_ref_itself.add_node(5, type = 'EReference')
G_expected_added_ref_itself.add_node(6, type = 'EReference')
G_expected_added_ref_itself.add_node(7, type = 'EReference')
        
G_expected_added_ref_itself.add_edge(0, 1, type = 'eClassifiers')
G_expected_added_ref_itself.add_edge(1, 0, type = 'ePackage')
        
G_expected_added_ref_itself.add_edge(1, 4, type = 'eStructuralFeatures')
G_expected_added_ref_itself.add_edge(1, 5, type = 'eStructuralFeatures')
G_expected_added_ref_itself.add_edge(1, 6, type = 'eStructuralFeatures')
G_expected_added_ref_itself.add_edge(1, 7, type = 'eStructuralFeatures')
G_expected_added_ref_itself.add_edge(4, 1, type = 'eContainingClass')
G_expected_added_ref_itself.add_edge(5, 1, type = 'eContainingClass')
G_expected_added_ref_itself.add_edge(6, 1, type = 'eContainingClass')
G_expected_added_ref_itself.add_edge(7, 1, type = 'eContainingClass')
        
G_expected_added_ref_itself.add_edge(4, 1, type = 'eType')
G_expected_added_ref_itself.add_edge(5, 1, type = 'eType')
G_expected_added_ref_itself.add_edge(6, 1, type = 'eType')
G_expected_added_ref_itself.add_edge(7, 1, type = 'eType')

############################ add a reference that connects two classes
G_expected_added_ref = nx.MultiDiGraph()
G_expected_added_ref.add_node(0, type = 'EPackage')
G_expected_added_ref.add_node(1, type = 'EClass')
G_expected_added_ref.add_node(2, type = 'EClass')
G_expected_added_ref.add_node(4, type = 'EReference')
G_expected_added_ref.add_node(5, type = 'EReference')
G_expected_added_ref.add_node(6, type = 'EReference')
G_expected_added_ref.add_node(7, type = 'EReference')
        
G_expected_added_ref.add_edge(0, 1, type = 'eClassifiers')
G_expected_added_ref.add_edge(1, 0, type = 'ePackage')
G_expected_added_ref.add_edge(0, 2, type = 'eClassifiers')
G_expected_added_ref.add_edge(2, 0, type = 'ePackage')
        
G_expected_added_ref.add_edge(1, 4, type = 'eStructuralFeatures')
G_expected_added_ref.add_edge(1, 5, type = 'eStructuralFeatures')
G_expected_added_ref.add_edge(1, 6, type = 'eStructuralFeatures')
G_expected_added_ref.add_edge(1, 7, type = 'eStructuralFeatures')
G_expected_added_ref.add_edge(4, 1, type = 'eContainingClass')
G_expected_added_ref.add_edge(5, 1, type = 'eContainingClass')
G_expected_added_ref.add_edge(6, 1, type = 'eContainingClass')
G_expected_added_ref.add_edge(7, 1, type = 'eContainingClass')
        
G_expected_added_ref.add_edge(4, 1, type = 'eType')
G_expected_added_ref.add_edge(5, 1, type = 'eType')
G_expected_added_ref.add_edge(6, 1, type = 'eType')
G_expected_added_ref.add_edge(7, 2, type = 'eType')

############################ add eSuperType
G_expected_added_super = nx.MultiDiGraph()
G_expected_added_super.add_node(0, type = 'EPackage')
G_expected_added_super.add_node(1, type = 'EClass')
G_expected_added_super.add_node(2, type = 'EClass')
G_expected_added_super.add_node(4, type = 'EReference')
G_expected_added_super.add_node(5, type = 'EReference')
G_expected_added_super.add_node(6, type = 'EReference')

        
G_expected_added_super.add_edge(0, 1, type = 'eClassifiers')
G_expected_added_super.add_edge(1, 0, type = 'ePackage')
G_expected_added_super.add_edge(0, 2, type = 'eClassifiers')
G_expected_added_super.add_edge(2, 0, type = 'ePackage')
        
G_expected_added_super.add_edge(1, 4, type = 'eStructuralFeatures')
G_expected_added_super.add_edge(1, 5, type = 'eStructuralFeatures')
G_expected_added_super.add_edge(1, 6, type = 'eStructuralFeatures')
G_expected_added_super.add_edge(4, 1, type = 'eContainingClass')
G_expected_added_super.add_edge(5, 1, type = 'eContainingClass')
G_expected_added_super.add_edge(6, 1, type = 'eContainingClass')
        
G_expected_added_super.add_edge(4, 1, type = 'eType')
G_expected_added_super.add_edge(5, 1, type = 'eType')
G_expected_added_super.add_edge(6, 1, type = 'eType')
G_expected_added_super.add_edge(1, 2, type = 'eSuperTypes')

################ initial graph

G_initial = nx.MultiDiGraph()
G_initial.add_node(0, type = 'EPackage')
G_initial.add_node(1, type = 'EClass')
        
G_initial.add_edge(0, 1, type = 'eClassifiers')
G_initial.add_edge(1, 0, type = 'ePackage')


############### for graph2sequence
G_g2s = nx.MultiDiGraph()
G_g2s.add_node(0, type = 'EPackage')
G_g2s.add_node(1, type = 'EClass')
G_g2s.add_node(2, type = 'EClass')
G_g2s.add_node(4, type = 'EReference')

        
G_g2s.add_edge(0, 1, type = 'eClassifiers')
G_g2s.add_edge(1, 0, type = 'ePackage')
G_g2s.add_edge(0, 2, type = 'eClassifiers')
G_g2s.add_edge(2, 0, type = 'ePackage')
        
G_g2s.add_edge(1, 4, type = 'eStructuralFeatures')
G_g2s.add_edge(4, 1, type = 'eContainingClass')
        
G_g2s.add_edge(4, 1, type = 'eType')
G_g2s.add_edge(1, 2, type = 'eSuperTypes')


################ patterns for add a reference
pattern1_ref = nx.MultiDiGraph()
pattern1_ref.add_node(0, type = ['EClass'], ids = {0,1})
pattern1_ref.add_node(1, type = 'EReference')
pattern1_ref.add_edge(0, 1, type = 'eStructuralFeatures')
pattern1_ref.add_edge(1, 0, type = 'eContainingClass')
pattern1_ref.add_edge(1, 0, type = 'eType')
        
pattern2_ref = nx.MultiDiGraph()
pattern2_ref.add_node(0, type = ['EClass'], ids = {0})
pattern2_ref.add_node(1, type = 'EReference')
pattern2_ref.add_node(2, type = ['EClass'], ids = {1})
pattern2_ref.add_edge(0, 1, type = 'eStructuralFeatures')
pattern2_ref.add_edge(1, 0, type = 'eContainingClass')
pattern2_ref.add_edge(1, 2, type = 'eType')

################ patterns for add eSuperTypes

pattern1_st = nx.MultiDiGraph()
pattern1_st.add_node(0, type = ['EClass'], ids = {0})
pattern1_st.add_node(1, type = ['EClass'], ids = {1})
pattern1_st.add_edge(0, 1, type = 'eSuperTypes')

################ patterns for addClass

pattern1_ac = nx.MultiDiGraph()
pattern1_ac.add_node(0, type = ['EPackage'], ids = {0})
pattern1_ac.add_node(1, type = 'EClass')
pattern1_ac.add_edge(0, 1, type = 'eClassifiers')
pattern1_ac.add_edge(1, 0, type = 'ePackage')
