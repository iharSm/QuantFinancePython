import pandas as pd
import numpy as np
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep
import src.market_simulator.MarketSimulator as ms

def find_events(ls_symbols, d_data, bolinger):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    eventNumber = 0; 
    
    orders_book = pd.DataFrame(columns=['year', 'month', 'day', 'symbol', 'order_type', 'number_of_shares'])
    
    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            bolinger_for_equity_today = bolinger[s_sym].ix[ldt_timestamps[i]]
            bolinger_for_equity_yesterday = bolinger[s_sym].ix[ldt_timestamps[i - 1]]
            bolinger_for_market_today = bolinger['SPY'].ix[ldt_timestamps[i]]
            bolinger_for_market_yesterday = bolinger['SPY'].ix[ldt_timestamps[i - 1]]
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1

            # Event is found if the symbol is down more then 3% while the
            # market is up more then 2%
            # if f_symreturn_today <= -0.03 and f_marketreturn_today >= 0.02:
            
            if (bolinger_for_equity_today < -2.0 and 
                bolinger_for_equity_yesterday >= -2.0 and
                bolinger_for_market_today >= 1.5) :
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                b = [ldt_timestamps[i].year, ldt_timestamps[i].month, ldt_timestamps[i].day, s_sym, 'BUY', 100]
                if i + 5 < len(ldt_timestamps):
                    s = [ldt_timestamps[i + 5].year, ldt_timestamps[i + 5].month, ldt_timestamps[i + 5].day, s_sym, 'SELL', 100]
                else:
                    s = [ldt_timestamps[len(ldt_timestamps) - 1].year, ldt_timestamps[len(ldt_timestamps) - 1].month, ldt_timestamps[len(ldt_timestamps) - 1].day, s_sym, 'SELL', 100]
                # d = {'year' : ldt_timestamps[i].year, 'month' : ldt_timestamps[i].month, 'day' : ldt_timestamps[i].day, 'symbol' :  s_sym,'order_type' : 'BUY', 'number_of_shares' : 100}
                # df = pd.DataFrame(d, index = [1], columns = ['year', 'month', 'day', 'symbol', 'order_type', 'number_of_shares'])
                # orders_book.append(df, ignore_index = True)
                # d = {'year' : ldt_timestamps[i+5].year, 'month' : ldt_timestamps[i+5].month, 'day' : ldt_timestamps[i+5].day, 'symbol' :  s_sym,'order_type' : 'BUY', 'number_of_shares' : 100}
                # df = pd.DataFrame(d, index = [1], columns = ['year', 'month', 'day', 'symbol', 'order_type', 'number_of_shares'])
                # orders_book.append(df, ignore_index = True)
                orders_book.loc[eventNumber] = b
                eventNumber += 1
                orders_book.loc[eventNumber] = s
                eventNumber += 1

    orders_book.to_csv('order_book.csv')
    print "/n Number of events: {}".format(eventNumber / 2)
    return df_events


if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    market = ms.MarketSimulator()
    market.set_dates(dt_start, dt_end)
    # goog = market.retrieve_closing_prices_for_stock('MSFT')['close']
    window = 20
    b = market.get_bolinger_for_list(ls_symbols, d_data, window)
    
    df_events = find_events(ls_symbols, d_data, b)
    
    
    print "Creating a Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy_12_1.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
    print "done"
