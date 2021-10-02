#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 15:08:38 2021

@author: Jose Antonio
"""

from dmg.edits.pallete import Pallete
import dmg.edits.editoperations as ed
import networkx as nx


dic_nodes_yak = {'Transition': 0,
                 'Region': 1,
                 'Statechart': 2,
                 'State': 3,
                 'FinalState': 4,
                 'Choice': 5,
                 'Entry': 6,
                 'Exit': 7,
                 'Synchronization': 8}

dic_edges_yak = {'vertices': 0,
                 'incomingTransitions': 1,
                 'outgoingTransitions': 2,
                 'target': 3,
                 'source': 4,
                 'regions': 5,
                 'vertices_inv': 6,
                 'regions_inv': 7
                 }


################ addRegion

pattern_ar = nx.MultiDiGraph()
pattern_ar.add_node(0, type = ['Statechart','State'], ids = {0})
pattern_ar.add_node(1, type = 'Region')
pattern_ar.add_edge(0, 1, type = 'regions')
addRegion = ed.EditOperation([pattern_ar], [0])

############### addState

pattern_as = nx.MultiDiGraph()
pattern_as.add_node(0, type = ['Region'], ids = {0})
pattern_as.add_node(1, type = 'State')
pattern_as.add_edge(0, 1, type = 'vertices')
addState = ed.EditOperation([pattern_as], [0])

############### addEntry

pattern_ae = nx.MultiDiGraph()
pattern_ae.add_node(0, type = ['Region'], ids = {0})
pattern_ae.add_node(1, type = 'Entry')
pattern_ae.add_edge(0, 1, type = 'vertices')
addEntry = ed.EditOperation([pattern_ae], [0])

############### addSynchronization

pattern_asyn = nx.MultiDiGraph()
pattern_asyn.add_node(0, type = ['Region'], ids = {0})
pattern_asyn.add_node(1, type = 'Synchronization')
pattern_asyn.add_edge(0, 1, type = 'vertices')
addSynchronization = ed.EditOperation([pattern_asyn], [0])


############### addChoice

pattern_ach = nx.MultiDiGraph()
pattern_ach.add_node(0, type = ['Region'], ids = {0})
pattern_ach.add_node(1, type = 'Choice')
pattern_ach.add_edge(0, 1, type = 'vertices')
addChoice = ed.EditOperation([pattern_ach], [0])

############### addExit

pattern_aex = nx.MultiDiGraph()
pattern_aex.add_node(0, type = ['Region'], ids = {0})
pattern_aex.add_node(1, type = 'Exit')
pattern_aex.add_edge(0, 1, type = 'vertices')
addExit = ed.EditOperation([pattern_aex], [0])

############### addFinalState

pattern_afs = nx.MultiDiGraph()
pattern_afs.add_node(0, type = ['Region'], ids = {0})
pattern_afs.add_node(1, type = 'FinalState')
pattern_afs.add_edge(0, 1, type = 'vertices')
addFinalState = ed.EditOperation([pattern_afs], [0])

############### addTransition

pattern_ati = nx.MultiDiGraph()
pattern_ati.add_node(0, type = ['State','Choice','Exit','FinalState',
                    'Synchronization'], ids = {0,1})
pattern_ati.add_node(1, type = 'Transition')
pattern_ati.add_edge(0, 1, type = 'outgoingTransitions')
pattern_ati.add_edge(1, 0, type = 'source')
pattern_ati.add_edge(1, 0, type = 'target')
pattern_ati.add_edge(0, 1, type = 'incomingTransitions')

pattern_at = nx.MultiDiGraph()
pattern_at.add_node(0, type = ['State','Choice','Exit','FinalState',
                    'Synchronization','Entry'], ids = {0})
pattern_at.add_node(1, type = 'Transition')
pattern_at.add_node(2, type = ['State','Choice','Exit','FinalState',
                    'Synchronization'], ids = {1})
pattern_at.add_edge(0, 1, type = 'outgoingTransitions')
pattern_at.add_edge(1, 0, type = 'source')
pattern_at.add_edge(1, 2, type = 'target')
pattern_at.add_edge(2, 1, type = 'incomingTransitions')

addTransition = ed.EditOperation([pattern_ati, pattern_at], [0,1])


dic_operations_yak = {
    0: addRegion,
    1: addState,
    2: addEntry,
    3: addSynchronization,
    4: addChoice,
    5: addExit,
    6: addFinalState,
    7: addTransition
    }

G_initial_yak = nx.MultiDiGraph()
G_initial_yak.add_node(0, type = 'Statechart')
G_initial_yak.add_node(1, type = 'Region')
G_initial_yak.add_edge(0, 1, type = 'regions')

yakindu_separator = '_'

metafilter_refs = ['Region.vertices', 
                   'CompositeElement.regions',
                   'Vertex.outgoingTransitions',
                   'Vertex.incomingTransitions',
                   'Transition.target',
                   'Transition.source']

yakindu_pallete = Pallete(dic_operations_yak, dic_nodes_yak, 
                          dic_edges_yak, [G_initial_yak])

max_len = 2