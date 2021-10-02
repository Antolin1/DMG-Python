#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 15:57:58 2021

@author: Jose Antonio
"""

import unittest
import subprocess
import pygraphviz
from networkx.drawing import nx_agraph
import dmg.graphUtils as gu
from networkx.algorithms.isomorphism import is_isomorphic
import tests.graphs4test as g4t
import dmg.model2graph.model2graph as m2g

class Testm2gJava(unittest.TestCase):
    
    def test_ecoreJava(self):
        #print('TODO')
        x = subprocess.Popen(["java", "-jar", 
                              "java/model2graph/target/model2graph-0.0.1-jar-with-dependencies.jar", "ecore-github", 
                              "data/testmodels/testEcore.ecore"], 
                             stderr=subprocess.PIPE, 
                             stdout=subprocess.PIPE,
                             text=True)
        out,err = x.communicate()
        #print(out)
        #print(err)
        G = nx_agraph.from_agraph(pygraphviz.AGraph(out))
        G = gu.fixDotGraph(G)
        #print(G.edges(data=True))
        #print(G.nodes(data=True))
        
        self.assertTrue(is_isomorphic(G, g4t.G_testEcore, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        
        self.assertTrue(is_isomorphic(m2g.model2graphJava('ecore-github',
                                                      "data/testmodels/testEcore.ecore"), g4t.G_testEcore, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
        
    def test_rdsJava(self):
        x = subprocess.Popen(["java", "-jar", 
                              "java/model2graph/target/model2graph-0.0.1-jar-with-dependencies.jar", "rds-genmymodel", 
                              "data/testmodels/testRDS.xmi"], 
                             stderr=subprocess.PIPE, 
                             stdout=subprocess.PIPE,
                             text=True)
        out,err = x.communicate()
        #print(out)
        #print(err)
        G = nx_agraph.from_agraph(pygraphviz.AGraph(out))
        G = gu.fixDotGraph(G)
        #print(G.edges(data=True))
        #print(G.nodes(data=True))
            
        self.assertTrue(is_isomorphic(G, g4t.G_rds, 
                                          gu.node_match_type, 
                                          gu.edge_match_type))
        self.assertTrue(is_isomorphic(m2g.model2graphJava('rds-genmymodel',
                                                      "data/testmodels/testRDS.xmi"), g4t.G_rds, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
    
    def test_yakinduJava(self):
        G1 = m2g.model2graphJava('yakindu-github', "data/testmodels/outYak.xmi")
        self.assertTrue(is_isomorphic(G1, g4t.G_yak, 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
    

