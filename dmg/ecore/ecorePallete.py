#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 15:35:02 2021

@author: Jose Antonio
"""

from dmg.edits.pallete import Pallete
import dmg.edits.editoperations as ed
import networkx as nx

dic_nodes_ecore = {'EClass': 0,
                 'EReference': 1,
                 'EAttribute': 2,
                 'EPackage': 3,
                 'EDataType': 4,
                 'EEnum': 5,
                 'EEnumLiteral': 6}

dic_edges_ecore = {'ePackage': 0,
                 'eStructuralFeatures': 1,
                 'eSuperTypes': 2,
                 'eType': 3,
                 'eContainingClass': 4,
                 'eClassifiers': 5,
                 'eLiterals': 6,
                 'eEnum': 7,
                 'eOpposite': 8,
                 'eType_inv': 9,
                 'eOpposite_inv': 10
                 }


################ addClass

pattern_ac = nx.MultiDiGraph()
pattern_ac.add_node(0, type = ['EPackage'], ids = {0})
pattern_ac.add_node(1, type = 'EClass')
pattern_ac.add_edge(0, 1, type = 'eClassifiers')
pattern_ac.add_edge(1, 0, type = 'ePackage')
addClass = ed.EditOperation([pattern_ac], [0])

################ addDataType

pattern_ad = nx.MultiDiGraph()
pattern_ad.add_node(0, type = ['EPackage'], ids = {0})
pattern_ad.add_node(1, type = 'EDataType')
pattern_ad.add_edge(0, 1, type = 'eClassifiers')
pattern_ad.add_edge(1, 0, type = 'ePackage')
addDatatype = ed.EditOperation([pattern_ad], [0])


################ addEnum

pattern_ae = nx.MultiDiGraph()
pattern_ae.add_node(0, type = ['EPackage'], ids = {0})
pattern_ae.add_node(1, type = 'EEnum')
pattern_ae.add_edge(0, 1, type = 'eClassifiers')
pattern_ae.add_edge(1, 0, type = 'ePackage')
addEnum = ed.EditOperation([pattern_ae], [0])

################ addLiteral

pattern_al = nx.MultiDiGraph()
pattern_al.add_node(0, type = ['EEnum'], ids = {0})
pattern_al.add_node(1, type = 'EEnumLiteral')
pattern_al.add_edge(0, 1, type = 'eLiterals')
pattern_al.add_edge(1, 0, type = 'eEnum')
addLiteral = ed.EditOperation([pattern_al], [0])

################ addSuperType

pattern_as = nx.MultiDiGraph()
pattern_as.add_node(0, type = ['EClass'], ids = {0})
pattern_as.add_node(1, type = ['EClass'], ids = {1})
pattern_as.add_edge(0, 1, type = 'eSuperTypes')
addSuperType = ed.EditOperation([pattern_as], [0,1])

#TODO: add the rest of edit ops and put a set of graphs as intial graphs in the pallete

################ addReference

pattern_ar = nx.MultiDiGraph()
pattern_ar.add_node(0, type = ['EClass'], ids = {0})
pattern_ar.add_node(1, type = ['EClass'], ids = {1})
pattern_ar.add_node(2, type = 'EReference')
pattern_ar.add_edge(0, 2, type = 'eStructuralFeatures')
pattern_ar.add_edge(2, 0, type = 'eContainingClass')
pattern_ar.add_edge(2, 1, type = 'eType')

pattern_ar_it = nx.MultiDiGraph()
pattern_ar_it.add_node(0, type = ['EClass'], ids = {0,1})
pattern_ar_it.add_node(1, type = 'EReference')
pattern_ar_it.add_edge(0, 1, type = 'eStructuralFeatures')
pattern_ar_it.add_edge(1, 0, type = 'eContainingClass')
pattern_ar_it.add_edge(1, 0, type = 'eType')

addReference = ed.EditOperation([pattern_ar, pattern_ar_it], [0,1])

################ addReferenceEOpposite

pattern_areo = nx.MultiDiGraph()
pattern_areo.add_node(0, type = ['EClass'], ids = {0})
pattern_areo.add_node(1, type = ['EClass'], ids = {1})
pattern_areo.add_node(2, type = 'EReference')
pattern_areo.add_node(3, type = 'EReference')
pattern_areo.add_edge(0, 2, type = 'eStructuralFeatures')
pattern_areo.add_edge(2, 0, type = 'eContainingClass')
pattern_areo.add_edge(2, 1, type = 'eType')
pattern_areo.add_edge(1, 3, type = 'eStructuralFeatures')
pattern_areo.add_edge(3, 1, type = 'eContainingClass')
pattern_areo.add_edge(3, 0, type = 'eType')
pattern_areo.add_edge(3, 2, type = 'eOpposite')
pattern_areo.add_edge(2, 3, type = 'eOpposite')

pattern_areo_it = nx.MultiDiGraph()
pattern_areo_it.add_node(0, type = ['EClass'], ids = {0,1})
pattern_areo_it.add_node(1, type = 'EReference')
pattern_areo_it.add_node(2, type = 'EReference')
pattern_areo_it.add_edge(0, 1, type = 'eStructuralFeatures')
pattern_areo_it.add_edge(1, 0, type = 'eContainingClass')
pattern_areo_it.add_edge(1, 0, type = 'eType')
pattern_areo_it.add_edge(0, 2, type = 'eStructuralFeatures')
pattern_areo_it.add_edge(2, 0, type = 'eContainingClass')
pattern_areo_it.add_edge(2, 0, type = 'eType')
pattern_areo_it.add_edge(2, 1, type = 'eOpposite')
pattern_areo_it.add_edge(1, 2, type = 'eOpposite')

addReferenceEOpposite = ed.EditOperation([pattern_areo, pattern_areo_it], [0,1])


############# addEAttribute

pattern_aea = nx.MultiDiGraph()
pattern_aea.add_node(0, type = ['EClass'], ids = {0})
pattern_aea.add_node(1, type = ['EDataType', 'EEnum'], ids = {1})
pattern_aea.add_node(2, type = 'EAttribute')
pattern_aea.add_edge(0, 2, type = 'eStructuralFeatures')
pattern_aea.add_edge(2, 0, type = 'eContainingClass')
pattern_aea.add_edge(2, 1, type = 'eType')

addEAttribute = ed.EditOperation([pattern_aea], [0,1])

dic_operations_ecore = {
    0: addEAttribute,
    1: addReference,
    2: addSuperType,
    3: addLiteral,
    4: addEnum,
    5: addDatatype,
    6: addClass,
    7: addReferenceEOpposite
    }

G_initial_ecore_1 = nx.MultiDiGraph()
G_initial_ecore_1.add_node(0, type = 'EPackage')
G_initial_ecore_1.add_node(1, type = 'EClass')
G_initial_ecore_1.add_edge(0, 1, type = 'eClassifiers')
G_initial_ecore_1.add_edge(1, 0, type = 'ePackage')

G_initial_ecore_2 = nx.MultiDiGraph()
G_initial_ecore_2.add_node(0, type = 'EPackage')
G_initial_ecore_2.add_node(1, type = 'EDataType')
G_initial_ecore_2.add_edge(0, 1, type = 'eClassifiers')
G_initial_ecore_2.add_edge(1, 0, type = 'ePackage')

G_initial_ecore_3 = nx.MultiDiGraph()
G_initial_ecore_3.add_node(0, type = 'EPackage')
G_initial_ecore_3.add_node(1, type = 'EEnum')
G_initial_ecore_3.add_edge(0, 1, type = 'eClassifiers')
G_initial_ecore_3.add_edge(1, 0, type = 'ePackage')

ecore_separator = '_'

ecore_pallete = Pallete(dic_operations_ecore, dic_nodes_ecore, 
                          dic_edges_ecore, [G_initial_ecore_1,
                                          G_initial_ecore_2,
                                          G_initial_ecore_3])
