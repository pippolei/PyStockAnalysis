#encoding:gbk
import time
import datetime
import os
import numpy as np
import pandas as pd
import logging

def init(ContextInfo):
    stock1 = ContextInfo.get_stock_list_in_sector('沪深300')
    stock2 = ContextInfo.get_stock_list_in_sector('中证500')
    ContextInfo.s = stock1 + stock2
    #ContextInfo.s = ContextInfo.get_stock_list_in_sector('沪深A股')
    ContextInfo.set_universe(ContextInfo.s)
    ContextInfo.myflag = False
    ContextInfo.accountID='416600037920'
    print('hellow init')

def handlebar(ContextInfo):
    d = ContextInfo.barpos
    nowDate = int(timetag_to_datetime(ContextInfo.get_bar_timetag(d),'%Y%m%d'))
    
    if (nowDate == 20190904):
        print("position information")
        objlist = get_trade_detail_data(ContextInfo.accountID,'stock','position')
        for obj in objlist:
            print(obj.m_strInstrumentID)
            print("BuyDate is:"+obj.m_strOpenDate)
            print("Trading day is:"+obj.m_strTradingDAy)
            #print(dir(obj))
        print("deal information")
        objlist = get_trade_detail_data(ContextInfo.accountID,'stock','deal')
        for obj in objlist:
            print(obj.m_strInstrumentID)
            print(obj.m_strTradeDate)
            #print(dir(obj))
    else:
        pass
    if(ContextInfo.is_last_bar()):
        print("Job Done")


