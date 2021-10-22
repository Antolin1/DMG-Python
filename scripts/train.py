#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 12:02:28 2021

@author: Jose Antonio
"""

import sys
import os
import glob
sys.path.append(os.getcwd())

from argparse import ArgumentParser
# definition of the option parser
parser = ArgumentParser(description='Script for training the generator')

parser.add_argument("-s", "--save", dest="save_path",
                    help="path to save the model file.", metavar="FILE", 
                    required=True)
parser.add_argument("-td", "--traindetails", dest="save_details",
                    help="path to save the details of the training.", metavar="FILE", 
                    required=True)
parser.add_argument("-d", "--dataset", dest="dataset", 
                    choices=['ecore-github', 'rds-genmymodel', 
                             'yakindu-github','yakindu-exercise'], 
                    help="dataset considered.",
                    required=True)
parser.add_argument("-pd", "--pathdataset", dest="path_dataset",
                    help="folder of the dataset.", metavar="DIR", 
                    required=True)
parser.add_argument("-e", "--epochs", dest="epochs",
                    help="max epochs.", type=int, 
                    required=True)
parser.add_argument("-es", "--earlyStopping", dest="earlyStop", 
                    choices=['clean','iso', 'inco', 'trainloss'], 
                    help="criteria to stop.", default = 'trainloss')
parser.add_argument("-sh", "--shuffle", dest="shuffle", 
                    choices=['True', 'False'], 
                    help="shuffle actions", default = 'False', required=False)
parser.add_argument("-sd", "--seed", dest="seed",
                    help="set seed", type=int, default = 123)
parser.add_argument("-emf", "--emf_backend", dest="emf",
                    choices=['python', 'java'],
                    help="backend to parse the models.",
                    required=True)
parser.add_argument("-v", "--verbose", dest="verbose_mode", type=int, 
                    required=False, default=1,
                    help="verbose mode (should be in {0,1}).")
parser.add_argument("-b", "--batch", dest="batch", type=int, 
                    required=False, default=64,
                    help="batch size.")
parser.add_argument("-hi", "--hidden", dest="hidden_dim", type=int, 
                    required=False, default=128,
                    help="hidden dim of the nn size.")
#parser.add_argument("-mp", "--multiprocess", dest="mp", type=int, 
#                    required=False, default=10,
#                    help="number of processes.")
parser.add_argument("-k", "--k_samples", dest="k", type=int,
                    required=False, default=-1,
                    help="number of processes.")
parser.add_argument("-lr", "--learningRate", dest="lr", type=float,
                    required=False, default=0.001,
                    help="number of processes.")
#add argument to use the easrly stopping over the trainset
# get inputs
args = parser.parse_args()
model_path = args.save_path
dataset = args.dataset
path_dataset = args.path_dataset
epochs = args.epochs
early = args.earlyStop
shuffle = bool(args.shuffle)
seed = args.seed
backend = args.emf
verbose = (args.verbose_mode == 1)
hidden_dim = args.hidden_dim
batch_size = args.batch
lr = args.lr
#numProcess = args.mp
path_train_details = args.save_details
k = args.k


#paths
train_path = path_dataset + '/train'
test_path = path_dataset + '/test'

#seed for training
import torch
import numpy as np
import random

torch.manual_seed(seed)
random.seed(seed)
np.random.seed(seed)

#from utils4scripts import (getSeparator, getMaxLen, 
#                           getDicNodes, getDicEdges, 
#                           getDicOperations, getInconsistent,
#                           getGraph, getPallete)

from modelSet import datasets_supported

msetObject = datasets_supported[dataset]
# Load graphs
#graphs_train = [getGraph(f,dataset,backend) 
#                for f in glob.glob(train_path + "/*")]
#graphs_test = [getGraph(f,dataset,backend) 
#                for f in glob.glob(test_path + "/*")]

graphs_train = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(train_path + "/*")]
graphs_test = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(test_path + "/*")]
if verbose:
    print('Number of graphs train:', len(graphs_train))
    print('Number of graphs test:', len(graphs_test))

# Get pallete
pallete = msetObject.pallete#getPallete(dataset)
pallete.shuffle = shuffle
separator = pallete.separator#getSeparator(dataset)

#Training phase
from dmg.deeplearning.generativeModel import GenerativeModel
from dmg.deeplearning.earlyStopping import EarlyStopping
from dmg.deeplearning.generativeModel import sampleGraph
import torch.nn as nn
import multiprocess as mp
from torch_geometric.data import DataLoader
from dmg.deeplearning.dataGeneration import sequence2data
from dmg.deeplearning.dataGeneration import addInvEdges
from networkx.algorithms.isomorphism import is_isomorphic
import dmg.graphUtils as gu
import time



#distributed function
def f(g):
    sequence = pallete.graphToSequence(g)
    sequence = [(addInvEdges(s[0], pallete, separator),s[1]) for s in sequence]
    return sequence2data(sequence, pallete, pallete.max_len)#getMaxLen(dataset)

#losses
criterion_node = nn.CrossEntropyLoss(reduction = 'mean', ignore_index=-1)
criterion_action = nn.CrossEntropyLoss(reduction = 'mean')
criterion_finish = nn.BCELoss(reduction = 'mean')
#model
model = GenerativeModel(hidden_dim, msetObject.dic_nodes, 
                        msetObject.dic_edges, 
                        msetObject.operations)
#optimizer
opt = torch.optim.Adam(model.parameters(), lr=lr)
#early stopping object

mode = None
if early == 'clean':
    mode = 'max'
elif early == 'iso':
    mode = 'min'
elif early == 'inco':
    mode = 'min'
else:
    mode = 'min'
es = EarlyStopping(opt, model, model_path, patience = 10, mode = mode)
#incosistences, isomorfics and clean
prop_inconsistent = []
prop_isomorfic = []
prop_clean = []
max_size = np.max([len(g) for g in graphs_train])
losses = []

listDatasMontecarlo = []
if k!=-1:
    for j in range(k):
        with mp.Pool(10) as pool:
            listDatas = pool.map(f, graphs_train)
        listDatas = [r for rr in listDatas for r in rr]
        listDatasMontecarlo = listDatasMontecarlo + listDatas

start_time = time.monotonic()
for epoch in range(epochs):
    model.train()
    total_loss = 0
    
    listDatas = []
    if k == -1:
        with mp.Pool(10) as pool:
            listDatas = pool.map(f, graphs_train)
        listDatas = [r for rr in listDatas for r in rr]
    
    loader = None
    if k == -1:
        loader = DataLoader(listDatas, batch_size=batch_size, 
                                num_workers = 3, 
                                shuffle=False)
    else:
        loader = DataLoader(listDatasMontecarlo, batch_size=batch_size, 
                                num_workers = 3, 
                                shuffle=False)
    #training
    for data in loader:
        opt.zero_grad()
        action, nodes, finish = model(data.x, data.edge_index, 
                        torch.squeeze(data.edge_attr,dim=1), 
                data.batch, data.sequence, data.nodes, data.len_seq, data.action)
        
        nodes = torch.unsqueeze(nodes, dim = 2).repeat(1,1,2)
        nodes[:,:,0] = 1 - nodes[:,:,1]
            
        L = torch.max(data.len_seq).item()
        gTruth = data.sequence_masked[:,0:L]
        loss = (criterion_node(nodes.reshape(-1,2), gTruth.flatten()) +
                    criterion_action(action, data.action) +
                    criterion_finish(finish.flatten(), data.finished.float())) / 3
        total_loss += loss.item()
        loss.backward()
        opt.step()
    
    if verbose:
        print('Epoch',epoch,'Loss Traning',total_loss/(len(loader)))
    losses.append(total_loss/(len(loader)))
    
    if early in ['clean','iso', 'inco']:
        model.eval()
        samples = [sampleGraph(pallete.initialGraphs[0], pallete, model, 
                               max_size, separator) 
               for i in range(500)]
        inconsistents = []
        for s in samples:
            if msetObject.inconsistency(s):
                inconsistents.append(s)
        inco_prop = len(inconsistents)*100/len(samples)
        prop_inconsistent.append(inco_prop)
        
        iso = []
        for s in samples:
            for g in graphs_train:
                if (is_isomorphic(s,g,gu.node_match_type, gu.edge_match_type)):
                    iso.append(s)
                    break
        
        iso_prop = len(iso)*100/len(samples)
        prop_isomorfic.append(iso_prop)
        clean_new_models = [g for g in samples if (not g in inconsistents) and (not g in iso)]
        clean_pr = len(clean_new_models)*100/len(samples)
        prop_clean.append(clean_pr)
        
        if verbose:
            print('Prop inconsistent:', inco_prop)
            print('Prop isomorfic:', iso_prop)
            print('Prop clean:', clean_pr)
        
        metric = None
        if early == 'clean':
            metric = clean_pr
        elif early == 'iso':
            metric = iso_prop
        else:
            metric = inco_prop
            
        if es.step(metric, epoch):
            break
    else:
        if es.step(total_loss/(len(loader)), epoch):
            break
    
train_duration = time.monotonic() - start_time
    #scheduler.step()
    #if do_eval:
    #    print('Epoch',epoch,'Loss Val',val_loss/(len(loader_val)))
dic_details = {
    "incosistent" : prop_inconsistent,
    "isomorfic" : prop_isomorfic,
    "clean" : prop_clean,
    "loss" : losses,
    "time" : train_duration
    }

import json
with open(path_train_details, 'w') as f:
    json.dump(dic_details, f)