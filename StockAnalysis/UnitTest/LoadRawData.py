# coding=gbk
import os
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib
import sys
import datetime
import gc

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None 


sys.path.append("C:/git/PyAnalysis")
import lib.stockdatalib as datalib

importfile_path = "C:/StockAnalysis/sample"
filedir = "C:/StockAnalysis/py/"
for root, dirs, files in os.walk(filedir):
    for file in files:
        if 'stock_full_py_' in os.path.splitext(file)[0]:
            os.remove(filedir+file)

os.chdir(importfile_path)
for root, dirs, files in os.walk(importfile_path):
    pass




df = pd.DataFrame()
length = len(files)
curfile = 0;
for filename in files:
    curfile+=1
    starttime = datetime.datetime.now()
    stockitem = pd.read_csv(filename, sep = "\t", skiprows= 2, header=None, encoding='iso-8859-1', index_col=False)
    stockitem.drop(stockitem.tail(1).index, inplace = True)
    stockitem.drop((stockitem.shape[1]-1), axis = 1,inplace = True) #去除最后一列
    stockitem.columns = ["date","start","high", "low","end","volume" ]
    stockitem.reset_index(inplace=True) # index改为column
    stockitem["code"] = "s" + filename[3:9]
    stockitem["date"] = stockitem["date"].apply(lambda x: x[0:4]+x[5:7]+x[8:10]).astype(int)
    stockitem = stockitem[(stockitem["high"]>=0.3) & (stockitem["volume"]>=100)]
    if (datalib.validStock(stockitem)):        
        frame = [df, datalib.getStockFull(stockitem)]
        df = pd.concat(frame, axis = 0) 
    endtime = datetime.datetime.now()
    print (endtime.strftime("%Y-%m-%d %H:%M:%S") + ":  " + "s" + filename[3:9] + "  " + str(curfile) + "/" + str(length) + "-- Time passed" + str((endtime - starttime).total_seconds()))
    if curfile % 100 == 0:
        print ("Data Collection")
        gc.collect()
        df.to_csv("C:/StockAnalysis/py/stock_full_py_" + str(curfile) + ".csv", index = False)
        df = pd.DataFrame()



df.to_csv("C:/StockAnalysis/py/stock_full_py_last.csv", index = False)
print("export done, start to merge")

df = pd.DataFrame()

os.chdir(filedir)
for root, dirs, files in os.walk(filedir):
    for file in files:
        if 'stock_full_py_' in os.path.splitext(file)[0]:
            stockitem = pd.read_csv(file)
            frame = [df, stockitem]  
            df = pd.concat(frame, axis = 0, sort = False)

cols = list(df)
cols.insert(0, cols.pop(cols.index("code")))    
df = df.loc[:,cols]       
df.to_csv("C:/StockAnalysis/py/stock_full_py.csv", index = False)     
print("completed!!!")
print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))





    
    
    

