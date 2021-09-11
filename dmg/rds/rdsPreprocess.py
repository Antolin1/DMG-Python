#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 09:59:29 2021

@author: Jose Antonio
"""

from lxml import etree as ET

#remove types that cannot be resolved
#TODO resolve them by using Ecore in Java I guess
def removeTypes(path_in, path_out):
    tree = ET.parse(path_in)
    for element in tree.iter():
        if (element.tag == 'type') :
            element.getparent().remove(element)
    tree.write(path_out)
