#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 14:53:01 2021

@author: Jose Antonio
"""

import torch
import torch.nn as nn
import torch_geometric.nn as pyg_nn
import torch_geometric.utils as pyg_utils
import torch.nn.functional as F
from torch_scatter import scatter
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from torch_scatter.composite import scatter_softmax


class GenerativeModel(nn.Module):
    
    def __init__(self, hidden_dim, vocab_nodes, vocab_edges, vocab_actions):
        super(GenerativeModel, self).__init__()
            
            
        self.emb_nodes = nn.Embedding(len(vocab_nodes), hidden_dim)
        self.emb_actions = nn.Embedding(len(vocab_actions), hidden_dim)
            
        self.convolution = pyg_nn.Sequential('x, edge_index, edge_type', [
            (pyg_nn.GCNConv(hidden_dim, hidden_dim), 'x, edge_index, edge_type-> x'),
            nn.ReLU(inplace=True),
            (pyg_nn.GCNConv(hidden_dim, hidden_dim), 'x, edge_index, edge_type-> x'),
            nn.ReLU(inplace=True),
            (pyg_nn.GCNConv(hidden_dim, hidden_dim), 'x, edge_index, edge_type-> x'),
            nn.ReLU(inplace=True)
        ])
            
        self.gru = nn.GRU(hidden_dim, hidden_dim, 1, batch_first = True)
            
        self.linAction = nn.Linear(hidden_dim, hidden_dim)
        self.linAction_final = nn.Linear(hidden_dim, len(vocab_actions))
            
        self.linNodes = nn.Linear(2 * hidden_dim, hidden_dim)
        self.linNodes_final = nn.Linear(hidden_dim, 1)
        

    
    def forward(self, nodeTypes, edge_index, edge_attr, 
                bs, sequence_input, nodes_bs, len_seq, action_input):
        
        #node embeddings
        nodeTypes = self.emb_nodes(nodeTypes)
        nodeEmbeddings = self.convolution(nodeTypes, edge_index, edge_attr)
        
        #graph embedding, bxhidden_dim
        h_G = pyg_nn.global_mean_pool(nodeEmbeddings, bs)
        
        #infer action
        action = F.relu(self.linAction(h_G))
        action = self.linAction_final(action)
        
        #emulate SOS token, the sos token must be the action
        #action input: bxh
        sos = self.emb_actions(action_input)
        sos = torch.unsqueeze(sos, dim = 1)
        
        #generate sequence
        emb_seq = (torch.unsqueeze(sequence_input,2)*
                       torch.unsqueeze(nodeEmbeddings, dim = 1))
        
        #b x max_len x h
        out = scatter(emb_seq, bs, dim=0, reduce="sum")
        input_gru = torch.cat((sos, out), dim = 1)
        
        #h_0 of gru
        h_0 = torch.unsqueeze(h_G, dim = 0)
        #pack to gru
        pack = pack_padded_sequence(input_gru, len_seq, batch_first=True, 
                             enforce_sorted=False)
        
        output, h_n = self.gru(pack, h_0)
        #bxlxh
        seq_unpacked, lens_unpacked = pad_packed_sequence(output, 
                                                          batch_first=False)
        
        #nxlxh
        out_gru = torch.repeat_interleave(seq_unpacked, nodes_bs, dim = 0)
        nodeEmb_unsq = torch.unsqueeze(nodeEmbeddings, dim = 1).repeat(1,
                                                                       out_gru.shape[1],1)
        
        concats = torch.cat((out_gru, nodeEmb_unsq), dim = 2)
        concats = F.relu(self.linNodes(concats))
        
        #nxlx1
        nodes_final = torch.squeeze(self.linNodes_final(concats), dim = 2)
        #n x l
        nodes_final = scatter_softmax(nodes_final, bs, dim = 0)
        
        return action, nodes_final
        
        