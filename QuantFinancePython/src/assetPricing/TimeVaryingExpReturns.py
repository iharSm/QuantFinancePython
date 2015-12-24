'''
Created on Feb 1, 2015

@author: deazz
'''

import sys 
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import lognorm

class TimeVaryingExpReturns:
    sigma_eps = 0.018
    sigma_delta = 0.18
    phi = 0.94
    rho = -0.80756
    
    
    #Chol = np.array([[sigma_eps, 0],[rho*sigma_delta, np.sqrt(1-rho**2)*sigma_delta]])
    
    def corrRV(self, correlation, N):
        mean = (0,0)
        cov = [[1,correlation],[correlation,1]]
        return np.random.multivariate_normal(mean,cov, N)
    
    def model(self, errors):
        x_0 = 0
        x = [x_0]
        r = [0]
        for epsilon, delta in errors:
            x.append(self.phi*x[-1]+epsilon)
            r.append(x[-1]+delta)
            
        self.df = pd.DataFrame({'x': pd.Series(x), 'r': pd.Series(r)})    
        self.df['r5'] = self.df['r']+self.df['r'].shift(-1)+ self.df['r'].shift(-2) +self.df['r'].shift(-3) + self.df['r'].shift(-4)
        self.df['r1'] = self.df['r'].shift(-1)
        self.df['r5'] = self.df['r5'].fillna(method='ffill')
        self.df['r1'] = self.df['r1'].fillna(method='ffill')
        print self.df
        return x,r
    
    def regression(self, x, y):
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        print "slope: {}".format(slope)
        print "intercept: {}".format(intercept)
        print "r^2: {}".format(r_value**2)
        print "p_value: {}".format(p_value)
        print "std_err: {}".format(std_err)
        print "std of a+b*x: {}".format(slope**2*np.std(self.df['x']))
        print "std r: {}".format(np.std(self.df['r']))
        

if __name__ == '__main__':
    expRet = TimeVaryingExpReturns()
    x,r = expRet.model(expRet.corrRV(expRet.rho, 100))
    print "mean of expected return x: {}".format(np.mean(x))
    print "mean of log returns r: {}".format(np.mean(r))
    expRet.regression(x, r)
    expRet.regression(r, expRet.df['r1'])


    plt.plot(x,expRet.df['r5'],'x')
    plt.axis('equal')
    plt.show()