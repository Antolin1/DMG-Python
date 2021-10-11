# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:45:18 2021

@author: Jose Antonio
"""

import sys
import glob
#from utils4scripts import getGraph
import numpy as np
from KDEpy.bw_selection import improved_sheather_jones
import random
#from utils4scripts import getMetamodel, getPackage, getRoot
from argparse import ArgumentParser
from modelSet import datasets_supported
import seaborn as sns
import matplotlib.pyplot as plt


random.seed(1)
np.random.seed(1)

def getSolver(generator):
    if (generator == 'viatra'):
        return 'ViatraSolver'
    elif (generator == 'alloy'):
        return 'AlloySolver'

# add alloy, viatra option and number of samples option
def main():
    
    parser = ArgumentParser(description='Script for generate config files using KDE')


    parser.add_argument("-d", "--dataset", dest="dataset", 
                        choices=['ecore-github', 'rds-genmymodel', 
                                 'yakindu-github','yakindu-exercise'], 
                        help="dataset considered.",
                        required=True)
    parser.add_argument("-pd", "--pathdataset", dest="path_dataset",
                        help="folder of the dataset.", metavar="DIR", 
                        required=True)
    parser.add_argument("-emf", "--emf_backend", dest="emf",
                        choices=['python', 'java'],
                        help="backend to parse the models.",
                        required=True)
    
    parser.add_argument("-g", "--generator", dest="gen",
                        choices=['alloy', 'viatra'],
                        help="generator considered.",
                        required=True)
    
    parser.add_argument("-nm", "--numberModels", dest="number_models",
                        help="number of models to generate.", type=int, default = 500)
    
    parser.add_argument("-r", "--runtime", dest="runtime",
                        help="max runtime.", type=int, default = 180)
    
    parser.add_argument("-c", "--candidates", dest="cand",
                        help="candidates in each run.", type=int, default = 1)
    
    parser.add_argument("-ps", "--pathsyn", dest="path_syn",
                        help="output folder.", metavar="DIR", 
                        required=True)
    
    parser.add_argument("-p", "--plot", dest="plot", choices=['True', 'False'],
                        required=False, default="True",
                        help="if plot distributions.")
    
    
    args = parser.parse_args()
    
    dataset_path = args.path_dataset
    dataset = args.dataset
    backend = args.emf
    #TODO: implement these two options
    #add viatra alloy config models
    generator = args.gen #viatra or alloy
    samples = args.number_models
    runtime = args.runtime
    number = args.cand
    save_path = args.path_syn
    msetObject = datasets_supported[dataset]
    plot = bool(args.plot)
    
    
    train_path = dataset_path + '/train'
    graphs_train = [msetObject.getGraphReal(f,backend) 
                for f in glob.glob(train_path + "/*")]
    
    numberObjects = np.array([[len([n for n in G])] for G in graphs_train])
    #print(numberObjects.shape)
    
    kernel_std = improved_sheather_jones(numberObjects)  # Shape (obs, dims)

    resampled_data = np.random.choice(numberObjects.flatten(), size=samples, replace=True)
    resampled_data = resampled_data + np.random.randn(samples) * kernel_std
    #print(resampled_data)
    
    vsconfig = None
    with open('./data/vsconfigs/model.vsconfig', 'r') as file:
        vsconfig = file.read()
    
    rounded = []
    lower, upper = msetObject.bounds
    #delete upperbound and lowerbound
    for i,n in enumerate(resampled_data):
        candidate = int(round(n))
        if candidate < lower or candidate > upper:
            continue
        rounded.append(candidate)
        replaced = vsconfig.replace('put_here_nodes', str(candidate))
        replaced = replaced.replace('put_here_metamodel', msetObject.synMetamodelName)
        replaced = replaced.replace('put_here_package', msetObject.packageSyn)
        replaced = replaced.replace('root_class', msetObject.rootSyn)
        replaced = replaced.replace('set_runtime', str(runtime))
        replaced = replaced.replace('set_number', str(number))
        replaced = replaced.replace('put_here_solver', getSolver(generator))
        replaced = replaced.replace('outputs', 'outputs'+str(i))
        #print(replaced)
        with open(save_path+"/"+str(i)+".vsconfig", "w") as text_file:
            text_file.write(replaced)
    
    if plot:
        fig, axs = plt.subplots(ncols=2)
        sns.histplot(rounded, stat = 'density', ax=axs[0], color = 'red')
        sns.histplot(np.array([len([n for n in G]) 
                               for G in graphs_train]), stat = 'density', ax=axs[0],
                     color = 'blue')
        sns.distplot(rounded, hist=False, kde=True, 
                 bins=int(180/5), color = 'red', label = 'Syn', ax=axs[1])
        sns.distplot(np.array([len([n for n in G]) 
                               for G in graphs_train]), hist=False, kde=True, 
                 bins=int(180/5), color = 'blue', label = 'Real', ax=axs[1])
if __name__ == "__main__":
    main()