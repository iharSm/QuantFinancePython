import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import numpy as nu
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import os


class Portfolio:
    #def equities = []
    #def allocations = []
    
    def __init__(self, equities, allocations):
        self.equities = equities
        self.allocations = allocations

class PortfolioSimulation:
    #def portfolio
    #def start_date
    #def end_date
    dao =  da.DataAccess('Yahoo', cachestalltime=0)
     
    def __init__(self, portfolio, start_date, end_date):
        self.portfolio = portfolio
        self.start_date = start_date
        self.end_date = end_date
           
    def get_data(self, keys):
        dt.timedelta(hours=16)
        ldt_timestamps = du.getNYSEdays(self.start_date, self.end_date, dt.timedelta(hours=16))
        data = self.dao.get_data(ldt_timestamps, self.portfolio.equities, keys)
        return dict(zip(keys, data))
    
    def data_fix(self, map):
        map = map.fillna(method='ffill')
        map = map.fillna(method='bfill')
        map = map.fillna(1.0)
        
    def calculate_returns(self, equity_prices):
        return tsu.returnize0(equity_prices)
                                  
    def simulate(self):
        return 0
        
    def calculate_optimal_allocations(self):
        return 0

    def print_results(self):
        print '\n allocated returns: \n  {}'.format(allocated_ret)
        print '\n comulative daily returns:\n {}'.format(cumulative_daily_return)
        print '\n mean: \n {}'.format(mean)
        print '\n standard deviation:\n {} \n'.format(std) 
        print '\n Sharpe ratio:\n {} \n'.format(sharpe)
    


def  simulate(startdate, enddate, equities, allocations):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(startdate, enddate, dt_timeofday)

   # c_dataobj = da.DataAccess('Yahoo')
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = [ 'close', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, equities, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
   # index_data = c_dataobj.get_data(ldt_timestamps, ['$SPX'], ls_keys)
    # i_data = dict(zip(ls_keys, index_data))
    # rint d_data['close']

    na_pr = d_data['close']
    na_pr = na_pr.fillna(method='ffill')
    na_pr = na_pr.fillna(method='bfill')
    na_pr = na_pr.fillna(1.0)
    
    na_price = na_pr.values
    
    # index_pr = i_data['close']
    # index_pr = index_pr.fillna(method='ffill')
    # index_pr = index_pr.fillna(method='bfill')
    # index_pr = index_pr.fillna(1.0)
    
    # index_price = index_pr.values

   # print na_price
   # print na_price[1, :]
    # na_normalized_price = na_price / na_price[0, :]
    
    na_rets = na_price.copy()
    # na_rets = na_normalized_price.copy()
    tsu.returnize0(na_rets)
    
    # index_rets = index_price.copy()
    # tsu.returnize0(index_rets)
   
   # plt.plot(ldt_timestamps, na_rets)
    # plt.legend(equities)
   # plt.ylabel('Adjusted Close')
   # plt.xlabel('Date')
   # plt.draw()
   # plt.show()

    print na_rets
    allocated_ret = na_rets * allocations
    print '\n allocated returns: \n  {}'.format(allocated_ret)
    cumulative_daily_return = nu.sum(allocated_ret, axis=1)
    print '\n comulative daily returns:\n {}'.format(cumulative_daily_return)

    mean = nu.mean(cumulative_daily_return)
    # index_mean = nu.mean(index_rets)
    print '\n mean: \n {}'.format(mean)
    
    std = nu.std(cumulative_daily_return)
    print '\n standard deviation:\n {} \n'.format(std) 

   # sharpe = (mean - index_mean) / nu.std(cumulative_daily_return - index_rets)
    sharpe = (mean) * nu.sqrt(252) / nu.std(cumulative_daily_return)
    print '\n Sharpe ratio:\n {} \n'.format(sharpe)

    return std, mean, sharpe, nu.prod(cumulative_daily_return + 1)

# vol, daily_ret, sharpe, cum_ret = simulate(dt.datetime(2010, 1, 1), dt.datetime(2010, 12, 31), ['AXP', 'HPQ', 'IBM', 'HNZ'], [0.0, 0.0, 0.0, 1.0])

# vol, daily_ret, sharpe, cum_ret = simulate(dt.datetime(2011, 1, 1), dt.datetime(2011, 12, 31), ['AAPL', 'GLD', 'GOOG', 'XOM'], [0.4, 0.4, 0.0, 0.2])

#vol, daily_ret, sharpe, cum_ret = simulate(dt.datetime(2010, 1, 1), dt.datetime(2010, 12, 31),  ['BRCM', 'TXN', 'AMD', 'ADI'] , [0.4, 0.6, 0.0, 0.])

max_sharpe = 0
max_vol = 0
max_daily_ret = 0
max_cum_ret = 0;
allocations = []

for i in nu.arange(0, 1.1, 0.1):
    for j in nu.arange(0, 1.1, 0.1):
        for k in nu.arange(0, 1.1, 0.1):
           for l in nu.arange(0, 1.1, 0.1): 
               if i + j + k + l == 1 :
                   vol, daily_ret, sharpe, cum_ret = simulate(dt.datetime(2010, 1, 1), dt.datetime(2010, 12, 31),  ['BRCM', 'TXN', 'IBM', 'HNZ']  , [i, j, k, l])
                   print [i, j, k, l]
                   if sharpe > max_sharpe:
                       max_sharpe = sharpe
                       max_vol = vol
                       max_daily_ret = daily_ret
                       max_cum_ret = cum_ret
                       allocations = [i, j, k, l]

print max_vol
print max_daily_ret
print max_sharpe
print max_cum_ret
print allocations







