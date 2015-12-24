import sys 
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
#import pylab
import matplotlib.pyplot as plt
from sets import Set
from numpy import NaN


class MarketSimulator:
    keys = ['year', 'month', 'day', 'symbol', 'order_type', 'number_of_shares']

    #def __init__(self):

        
    def calculate_portfolio_values_by_orders(self, initialCash, ordersPath, valuesPath):  
        self.initialCash = long(initialCash)
        self.ordersPath = ordersPath
        self.valuesPath = valuesPath
        
        self.orders_frame = pd.read_csv("./"+ordersPath,
                            names = self.keys
                            ,index_col=False).sort(columns = ['year', 'month', 'day'], ascending=True)
        self.orders_frame ['date'] = pd.to_datetime(self.orders_frame.apply(lambda x: str(x['year']) + " "
                    + " " + str(x['month'])
                    + " " + str(x['day'])
                    + " " + '16:00:00', 1))
        print self.orders_frame 
        self.retrieve_closing_prices()
        
    def calculate_portfolio_values(self):
        cash = self.initialCash
        l = [0] * len(self.keys)
        stocks = dict(zip(self.keys, l))
        prices = self.closing_prices['close']
        
        number_of_stocks = [ x + '_COUNT' for x in self.symbol_set]
        number_of_stocks.remove('SPY_COUNT')
        self.values = pd.DataFrame(index = prices.index, columns = number_of_stocks)
        self.values = self.values.fillna(0)
        self.values['total_value'] = self.initialCash
        self.values['cash'] = self.initialCash
        
        fr = self.orders_frame
        fr = fr.drop('year',1)
        fr = fr.drop('month',1)
        fr = fr.drop('day',1)
        self.values = fr.join(self.values, on = 'date', how='outer', sort=True)
        self.values = self.values.join(self.closing_prices['close'], on = 'date', how='outer', sort=True)
        ind = range(len(self.values.index))
        self.values.index = ind
        print self.values
        
        count = self.values[number_of_stocks].head(1)
        cash = self.values['cash'].head(1)
        for i, row in self.values.iterrows():
            if not pd.isnull(row['symbol']):
                price = row[row['symbol']]
                if row['order_type'] == 'BUY':
                    count[row['symbol']+'_COUNT'] += row['number_of_shares']
                    cash -= row['number_of_shares']*price
                else :
                    count[row['symbol']+'_COUNT'] -= row['number_of_shares']
                    cash += row['number_of_shares']*price
            self.values.loc[i, 'cash'] = cash[0]
            self.values.loc[i, number_of_stocks] = count
        
        stocks = self.symbol_set
        stocks.remove('SPY')
        sum = self.values[stocks[0]]*0
        
        for stock in stocks :
            self.values[stock] = self.values[stock].fillna(method='ffill')
            self.values[stock] = self.values[stock].fillna(method='bfill')
            self.values[stock] = self.values[stock].fillna(1.0)
        
        for stock in stocks :
            sum += self.values[stock]*self.values[stock+'_COUNT']
            print ' {}  -- {} -- {} -- {}'.format(sum[0], stock, self.values[stock][0], self.values[stock+'_COUNT'][0])
        self.print_to_file(sum, 'sum.csv')
        self.values['total_value'] = self.values['cash'] + sum
        
        self.print_to_file(self.values, 'all_values.csv')

        df = self.values[['date','total_value']].copy()
        df.index = df.date
        df = df.drop('date', 1)
        return df
            
       
    def retrieve_closing_prices(self): 
        symbol_set = list(Set(self.orders_frame['symbol']))
        self.symbol_set = symbol_set
        start_date = self.orders_frame.iloc[:, :3].head(1)
        end_date = self.orders_frame.iloc[:, :3].tail(1)
             
        dt_start = dt.datetime(start_date['year'], start_date['month'], start_date['day'])
        dt_end = dt.datetime(end_date['year'], end_date['month'], end_date['day'])
        dt_end += dt.timedelta(days = 1);
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
        self.dates = ldt_timestamps

        dataobj = da.DataAccess('Yahoo')
        symbol_set.append('SPY')

        ls_keys = ['close']
        ldf_data = dataobj.get_data(ldt_timestamps, symbol_set, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        print d_data
        self.closing_prices = d_data
    
    def set_dates(self, start_date, end_date):
        self.dates = du.getNYSEdays(start_date, end_date, dt.timedelta(hours=16))
    
    def retrieve_closing_prices_for_stock(self, stock):
        dataobj = da.DataAccess('Yahoo')
        ls_keys = ['close']
        ldf_data = dataobj.get_data(self.dates, [stock], ls_keys)
        return dict(zip(ls_keys, ldf_data))
        
    def print_to_file(self, frame, file):
        frame.to_csv(file)
        
    def analyse(self, portfolio, benchmark):
        benchmark_prices = self.retrieve_closing_prices_for_stock(benchmark)
        
       
        portfolio = portfolio.groupby(level = 0)
        portfolio = portfolio.last()
        portfolio_returns = portfolio['total_value'].copy()
        tsu.returnize0(portfolio_returns)
        portfolio_mean = np.mean(portfolio_returns)
        print portfolio_returns
        portfolio_std = np.std(portfolio_returns)
        
        benchmark_returns = benchmark_prices['close']
        benchmark_returns = benchmark_returns[benchmark]
        tsu.returnize0(benchmark_returns)
        benchmark_mean = np.mean(benchmark_returns)
        benchmark_std = np.std(benchmark_returns)

        print 'Sharpe Ratio of Fund : {}'.format(np.sqrt(252)*portfolio_mean/portfolio_std)
        print 'Sharpe Ratio of {} : {}\n'.format(benchmark, np.sqrt(252)*benchmark_mean/benchmark_std)
        print 'Total Return of Fund : {}'.format(np.prod(portfolio_returns + 1, axis = 1))
        print 'Total Return of {} : {}\n'.format(benchmark, np.prod(benchmark_returns + 1, axis = 1))
        print 'Standard Deviation of Fund: {}'.format(portfolio_std)
        print 'Standard Deviation of {}: {}\n'.format(benchmark,benchmark_std)
        print 'Average Daily Return of Fund: {}'.format(portfolio_mean)
        print 'Average Daily Return of Fund {} : {}'.format(benchmark,benchmark_mean)
        
        
    def get_bollinger(self, frame, window):
        plt.clf()
        print pd.rolling_mean(frame, window)
        print pd.rolling_std(frame,window)
      #  print (frame['AAPL'] - pd.rolling_mean(frame, 20)['AAPL'])/pd.rolling_std(frame,20)['AAPL']
        bolinger_val = (frame - pd.rolling_mean(frame, window))/pd.rolling_std(frame,window)
#         self.print_to_file(bolinger_val, './bolinger.csv')
#         bollinger1 = lambda x : (x.mean()+x.std())
#         bollinger2 = lambda x : (x.mean()-x.std())
#         roll_average = lambda x : x.mean()
#         plt.subplot(211)
#         plt.plot(pd.rolling_apply(frame, window, roll_average))
#         plt.plot(pd.rolling_apply(frame, window, bollinger1))
#         plt.plot(pd.rolling_apply(frame, window, bollinger2))
#         plt.plot(frame)
#         plt.subplot(212)
#         plt.plot(bolinger_val)
      #  plt.show()
        return bolinger_val
        
    def get_bolinger_for_list(self, symbols, data, window):   
        bolinger = pd.DataFrame(index = data['close'].index, columns = symbols)
        for s_sym in symbols: 
            bolinger[s_sym] = self.get_bollinger(data['close'][s_sym], window)
        return bolinger 
        
    
if __name__ == '__main__':
    print "cash: {}".format(sys.argv[1])
    print "orders: {}".format(sys.argv[2])
    print "values: {}".format(sys.argv[3])
    market = MarketSimulator()
    market.set_dates(dt.datetime(2008,1,1), dt.datetime(2009,12,30))
    
    market.calculate_portfolio_values_by_orders(sys.argv[1], sys.argv[2], sys.argv[3])
    portfolio = market.calculate_portfolio_values()
    market.print_to_file(portfolio, market.valuesPath)
    market.analyse(portfolio, '$SPX')
#     goog = market.retrieve_closing_prices_for_stock('MSFT')['close']
#     window = 20
#     market.get_bollinger(goog, window)
