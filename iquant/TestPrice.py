#encoding:gbk
import time,datetime
import numpy as np
import pandas as pd

def init(ContextInfo):
    stock1 = ContextInfo.get_stock_list_in_sector('����300')
    stock2 = ContextInfo.get_stock_list_in_sector('��֤500')
    ContextInfo.s = stock1 + stock2
    ContextInfo.set_universe(ContextInfo.s)
    #ContextInfo.s = ContextInfo.get_stock_list_in_sector('����A��')
    print('hellow init')

def handlebar(ContextInfo):
    d = ContextInfo.barpos
    nowDate = int(timetag_to_datetime(ContextInfo.get_bar_timetag(d),'%Y%m%d'))
    
    if (nowDate == 20170104):
        price = ContextInfo.get_history_data(2,'1d','close',2)
        #print(price)
        print(price['000975.SZ'])
        #����ǰ��Ȩ10.53
        #������Ȩ15.46
    else:
        pass
    if(ContextInfo.is_last_bar()):
        print("Job Done")


