# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 16:22:25 2021

@author: Jose Antonio
"""
import networkx as nx
import numpy as np
from itertools import combinations

class EditOperation:
    #: list(nx.Graph), set(str)
    def __init__(self, patterns):
        self.patterns = patterns
        #TODO: consistency of the patterns
        
    #there should be nodes with attribute 'ids'
    # nx.Graph
    def canApply(self, G) -> bool:
        return self.selectPattern(G) != None
    
    # return the result of the edit. It removes the 'ids' attrs.
    def applyEdit(self, G):
        pat = self.selectPattern(G)
        if pat == None:
            return None
        all_ids = [n for n in G.nodes()] + [n for n in pat.nodes()]
        max_id_add = np.max(all_ids) + 1
        
        map_G = {}
        map_edit = {}
        
        for n in G:
            if 'ids' in G.nodes[n]:
                key = G.nodes[n]['ids']
                map_G[n] = max_id_add
                for m in pat:
                     if 'ids' in pat.nodes[m] and pat.nodes[m]['ids'] == key:
                         map_edit[m] = max_id_add
                         break
                max_id_add = max_id_add + 1
        
        
        for m in pat:
            if not 'ids' in pat.nodes[m]:
                map_edit[m] = max_id_add
                max_id_add = max_id_add + 1
                
        new_pat = nx.MultiDiGraph(pat)
        new_G = nx.MultiDiGraph(G)
        
        new_pat = nx.relabel_nodes(new_pat, map_edit)
        new_G = nx.relabel_nodes(new_G, map_G)
        
        G_compose = nx.compose(new_pat, new_G)
        #fix ids
        new_map = {}
        j = 0
        for n in G_compose:
            new_map[n] = j
            j = j + 1
            if ('ids' in G_compose.nodes[n]):
                del G_compose.nodes[n]['ids']
            
                
        G_compose_final = nx.relabel_nodes(G_compose, new_map)
        return G_compose_final

    def selectPattern(self, G):
        dic_spe_nodes_G = {}
        for n in G.nodes():
            if 'ids' in G.nodes[n]:
                for idd in G.nodes[n]['ids']:
                    dic_spe_nodes_G[idd] = n
        
                    
        dic_patterns = self.getDictNodes()
        for j,dp in enumerate(dic_patterns):
            #check keys
            if (set(dp.keys()) != set(dic_spe_nodes_G.keys())):
                continue
            
            valid = True
            #check combinations
            for k1,k2 in combinations(dp.keys(), 2):
                if (dp[k1] == dp[k2]) != (dic_spe_nodes_G[k1] == dic_spe_nodes_G[k2]):
                    valid = False
                    break
            if not valid:
                continue
            #check types
            valid = True
            for k,v in dic_spe_nodes_G.items():
                node_G = G.nodes[v]
                node_p = self.patterns[j].nodes[dp[k]]
                if not node_G['type'] in node_p['type']:
                    valid = False
            if valid:
                return self.patterns[j]
        return None
            
                    
    def getDictNodes(self):
        result = []
        for G in self.patterns:
            dic_spe = {}
            for n in G.nodes():
                if 'ids' in G.nodes[n]:
                    for idd in G.nodes[n]['ids']:
                        dic_spe[idd] = n
            result.append(dic_spe)
        return result
                    
        
        
        
