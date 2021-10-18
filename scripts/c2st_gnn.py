#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 18:50:01 2021

@author: Jose Antonio
"""

from torch_geometric.data import Data
from dmg.deeplearning.dataGeneration import generateTensorsFromGraph
from dmg.deeplearning.dataGeneration import addInvEdges
from dmg.deeplearning.earlyStopping import EarlyStopping
from torch.utils.data import random_split
from dmg.realism.discriminativeModel import DiscriminativeModel
from torch_geometric.data import DataLoader
import torch.nn as nn
import torch
import random
import os

import scipy.stats as st
import math

def C2ST_pvalue(acc,n_test):
    return st.norm.cdf(-(acc-0.5)/(math.sqrt(1/(4*n_test))))

def C2ST_GNN(synthetics, graphs_test, dataset, epochs = 100, verbose = False):
    syns = []
    for G in random.sample(synthetics,min(len(synthetics),len(graphs_test))):
        G_inv = addInvEdges(G, dataset.pallete, dataset.pallete.separator)
        tensors = generateTensorsFromGraph(G_inv, dataset.pallete, 2, 2)
        data =  Data(x = tensors[0],
                    edge_index = tensors[-2], 
                    edge_attr = tensors[-1],
                    y = torch.tensor(0))
        syns.append(data)
    
    reals = []
    for G in random.sample(graphs_test,min(len(synthetics),len(graphs_test))):
        G_inv = addInvEdges(G, dataset.pallete, dataset.pallete.separator)
        tensors = generateTensorsFromGraph(G_inv, dataset.pallete, 2, 2)
        data =  Data(x = tensors[0],
                    edge_index = tensors[-2], 
                    edge_attr = tensors[-1],
                    y = torch.tensor(1))
        reals.append(data)
        
    dataset_data = syns + reals
    train_len = int(0.7*len(dataset_data))
    val_len = int(0.15 * len(dataset_data))
    test_len = len(dataset_data) - train_len - val_len
    train, val, test = random_split(dataset_data, [train_len, val_len, test_len], 
                                    generator=torch.Generator().manual_seed(42))
    train_loader = DataLoader(train, batch_size=32, num_workers = 5, shuffle=True)
    val_loader = DataLoader(val, batch_size=1, num_workers = 5, shuffle=True)
    test_loader = DataLoader(test, batch_size=1, num_workers = 5, shuffle=True)
    
    model = DiscriminativeModel(64, 64, 0.0, dataset.dic_nodes, dataset.dic_edges).cpu()
    #epochs = 30
    criterion = nn.BCELoss()
    
    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    es = EarlyStopping(opt, model, 'auxiliar.m', mode = 'max', patience = 10)
    
    for e in range(epochs):
        total_loss = 0.0
        b = 1
        model.train()
        for data in train_loader:
            
            opt.zero_grad()
            
            pred = model(data.x.cpu(), data.edge_index.cpu(),
              torch.squeeze(data.edge_attr.cpu(),dim=1),data.batch.cpu())
            
            loss = criterion(torch.squeeze(pred, dim = 1), data.y.float().cpu())
            total_loss += loss.item()
            
            loss.backward()
            opt.step()
            b = b + 1
        if verbose:
            print('Epoch',e,'Loss',total_loss/b)
        
        #evaluation phase
        model.eval()
        count = 0.0
        with torch.no_grad():
            for data in val_loader:
                pred = model(data.x.cpu(), data.edge_index.cpu(),
                             torch.squeeze(data.edge_attr.cpu(),dim=1),
                             data.batch.cpu())
                if pred[0].item() > 0.5:
                    pred = 1
                else:
                    pred = 0
                if pred == data.y.long().item():
                    count = count + 1
        acc_val = count/len(val_loader)
        if (es.step(acc_val,e)):
            break
        if verbose:
            print('Epoch',e,'Acc val', acc_val)
    #load model
    model = DiscriminativeModel(64, 64, 0.0, dataset.dic_nodes, dataset.dic_edges).cpu()
    checkpoint = torch.load('auxiliar.m',map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    
    #evaluate on test set
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
            
    acc = count/len(test_loader)
    p_val = C2ST_pvalue(count/len(test_loader), len(test_loader))
    test_samples = len(test_loader)
    if verbose:
        print('Acc', acc)
        print('p-value', p_val)
        print('Test samples:', test_samples)
    #remove auxiliar.m
    os.remove("auxiliar.m") 
    return (acc, p_val, test_samples)
