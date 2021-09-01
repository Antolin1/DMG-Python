# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 16:22:25 2021

@author: Jose Antonio
"""
import networkx as nx
import numpy as np

class EditOperation:
    #: list(nx.Graph), set(str)
    def __init__(self, patterns, 
                 identifiers):
        self.patterns = patterns
        self.identifiers = identifiers
        ##check the vality patterns with identifiers
    
    #there should be nodes with attribute 'ids'
    # nx.Graph
    def canApply(self, G) -> bool:
        pairs_G = []
        for n in G.nodes():
            if 'ids' in G.nodes[n]:
                pairs_G.append((G.nodes[n]['type'],G.nodes[n]['ids']))
                
        pairsSelf = self.getPairTypeIds()
        for p in pairsSelf:
            if (len(p) != len(pairs_G)):
                continue
            if len([pg for pg in pairs_G if not pg in p]) == 0:
                return True
        return False
        
    def getPairTypeIds(self):
        result = []
        for p in self.patterns:
            pairs = []
            for n in p.nodes():
                if 'ids' in p.nodes[n]:
                    pairs.append((p.nodes[n]['type'],p.nodes[n]['ids']))
            result.append(pairs)
        return result
    
    def selectPattern(self, G):
        pairs_G = []
        for n in G.nodes():
            if 'ids' in G.nodes[n]:
                pairs_G.append((G.nodes[n]['type'],G.nodes[n]['ids']))
                
        pairsSelf = self.getPairTypeIds()
        for j,p in enumerate(pairsSelf):
            if (len(p) != len(pairs_G)):
                continue
            if len([pg for pg in pairs_G if not pg in p]) == 0:
                return self.patterns[j]
        return None
    
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
                
        new_pat = nx.MultiGraph(pat)
        new_G = nx.MultiGraph(G)
        
        new_pat = nx.relabel_nodes(new_pat, map_edit)
        new_G = nx.relabel_nodes(new_G, map_G)
        
        return nx.compose(new_G, new_pat)

        
                    
        
        
        
