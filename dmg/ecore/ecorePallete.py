#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 15:35:02 2021

@author: Jose Antonio
"""

from dmg.edits.pallete import Pallete
import dmg.edits.editoperations as ed
import networkx as nx

dic_nodes_yak = {'EClass': 0,
                 'EReference': 1,
                 'EAttribute': 2,
                 'EPackage': 3,
                 'EDataType': 4,
                 'EEnum': 5,
                 'EEnumLiteral': 6}

dic_edges_yak = {'ePackage': 0,
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

