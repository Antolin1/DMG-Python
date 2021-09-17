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
import ntpath
import dmg.graphUtils as gu
from networkx.algorithms.isomorphism import is_isomorphic

def main():
    dataset_path = sys.argv[1]
    preprodataset_path = sys.argv[2]
    train_path = sys.argv[3]
    test_path = sys.argv[4]
    val_path = sys.argv[5]
    type_model = sys.argv[6]
    
    if not os.path.exists(preprodataset_path):
        os.makedirs(preprodataset_path)
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    if not os.path.exists(test_path):
        os.makedirs(test_path)
    if not os.path.exists(val_path):
        os.makedirs(val_path)
    
    files = glob.glob(dataset_path +'/*')
    ##delete layout
    for f in files:
        p = Path(f)
        full_file_name = p.stem +'.'+f.split('.')[-1]
        if type_model.lower() == 'yakindu':
            removeLayout(f,preprodataset_path+'/'+full_file_name)
        elif type_model.lower() == 'rds':
            removeTypes(f,preprodataset_path+'/'+full_file_name)
    ##load and remove small models
    
    metafilter_refs = None
    metafilter_cla = None
    metafilterobj = None
    meta_models = None
    metafilter_atts = None
    pallete = None
    G_initial = None
    
    if type_model.lower() == 'yakindu':
        metafilter_refs = ['Region.vertices', 
                               'CompositeElement.regions',
                               'Vertex.outgoingTransitions',
                               'Vertex.incomingTransitions',
                               'Transition.target',
                               'Transition.source']
        metafilter_cla = list(yp.dic_nodes_yak.keys())
            
        metafilter_atts = None
            
        metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                     attributes = metafilter_atts,
                     classes = metafilter_cla)
            
        meta_models = glob.glob("data/metamodels/yakinduComplete/*")
        
        pallete = yp.yakindu_pallete
        G_initial= yp.G_initial_yak
        
    elif type_model.lower() == 'rds':
        metafilter_refs = ['Database.elements', 
                           'Table.indexes',
                           'Table.columns',
                           'Index.indexColumns',
                           'IndexColumn.column',
                           'Reference.primaryKeyColumns',
                           'Reference.foreignKeyColumns',
                           'Column.primaryReferences',
                           'Column.foreignReferences']
        metafilter_cla = ['Database', 'Column','Table',
                          'Index', 'IndexColumn','Reference']  
        metafilter_atts = None
        metafilterobj = mf.MetaFilter(references = metafilter_refs, 
                     attributes = metafilter_atts,
                     classes = metafilter_cla)
        meta_models = ['data/metamodels/rds_manual.ecore']
        pallete = rds.rds_pallete
        G_initial= rds.G_initial_rds
    
    files = glob.glob(preprodataset_path +'/*')
    for f in files:
        #TODO: solve exception in RDS and develop and take a good metamodel for RDS
        try:
            G1 = m2g.getGraphFromModel(f, 
                                  meta_models, metafilterobj,
                                  consider_atts = False)
        except Exception as e:
            print(e)
            print('Exception m2g in', f)
            #os.remove(f)
            continue
        if type_model.lower() == 'yakindu':
            if len(G1) < 5:
                os.remove(f)
        if type_model.lower() == 'rds':
            if len(G1) < 7:
                os.remove(f)
        
        #remove models that cannot be reached
        seq = pallete.graphToSequence(G1)
        if not is_isomorphic(G_initial, 
                seq[-1][0], 
                gu.node_match_type, 
                gu.edge_match_type):
            os.remove(f)
        
    
    files = glob.glob(preprodataset_path +'/*')
    #train/test/val split
    train_v, test =  train_test_split(files, test_size=0.3, random_state=42)
    train, val =  train_test_split(train_v, test_size=0.2, random_state=42)
    
    for f in train:
        copyfile(f, train_path+'/'+ntpath.basename(f))
    for f in test:
        copyfile(f, test_path+'/'+ntpath.basename(f))
    for f in val:
        copyfile(f, val_path+'/'+ntpath.basename(f))
            
if __name__ == "__main__":
    main()
            