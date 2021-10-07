# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:45:18 2021

@author: Jose Antonio
"""

import sys
import glob
from utils4scripts import getGraph
import numpy as np
from KDEpy.bw_selection import improved_sheather_jones
import random
from utils4scripts import getMetamodel, getPackage, getRoot
random.seed(1)
np.random.seed(1)

def getSolver(generator):
    if (generator == 'viatra'):
        return 'ViatraSolver'
    elif (generator == 'alloy'):
        return 'AlloySolver'

# add alloy, viatra option and number of samples option
def main():
    dataset_path = sys.argv[1]
    dataset = sys.argv[2]
    backend = sys.argv[3]
    #TODO: implement these two options
    #add viatra alloy config models
    generator = sys.argv[4] #viatra or alloy
    samples = int(sys.argv[5])
    runtime = int(sys.argv[6])
    number = int(sys.argv[7])
    save_path = sys.argv[8]
    
    
    train_path = dataset_path + '/train'
    graphs_train = [getGraph(f,dataset,backend) 
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
    
    #delete upperbound and lowerbound
    for i,n in enumerate(resampled_data):
        replaced = vsconfig.replace('put_here_nodes', str(int(round(n))))
        replaced = replaced.replace('put_here_metamodel', getMetamodel(dataset))
        replaced = replaced.replace('put_here_package', getPackage(dataset))
        replaced = replaced.replace('root_class', getRoot(dataset))
        replaced = replaced.replace('set_runtime', str(runtime))
        replaced = replaced.replace('set_number', str(number))
        replaced = replaced.replace('put_here_solver', getSolver(generator))
        replaced = replaced.replace('outputs', 'outputs'+str(i))
        print(replaced)
        with open(save_path+"/"+str(i)+".vsconfig", "w") as text_file:
            text_file.write(replaced)
if __name__ == "__main__":
    main()