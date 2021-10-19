#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 17:25:42 2021

@author: Jose Antonio
"""

import unittest
import tests.graphs4test as g4t
import dmg.graphUtils as gu
import dmg.realism.metrics as m

class TestMetrics(unittest.TestCase):
    
    def test_degree(self):
        list_deg = m.getListDegree(g4t.G_testEcore)
        self.assertEqual(len(list_deg), 4)
        self.assertTrue(6 in list_deg)
        self.assertTrue(3 in list_deg)
        self.assertTrue(3 in list_deg)
        self.assertTrue(2 in list_deg)
        
        list_deg_out = m.getListOutDegree(g4t.G_testEcore)
        self.assertEqual(len(list_deg_out), 4)
        self.assertTrue(3 in list_deg_out)
        self.assertTrue(1 in list_deg_out)
        self.assertTrue(2 in list_deg_out)
        self.assertTrue(1 in list_deg_out)
        
        list_deg_in = m.getListInDegree(g4t.G_testEcore)
        self.assertEqual(len(list_deg_in), 4)
        self.assertTrue(3 in list_deg_in)
        self.assertTrue(1 in list_deg_in)
        self.assertTrue(2 in list_deg_in)
        self.assertTrue(1 in list_deg_in)
    
    def test_refMetrics(self):
         dims = ['eClassifiers','ePackage','eSuperTypes']
         dds = m.dimensionalDegree(g4t.G_testEcore, 'eClassifiers', dims)
         self.assertEqual(len(dds), 4)
         self.assertTrue(3 in dds)
         self.assertTrue(1 in dds)
         self.assertTrue(not 2 in dds)
         
         dds = m.dimensionalDegree(g4t.G_testEcore, 'eSuperTypes', dims)
         self.assertEqual(len(dds), 4)
         self.assertTrue(not 3 in dds)
         self.assertTrue(1 in dds)
         self.assertTrue(0 in dds)
         self.assertTrue(set([0,1])== set(dds))
         
         self.assertTrue({0: 0.75, 1: 1.0, 2: 1.0, 3: 0.75} 
                         == m.MPC(g4t.G_testEcore, dims))
         
         nas = m.nodeActivity(g4t.G_testEcore, dims)
         self.assertEqual(len(nas), 4)
         self.assertEqual(set(nas),{float(2)/len(dims),float(3)/len(dims)})
