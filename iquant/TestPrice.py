#encoding:gbk
import time,datetime
import numpy as np
import pandas as pd

def init(ContextInfo):
    stock1 = ContextInfo.get_stock_list_in_sector('沪深300')
    stock2 = ContextInfo.get_stock_list_in_sector('中证500')
    ContextInfo.s = stock1 + stock2
    ContextInfo.set_universe(ContextInfo.s)
    #ContextInfo.s = ContextInfo.get_stock_list_in_sector('沪深A股')
    print('hellow init')

def handlebar(ContextInfo):
    d = ContextInfo.barpos
    nowDate = int(timetag_to_datetime(ContextInfo.get_bar_timetag(d),'%Y%m%d'))
    
    if (nowDate == 20201016):
        code = '600109.SH'
        close = ContextInfo.get_history_data(20,'1d','close',1, False)
        open = ContextInfo.get_history_data(20,'1d','open',1, False)
        high = ContextInfo.get_history_data(20,'1d','high',1, False)
        low = ContextInfo.get_history_data(20,'1d','low',1, False)
        #print(price)
        print(close[code])
        print(open[code])
        print(high[code])
        print(low[code])
        #期望前复权10.53
        #期望后复权15.46
    else:
        pass
    if(ContextInfo.is_last_bar()):
        print("Job Done")


