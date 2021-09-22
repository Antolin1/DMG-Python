#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 09:36:17 2021

@author: Jose Antonio
"""


def numberInconmigTransitions(G, n):
    count = 0
    for n2 in G[n]:
        for e in G[n][n2]:
            if G[n][n2][e]['type'] == 'incomingTransitions':
                count = count + 1
    return count

def numberOutgoingTransitions(G, n):
    count = 0
    for n2 in G[n]:
        for e in G[n][n2]:
            if G[n][n2][e]['type'] == 'outgoingTransitions':
                count = count + 1
    return count

def containsEntry(G,n):
    for n2 in G[n]:
        if G.nodes[n2]['type'] == 'Entry':
            return True
    return False

## No entry in region
def noEntryRegion(G):
    for n in G.nodes():
        if G.nodes[n]['type'] == 'Region' and (not containsEntry(G,n)):
            return True
    return False

def entries(G,n):
    e = 0
    for n2 in G[n]:
        if G.nodes[n2]['type'] == 'Entry':
            e = e + 1
    return e

## Multiple entry in region
def multipleEntryRegion(G):
    for n in G.nodes():
        if G.nodes[n]['type'] == 'Region' and (entries(G,n) > 1):
            return True
    return False

def toEntry(G,n):
    for n2 in G[n]:
        if G.nodes[n2]['type'] == 'Entry':
            for e in G[n][n2]:
                if G[n][n2][e]['type'] == 'target':
                    return True
    return False

## Incoming to entry
def incomingToEntry(G):
    for n in G.nodes():
        if G.nodes[n]['type'] == 'Transition' and toEntry(G,n):
            return True
    return False


def entryOutTran(G):
    for n in G.nodes():
        if G.nodes[n]['type'] == 'Entry' and (numberOutgoingTransitions(G, n) != 1):
            return True
    return False


def exitFinal(G):
    for n in G.nodes():
        if (G.nodes[n]['type'] == 'Exit' or 
            G.nodes[n]['type'] == 'Final') and (numberOutgoingTransitions(G, n) > 0):
            return True
    return False

def containsStates(G,n):
    for n2 in G[n]:
        if G.nodes[n2]['type'] == 'State':
            return True
    return False

## No state in region
def noStateRegion(G):
    for n in G.nodes():
        if G.nodes[n]['type'] == 'Region' and (not containsStates(G,n)):
            return True
    return False

def choice(G):
    for n in G.nodes():
        if (G.nodes[n]['type'] == 'Choice') and (numberInconmigTransitions(G, n) == 0 
                                                 or numberOutgoingTransitions(G, n) == 0) :
            return True
    return False

def inconsistent(G):
    return (noEntryRegion(G) or multipleEntryRegion(G)
            or incomingToEntry(G) or noStateRegion(G) or 
            choice(G) or exitFinal(G) or entryOutTran(G))