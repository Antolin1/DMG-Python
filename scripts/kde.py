# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:45:18 2021

@author: Jose Antonio
"""

import sys
import glob
from utils4scripts import getGraph
import numpy as np
from KDEpy import FFTKDE
from KDEpy.bw_selection import improved_sheather_jones
import matplotlib.pyplot as plt
import random
random.seed(1)
np.random.seed(1)

# add alloy, viatra option and number of samples option
def main():
    dataset_path = sys.argv[1]
    dataset = sys.argv[2]
    backend = sys.argv[3]
    #TODO: implement these two options
    #add viatra alloy config models
    generator = sys.argv[4]
    samples = sys.argv[5]
    
    train_path = dataset_path + '/train'
    graphs_train = [getGraph(f,dataset,backend) 
                for f in glob.glob(train_path + "/*")]
    
    numberObjects = np.array([[len([n for n in G])] for G in graphs_train])
    
    kernel_std = improved_sheather_jones(numberObjects)  # Shape (obs, dims)
    size = 500
    resampled_data = np.random.choice(numberObjects.flatten(), size=size, replace=True)
    resampled_data = resampled_data + np.random.randn(size) * kernel_std
    print(resampled_data)
    
    #x,y = FFTKDE(kernel='gaussian', bw='ISJ').fit(numberObjects).evaluate()
    
    #plt.plot(x, y, label="FFTKDE with Improved Sheather Jones (ISJ)")
    #plt.show()

    #params = {'bandwidth': np.logspace(-1, 1, 20),
    #     'kernel':['gaussian', 'tophat']}
    #grid = GridSearchCV(KernelDensity(), params)
    #grid.fit(np.array(numberObjects))
    #print("best bandwidth: {0}".format(grid.best_estimator_.bandwidth))
    #print("best kernel: {0}".format(grid.best_estimator_.kernel))

if __name__ == "__main__":
    main()