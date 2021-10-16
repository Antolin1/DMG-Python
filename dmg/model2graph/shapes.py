# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 13:02:48 2021

@author: Jose Antonio
"""
from pyecore.ecore import EClass
from pyecore.resources import ResourceSet, URI


def uniques(listt):
    dic = []
    for s1 in listt:
        iso = False
        for s2 in dic:
            if compareShapes(s1,s2):
                iso = True
        if not iso:
            dic.append(s1)
    return dic


def getAllSuperClasses(inputClass, pathMetamodels):
    #to do ecore nonetype elemnt
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

def getCategoricalDistribution(listShapes):
    dic = {}
    total = len(listShapes)
    for s1 in listShapes:
        iso = False
        for s2 in dic:
            if compareShapes(s1,s2):
                iso = True
                dic[s2] = dic[s2] + 1
                break
        if not iso:
            dic[s1] = 1
    for s in dic:
        dic[s] = float(dic[s])/float(total)
    return dic

def computeMD(cat_shape1, cat_shape2):
    dis = 0
    for s1 in cat_shape1:
        iso = False
        for s2 in cat_shape2:
            if compareShapes(s1,s2):
                dis = dis + abs(cat_shape1[s1] - cat_shape2[s2])
                iso = True
                break
        if not iso:
            dis = dis + cat_shape1[s1]
    for s2 in cat_shape2:
        iso = False
        for s1 in cat_shape1:
            if compareShapes(s1,s2):
                iso = True
                break
        if not iso:
            dis = dis + cat_shape2[s2]
    return dis

def externalDiversity(G1, G2, i, pathMetamodels):
    shapes1 = getShapesDP(G1, i, pathMetamodels)
    shapes1 = [r[-1] for r in shapes1.values()]
    shapes1 = getCategoricalDistribution(shapes1) 
    shapes2 = getShapesDP(G2, i, pathMetamodels)
    shapes2 = [r[-1] for r in shapes2.values()]
    shapes2 = getCategoricalDistribution(shapes2) 
    return computeMD(shapes1, shapes2)

# don't know if the implentation is correct
def getShapesDP(G, i, pathMetamodels):
    result = {}
    superTypes = {}
    for n in G:
        result[n] = ['empty']
        type = G.nodes[n]['type']
        superTypes[n] = getAllSuperClasses(type, pathMetamodels)
    for j in range(i):
        for n in G:
            superTypes_n = superTypes[n]
            shape_previous = result[n][j]
            result_n = []
            result_n.append(shape_previous)
            part_result = list(set([(clazz, 1) 
                   for clazz in superTypes_n
                   + [G.nodes[n]['type']]]))
            
            ### out nodes
            tuples3_out = []
            for m in G[n]:
                shape_m = result[m][j]
                for e in G[n][m]:
                    type_edge = G[n][m][e]['type']
                    tuples3_out.append((type_edge, 1, shape_m))
            ##remove dup tup3
            t_3 = []
            for r in tuples3_out:
                dup = False
                for t in t_3:
                    if (t[0] == r[0]) and compareShapes(t[2], r[2]) :
                        dup = True
                        break
                if not dup:
                    t_3.append(r)
            ### in nodes
            tuples3_in = []
            for m, _, d in G.in_edges(n, data = True):
                shape_m = result[m][j]
                type_edge = d['type']
                tuples3_in.append((type_edge, 2, shape_m))
            t_3_in = []
            for r in tuples3_in:
                dup = False
                for t in t_3_in:
                    if (t[0] == r[0]) and compareShapes(t[2], r[2]) :
                        dup = True
                        break
                if not dup:
                    t_3_in.append(r)
            part_result = part_result + t_3 + t_3_in
            part_result = tuple(part_result)
            result_n.append(part_result)
            result_n = tuple(result_n)
            result[n].append(result_n)
        
    return result

def internalDiversityDP(G, i, pathMetamodels):
    shapes = getShapesDP(G, i, pathMetamodels)
    last_shapes = [r[-1] for r in shapes.values()]
    return len(uniques(last_shapes))/float(len(G))

def internalDiversityShapes(last_shapes):
    return len(uniques(last_shapes))/float(len(last_shapes))

from functools import reduce

def compTup2(a,b):
    return reduce(lambda b1,b2: b1 and b2, 
                  map(lambda e1,e2: e1==e2, a, b), True)
def compTup3(a,b):
    return reduce(lambda b1,b2: b1 and b2, 
                  map(lambda e1,e2: e1[0]==e2[0] 
                      and compareShapes(e1[2],e2[2]), a, b), True)

def compareShapes(shape1, shape2):
    if shape1 == 'empty' and shape2 == 'empty':
        return True
    if shape1 == 'empty':
        return False
    if shape2 == 'empty':
        return False
    
    shape11 = shape1[0]
    shape22 = shape2[0]
    if not compareShapes(shape11, shape22):
        return False
    
    class1 = [t for t in shape1[1] if len(t) == 2]
    class2 = [t for t in shape2[1] if len(t) == 2]
    if not compTup2(class1,class2):
        return False
    class1 = [t for t in shape1[1] if len(t) == 3]
    class2 = [t for t in shape2[1] if len(t) == 3]
    if not compTup3(class1,class2):
        return False
    return True
    

        