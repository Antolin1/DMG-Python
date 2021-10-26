# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 10:57:14 2021

@author: Jose Antonio
"""

import unittest
import tests.graphs4test as g4t
import dmg.yakindu.yakinduConsistency as conYAK
import dmg.rds.rdsConsistency as conRDS
import dmg.ecore.ecoreConsistency as conECORE

class TestConsistency(unittest.TestCase):
    
    def test_consistency_yakindu(self):
        #print('Test consistency')
        self.assertTrue(conYAK.noEntryRegion(g4t.G_yak_inco))
        self.assertFalse(conYAK.noEntryRegion(g4t.G_yak))
        
        self.assertTrue(conYAK.noStateRegion(g4t.G_yak_inco))
        self.assertFalse(conYAK.noStateRegion(g4t.G_yak))
        
        self.assertTrue(conYAK.multipleEntryRegion(g4t.G_yak_inco_2))
        self.assertFalse(conYAK.multipleEntryRegion(g4t.G_yak))
        
        self.assertTrue(conYAK.incomingToEntry(g4t.G_yak_inco_2))
        self.assertFalse(conYAK.incomingToEntry(g4t.G_yak))
        
        self.assertTrue(conYAK.choice(g4t.G_yak_inco_2))
        self.assertFalse(conYAK.choice(g4t.G_yak))
        #entryOutTran
        self.assertTrue(conYAK.entryOutTran(g4t.G_yak_inco_3))
        self.assertFalse(conYAK.entryOutTran(g4t.G_yak))
        
        self.assertTrue(conYAK.exitFinal(g4t.G_yak_inco_3))
        self.assertFalse(conYAK.exitFinal(g4t.G_yak))
        
        self.assertFalse(conYAK.exitFinal(g4t.G_yak))
        
        self.assertTrue(conYAK.inconsistent(g4t.G_yak_inco_2))
        self.assertTrue(conYAK.inconsistent(g4t.G_yak_inco_3))
        self.assertTrue(conYAK.inconsistent(g4t.G_yak_inco))
        
    def test_consistency_rds(self):
        self.assertTrue(conRDS.inconsistenceEqualRefs(g4t.rds_inco))
        self.assertTrue(conRDS.inconsistenceIcCons(g4t.rds_inco))
        self.assertTrue(conRDS.ref2thesameColumn(g4t.rds_inco))
        self.assertTrue(conRDS.inconsistent(g4t.rds_inco))
        self.assertFalse(conRDS.inconsistenceIcCons(g4t.G_rds))
        self.assertFalse(conRDS.inconsistenceEqualRefs(g4t.G_rds))
        self.assertFalse(conRDS.ref2thesameColumn(g4t.G_rds))
        self.assertFalse(conRDS.inconsistent(g4t.G_rds))
    
    def test_consistency_ecore(self):
        self.assertFalse(conECORE.inconsistent(g4t.G_test_small_ecore))
        self.assertFalse(conECORE.inconsistent(g4t.G_ecore_inco_correct))
        self.assertTrue(conECORE.inconsistent(g4t.G_ecore_inco))
        self.assertTrue(conECORE.inconsistent(g4t.G_ecore_inco_2))
        self.assertTrue(conECORE.restrictionOpposite(g4t.G_ecore_inco))
        self.assertTrue(conECORE.opositeOfItself(g4t.G_ecore_inco))
        self.assertTrue(conECORE.restrictionSameClasses(g4t.G_ecore_inco_2))
        self.assertFalse(conECORE.restrictionSameClasses(g4t.G_ecore_inco_correct))
        self.assertTrue(conECORE.referenceDoesNotHaveType(g4t.G_ecore_inco))
        self.assertTrue(conECORE.referenceDoesNotHaveType(g4t.G_ecore_inco_2))
        self.assertTrue(conECORE.attributeDoesNotHaveType(g4t.G_ecore_inco_2))
        self.assertTrue(conECORE.attributeDoesNotHaveType(g4t.G_ecore_inco))
        
    
        