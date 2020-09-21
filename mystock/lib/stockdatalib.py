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


START_ATTRIBUTE = 190
START_ANALYSIS = 200
ATTR_CALC_STARTINDEX = 70
FLOAT_MIN = 0.0000001

#从YYYYMMDD转换到YYYYY-MM-DD
def formatDate(intdate):
    intdate = str(intdate)
    return intdate[0:4] + "-" + intdate[4:6] + "-" + intdate[6:8]

def getDefaultSell(stockdata, day, winrate, lossrate):
    end = stockdata["end"]
    date = stockdata["date"]
    index = stockdata["index"]
    start = stockdata["start"]
    winend = end * (1 + winrate)
    lossend = end * (1 - lossrate)    
    
    newdata = pd.DataFrame()
    newdata["end0"] = end  
    for i in range(day):
        newdata["end"+str(i+1)] = end.shift(-1 - i, fill_value = end.iloc[-1])
    ifwin = newdata.values > winend.values[:,None] + FLOAT_MIN
    ifloss = newdata.values + FLOAT_MIN < lossend.values[:,None]
    #argmax 第一个为 真的
    #只要有一个止赢或者止损就为真
    cmp_result = (ifwin | ifloss).argmax(axis = 1)
    cmp_result = np.where(cmp_result==0,day,cmp_result) #np.where 如果满足条件，用 day替换，不然就保持原值 
    
    np_index = np.array(index)
    sellindex = np_index + cmp_result
    for j in range(day):  #最后day的值全部都用最后一天代替
        sellindex[-1 - j] = np_index[-1]
    sellprice = pd.Series(sellindex).apply(lambda x: start[x + 1] if x < len(start) - 1 else end[x])
    selldate = date[sellindex]    
    return sellindex, selldate.values, sellprice.values

def getStockFull(stockdata):
    newdata = stockdata.copy()
    end = stockdata["end"]
    low = stockdata["low"]
    high = stockdata["high"]
    start = stockdata["start"]
    
    #向下移一个，第一行为空，第二行为原第一行的值
    cmpdata = stockdata["end"].shift(1,fill_value = 1)
    #向上移一个，最后一行为空，第一行为原第二行的值 
    cmpdata_low = stockdata["low"].shift(-1, fill_value = 0)
    cmpdata_start = stockdata["start"].shift(-1, fill_value = end.iloc[-1])
    
    newdata["RIZERATE"] = (np.nan_to_num((end - cmpdata) / cmpdata)).astype(float)
    #newdata["RIZE_PREEND"] = (end - cmpdata) > FLOAT_MIN
    #newdata["RIZE_START"] = (end - start) > FLOAT_MIN
    #newdata["CANBUY"] = (cmpdata_low < end)
    newdata["BUYPRICE1"] = end
    newdata["BUYPRICE2"] = cmpdata_start
    newdata["BUYPRICE3"] = end * 0.98
    newdata["BUYPRICE4"] = end * 0.99
    newdata["AVE5"] = ta.MA(np.array(end), 5)  # @UndefinedVariable
    newdata["AVE10"] = ta.MA(np.array(end), 10)  # @UndefinedVariable
    newdata["AVE20"] = ta.MA(np.array(end), 20)  # @UndefinedVariable
    newdata["AVE30"] = ta.MA(np.array(end), 30)  # @UndefinedVariable
    newdata["AVE60"] = ta.MA(np.array(end), 60)  # @UndefinedVariable    
    volume = [float(x) for x in stockdata["volume"]]
    newdata["AVE_VOLUME10"] = ta.MA(np.array(volume),10) # @UndefinedVariable  
    newdata["AVE_VOLUME20"] = ta.MA(np.array(volume),20) # @UndefinedVariable  
    newdata["AVE_VOLUME60"] = ta.MA(np.array(volume),60) # @UndefinedVariable 
    newdata["LOW5"] = ta.MIN(end,5) # @UndefinedVariable 
    newdata["LOW10"] = ta.MIN(end,10) # @UndefinedVariable
    newdata["LOW20"] = ta.MIN(end,20) # @UndefinedVariable
    newdata["LOW60"] = ta.MIN(end,60) # @UndefinedVariable
    newdata["LOW130"] = ta.MIN(end,130) # @UndefinedVariable
    newdata["HIGH5"] = ta.MAX(end,5) # @UndefinedVariable
    newdata["HIGH10"] = ta.MAX(end,10) # @UndefinedVariable
    newdata["HIGH20"] = ta.MAX(end,20) # @UndefinedVariable
    newdata["HIGH60"] = ta.MAX(end,60) # @UndefinedVariable
    newdata["HIGH130"] = ta.MAX(end,130) # @UndefinedVariable
    
    newdata["TR"] = np.max(pd.DataFrame([np.abs(high - cmpdata), high - low, np.abs(cmpdata - low)]))
    newdata["ATR"] = ta.MA(np.array(newdata["TR"]), 10) # @UndefinedVariable
    #newdata["EMA12"] = ta.EMA(end, 12) # @UndefinedVariable
    #newdata["EMA26"] = ta.EMA(end, 26) # @UndefinedVariable
    #newdata["DIF"],newdata["DEA"],nodata  = ta.MACD(end, 12,26,9) # @UndefinedVariable
    newdata["POST1"] = (end.shift(-1, fill_value = end.iloc[-1])  - end) / end
    newdata["POST2"] = (end.shift(-2, fill_value = end.iloc[-1])  - end) / end
    newdata["POST3"] = (end.shift(-3, fill_value = end.iloc[-1])  - end) / end
    newdata["POST4"] = (end.shift(-4, fill_value = end.iloc[-1])  - end) / end
    newdata["POST5"] = (end.shift(-5, fill_value = end.iloc[-1])  - end) / end
    
    newdata["END_ABOVE_AVE_10"] = ((end - newdata["AVE10"]) > FLOAT_MIN).astype(int)
    newdata["END_ABOVE_AVE_20"] = ((end - newdata["AVE20"]) > FLOAT_MIN).astype(int)
    newdata["END_ABOVE_AVE_60"] = ((end - newdata["AVE60"]) > FLOAT_MIN).astype(int)
    newdata["A10_ABOVE_20"] = ((newdata["AVE10"] - newdata["AVE20"]) > FLOAT_MIN).astype(int)
    newdata["A10_ABOVE_60"] = ((newdata["AVE10"] - newdata["AVE60"]) > FLOAT_MIN).astype(int)
    newdata["A20_ABOVE_60"] = ((newdata["AVE20"] - newdata["AVE60"]) > FLOAT_MIN).astype(int)
    newdata["A10V_ABOVE_60V"] = ((newdata["AVE_VOLUME10"] - newdata["AVE_VOLUME60"] * 1.5) > FLOAT_MIN).astype(int)
    
    
    
    newdata["END_FAR_ABOVE_05"] = ((end - newdata["AVE5"] * 1.06) > FLOAT_MIN).astype(int)
    newdata["END_FAR_BELOW_05"] = ((end - newdata["AVE5"] * 0.94) < FLOAT_MIN).astype(int)
    newdata["END_ABOVE_HIGH_60"] = ((end - newdata["HIGH60"] * 0.85) < FLOAT_MIN).astype(int)
    newdata["END_BELOW_LOW_60"] = ((end - newdata["LOW60"] * 1.35) > FLOAT_MIN).astype(int)
    
    newdata["CROSS_AVE_5"] = ((end - newdata["AVE5"] > FLOAT_MIN) & (cmpdata - newdata["AVE5"] < FLOAT_MIN)).astype(int)
    newdata["CROSS_AVE_10"] = ((end - newdata["AVE10"] > FLOAT_MIN) & (cmpdata - newdata["AVE10"] < FLOAT_MIN)).astype(int)
    newdata["CROSS_AVE_20"] = ((end - newdata["AVE20"] > FLOAT_MIN) & (cmpdata - newdata["AVE20"] < FLOAT_MIN)).astype(int)
    newdata["CROSS_AVE_60"] = ((end - newdata["AVE60"] > FLOAT_MIN) & (cmpdata - newdata["AVE60"] < FLOAT_MIN)).astype(int)
    #       'START_RIZE', 'START_RIZE_BIG', 'IS_BIG_RIZE', 'IS_MEDIUM_RIZE',
    newdata["START_RIZE"] = ((start - cmpdata) > FLOAT_MIN).astype(int)
    newdata["START_RIZE_BIG"] = ((start - cmpdata * 1.02) > FLOAT_MIN).astype(int)
    newdata["END_RIZE_START"] = ((end - start) > FLOAT_MIN).astype(int)
    
    newdata["IS_BIG_RIZE"] = (newdata["RIZERATE"] - 0.04 > FLOAT_MIN).astype(int)
    newdata["IS_MEDIUM_RIZE"] = (newdata["RIZERATE"] - 0.02 > FLOAT_MIN).astype(int)
    
    newdata["RIZE1"] = (end < cmpdata * 0.97).astype(int) 
    newdata["RIZE2"] = ((end < cmpdata * 0.99) * (end >= cmpdata * 0.97)).astype(int)
    newdata["RIZE3"] = ((end < cmpdata * 1.01) * (end >= cmpdata * 0.99)).astype(int)
    newdata["RIZE4"] = ((end < cmpdata * 1.03) * (end >= cmpdata * 1.01)).astype(int)
    newdata["RIZE5"] = (end >= cmpdata * 1.03).astype(int)
    
    (newdata["DEF_SELL_SHORT_index"],newdata["DEF_SELL_SHORT_date"],newdata["DEF_SELL_SHORT_price"]) = pd.Series(getDefaultSell(stockdata, 20, 100, 1))
    (newdata["DEF_SELL_MEDIUM_index"],newdata["DEF_SELL_MEDIUM_date"],newdata["DEF_SELL_MEDIUM_price"]) = getDefaultSell(stockdata, 20, 100, 0.08)
    (newdata["DEF_SELL_LONG_index"],newdata["DEF_SELL_LONG_date"],newdata["DEF_SELL_LONG_price"]) = getDefaultSell(stockdata, 40, 100, 1)
    (newdata["DEF_SELL_END_index"],newdata["DEF_SELL_END_date"],newdata["DEF_SELL_END_price"]) = getDefaultSell(stockdata, 40, 100, 0.08)

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
    c = data_py.iloc[:,1:] - data.iloc[:,1:] #a = data[["DEF_SELL_SHORT_date","DEF_SELL_SHORT_price"]][START_ATTRIBUTE:]
    coldiff = abs(c.iloc[START_ATTRIBUTE:,:].sum())
    diff = sum(coldiff) + (data.shape[0] - data_py.shape[0])
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






