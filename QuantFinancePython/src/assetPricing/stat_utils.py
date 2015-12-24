'''
Created on Jan 24, 2015

@author: deazz
'''
import sys 
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import lognorm

def ArithmeticReturn_Expectation(T, mu, sigma):
   # return math.exp(T*(mu + 0.5*sigma*sigma))
   return math.exp(T*mu)

def ArithmeticReturn_std(T, mu, sigma):
    #return math.exp(mu*T+0.5*T*sigma*sigma)*math.sqrt(math.exp(T*sigma*sigma)-1)
    return math.sqrt(math.exp(sigma*sigma*T)-1)*math.exp(mu*T)

def ArithmeticReturn_Sharpe(T, mu, sigma):
    return (ArithmeticReturn_Expectation(T, mu, sigma)-1)/ArithmeticReturn_std(T, mu, sigma)

def plotLognormalDistribution(label, mu, sigma):
    dist=lognorm([sigma],loc=mu)
    x=np.linspace(0,6,200)
    d = plt.plot(x,dist.pdf(x), label = label)
    print "lognormal {} {} \n".format(mu, sigma)
    print "mean: {}\n".format(dist.mean())
    print "median {}\n". format(dist.median())
    print "mode {}\n".format(np.exp(mu - sigma**2))
    print "probability that x < mean {}".format(dist.cdf(dist.mean()))
    dist.mean()
   # plt.plot(x,dist.cdf(x))
    
def plot_sharpe() :
    print ArithmeticReturn_Expectation(100, 0.06, 0.2)
    print ArithmeticReturn_std(100, 0.06, 0.2)
    print ArithmeticReturn_Sharpe (100, 0.06, 0.2)
    
    t = np.arange(1, 100, 1)
    
    sh = []
    h = []
    for i in t:
        sh.append(ArithmeticReturn_Sharpe(i,  0.06, 0.2))
        h.append(0.06*math.sqrt(i)/0.2)
    plt.plot(t, sh)
    plt.plot(t, h)
    plt.show()   

if __name__ == '__main__':
    mu = 0.06
    sigma = 0.2
    
    t = [10]
    for i in t :
        plotLognormalDistribution(i, ArithmeticReturn_Expectation(i, mu, sigma), ArithmeticReturn_std(i, mu, sigma))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()
    
    T = 100
    print "mean {}".format(math.exp(T*mu))
    print "std: {}".format(math.sqrt(math.exp(sigma*sigma*T)-1)*math.exp(mu*T))
    print "sharpe: {}".format((math.exp(T*mu) - 1)/(math.sqrt(math.exp(sigma*sigma*T)-1)*math.exp(mu*T)))
    