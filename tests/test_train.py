#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 10:16:35 2021

@author: Jose Antonio
"""

import unittest
from dmg.deeplearning.generativeModel import GenerativeModel, sampleGraph
import dmg.model2graph.model2graph as m2g
import dmg.model2graph.metafilter as mf
from networkx.algorithms.isomorphism import is_isomorphic
from dmg.deeplearning.dataGeneration import sequence2data, data2graph, addInvEdges
import dmg.yakindu.yakinduPallete as yp
from tests.test_deepl import node_match_type_ids
from torch_geometric.data import DataLoader
import torch.nn.functional as F
import glob
import dmg.graphUtils as gu
import random
import torch
import torch.nn as nn
random.seed(123)
torch.manual_seed(0)

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
files = glob.glob("data/testTrain/*")
graphs = [m2g.getGraphFromModel(f, 
                              meta_models, metafilterobj,
                              consider_atts = False) for f in files]


epochs = 500
hidden_dim = 128
max_len = 2
batch_size = 32
num_samples = 10

criterion_node = nn.CrossEntropyLoss(reduction = 'mean',ignore_index=-1)
criterion_action = nn.CrossEntropyLoss(reduction = 'mean')
criterion_finish = nn.BCELoss(reduction = 'mean')
model = GenerativeModel(hidden_dim, yp.dic_nodes_yak, 
                        yp.dic_edges_yak, yp.dic_operations_yak)
opt = torch.optim.Adam(model.parameters(), lr=0.0001)

listDatas = []
for g in graphs:
    sequence = yp.yakindu_pallete.graphToSequence(g)
    sequence = [(addInvEdges(s[0], yp.yakindu_pallete, 
                             yp.yakindu_separator),s[1]) 
                            for s in sequence]
    listDatas = listDatas + sequence2data(sequence, 
                                          yp.yakindu_pallete, 
                                          max_len)

class TestTrain(unittest.TestCase):
    
    def test_input_train(self):
        for j,data in enumerate(listDatas):
            self.assertEqual(data.x.shape[0], len(sequence[j][0]))
            self.assertEqual(data.edge_index.shape[1], 
                             len(sequence[j][0].edges))
            self.assertEqual(data.edge_attr.shape[0], 
                             len(sequence[j][0].edges))
            self.assertEqual(data.action.item(), 
                             sequence[j][1])
            self.assertEqual(data.sequence.shape[1], 
                             max_len)
            self.assertEqual(data.sequence.shape[0], 
                             len(sequence[j][0]))
            
            self.assertEqual(data.nodes.item(), 
                             len(sequence[j][0]))
            
            self.assertEqual(data.len_seq.item(), 
                             len(yp.yakindu_pallete.getSpecialNodes(sequence[j][1])))
            
            if j == 0:
                self.assertEqual(data.finished.item(), 1)
            else:
                self.assertEqual(data.finished.item(), 0)
            
            graph_inv = data2graph(data, yp.yakindu_pallete)
            self.assertTrue(is_isomorphic(graph_inv, 
                                      sequence[j][0], 
                                      gu.node_match_type, 
                                      gu.edge_match_type))
            np_seq = data.sequence.numpy()
            for i,l in enumerate(np_seq):
                for t,c in enumerate(l):
                    if (c == 1):
                        if ('ids' in graph_inv.nodes[i]):
                            graph_inv.nodes[i]['ids'].add(t)
                        else:
                            graph_inv.nodes[i]['ids'] = set([t])
                            
            self.assertTrue(is_isomorphic(graph_inv, 
                                      sequence[j][0], 
                                      node_match_type_ids, 
                                      gu.edge_match_type))
    
    def test_trainGenerativeModel(self):
        #for g in graphs:
        #    print(g.nodes(data=True))
        #    print(g.edges(data=True))
        #print('---'*10)

        for epoch in range(epochs):
            model.train()
            total_loss = 0
            listDatas = []
            for g in graphs:
                sequence = yp.yakindu_pallete.graphToSequence(g)
                sequence = [(addInvEdges(s[0], yp.yakindu_pallete, 
                                         yp.yakindu_separator),s[1]) 
                            for s in sequence]
                listDatas = listDatas + sequence2data(sequence, 
                                                      yp.yakindu_pallete, 
                                                      max_len)
            loader = DataLoader(listDatas, batch_size=batch_size, 
                            num_workers = 0, 
                            shuffle=False)
            for j,data in enumerate(loader):
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

            #print('Loss:',total_loss)
        loader = DataLoader(listDatas, batch_size=1, 
                            num_workers = 0, 
                            shuffle=False)
        for j,data in enumerate(loader):
            if (j == 0):
                action, nodes, finish = model(data.x, data.edge_index, 
                                torch.squeeze(data.edge_attr,dim=1), 
                        data.batch, data.sequence, data.nodes, data.len_seq, data.action)
                
                print(data.x)
                print(nodes)
                print(finish)
                print(F.softmax(torch.squeeze(action)))
                print(data.sequence_masked[:,0:L])
                
            
        ##sample
        model.eval()
        samples = [sampleGraph(yp.G_initial_yak, yp.yakindu_pallete, 
                                   model, 50, yp.yakindu_separator, debug=True) 
                       for i in range(num_samples)]
            
        iso = []
        for s in samples:
            #print(s.nodes(data=True))
            #print(s.edges(data=True))
            #print()
            for g in graphs:
                if (is_isomorphic(s,g,gu.node_match_type, 
                                  gu.edge_match_type)):
                    iso.append(s)
                    break
        proportion_iso = len(iso)/len(samples)
        print('Proportion:', proportion_iso)
        self.assertGreater(proportion_iso, 0.05)