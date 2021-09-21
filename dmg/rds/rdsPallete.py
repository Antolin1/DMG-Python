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
                 'foreignReferences': 8,
                 'elements_inv': 9,
                 'indexes_inv': 10,
                 'columns_inv': 11,
                 'indexColumns_inv': 12,
                 'column_inv': 13
                 }


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

################ addIndexColumn

pattern_aic = nx.MultiDiGraph()
pattern_aic.add_node(0, type = ['Index'], ids = {0})
pattern_aic.add_node(1, type = 'IndexColumn')
#pattern_aic.add_node(2, type = ['Column'], ids = {1})
pattern_aic.add_edge(0, 1, type = 'indexColumns')
#pattern_aic.add_edge(1, 2, type = 'column')
addIndexColumn = ed.EditOperation([pattern_aic], [0])

################ addColumntoIC

pattern_aic2c = nx.MultiDiGraph()
pattern_aic2c.add_node(0, type = ['IndexColumn'], ids = {0})
pattern_aic2c.add_node(1, type = ['Column'], ids = {1})
pattern_aic2c.add_edge(0, 1, type = 'column')
addColumntoIC = ed.EditOperation([pattern_aic2c], [0, 1])

################ addReference

pattern_ref = nx.MultiDiGraph()
pattern_ref.add_node(0, type = ['Column'], ids = {0})
pattern_ref.add_node(1, type = 'Reference')
pattern_ref.add_node(2, type = ['Column'], ids = {1})
pattern_ref.add_node(3, type = ['Database'], ids = {2})
pattern_ref.add_edge(0, 1, type = 'primaryReferences')
pattern_ref.add_edge(1, 2, type = 'foreignKeyColumns')
pattern_ref.add_edge(1, 0, type = 'primaryKeyColumns')
pattern_ref.add_edge(2, 1, type = 'foreignReferences')
pattern_ref.add_edge(3, 1, type = 'elements')
addReference = ed.EditOperation([pattern_ref], [0,1,2])


dic_operations_rds = {
    0: addReference,
    1: addIndexColumn,
    2: addIndex,
    3: addColumn,
    4: addTable,
    5: addColumntoIC
    }

G_initial_rds = nx.MultiDiGraph()
G_initial_rds.add_node(0, type = 'Database')
G_initial_rds.add_node(1, type = 'Table')
G_initial_rds.add_edge(0, 1, type = 'elements')

rds_pallete = Pallete(dic_operations_rds, dic_nodes_rds, 
                          dic_edges_rds, [G_initial_rds])

rds_separator = '_'