#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 17:31:52 2021

@author: Jose Antonio
"""

from pyecore.ecore import EReference, EAttribute

class MetaFilter:
    def __init__(self, references = None, 
                 attributes = None,
                 classes = None):
        self.references = references
        self.attributes = attributes
        self.classes = classes
    
    def pass_filter_object(self, o):
        if (self.classes == None):
            return True
        clazz = o.eClass
        if (clazz.name in self.classes):
            return True
        for ct in clazz.eAllSuperTypes():
            if (ct.name in self.classes):
                return True
        return False
        
    def pass_filter_structural(self, o):
        if (isinstance(o, EReference)):
            if (self.references == None):
                return True
            search = o.eContainingClass.name + "." + o.name;
            if (search in self.references):
                return True
            return False
        if (isinstance(o, EAttribute)):
            if (self.attributes == None):
                return True
            search = o.eContainingClass.name + "." + o.name;
            if (search in self.attributes):
                return True
            return False
        return False
            
        
        