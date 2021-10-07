#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 14:46:52 2021

@author: Jose Antonio
"""

import os
import sys

sys.path.append(os.getcwd())

import dmg.yakindu.yakinduPallete as yp
import dmg.ecore.ecorePallete as ecore
import dmg.rds.rdsPallete as rds

def getSeparator(dataset):
    if dataset.lower() == 'yakindu-github':
        return yp.yakindu_separator
    elif dataset.lower() == 'yakindu-exercise':
        return yp.yakindu_separator
    elif dataset.lower() == 'ecore-github':
        return ecore.ecore_separator
    elif dataset.lower() == 'rds-genmymodel':
        return rds.rds_separator

def getMaxLen(dataset):
    if dataset.lower() == 'yakindu-github':
        return yp.max_len
    elif dataset.lower() == 'yakindu-exercise':
        return yp.max_len
    elif dataset.lower() == 'ecore-github':
        return ecore.max_len
    elif dataset.lower() == 'rds-genmymodel':
        return rds.max_len
    
def getDicNodes(dataset):
    if dataset.lower() == 'yakindu-github':
        return yp.dic_nodes_yak
    elif dataset.lower() == 'yakindu-exercise':
        return yp.dic_nodes_yak
    elif dataset.lower() == 'ecore-github':
        return ecore.dic_nodes_ecore
    elif dataset.lower() == 'rds-genmymodel':
        return rds.dic_nodes_rds

def getDicEdges(dataset):
    if dataset.lower() == 'yakindu-github':
        return yp.dic_edges_yak
    elif dataset.lower() == 'yakindu-exercise':
        return yp.dic_edges_yak
    elif dataset.lower() == 'ecore-github':
        return ecore.dic_edges_ecore
    elif dataset.lower() == 'rds-genmymodel':
        return rds.dic_edges_rds
    
def getDicOperations(dataset):
    if dataset.lower() == 'yakindu-github':
        return yp.dic_operations_yak
    elif dataset.lower() == 'yakindu-exercise':
        return yp.dic_operations_yak
    elif dataset.lower() == 'ecore-github':
        return ecore.dic_operations_ecore
    elif dataset.lower() == 'rds-genmymodel':
        return rds.dic_operations_rds

def getMetamodel(dataset):
    if dataset.lower() == 'yakindu-github':
        return 'yakindu_simplified.ecore'
    elif dataset.lower() == 'yakindu-exercise':
        return 'yakindu_simplified.ecore'
    elif dataset.lower() == 'ecore-github':
        return 'smallEcore.ecore'
    elif dataset.lower() == 'rds-genmymodel':
        return 'rdsSimplified.ecore'
    
def getRoot(dataset):
    if dataset.lower() == 'yakindu-github':
        return 'Statechart'
    elif dataset.lower() == 'yakindu-exercise':
        return 'Statechart'
    elif dataset.lower() == 'ecore-github':
        return 'EPackage'
    elif dataset.lower() == 'rds-genmymodel':
        return 'Database'

def getPackage(dataset):
    if dataset.lower() == 'yakindu-github':
        return 'yakindumm'
    elif dataset.lower() == 'yakindu-exercise':
        return 'yakindumm'
    elif dataset.lower() == 'ecore-github':
        return 'smallEcore'
    elif dataset.lower() == 'rds-genmymodel':
        return 'rds'

from dmg.yakindu.yakinduConsistency import inconsistent as icy
from dmg.ecore.ecoreConsistency import inconsistent as ice
from dmg.rds.rdsConsistency import inconsistent as icr

def getInconsistent(dataset):
    if dataset.lower() == 'yakindu-github':
        return icy
    elif dataset.lower() == 'yakindu-exercise':
        return icy
    elif dataset.lower() == 'ecore-github':
        return ice
    elif dataset.lower() == 'rds-genmymodel':
        return icr
    
from dmg.yakindu.yakinduPreprocess import removeLayout
from dmg.rds.rdsPreprocess import removeTypes
from shutil import copyfile
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
import glob

def getPreprocess(dataset):
    if dataset.lower() == 'yakindu-github':
        return removeLayout
    elif dataset.lower() == 'yakindu-exercise':
        return copyfile
    elif dataset.lower() == 'ecore-github':
        return copyfile
    elif dataset.lower() == 'rds-genmymodel':
        return removeTypes

def getUpperLower(dataset):
    if dataset.lower() == 'yakindu-github':
        return (5, float('inf'))
    elif dataset.lower() == 'yakindu-exercise':
        return (5, float('inf'))
    elif dataset.lower() == 'ecore-github':
        return (3, 200)
    elif dataset.lower() == 'rds-genmymodel':
        return (7, float('inf'))

def getGraph(f, dataset, backend):
    if backend.lower() == "java":
        return m2g.model2graphJava(dataset.lower(), f)
    elif backend.lower() == "python":
        metafilter_refs = None
        metafilter_cla = None
        metafilterobj = None
        meta_models = None
        metafilter_atts = None
        if dataset.lower() == 'yakindu-github':
            metafilter_refs = yp.metafilter_refs
            metafilter_cla = list(yp.dic_nodes_yak.keys())
            metafilter_atts = None
            metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                     attributes = metafilter_atts,
                     classes = metafilter_cla)
            meta_models = glob.glob("data/metamodels/yakinduComplete/*")
        
        elif dataset.lower() == 'yakindu-exercise':
            metafilter_refs = yp.metafilter_refs
            metafilter_cla = list(yp.dic_nodes_yak.keys())
            metafilter_atts = None
            metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                     attributes = metafilter_atts,
                     classes = metafilter_cla)
            meta_models = ['data/metamodels/yakindu_simplified.ecore']
            
        elif dataset.lower() == 'ecore-github':
            metafilter_refs = ecore.metafilter_refs
            metafilter_cla = list(ecore.dic_nodes_ecore.keys())
            metafilter_atts = None
            metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                     attributes = metafilter_atts,
                     classes = metafilter_cla)
            meta_models = []  
            
        elif dataset.lower() == 'rds-genmymodel':
            metafilter_refs = rds.metafilter_refs
            metafilter_cla = list(rds.dic_nodes_rds.keys())
            metafilter_atts = None
            metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                     attributes = metafilter_atts,
                     classes = metafilter_cla)
            meta_models = ['data/metamodels/rds_manual.ecore']
        
        return m2g.getGraphFromModel(f, meta_models, metafilterobj,
                                  consider_atts = False)

def getGraphOfBaselines(f, dataset, backend):
    if backend.lower() == "java":
        return m2g.model2graphJava(dataset.lower(), f)
    elif backend.lower() == "python":
        if dataset.lower() == 'yakindu-github':
            return getGraph(f, 'yakindu-exercise', backend)
        else:
            return getGraph(f, dataset, backend)
        
        
    

def getPallete(dataset):
    if dataset.lower() == 'yakindu-github':
        return yp.yakindu_pallete
    elif dataset.lower() == 'yakindu-exercise':
        return yp.yakindu_pallete
    elif dataset.lower() == 'ecore-github':
        return ecore.ecore_pallete
    elif dataset.lower() == 'rds-genmymodel':
        return rds.rds_pallete
