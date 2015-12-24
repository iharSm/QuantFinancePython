'''
Created on Jan 25, 2015

@author: deazz
'''
import sys 
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import lognorm



if __name__ == '__main__':
    df = pd.DataFrame.from_csv('assetpricing_data_ps1_data.csv')
    # Return       D/P   D_grows  T-bill_ret
    
    print "mean of stock returns: {}".format(np.mean(df['Return']))
    print "mean of treasures returns: {}".format(np.mean(df['T-bill_ret']))
    
    mean_excess_return = np.mean(df['Return']-df['T-bill_ret'])
    print "mean of excess returns: {}".format(mean_excess_return)
    print "standard deviation of stock returns: {}".format(np.std(df['Return']))
    print "standard deviation of treasures returns: {}".format(np.std(df['T-bill_ret']))
    std_excess_return = np.std(df['Return']-df['T-bill_ret'])
    df['excess_return'] = df['Return']-df['T-bill_ret']
    print "standard deviation of excess returns: {}".format(std_excess_return)
    print "Sharpe ratio of excess returns: {} ".format(mean_excess_return/std_excess_return)
    
    plt.plot(df.index , df['Return'], label = 'stock returns')
    plt.plot(df.index, df['T-bill_ret'], label = 'T-bill returns')
    plt.plot(df.index, df['Return'] - df['T-bill_ret'], label = 'Excess returns')
    plt.plot(df.index, df['D/P'], label = 'Dividends to Price ratio')
    #plt.plot(df.index, df.mean)
    plt.legend(loc=2, borderaxespad=0.)
    #plt.show()
    
    #add shifted stock returns column
    df['Return_shift'] = df['Return'].shift(1)
    df['bill_ret_shift'] = df['T-bill_ret'].shift(1)
    df['excess_return_shift'] = df['excess_return'].shift(1)
    df['D/P_shift'] = df['D/P'].shift(1)
    df['Return_shift'] = df['Return_shift'].fillna(method='bfill')
    df['bill_ret_shift'] = df['bill_ret_shift'].fillna(method='bfill')
    df['excess_return_shift'] = df['excess_return_shift'].fillna(method='bfill')
    df['D/P_shift'] = df['D/P_shift'].fillna(method='bfill')
    ####################################################################################
    slope, intercept, r_value, p_value, std_err = stats.linregress(df['Return_shift'], df['Return'])
    print "\n\nStock returns stats:"
    print "slope: {}".format(slope)
    print "t-statistics: {}".format(slope/std_err)
    print "Regression R^2: {}".format(r_value**2)
    
    df['Stock_Expected_returns'] = slope*df['Return_shift'] + intercept
   # print df
    print "expected return: {}".format(np.mean(df['Stock_Expected_returns']))
    print "std of expected returns: {}".format(np.std(df['Stock_Expected_returns']))
    #################################################################################################
    slope, intercept, r_value, p_value, std_err = stats.linregress(df['bill_ret_shift'], df['T-bill_ret'] )
    print "\n\n T-bill returns stats:"
    print "slope: {}".format(slope)
    print "t-statistics: {}".format(slope/std_err)
    print "Regression R^2: {}".format(r_value**2)
    
    df['TBill_Expected_returns'] = slope*df['bill_ret_shift'] + intercept
   # print df
    print "expected return: {}".format(np.mean(df['TBill_Expected_returns']))
    print "std of expected returns: {}".format(np.std(df['TBill_Expected_returns']))
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(df['excess_return_shift'], df['excess_return'])
    print "\n\n Excess returns stats:"
    print "slope: {}".format(slope)
    print "t-statistics: {}".format(slope/std_err)
    print "Regression R^2: {}".format(r_value**2)
    
    df['Excess_Expected_returns'] = slope*df['excess_return_shift'] + intercept
   # print df
    print "expected return: {}".format(np.mean(df['Excess_Expected_returns']))
    print "std of expected returns: {}".format(np.std(df['Excess_Expected_returns']))
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(df['D/P_shift'], df['Return'] - df['T-bill_ret'] )
    print "\n\n  forecasting regressions of excess returns:"
    print "slope: {}".format(slope)
    print "t-statistics: {}".format(slope/std_err)
    print "Regression R^2: {}".format(r_value**2)
    
    df['DP_Expected_returns'] = slope*df['D/P_shift'] + intercept
   # print df
    print "expected return: {}".format(np.mean(df['DP_Expected_returns']))
    print "std of expected returns: {}".format(np.std(df['DP_Expected_returns']))
    print p_value
