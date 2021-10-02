#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 12:02:28 2021

@author: Jose Antonio
"""

import sys
import os
sys.path.append(os.getcwd())

from argparse import ArgumentParser

parser = ArgumentParser(description='Script for training the generator')

parser.add_argument("-s", "--save", dest="save_path",
                    help="path to save the model file", metavar="FILE", 
                    required=True)
parser.add_argument("-d", "--dataset", dest="dataset", 
                    choices=['ecore-github', 'rds-genmymodel', 
                             'yakindu-github','yakindu-exercise'], 
                    help="dataset considered",
                    required=True)
parser.add_argument("-pd", "--pathdataset", dest="path_dataset",
                    help="folder of the dataset", metavar="DIR", 
                    required=True)
parser.add_argument("-e", "--epochs", dest="epochs",
                    help="max epochs", type=int, 
                    required=True)
parser.add_argument("-es", "--earlyStopping", dest="earlyStop", 
                    choices=['clean','iso', 'inco'], 
                    help="criteria to stop", default = 'clean')
parser.add_argument("-sh", "--shuffle", dest="shuffle", 
                    choices=['True', 'False'], 
                    help="shuffle actions", default = 'True')


args = parser.parse_args()

model_path = args.save_path
dataset = args.dataset
path_dataset = args.path_dataset