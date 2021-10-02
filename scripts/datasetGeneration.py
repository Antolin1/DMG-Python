#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 15:55:53 2021

@author: Jose Antonio
"""
import sys
import os
sys.path.append(os.getcwd())

import glob
from pathlib import Path
from shutil import copyfile
from dmg.yakindu.yakinduPreprocess import removeLayout
from dmg.rds.rdsPreprocess import removeTypes
from sklearn.model_selection import train_test_split
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
import dmg.yakindu.yakinduPallete as yp
import dmg.rds.rdsPallete as rds
import dmg.ecore.ecorePallete as ecore
import ntpath
import dmg.graphUtils as gu
from networkx.algorithms.isomorphism import is_isomorphic

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

def getPallete(dataset):
    if dataset.lower() == 'yakindu-github':
        return yp.yakindu_pallete
    elif dataset.lower() == 'yakindu-exercise':
        return yp.yakindu_pallete
    elif dataset.lower() == 'ecore-github':
        return ecore.ecore_pallete
    elif dataset.lower() == 'rds-genmymodel':
        return rds.rds_pallete

def main():
    
    dataset_path = sys.argv[1]
    dataset = sys.argv[2]
    backend = sys.argv[3]
    
    raw_path = dataset_path + '/' + 'raw'
    preprodataset_path = dataset_path + '/' + 'preprocess'
    train_path = dataset_path + '/' + 'train'
    test_path = dataset_path + '/' + 'test'
    
    if not os.path.exists(preprodataset_path):
        os.makedirs(preprodataset_path)
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    if not os.path.exists(test_path):
        os.makedirs(test_path)
    
    #PREPROCESS
    files = glob.glob(raw_path +'/*')
    for f in files:
        p = Path(f)
        full_file_name = p.stem +'.'+f.split('.')[-1]
        preprocess = getPreprocess(dataset)
        preprocess(f,preprodataset_path+'/'+full_file_name)
    
    
    #CHECK SEQ GENERATION AND BOUNDS
    files = glob.glob(preprodataset_path +'/*')
    for f in files:
        #TODO: solve exception in RDS and develop and take a good metamodel for RDS
        #TODO: solve exception in ecore, this is caused by proxy elements. 
        #Elements defined in the model that are in other models.
        #TODO: too big ecore models too slow
        #TODO: deal with instanceClassName="java.lang.Integer" in eattributes
        G1 = None
        try:
            G1 = getGraph(f, dataset, backend)
        except: # Exception as e:
            #print(e.with_traceback())
            print('Remove exception m2g in', f)
            os.remove(f)
            continue
        
        lower, upper = getUpperLower(dataset)
        if len(G1) < lower or len(G1) > upper:
            os.remove(f)
            print('Remove out of bounds in', f)
            continue
        
        pallete = getPallete(dataset)
        G_initials = pallete.initialGraphs
        #remove models that cannot be reached
        seq = pallete.graphToSequence(G1)
        is_iso = False
        if len(seq) == 0:
            print('Remove Seq 0 in', f)
            os.remove(f)
            continue
        
        for G_initial in G_initials:
            if is_isomorphic(G_initial, 
                    seq[-1][0], 
                    gu.node_match_type, 
                    gu.edge_match_type):
                is_iso = True
        
        if not is_iso:
            print('Remove not iso:', f)
            os.remove(f)
        
    #TRAIN TEST SPLIT
    files = glob.glob(preprodataset_path +'/*')
    train, test =  train_test_split(files, test_size=0.3, random_state=42)
    
    for f in train:
        copyfile(f, train_path+'/'+ntpath.basename(f))
    for f in test:
        copyfile(f, test_path+'/'+ntpath.basename(f))
    
            
if __name__ == "__main__":
    main()
            