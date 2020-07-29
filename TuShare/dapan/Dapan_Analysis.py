# coding=gbk
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
import numpy as np
import pandas as pd
import datetime
import sys
#sys.path.append(r"C:\Users\kenny\workspace\TuShare\lib")
from lib import StockAttr as sa
from lib import predict as pre


os.chdir("C:/mystock/TuShare")
pd.set_option('display.max_columns', None)
df = pd.read_csv("sh000001.csv", index_col = False)
df.sort_values(['date'], ascending = True, inplace = True)  #按照日期排序

#求5日平均值
avg5 = sa.average(df, 5, 'close')
#求10日平均值
avg10 = sa.average(df, 10, 'close')
avg20 = sa.average(df, 20, 'close')
avg60 = sa.average(df, 60, 'close')


EMA12 = sa.EMA(df['close'], 12)
EMA26 = sa.EMA(df['close'], 26)
DIF = EMA12 - EMA26
DIF.name = "DIF"
DEA = sa.EMA(DIF, 9)
DEA.name = "DEA"
MACD = (DIF - DEA) * 2
MACD.name = "MACD"
frame = [df, avg5, avg10, avg20, avg60, EMA12,EMA26, DIF, DEA, MACD]
df = pd.concat(frame, axis=1)
df.to_csv("sh000001_ana.csv")


result = pd.Series(np.zeros(df.shape[0]))
for i in range(0, df.shape[0] - 2):
    result[i] = 1 if df.ix[i + 1, 'close'] > df.ix[i, 'close'] else 0 
        
result.name = "result" 
    
close = sa.IsRize(df, 'close')
print(pre.accuracy_binary(result, close))
rize_avg5 = sa.IsRize(df, 'avg5')
print(pre.accuracy_binary(result, rize_avg5))
rize_avg10 = sa.IsRize(df, 'avg10')
print(pre.accuracy_binary(result, rize_avg10))
rize_avg20 = sa.IsRize(df, 'avg20')
print(pre.accuracy_binary(result, rize_avg20))
rize_avg60 = sa.IsRize(df, 'avg60')
print(pre.accuracy_binary(result, rize_avg60))
rize_macd = sa.IsRize(df, 'MACD')
print(pre.accuracy_binary(result, rize_macd))
frame = [df, result, close, rize_avg5, rize_avg10, rize_macd]
df = pd.concat(frame, axis=1)
df.to_csv("sh000002_ana.csv")

