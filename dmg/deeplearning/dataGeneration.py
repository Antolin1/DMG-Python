#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 13:38:52 2021

@author: Jose Antonio
"""

from torch_geometric.data import Data
import torch
import networkx as nx


def addInvEdges(G, pallete, sep):
    G_new = nx.MultiDiGraph(G)
    for edge in pallete.dic_edges:
        if sep in edge:
            orginial_edge = edge.split(sep)[0]
            for e in list(G.edges.data()):
                if e[2]['type'] == orginial_edge:
                    G_new.add_edge(e[1],e[0], type = edge)
    return G_new

def removeInvEdges(G, pallete, sep):
    G_new = nx.MultiDiGraph(G)
    remove = []
    for edge in pallete.dic_edges:
        if sep in edge:
            for e in G.edges:
                if G[e[0]][e[1]][e[2]]['type'] == edge:
                    remove.append((e[0],e[1], e[2]))
    
    for s, t, k in remove:
        G_new.remove_edge(s, t, k)
    return G_new

def generateTensorsFromGraph(G, pallete, max_length_special_nodes, len_seq):
    nodeTypes = []
    for n in range(len(G)):
        nodeTypes.append(pallete.dic_nodes[G.nodes[n]['type']])
    
    # special nodes, shape: max_len x nodes
    # special_nodes = [[0 for i in range(len(G))]
    #                 for j in range(max_length_special_nodes)]
    # special nodes, shape: nodes x max_len
    special_nodes = [[0 for j in range(max_length_special_nodes)]
                     for i in range(len(G))]
    special_nodes_masked = [[0 if j < len_seq else -1 for j in range(max_length_special_nodes)]
                     for i in range(len(G))]
    for n in range(len(G)):
        if 'ids' in G.nodes[n]:
            for idd in G.nodes[n]['ids']:
                special_nodes[n][idd] = 1
                special_nodes_masked[n][idd] = 1
    # edges
    edges = []
    edges_lab = []
    for e in list(G.edges.data()):
        source = e[0]
        target = e[1]
        lab = e[2]['type']
        edges.append([source,target])
        lab = pallete.dic_edges[lab]
        edges_lab.append(lab)
    
    return (torch.tensor(nodeTypes), 
            torch.tensor(special_nodes),
            torch.tensor(special_nodes_masked),
            torch.transpose(torch.tensor(edges), 0, 1),
            torch.unsqueeze(torch.tensor(edges_lab),dim=1))

# graphs of the sequence must have ids 0,1,2...len(g)
def graph2dataPreAction(G, pallete):
     nT, sN, sNM, edges, edges_lab = generateTensorsFromGraph(G, 
                                                              pallete, 2, 1)
     data = Data(x = nT,
                edge_index = edges, 
                edge_attr = edges_lab,
                nodes = torch.tensor(len(G)))
     return data
 
def graph2dataPostAction(G, pallete, max_length_special_nodes, len_seq):
    nT, sN, sNM, edges, edges_lab = generateTensorsFromGraph(G,pallete, 
                                                             max_length_special_nodes, 
                                                             len_seq)
    data = Data(x = nT,
                edge_index = edges, 
                edge_attr = edges_lab,
                nodes = torch.tensor(len(G)),
                sequence = sN,
                sequence_masked = sNM)
    return data
    

# graphs of the sequence must have ids 0,1,2...len(g)
def sequence2data(sequence, pallete, max_length_special_nodes):
    result = []
    for j, (G, id_edit) in enumerate(sequence):
        nT, sN, sNM, edges, edges_lab = generateTensorsFromGraph(G, 
                                                                 pallete, 
                                                            max_length_special_nodes,
                                                            len(pallete.getSpecialNodes(id_edit)))
        finished = None
        if j == 0:
            finished = torch.tensor(1)
        else:
            finished = torch.tensor(0)
        data = Data(x = nT,
                edge_index = edges, 
                edge_attr = edges_lab,
                action = torch.tensor(id_edit),
                nodes = torch.tensor(len(G)),
                sequence = sN,
                sequence_masked = sNM,
                len_seq = torch.tensor(len(pallete.getSpecialNodes(id_edit))),
                finished = finished)
        result.append(data)
    
    return result


def data2graph(data, pallete):
    G = nx.MultiDiGraph()
    vocab_nodes_2 = {y:x for x,y in pallete.dic_nodes.items()}
    vocab_edges_2 = {y:x for x,y in pallete.dic_edges.items()}
    for n,t in enumerate(data.x.numpy()):
        G.add_node(n, type=vocab_nodes_2[t])
    edges = torch.transpose(data.edge_index, 0, 1)
    for n,e in enumerate(edges.numpy()):
        s = e[0]
        t = e[1]
        n = vocab_edges_2[torch.squeeze(data.edge_attr[n]).item()]
        G.add_edge(s, t, type=n)
    return G
    
