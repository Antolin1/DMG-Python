#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 12:15:01 2021

@author: Jose Antonio
"""

from multiset import Multiset

def node_match_type(n1,n2):
    return n1['type'] == n2['type']

def edge_match_type(e1,e2):
    t1 = []
    t2 = []
    for e in e1:
        t1.append(e1[e]['type'])
    for e in e2:
        t2.append(e2[e]['type'])
    return Multiset(t1) == Multiset(t2)

def node_match_type_atts(n1,n2):
    typess = node_match_type(n1, n2)
    return typess and (n1['atts'] == n2['atts'])