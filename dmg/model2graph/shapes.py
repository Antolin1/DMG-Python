# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 13:02:48 2021

@author: Jose Antonio
"""
from pyecore.ecore import EClass
from pyecore.resources import ResourceSet, URI


def getAllSuperClasses(inputClass, pathMetamodels):
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
    element = None
    for e in list_elements:
        if isinstance(e, EClass) and e.name == inputClass:
            element = e
            break
    return [c.name for c in element.eAllSuperTypes()]


def getShape(G, n, i, pathMetamodels):
    if i == 0:
        return 'empty'
    supertypes = getAllSuperClasses(G.nodes[n]['type'], pathMetamodels)
    shape_previous = getShape(G, n, i-1, pathMetamodels)
    result = []
    result.append(shape_previous)
    part_result = [(clazz, 1) 
                   for clazz in supertypes
                   + [G.nodes[n]['type']]]
    ### out nodes
    for m in G[n]:
        shape_m = getShape(G, m, i-1, pathMetamodels)
        for e in G[n][m]:
             type_edge = G[n][m][e]['type']
             part_result.append((type_edge, 1, shape_m))
    ### in nodes
    
    
        