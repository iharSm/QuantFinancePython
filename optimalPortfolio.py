import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import numpy as nu
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import os


#clear = lambda: os.system('cls')
#clear()
os.system('cls')

#l_symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
dt_start = dt.datetime(2011, 1,1)
dt_end = dt.datetime(2011, 12, 31)


def  simulate(startdate, enddate, equities, allocations):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(startdate,enddate, dt_timeofday)

    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = [ 'close', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, equities, ls_keys)
    index_data = c_dataobj.get_data(ldt
    d_data = dict(zip(ls_keys, ldf_data))
    #rint d_data['close']

    na_price = d_data['close'].values
    # plt.clf()
    # plt.plot(ldt_timestamps, na_price)
    # plt.legend(ls_symbols)
    # plt.ylabel('Adjusted Close')
    # plt.xlabel('Date')
    # plt.draw()
    # plt.show()

   # print na_price
   # print na_price[1, :]
    na_normalized_price = na_price / na_price[0, :]
    #plt.clf()
    # plt.plot(ldt_timestamps, na_normalized_price)
    # plt.legend(ls_symbols)
    # plt.ylabel('Adjusted Close')
    # plt.xlabel('Date')
    # plt.draw()
    # plt.show()
    
    na_rets = na_price #na_normalized_price.copy()
    tsu.returnize0(na_rets)
   
    plt.plot(ldt_timestamps,na_rets)
    plt.legend(ls_symbols)
    plt.ylabel('Adjusted Close')
    plt.xlabel('Date')
   # plt.draw()
   # plt.show()

    print na_rets
    allocated_ret = na_rets*allocations
    print '\n allocated returns: \n  {}'.format(allocated_ret)
    cumulative_daily_return = nu.sum( allocated_ret,axis=1)
    print '\n comulative daily returns:\n {}'.format(cumulative_daily_return)

    mean = nu.mean(cumulative_daily_return)
    print '\n mean: \n {}'.format(mean)
    
    std = nu.sqrt(nu.std( allocated_ret))
    print '\n standard deviation:\n {} \n'.format(std) 

    sharpe = mean/std
    print '\n Sharpe ratio:\n {} \n'.format(sharpe)

    return std,mean,sharpe, nu.sum(cumulative_daily_return)

   vol, daily_ret, sharpe, cum_ret = simulate( dt.datetime(2011, 1,1), dt.datetime(2011, 1,31 ), ['AAPL', 'GLD', 'GOOG', 'XOM'], [0.4, 0.4, 0.0, 0.2])

print vol
print daily_ret
print sharpe
print cum_ret







