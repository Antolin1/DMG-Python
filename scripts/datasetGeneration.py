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
from sklearn.model_selection import train_test_split
import ntpath
import dmg.graphUtils as gu
from networkx.algorithms.isomorphism import is_isomorphic

from utils4scripts import getPreprocess, getGraph, getUpperLower, getPallete

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
            