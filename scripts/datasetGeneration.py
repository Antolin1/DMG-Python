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
from modelSet import datasets_supported
from argparse import ArgumentParser


def main():
    
    
    parser = ArgumentParser(description='Script for generating train and test')
    
    parser.add_argument("-d", "--dataset", dest="dataset", 
                    choices=['ecore-github', 'rds-genmymodel', 
                             'yakindu-github','yakindu-exercise'], 
                    help="dataset considered.",
                    required=True)
    parser.add_argument("-pd", "--pathdataset", dest="path_dataset",
                    help="folder of the dataset.", metavar="DIR", 
                    required=True)
    
    parser.add_argument("-emf", "--emf_backend", dest="emf",
                    choices=['python', 'java'],
                    help="backend to parse the models.",
                    required=True)
    
    args = parser.parse_args()
    
    dataset_path = args.path_dataset
    dataset = args.dataset
    backend = args.emf
    msetObject = datasets_supported[dataset]
    
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
        preprocess = msetObject.preprocess
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
            G1 = msetObject.getGraphReal(f,backend)
        except: # Exception as e:
            #print(e.with_traceback())
            print('Remove exception m2g in', f)
            os.remove(f)
            continue
        
        lower, upper = msetObject.bounds
        if len(G1) < lower or len(G1) > upper:
            os.remove(f)
            print('Remove out of bounds in', f)
            continue
        
        pallete = msetObject.pallete
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
    train, test =  train_test_split(files, test_size=0.4, random_state=42)
    
    for f in train:
        copyfile(f, train_path+'/'+ntpath.basename(f))
    for f in test:
        copyfile(f, test_path+'/'+ntpath.basename(f))
    
            
if __name__ == "__main__":
    main()
            