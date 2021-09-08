#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 15:55:53 2021

@author: Jose Antonio
"""
import sys
import glob
import os
from pathlib import Path
from dmg.yakindu.yakinduPreprocess import removeLayout
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
import dmg.yakindu.yakinduPallete as yp 

def main():
    dataset_path = sys.argv[1]
    preprodataset_path = sys.argv[2]
    files = glob.glob(dataset_path +'/*')
    ##delete layout
    for f in files:
        p = Path(f)
        full_file_name = p.stem + f.split('.')[-1]
        removeLayout(f,preprodataset_path+'/'+full_file_name)
    ##load and remove small models
    
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
    meta_models = glob.glob("data/metamodels/yakinduComplete/*")
    for f in files:
        G1 = m2g.getGraphFromModel(f, 
                              meta_models, metafilterobj,
                              consider_atts = False)
        if len(G1) < 5:
            os.remove(f)
            
if __name__ == "__main__":
    main()
            