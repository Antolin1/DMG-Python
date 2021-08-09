#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 17:31:52 2021

@author: Jose Antonio
"""

class MetaFilter:
    def __init__(self, references = None, 
                 attributes = None,
                 classes = None):
        self.references = references
        self.attributes = attributes
        self.classes = classes