#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 14:53:01 2021

@author: Jose Antonio
"""

import torch
import torch.nn as nn
import torch_geometric.nn as pyg_nn
import torch.nn.functional as F
from torch_scatter import scatter
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from torch_scatter.composite import scatter_softmax
from torch.distributions.categorical import Categorical
import networkx as nx
from dmg.deeplearning.dataGeneration import graph2dataPreAction, graph2dataPostAction, addInvEdges

def sampleGraph(G_0, pallete, model, max_size, sep, debug = False, debug_trials = False, max_trials = 100):
    G_aux = nx.MultiDiGraph(G_0)
    finish = False
    step = 0
    trials = 0
    while (len(G_aux) < max_size and (not finish)):
        G_aux_inv = addInvEdges(G_aux, pallete, sep)
        #sample action
        data = graph2dataPreAction(G_aux_inv, pallete)
        batch = torch.tensor([0]*len(G_aux_inv))
        sampled_action, isLast, h_G, nodeEmbeddings = model.getActionAndFinish(
            data.x, data.edge_index, 
            torch.squeeze(data.edge_attr,dim=1),
                        batch)
        if debug:
            print('Step', step)
            print('Action', sampled_action.item())
            print('Is last', isLast.item() == 1)
        
        if isLast.item() == 1:
            finish = True
        sampled_action = sampled_action.item()
        #sample nodes
        special_nodes = pallete.getSpecialNodes(sampled_action)
        for j, idd in enumerate(special_nodes):
            if idd == 0:
                data = graph2dataPreAction(G_aux_inv, pallete)
                sampled_node = model.getNodes(h_G, nodeEmbeddings,
                batch, None, torch.tensor([sampled_action]), 
                None, data.nodes)
                G_aux.nodes[sampled_node.item()]['ids'] = {idd}
            else:
                G_aux_inv = addInvEdges(G_aux, pallete, sep)
                data = graph2dataPostAction(G_aux_inv, pallete, 
                                            j + 1, 
                                            j + 1)
                #print('Sequence:',data.sequence)
                sampled_node = model.getNodes(h_G, nodeEmbeddings,
                batch, data.sequence, torch.tensor([sampled_action]), 
                torch.tensor([j + 1]), data.nodes)
                if not 'ids' in G_aux.nodes[sampled_node.item()]:
                    G_aux.nodes[sampled_node.item()]['ids'] = {idd}
                else:
                    G_aux.nodes[sampled_node.item()]['ids'].add(idd)
        if debug:
            for n in G_aux:
                if 'ids' in G_aux.nodes[n]:
                    print('Node type', G_aux.nodes[n]['type'], 'Ids',G_aux.nodes[n]['ids'] )
                
        applied = pallete.applyEdit(G_aux, sampled_action)
        if applied!= None:
            if (trials > 0) and (debug_trials):
                print('There have been', trials, 'before')
            trials = 0
            G_aux = applied
            step = step + 1
            if debug:
                print()
        else:
            #print('Cannot apply')
            trials = trials + 1
            for n in G_aux:
                if ('ids' in G_aux.nodes[n]):
                    del G_aux.nodes[n]['ids']
            finish = False
            if trials == max_trials:
                return G_aux
    return G_aux


def sampleGraphLowerBound(G_0, pallete, model,sep, lowerbound, debug = False, 
                          debug_trials = False, max_trials = 100):
    G_aux = nx.MultiDiGraph(G_0)
    finish = False
    step = 0
    trials = 0
    while (len(G_aux) < lowerbound):
        G_aux_inv = addInvEdges(G_aux, pallete, sep)
        #sample action
        data = graph2dataPreAction(G_aux_inv, pallete)
        batch = torch.tensor([0]*len(G_aux_inv))
        sampled_action, isLast, h_G, nodeEmbeddings = model.getActionAndFinish(
            data.x, data.edge_index, 
            torch.squeeze(data.edge_attr,dim=1),
                        batch)
        if debug:
            print('Step', step)
            print('Action', sampled_action.item())
            print('Is last', isLast.item() == 1)
        
        if isLast.item() == 1:
            finish = True
        sampled_action = sampled_action.item()
        #sample nodes
        special_nodes = pallete.getSpecialNodes(sampled_action)
        for j, idd in enumerate(special_nodes):
            if idd == 0:
                data = graph2dataPreAction(G_aux_inv, pallete)
                sampled_node = model.getNodes(h_G, nodeEmbeddings,
                batch, None, torch.tensor([sampled_action]), 
                None, data.nodes)
                G_aux.nodes[sampled_node.item()]['ids'] = {idd}
            else:
                G_aux_inv = addInvEdges(G_aux, pallete, sep)
                data = graph2dataPostAction(G_aux_inv, pallete, 
                                            j + 1, 
                                            j + 1)
                #print('Sequence:',data.sequence)
                sampled_node = model.getNodes(h_G, nodeEmbeddings,
                batch, data.sequence, torch.tensor([sampled_action]), 
                torch.tensor([j + 1]), data.nodes)
                if not 'ids' in G_aux.nodes[sampled_node.item()]:
                    G_aux.nodes[sampled_node.item()]['ids'] = {idd}
                else:
                    G_aux.nodes[sampled_node.item()]['ids'].add(idd)
        if debug:
            for n in G_aux:
                if 'ids' in G_aux.nodes[n]:
                    print('Node type', G_aux.nodes[n]['type'], 'Ids',G_aux.nodes[n]['ids'] )
                
        applied = pallete.applyEdit(G_aux, sampled_action)
        if applied!= None:
            if (trials > 0) and (debug_trials):
                print('There have been', trials, 'before')
            trials = 0
            G_aux = applied
            step = step + 1
            if debug:
                print()
        else:
            #print('Cannot apply')
            trials = trials + 1
            for n in G_aux:
                if ('ids' in G_aux.nodes[n]):
                    del G_aux.nodes[n]['ids']
            finish = False
            if trials == max_trials:
                return G_aux
    return G_aux
                    

class GenerativeModel(nn.Module):
    
    def __init__(self, hidden_dim, vocab_nodes, vocab_edges, vocab_actions,
                 attention = False, numGNNLayers = 2):
        super(GenerativeModel, self).__init__()
            
            
        self.emb_nodes = nn.Embedding(len(vocab_nodes), hidden_dim)
        self.emb_actions = nn.Embedding(len(vocab_actions), hidden_dim)
            
        self.convolution = pyg_nn.Sequential('x, edge_index, edge_type', [
            (pyg_nn.RGCNConv(hidden_dim, hidden_dim, 
                             num_relations = len(vocab_edges)), 'x, edge_index, edge_type-> x'),
            nn.ReLU(inplace=True)
        ] * numGNNLayers)
            
        self.gru = nn.GRU(hidden_dim, hidden_dim, 1, batch_first = True)
            
        self.linAction = nn.Linear(hidden_dim, hidden_dim)
        self.linAction_final = nn.Linear(hidden_dim, len(vocab_actions))
            
        self.linNodes = nn.Linear(2 * hidden_dim, hidden_dim)
        self.linNodes_final = nn.Linear(hidden_dim, 1)
        self.finishedLin = nn.Linear(hidden_dim, hidden_dim)
        self.finishedFinal = nn.Linear(hidden_dim, 1)
        
        self.globalattention = attention
        if self.globalattention:
            self.globalAttentionFinish = pyg_nn.GlobalAttention(gate_nn = nn.Linear(hidden_dim, 1))
    
    #TODO: do it in batch
    #TODO: fix random seed
    def getActionAndFinish(self, nodeTypes, edge_index, edge_attr, bs):
        #node embeddings
        nodeTypes = self.emb_nodes(nodeTypes)
        nodeEmbeddings = self.convolution(nodeTypes, edge_index, edge_attr)
        #graph embedding, bxhidden_dim
        h_G = None
        if self.globalattention:
            h_G = self.globalAttentionFinish(nodeEmbeddings, bs) 
        else:
            h_G = pyg_nn.global_mean_pool(nodeEmbeddings, bs)
        #infer action
        action = F.relu(self.linAction(h_G))
        action = self.linAction_final(action)
        m = Categorical(F.softmax(torch.squeeze(action)))
        #infer finished
        final = F.relu(self.finishedLin(h_G))
        final = F.sigmoid(self.finishedFinal(final))
        isLast = torch.bernoulli(final)
        return m.sample(), isLast, h_G, nodeEmbeddings
    
    def getNodes(self, h_G, nodeEmbeddings,
                bs, sequence_input, action_input, len_seq, nodes_bs):
        
        #action
        sos = self.emb_actions(action_input)
        sos = torch.unsqueeze(sos, dim = 1)
        
        input_gru = None
        if sequence_input == None:
            input_gru = sos
            len_seq = torch.tensor([1])
        else:
            emb_seq = (torch.unsqueeze(sequence_input,2)*
                       torch.unsqueeze(nodeEmbeddings, dim = 1))
            out = scatter(emb_seq, bs, dim=0, reduce="sum")        
            input_gru = torch.cat((sos, out), dim = 1)
        
        #h_0 of gru
        h_0 = torch.unsqueeze(h_G, dim = 0)
        #pack to gru
        pack = pack_padded_sequence(input_gru, len_seq, batch_first=True, 
                             enforce_sorted=False)
        
        output, h_n = self.gru(pack, h_0)
        seq_unpacked, lens_unpacked = pad_packed_sequence(output, 
                                                          batch_first=True)
        
        out_gru = torch.repeat_interleave(seq_unpacked, nodes_bs, dim = 0)
        
        nodeEmb_unsq = torch.unsqueeze(nodeEmbeddings, 
                                       dim = 1).repeat(1,out_gru.shape[1],1)
        
        concats = torch.cat((out_gru, nodeEmb_unsq), dim = 2)
        concats = F.relu(self.linNodes(concats))
        
        
        #nxlx1
        nodes_final = torch.squeeze(self.linNodes_final(concats), dim = 2)
        #n x l
        nodes_final = scatter_softmax(nodes_final, bs, dim = 0)
        #if not self.training:
        #    print(nodes_final)
        #    print(nodes_final[:,-1])
        #    print()
        m = Categorical(nodes_final[:,-1])
        
        return m.sample()
        

    
    def forward(self, nodeTypes, edge_index, edge_attr, 
                bs, sequence_input, nodes_bs, len_seq, 
                action_input):
        
        L = torch.max(len_seq)
        sequence_input = sequence_input[:,0:L]
        
        #node embeddings
        N = nodeTypes.shape[0]
        nodeTypes = self.emb_nodes(nodeTypes)
        H  = nodeTypes.shape[1]
        nodeEmbeddings = self.convolution(nodeTypes, edge_index, edge_attr)
        assert nodeEmbeddings.shape[0] == N
        assert nodeEmbeddings.shape[1] == H
        
        B = nodes_bs.shape[0]
        #graph embedding, bxhidden_dim
        h_G = None
        if self.globalattention:
            h_G = self.globalAttentionFinish(nodeEmbeddings, bs) 
        else:
            h_G = pyg_nn.global_mean_pool(nodeEmbeddings, bs)
        assert h_G.shape[0] == B
        assert h_G.shape[1] == H
        
        #infer action
        action = F.relu(self.linAction(h_G))
        action = self.linAction_final(action)
        
        #infer finished
        final = F.relu(self.finishedLin(h_G))
        final = F.sigmoid(self.finishedFinal(final))
        
        #emulate SOS token, the sos token must be the action
        #action input: bxh
        sos = self.emb_actions(action_input)
        assert sos.shape[0] == B
        assert sos.shape[1] == H
        sos = torch.unsqueeze(sos, dim = 1)
        
        L = sequence_input.shape[1]
        #generate sequence
        emb_seq = (torch.unsqueeze(sequence_input,2)*
                       torch.unsqueeze(nodeEmbeddings, dim = 1))
        assert emb_seq.shape[0] == N
        assert emb_seq.shape[1] == L
        assert emb_seq.shape[2] == H
        
        #b x max_len x h
        out = scatter(emb_seq, bs, dim=0, reduce="sum")
        assert out.shape[0] == B
        assert out.shape[1] == L
        assert out.shape[2] == H
        
        input_gru = torch.cat((sos, out), dim = 1)
        assert input_gru.shape[0] == B
        assert input_gru.shape[1] == L + 1
        assert input_gru.shape[2] == H
        
        #h_0 of gru
        h_0 = torch.unsqueeze(h_G, dim = 0)
        #pack to gru
        pack = pack_padded_sequence(input_gru, len_seq, batch_first=True, 
                             enforce_sorted=False)
        
        output, h_n = self.gru(pack, h_0)
        #bxlxh
        seq_unpacked, lens_unpacked = pad_packed_sequence(output, 
                                                          batch_first=True)
        assert seq_unpacked.shape[0] == B
        assert seq_unpacked.shape[1] == L
        assert seq_unpacked.shape[2] == H
        
        
        #nxlxh
        out_gru = torch.repeat_interleave(seq_unpacked, nodes_bs, dim = 0)
        assert out_gru.shape[0] == N
        assert out_gru.shape[1] == L
        assert out_gru.shape[2] == H
        
        nodeEmb_unsq = torch.unsqueeze(nodeEmbeddings, dim = 1).repeat(1,
                                                                       out_gru.shape[1],1)
        assert nodeEmb_unsq.shape[0] == N
        assert nodeEmb_unsq.shape[1] == L
        assert nodeEmb_unsq.shape[2] == H
        
        concats = torch.cat((out_gru, nodeEmb_unsq), dim = 2)
        assert concats.shape[0] == N
        assert concats.shape[1] == L
        assert concats.shape[2] == (2 * H)
        
        concats = F.relu(self.linNodes(concats))
        assert concats.shape[2] == H
        
        #nxlx1
        nodes_final = torch.squeeze(self.linNodes_final(concats), dim = 2)
        #n x l
        nodes_final = scatter_softmax(nodes_final, bs, dim = 0)
        assert nodes_final.shape[0] == N
        assert nodes_final.shape[1] == L
        
        return action, nodes_final, final
        
        