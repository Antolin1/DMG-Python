# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 10:57:14 2021

@author: Jose Antonio
"""

import unittest
import tests.graphs4test as g4t
import dmg.yakindu.yakinduConsistency as con
import dmg.rds.rdsConsistency as conRDS

class TestConsistency(unittest.TestCase):
    
    def test_consistency_yakindu(self):
        #print('Test consistency')
        self.assertTrue(con.noEntryRegion(g4t.G_yak_inco))
        self.assertFalse(con.noEntryRegion(g4t.G_yak))
        
        self.assertTrue(con.noStateRegion(g4t.G_yak_inco))
        self.assertFalse(con.noStateRegion(g4t.G_yak))
        
        self.assertTrue(con.multipleEntryRegion(g4t.G_yak_inco_2))
        self.assertFalse(con.multipleEntryRegion(g4t.G_yak))
        
        self.assertTrue(con.incomingToEntry(g4t.G_yak_inco_2))
        self.assertFalse(con.incomingToEntry(g4t.G_yak))
        
        self.assertTrue(con.choice(g4t.G_yak_inco_2))
        self.assertFalse(con.choice(g4t.G_yak))
        #entryOutTran
        self.assertTrue(con.entryOutTran(g4t.G_yak_inco_3))
        self.assertFalse(con.entryOutTran(g4t.G_yak))
        
        self.assertTrue(con.exitFinal(g4t.G_yak_inco_3))
        self.assertFalse(con.exitFinal(g4t.G_yak))
        
        self.assertFalse(con.exitFinal(g4t.G_yak))
        
        self.assertTrue(con.inconsistent(g4t.G_yak_inco_2))
        self.assertTrue(con.inconsistent(g4t.G_yak_inco_3))
        self.assertTrue(con.inconsistent(g4t.G_yak_inco))
        
    def test_consistency_rds(self):
        self.assertTrue(conRDS.inconsistenceEqualRefs(g4t.rds_inco))
        self.assertTrue(conRDS.inconsistenceIcCons(g4t.rds_inco))
        self.assertFalse(conRDS.inconsistenceIcCons(g4t.G_rds))
        self.assertFalse(conRDS.inconsistenceEqualRefs(g4t.G_rds))
        