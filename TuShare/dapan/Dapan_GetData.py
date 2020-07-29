# coding=gbk
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
import pandas as pd
import tushare as ts

os.chdir("C:/mystock/TuShare")
pd.set_option('display.max_columns', None)
pro = ts.pro_api("28cacf3fd08f2da30fadedec0e2e550c2a7ed2d907d3b79547d0e293");

startyear = 2017
endyear = 2008

df = ts.get_h_data('000001', index=True, start=str(startyear) + '-01-01', end=str(startyear) + '-12-31')  # 上证指数
curyear = startyear - 1
while (curyear >= endyear):
    df2 = ts.get_h_data('000001', index=True, start=str(curyear) + '-01-01', end=str(curyear) + '-12-31')  # 上证指数
    frame = [df, df2]
    df = pd.concat(frame, axis=0)
    curyear -= 1

print(df)
df = df.reindex(index=df.index[::-1])
df.to_csv("train.csv")

test = ts.get_h_data('000001', index=True, start='2018-01-01')
test = test.reindex(index=test.index[::-1])
test.to_csv("test.csv")
print("done")