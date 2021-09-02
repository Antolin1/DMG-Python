# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 16:12:16 2021

@author: Jose Antonio
"""

def selectPattern2(self, G):
        dic_spe_nodes_G = {}
        dic_inv_G = defaultdict(list)
        for n in G.nodes():
            if 'ids' in G.nodes[n]:
                for idd in G.nodes[n]['ids']:
                    dic_spe_nodes_G[idd] = n
                    dic_inv_G[n].append(idd)
                    
        dic_patterns = self.getDictNodes()
        for j,(dp,di) in enumerate(dic_patterns):
            #check keys
            if (set(dp.keys()) != set(dic_spe_nodes_G.keys())):
                continue
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
            dic_inv = defaultdict(list)
            for n in G.nodes():
                if 'ids' in G.nodes[n]:
                    for idd in G.nodes[n]['ids']:
                        dic_spe[idd] = n
                        dic_inv[n].append(idd)
            result.append((dic_spe,dic_inv))
        return result