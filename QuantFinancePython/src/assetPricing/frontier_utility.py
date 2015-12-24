'''
Created on Feb 21, 2015

@author: deazz

def frontier():
    var_port = w_1 * var_1 + w_2 * var_2 + 2 * rho * np.sqrt(var_1) * np.sqrt(var_2)
    E_port = w_1 * E_1 + w_2 * E_2

'''

import sys 
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import lognorm

def frontier(var_1, var_2, E_1, E_2, rho):
    w_1 = np.arange(0,1, 0.01)
    w_2 = 1 - w_1
    var_port = w_1**2*var_1 + w_2**2*var_2 + 2*rho*w_1*w_2*np.sqrt(var_1)*np.sqrt(var_2)
    E_port = w_1*E_1 + w_2*E_2
    
    plt.plot( np.sqrt(var_port), E_port)
    
    
if __name__ == '__main__':
    w_1 = 0.5
    var_1 = 2
    var_2 = 3
    E_1 = 2
    E_2 = 3
    rho = 1
    
    #frontier(var_1, var_2, E_1, E_2, 1)
    frontier(var_1, var_2, E_1, E_2, -1)
    frontier(var_1, var_2, E_1, E_2, 0)
    frontier(var_1, var_2, E_1, E_2, 0.5)
       
    plt.show()