#coding=gbk
import os, math
import matplotlib
import numpy as np
import pandas as pd
import talib as ta
import datetime
import string
from sklearn.preprocessing import OneHotEncoder 
from sklearn.preprocessing import LabelEncoder


START_ATTRIBUTE = 130
START_ANALYSIS = 160
ATTR_CALC_STARTINDEX = 70
FLOAT_MIN = 0.0001

def getStockFull(stockdata):
    newdata = stockdata.copy()
    end = stockdata["end"]
    low = stockdata["low"]
    high = stockdata["high"]
    
    #向下移一个，第一行为空，第二行为原第一行的值
    cmpdata = stockdata["end"].shift(1)
    #向上移一个，最后一行为空，第一行为原第二行的值 
    cmpdata_low = stockdata["low"].shift(-1, fill_value = 0)
    cmpdata_start = stockdata["start"].shift(-1, fill_value = 100000)
    
    newdata["RIZE"] = np.nan_to_num((end - cmpdata) / cmpdata)
    newdata["CANBUY"] = (cmpdata_low < end)
    newdata["AVE5"] = ta.MA(np.array(end), 5)  # @UndefinedVariable
    newdata["AVE10"] = ta.MA(np.array(end), 10)  # @UndefinedVariable
    newdata["AVE13"] = ta.MA(np.array(end), 13)  # @UndefinedVariable
    newdata["AVE20"] = ta.MA(np.array(end), 20)  # @UndefinedVariable
    newdata["AVE30"] = ta.MA(np.array(end), 30)  # @UndefinedVariable
    newdata["AVE60"] = ta.MA(np.array(end), 60)  # @UndefinedVariable    
    volume = [float(x) for x in stockdata["volume"]]
    newdata["AVE_VOLUME10"] = ta.MA(np.array(volume),10) # @UndefinedVariable  
    newdata["AVE_VOLUME20"] = ta.MA(np.array(volume),20) # @UndefinedVariable  
    newdata["LOW10"] = ta.MIN(end,10) # @UndefinedVariable
    newdata["LOW20"] = ta.MIN(end,20) # @UndefinedVariable
    newdata["LOW60"] = ta.MIN(end,60) # @UndefinedVariable
    newdata["HIGH10"] = ta.MAX(end,10) # @UndefinedVariable
    newdata["HIGH20"] = ta.MAX(end,20) # @UndefinedVariable
    newdata["HIGH60"] = ta.MAX(end,60) # @UndefinedVariable
    #newdata["EMA12"] = ta.EMA(end, 12) # @UndefinedVariable
    #newdata["EMA26"] = ta.EMA(end, 26) # @UndefinedVariable
    #newdata["DIF"],newdata["DEA"],nodata  = ta.MACD(end, 12,26,9) # @UndefinedVariable
    newdata["POST1"] = (end.shift(-1, fill_value = end.iloc[-1])  - end) / end
    newdata["POST2"] = (end.shift(-2, fill_value = end.iloc[-1])  - end) / end
    newdata["POST3"] = (end.shift(-3, fill_value = end.iloc[-1])  - end) / end
    newdata["POST4"] = (end.shift(-4, fill_value = end.iloc[-1])  - end) / end
    newdata["POST5"] = (end.shift(-5, fill_value = end.iloc[-1])  - end) / end
    
    newdata["END_ABOVE_AVE_10"] = (end - newdata["AVE10"]) > FLOAT_MIN
    newdata["END_ABOVE_AVE_20"] = (end - newdata["AVE20"]) > FLOAT_MIN
    newdata["END_ABOVE_AVE_60"] = (end - newdata["AVE60"]) > FLOAT_MIN
    newdata["A10_ABOVE_20"] = (newdata["AVE10"] - newdata["AVE20"]) > FLOAT_MIN
    newdata["A10_ABOVE_60"] = (newdata["AVE10"] - newdata["AVE60"]) > FLOAT_MIN
    newdata["A20_ABOVE_60"] = (newdata["AVE20"] - newdata["AVE60"]) > FLOAT_MIN
    
    newdata["END_FAR_ABOVE_05"] = (end - newdata["AVE5"] * 1.1) > FLOAT_MIN
    newdata["END_FAR_BELOW_05"] = (end - newdata["AVE5"] * 0.9) < FLOAT_MIN
    newdata["END_ABOVE_HIGH_60"] = (end - newdata["HIGH60"] * 0.85) < FLOAT_MIN
    newdata["END_BELOW_LOW_60"] = (end - newdata["LOW60"] * 1.35) > FLOAT_MIN
    
    #       'START_RIZE', 'START_RIZE_BIG', 'IS_BIG_RIZE', 'IS_MEDIUM_RIZE',
    newdata["START_RIZE"] = (cmpdata_start - end) > FLOAT_MIN
    newdata["START_RIZE_BIG"] = (cmpdata_start - end * 1.02) > FLOAT_MIN
    newdata["IS_BIG_RIZE"] = newdata["RIZE"] - 0.04 > FLOAT_MIN
    newdata["IS_MEDIUM_RIZE"] = newdata["RIZE"] - 0.02 > FLOAT_MIN
    
    
    newdata["RIZE2"] = np.nan_to_num((high - low) / end)
    (newdata["DEF_SELL_SHORT_index"],newdata["DEF_SELL_SHORT_date"],newdata["DEF_SELL_SHORT_price"]) = pd.Series(getDefaultSell(stockdata, 5, 0.05, 0.03))
    (newdata["DEF_SELL_MEDIUM_index"],newdata["DEF_SELL_MEDIUM_date"],newdata["DEF_SELL_MEDIUM_price"]) = getDefaultSell(stockdata, 20, 100, 1)
    (newdata["DEF_SELL_LONG_index"],newdata["DEF_SELL_LONG_date"],newdata["DEF_SELL_LONG_price"]) = getDefaultSell(stockdata, 20, 100, 0.08)
    (newdata["DEF_SELL_END_index"],newdata["DEF_SELL_END_date"],newdata["DEF_SELL_END_price"]) = getDefaultSell(stockdata, 40, 100, 1)

    newdata = newdata.fillna(0)
    return newdata

    

def getDiffValue(code,g_stock1, g_stock2):
    codediff = ""
    stockitem = g_stock1.get_group(code)
    stockitem_py = g_stock2.get_group(code)
    stockitem.set_index('index', inplace=True)
    stockitem_py.set_index('index', inplace=True)
    
    #newdata = getStockFull(stockitem)
    newdata = stockitem.fillna(0)
    colsize = stockitem_py.shape[1]
    data_py = stockitem_py.fillna(0)
    data = newdata[data_py.columns]
    c = data_py.iloc[:,1:] - data.iloc[:,1:]
    coldiff = c.iloc[START_ATTRIBUTE:,:].sum()
    diff = sum(c.iloc[START_ATTRIBUTE:,:].sum()) + (data.shape[0] - data_py.shape[0])
    print(code + " total difference:" + str(diff) + " max diff column: " + abs(coldiff).idxmax() + " and size1:" + str(data.shape[0]) + "   size2:" + str(data_py.shape[0]))
    if data_py.shape[0] != data.shape[0]:
        codediff = codediff + code + " "
    return data, data_py, codediff, diff


def calculateEMA(period, closeArray, emaArray=[]):
    """计算指数移动平均"""
    length = len(closeArray)
    nanCounter = np.count_nonzero(np.isnan(closeArray))
    if not emaArray:
        emaArray.extend(np.tile([np.nan],(nanCounter + period - 1)))
        firstema = np.mean(closeArray[nanCounter:nanCounter + period - 1])    
        emaArray.append(firstema)    
        for i in range(nanCounter+period,length):
            ema=(2*closeArray[i]+(period-1)*emaArray[-1])/(period+1)
            emaArray.append(ema)        
    return np.array(emaArray)
    
def calculateMACD(closeArray,shortPeriod = 12 ,longPeriod = 26 ,signalPeriod =9):
    ema12 = calculateEMA(shortPeriod ,closeArray,[])
    ema26 = calculateEMA(longPeriod ,closeArray,[])
    diff = ema12-ema26    
    dea= calculateEMA(signalPeriod ,diff,[])
    macd = 2*(diff-dea)
    return macd,diff,dea 

#从YYYYMMDD转换到YYYYY-MM-DD
def formatDate(intdate):
    intdate = str(intdate)
    return intdate[0:4] + "-" + intdate[4:6] + "-" + intdate[6:8]


def validStock(stockitem):  
    if (stockitem.shape[0] < START_ANALYSIS
        or stockitem["end"].min() < 0.3        
        ):
        ret_value = 0
    else:
        ret_value = 1
    return ret_value
        
def getDefaultSell(stockdata, day, winrate, lossrate):
    end = stockdata["end"]
    date = stockdata["date"]
    index = stockdata["index"]
    winend = end * (1 + winrate)
    lossend = end * (1 - lossrate)    
    
    newdata = pd.DataFrame()
    newdata["end0"] = end  
    for i in range(day):
        newdata["end"+str(i+1)] = end.shift(-1 - i, fill_value = end.iloc[-1])
    ifwin = newdata.values > winend.values[:,None]
    ifloss = newdata.values < lossend.values[:,None]
    cmp_result = (ifwin | ifloss).argmax(axis = 1)
    cmp_result = np.where(cmp_result==0,day,cmp_result)
    
    np_index = np.array(index)
    sellindex = np_index + cmp_result
    for j in range(day):
        sellindex[-1 - j] = np_index[-1]
    sellprice = end[sellindex]
    selldate = date[sellindex]    
    return sellindex, selldate.values, sellprice.values
    
    

