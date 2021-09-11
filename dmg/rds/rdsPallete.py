#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 10:35:58 2021

@author: Jose Antonio
"""


from dmg.edits.pallete import Pallete
import dmg.edits.editoperations as ed
import networkx as nx


dic_nodes_rds = {'Database': 0,
                 'Column': 1,
                 'Table': 2,
                 'Index': 3,
                 'IndexColumn': 4,
                 'Reference': 5}

dic_edges_rds = {'elements': 0,
                 'indexes': 1,
                 'columns': 2,
                 'indexColumns': 3,
                 'column': 4,
                 'primaryKeyColumns': 5,
                 'foreignKeyColumns': 6,
                 'primaryReferences': 7,
                 'foreignReferences': 8}


################ addTable

pattern_at = nx.MultiDiGraph()
pattern_at.add_node(0, type = ['Database'], ids = {0})
pattern_at.add_node(1, type = 'Table')
pattern_at.add_edge(0, 1, type = 'elements')
addTable = ed.EditOperation([pattern_at], [0])

################ addColumn

pattern_ac = nx.MultiDiGraph()
pattern_ac.add_node(0, type = ['Table'], ids = {0})
pattern_ac.add_node(1, type = 'Column')
pattern_ac.add_edge(0, 1, type = 'columns')
addColumn = ed.EditOperation([pattern_ac], [0])

################ addIndex

pattern_ai = nx.MultiDiGraph()
pattern_ai.add_node(0, type = ['Table'], ids = {0})
pattern_ai.add_node(1, type = 'Index')
pattern_ai.add_edge(0, 1, type = 'indexes')
addIndex = ed.EditOperation([pattern_ai], [0])
