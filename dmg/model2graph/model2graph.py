#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 16:23:44 2021

@author: Jose Antonio
"""

from pyecore.ecore import EReference, EClass
import networkx as nx
from pyecore.resources import ResourceSet, URI
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

print(dir_path)

#Register metamodels
rset = ResourceSet()
resource = rset.get_resource(URI('./data/metamodels/smallEcore.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root

def getGraphFromModel(pathModel):
    
    #load model
    resource = rset.get_resource(URI(pathModel))
    #get list of all elements of the model
    list_elements = []
    for root in resource.contents:
        list_elements.append(root)
        list_elements = list_elements + list(root.eAllContents())
        
    #obtain graph
    nodes = {}
    i = 0
    G = nx.MultiDiGraph()
    for o in list_elements:
    #Register node
        if not o in nodes:
            nodes[o] = i
            i = i + 1
            G.add_node(nodes[o], type = o.eClass.name)
        for f in o.eClass.eAllStructuralFeatures():
            if (f.derived):
                continue
            if (isinstance(f, EReference)):
                if (f.many):
                    for o2 in o.eGet(f):
                        if o2 == None: #or o2.eIsProxy
                            continue
                        if not o2 in nodes:
                            nodes[o2] = i
                            i = i + 1
                            G.add_node(nodes[o2], type = o2.eClass.name)
                        G.add_edge(nodes[o],nodes[o2], type = f.name)
                else:
                    o2 = o.eGet(f)
                    if o2 == None: #or o2.eIsProxy
                            continue
                    if not o2 in nodes:
                        nodes[o2] = i
                        i = i + 1
                        G.add_node(nodes[o2], type = o2.eClass.name)
                    G.add_edge(nodes[o],nodes[o2], type = f.name)
    return G


def getModelFromGraph(pathMetamodel, G):
    # Register metamodel
    resource = rset.get_resource(URI(pathMetamodel))
    mm_root = resource.contents[0]
    rset.metamodel_registry[mm_root.nsURI] = mm_root
    
    #get all elements of the metamodel
    list_elements = []
    for root in resource.contents:
        list_elements.append(root)
        list_elements = list_elements + list(root.eAllContents())
    
    #get eclasses and references
    name_correspondence = {}
    name_ereferences = {}
    for e in list_elements:
        if isinstance(e, EClass):
            name_correspondence[e.name] = e
        if isinstance(e, EReference):
            name_ereferences[e.name] = e
    
    #graph to model
    nodes_objects = {}
    for n in G:
        eobj = None
        if not n in nodes_objects:
            type = G.nodes[n]['type']
            cal = name_correspondence[type]
            eobj = cal()
            nodes_objects[n] = eobj
        else:
            eobj = nodes_objects[n]
        
        for n2 in G[n]:
            eobj2 = None
            if not n2 in nodes_objects:
                type2 = G.nodes[n2]['type']
                cal2 = name_correspondence[type2]
                eobj2 = cal2()
                nodes_objects[n2] = eobj2
            else:
                eobj2 = nodes_objects[n2]
            for e in G[n][n2]:
                type_edge = G[n][n2][e]['type']
                if (name_ereferences[type_edge].many):
                    getattr(eobj,type_edge).add(eobj2)
                else:
                    setattr(eobj,type_edge,eobj2)
    return nodes_objects
        