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
from sklearn.model_selection import train_test_split
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
import dmg.yakindu.yakinduPallete as yp
import ntpath

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
    ##load and remove small models
    
    metafilter_refs = None
    metafilter_cla = None
    metafilterobj = None
    meta_models = None
    metafilter_atts = None
    
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
    
    files = glob.glob(preprodataset_path +'/*')
    for f in files:
        G1 = m2g.getGraphFromModel(f, 
                              meta_models, metafilterobj,
                              consider_atts = False)
        if type_model.lower() == 'yakindu':
            if len(G1) < 5:
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
            