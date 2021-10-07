#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 18:50:01 2021

@author: Jose Antonio
"""

from torch_geometric.data import Data
from dmg.deeplearning.dataGeneration import generateTensorsFromGraph
from dmg.deeplearning.dataGeneration import addInvEdges
from torch.utils.data import random_split
from dmg.realism.discriminativeModel import DiscriminativeModel
from torch_geometric.data import DataLoader
import torch.nn as nn
import torch
import random
from utils4scripts import (getSeparator, getMaxLen, 
                           getDicNodes, getDicEdges, 
                           getDicOperations, getInconsistent,
                           getGraph, getPallete)

import scipy.stats as st
import math

def C2ST_pvalue(acc,n_test):
    return st.norm.cdf(-(acc-0.5)/(math.sqrt(1/(4*n_test))))

def C2ST_GNN(synthetics, graphs_test, dataset, epochs = 50 ):
    separator = getSeparator(dataset)
    syns = []
    for G in random.sample(synthetics,min(len(synthetics),len(graphs_test))):
        G_inv = addInvEdges(G, getPallete(dataset), getSeparator(dataset))
        tensors = generateTensorsFromGraph(G_inv, getPallete(dataset), 2, 2)
        data =  Data(x = tensors[0],
                    edge_index = tensors[-2], 
                    edge_attr = tensors[-1],
                    y = torch.tensor(0))
        syns.append(data)
    
    reals = []
    for G in random.sample(graphs_test,min(len(synthetics),len(graphs_test))):
        G_inv = addInvEdges(G, getPallete(dataset), getSeparator(dataset))
        tensors = generateTensorsFromGraph(G_inv, getPallete(dataset), 2, 2)
        data =  Data(x = tensors[0],
                    edge_index = tensors[-2], 
                    edge_attr = tensors[-1],
                    y = torch.tensor(1))
        reals.append(data)
        
    dataset_data = syns + reals
    train_len = int(0.8*len(dataset_data))
    test_len = len(dataset_data) - int(0.8*len(dataset_data))
    train, test = random_split(dataset_data, [train_len, test_len], 
                                    generator=torch.Generator().manual_seed(42))
    train_loader = DataLoader(train, batch_size=32, num_workers = 5, shuffle=True)
    test_loader = DataLoader(test, batch_size=1, num_workers = 5, shuffle=True)
    
    model = DiscriminativeModel(64,64,0.0,getDicNodes(dataset),getDicEdges(dataset)).cpu()
    #epochs = 30
    criterion = nn.BCELoss()
    
    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    
    
    for e in range(epochs):
        total_loss = 0.0
        b = 1
        model.train()
        for data in train_loader:
            
            opt.zero_grad()
            
            pred = model(data.x.cpu(), data.edge_index.cpu(),
              torch.squeeze(data.edge_attr.cpu(),dim=1),data.batch.cpu())
            
            loss = criterion(torch.squeeze(pred), data.y.float().cpu())
            total_loss += loss.item()
            
            loss.backward()
            opt.step()
            b = b + 1
            
        print('Epoch',e,'Loss',total_loss/b)
    model.eval()
    count = 0
    for data in test_loader:
        pred = model(data.x.cpu(), data.edge_index.cpu(),
              torch.squeeze(data.edge_attr,dim=1).cpu(),data.batch.cpu())
        if pred[0].item() > 0.5:
            pred = 1
        else:
            pred = 0
        if pred == data.y.long().item():
            count = count + 1
        
    print('Acc', count/len(test_loader))
    print('p-value', C2ST_pvalue(count/len(test_loader), len(test_loader)))
    print('Test samples:', len(test_loader))
