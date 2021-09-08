#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 14:15:54 2021

@author: Jose Antonio
"""
from lxml import etree as ET

#remove layout stuff
def removeLayout(path_in, path_out):
    tree = ET.parse(path_in)
    root = tree.getroot()
    for child in root:
        if (child.tag == '{http://www.eclipse.org/gmf/runtime/1.0.2/notation}Diagram' or
            child.tag == '{http://www.eclipse.org/gmf/runtime/1.0.3/notation}Diagram') :
            child.getparent().remove(child)
    tree.write(path_out)