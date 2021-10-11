#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 15:10:08 2021

@author: Jose Antonio
"""

import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf

class ModelSet:
    
    def __init__(self, name,
                 pathsRealMeta, 
                 pathsSynMeta,
                 bounds,
                 inconsistency,
                 preprocess,
                 operations,
                 dic_edges,
                 edges,
                 dic_nodes,
                 pallete,
                 realMetamodelName,
                 synMetamodelName,
                 rootReal,
                 rootSyn,
                 packageReal,
                 packageSyn):
        self.name = name
        self.pathsRealMeta = pathsRealMeta
        self.pathsSynMeta = pathsSynMeta
        self.bounds = bounds
        self.inconsistency = inconsistency
        self.operations = operations
        self.dic_edges = dic_edges
        self.edges = edges
        self.dic_nodes = dic_nodes
        self.pallete = pallete
        self.preprocess = preprocess
        self.realMetamodelName = realMetamodelName
        self.synMetamodelName = synMetamodelName
        self.rootReal = rootReal
        self.rootSyn = rootSyn
        self.packageReal = packageReal
        self.packageSyn = packageSyn
    
    def getGraphReal(self, f, backend):
        if backend.lower() == "java":
            return m2g.model2graphJava(self.name, f, 'real')
        elif backend.lower() == "python":
            metafilter_refs = self.edges
            metafilter_cla = list(self.dic_nodes.keys())
            metafilter_atts = None
            metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                     attributes = metafilter_atts,
                     classes = metafilter_cla)
            meta_models = self.pathsRealMeta
            return m2g.getGraphFromModel(f, meta_models, metafilterobj,
                                  consider_atts = False)
        
    def getGraphSyn(self, f, backend):
        if backend.lower() == "java":
            return m2g.model2graphJava(self.name, f, 'syn')
        elif backend.lower() == "python":
            metafilter_refs = self.edges
            metafilter_cla = list(self.dic_nodes.keys())
            metafilter_atts = None
            metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                     attributes = metafilter_atts,
                     classes = metafilter_cla)
            meta_models = self.pathsSynMeta
            return m2g.getGraphFromModel(f, meta_models, metafilterobj,
                                  consider_atts = False)

from dmg.yakindu.yakinduConsistency import inconsistent as icy
from dmg.ecore.ecoreConsistency import inconsistent as ice
from dmg.rds.rdsConsistency import inconsistent as icr
from dmg.yakindu.yakinduPreprocess import removeLayout
from dmg.rds.rdsPreprocess import removeTypes
from shutil import copyfile
import glob
import dmg.yakindu.yakinduPallete as yp
import dmg.ecore.ecorePallete as ecore
import dmg.rds.rdsPallete as rds

yakindu_github = ModelSet(name = 'yakindu-github',
                          pathsRealMeta = glob.glob("data/metamodels/yakinduComplete/*"), 
                          pathsSynMeta = ['data/metamodels/yakindu_simplified.ecore'],
                          bounds = (5, float('inf')),
                          inconsistency = icy,
                          preprocess = removeLayout,
                          operations = yp.dic_operations_yak,
                          dic_edges = yp.dic_edges_yak,
                          edges = yp.metafilter_refs,
                          dic_nodes = yp.dic_nodes_yak,
                          pallete = yp.yakindu_pallete,
                          realMetamodelName = 'sgraph.ecore',
                          synMetamodelName = 'yakindu_simplified.ecore',
                          rootReal = 'Statechart',
                          rootSyn = 'Statechart',
                          packageReal = 'sgraph',
                          packageSyn = 'yakindumm')

yakindu_exercise = ModelSet(name = 'yakindu-exercise',
                          pathsRealMeta =  ['data/metamodels/yakindu_simplified.ecore'], 
                          pathsSynMeta = ['data/metamodels/yakindu_simplified.ecore'],
                          bounds = (5, float('inf')),
                          inconsistency = icy,
                          preprocess = copyfile,
                          operations = yp.dic_operations_yak,
                          dic_edges = yp.dic_edges_yak,
                          edges = yp.metafilter_refs,
                          dic_nodes = yp.dic_nodes_yak,
                          pallete = yp.yakindu_pallete,
                          realMetamodelName = 'yakindu_simplified.ecore',
                          synMetamodelName = 'yakindu_simplified.ecore',
                          rootReal = 'Statechart',
                          rootSyn = 'Statechart',
                          packageReal = 'yakindumm',
                          packageSyn = 'yakindumm')

ecore_github = ModelSet(name = 'ecore-github',
                          pathsRealMeta = [], 
                          pathsSynMeta = ['data/metamodels/smallEcore.ecore'],
                          bounds = (3, 200),
                          inconsistency = ice,
                          preprocess = copyfile,
                          operations = ecore.dic_operations_ecore,
                          dic_edges = ecore.dic_edges_ecore,
                          edges = ecore.metafilter_refs,
                          dic_nodes = ecore.dic_nodes_ecore,
                          pallete = ecore.ecore_pallete,
                          realMetamodelName = 'Ecore.ecore',
                          synMetamodelName = 'smallEcore.ecore',
                          rootReal = 'EPackage',
                          rootSyn = 'EPackage',
                          packageReal = 'ecore',
                          packageSyn = 'smallEcore')

rds_genmymodel = ModelSet(name = 'rds-genmymodel',
                          pathsRealMeta = ['data/metamodels/rds_manual.ecore'], 
                          pathsSynMeta = ['data/metamodels/rdsSimplified.ecore'],
                          bounds = (7, float('inf')),
                          inconsistency = icr,
                          preprocess = removeTypes,
                          operations = rds.dic_operations_rds,
                          dic_edges = rds.dic_edges_rds,
                          edges = rds.metafilter_refs,
                          dic_nodes = rds.dic_nodes_rds,
                          pallete = rds.rds_pallete,
                          realMetamodelName = 'rds_manual.ecore',
                          synMetamodelName = 'rdsSimplified.ecore',
                          rootReal = 'Database',
                          rootSyn = 'Database',
                          packageReal = 'rds',
                          packageSyn = 'rdsSimplified')

datasets_supported = {
    'ecore-github': ecore_github,
    'rds-genmymodel': rds_genmymodel,
    'yakindu-github': yakindu_github,
    'yakindu-exercise': yakindu_exercise
    }