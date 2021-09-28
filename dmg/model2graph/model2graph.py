#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 16:23:44 2021

@author: Jose Antonio
"""

from pyecore.ecore import EReference, EClass, EAttribute
import networkx as nx
from pyecore.resources import ResourceSet, URI
import subprocess
import pygraphviz
from networkx.drawing import nx_agraph
import dmg.graphUtils as gu

#Register metamodels
#rset = ResourceSet()
#resource = rset.get_resource(URI('./data/metamodels/smallEcore.ecore'))
#mm_root = resource.contents[0]
#rset.metamodel_registry[mm_root.nsURI] = mm_root

def getGraphFromModel(pathModel, pathMetamodels, metaFiler = None, 
                      consider_atts = True):
    rset = ResourceSet()
    for pathMetamodel in pathMetamodels:
        #load meta-model
        resource = rset.get_resource(URI(pathMetamodel))
        mm_root = resource.contents[0]
        rset.metamodel_registry[mm_root.nsURI] = mm_root
        #print(mm_root.nsURI, mm_root)
    
    #load model
    resource = rset.get_resource(URI(pathModel))
    #get list of all elements of the model
    list_elements = []
    for root in resource.contents:
        list_elements.append(root)
        list_elements = list_elements + list(root.eAllContents())
    
    return getGraphFromModelElements(list_elements, metaFiler = metaFiler, 
                      consider_atts = consider_atts)
        
   
def getGraphFromModelElements(list_elements, metaFiler = None, 
                      consider_atts = True):
    #obtain graph
    nodes = {}
    i = 0
    G = nx.MultiDiGraph()
    for o in list_elements:
        if (metaFiler!=None) and (not metaFiler.pass_filter_object(o)):
            continue
    #Register node
        if not o in nodes:
            nodes[o] = i
            i = i + 1
            G.add_node(nodes[o], type = o.eClass.name)
        dic_attributes = {}
        for f in o.eClass.eAllStructuralFeatures():
            if (f.derived):
                continue
            if (metaFiler!=None) and (not metaFiler.pass_filter_structural(f)):
                continue
            #references
            if (isinstance(f, EReference)):
                if (f.many):
                    for o2 in o.eGet(f):
                        if o2 == None: #or o2.eIsProxy
                            continue
                        #avoid adding elements thar are not in the model
                        if (not o2 in list_elements):
                            continue
                        if ((metaFiler!=None) and 
                            (not metaFiler.pass_filter_object(o2))):
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
                    #avoid adding elements thar are not in the model
                    if (not o2 in list_elements):
                            continue
                    if ((metaFiler!=None) and 
                            (not metaFiler.pass_filter_object(o2))):
                            continue
                    if not o2 in nodes:
                        nodes[o2] = i
                        i = i + 1
                        G.add_node(nodes[o2], type = o2.eClass.name)
                    G.add_edge(nodes[o],nodes[o2], type = f.name)
            #attributes
            elif (isinstance(f, EAttribute)):
                 if (f.many):
                     list_att_val = []
                     for o2 in o.eGet(f):
                        if o2 == None: #or o2.eIsProxy
                            list_att_val.append('<none>')   
                        else:
                            list_att_val.append(o2)
                     dic_attributes[f.name] = list_att_val
                 else:
                     o2 = o.eGet(f)
                     if o2 == None: #or o2.eIsProxy
                         dic_attributes[f.name] = '<none>'
                     else:
                         dic_attributes[f.name] = o2
        if consider_atts:             
            G.nodes[nodes[o]]['atts'] = dic_attributes              
    return G


def getModelFromGraph(pathMetamodels, G):
    # Register metamodel
    rset = ResourceSet()
    list_elements = []
    for pathMetamodel in pathMetamodels:
        #load meta-model
        resource = rset.get_resource(URI(pathMetamodel))
        mm_root = resource.contents[0]
        rset.metamodel_registry[mm_root.nsURI] = mm_root
        for root in resource.contents:
            list_elements.append(root)
            list_elements = list_elements + list(root.eAllContents())
    
    #get eclasses and references
    name_correspondence = {}
    name_ereferences = {}
    name_attributes = {}
    for e in list_elements:
        if isinstance(e, EClass):
            name_correspondence[e.name] = e
        if isinstance(e, EReference):
            name_ereferences[e.name] = e
        if isinstance(e, EAttribute):
            name_attributes[e.name] = e
    
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
        #TODO: the <none> token
        if 'atts' in G.nodes[n]:
            atts = G.nodes[n]['atts']
            for att_name, value in atts.items():
                if (name_attributes[att_name].many):
                    for v in value:
                        getattr(eobj,att_name).add(v)
                else:
                    setattr(eobj,att_name,value)
        
        #references
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

def serializeGraphModel(path, pathMetamodels, mainClass, G):
    nodes_objects = getModelFromGraph(pathMetamodels, G)
    for n,ob in nodes_objects.items():
        if ob.eClass.name == mainClass:
            rset = ResourceSet()
            resource = rset.create_resource(URI(path))  # This will create an XMI resource
            resource.append(ob)  # we add the EPackage instance in the resource
            resource.save()  # we then serialize it

def model2graphJava(modelType, pathmodel):
    x = subprocess.Popen(["java", "-jar", 
                              "java/model2graph/target/model2graph-0.0.1-jar-with-dependencies.jar", modelType, 
                              pathmodel], 
                             stderr=subprocess.PIPE, 
                             stdout=subprocess.PIPE,
                             text=True)
    out,err = x.communicate()
    #print(out)
    #print(err)
    G = nx_agraph.from_agraph(pygraphviz.AGraph(out))
    G = gu.fixDotGraph(G)
    return G
        