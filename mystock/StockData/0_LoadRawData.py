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


sys.path.append("C:/git/PyStockAnalysis/mystock/")
from lib.stockdatalib import *

database = "train2"
importfile_path = "C:/StockAnalysis/" + str(database)
filedir = "C:/StockAnalysis/py/" 

#待比较的文件列明
stockfull = pd.read_csv(filedir + "stock_full.csv", sep = ",", nrows = 10, index_col=False)

for root, dirs, files in os.walk(filedir):
    for file in files:
        if 'stock_full_py_' in os.path.splitext(file)[0]:
            os.remove(filedir+file)

os.chdir(importfile_path)
#通过循环files会储存所有的文件名
for root, dirs, files in os.walk(importfile_path):
    pass

startdate = 20110101

def validStock(stockitem):  
    if (stockitem.shape[0] < START_ANALYSIS    # @UndefinedVariable
        or stockitem["end"].min() < 0.3        
        ):
        ret_value = 0
    else:
        ret_value = 1
    return ret_value
        

    
    
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
    stockitem["code"] = "s" + filename[3:9]
    stockitem["date"] = stockitem["date"].apply(lambda x: x[0:4]+x[5:7]+x[8:10]).astype(int)
    stockitem = stockitem[(stockitem["high"]>=0.3) | (stockitem["volume"]>=100)]
    stockitem["volume"] = stockitem["volume"] / 1000
    stockitem = stockitem[stockitem["date"] >= startdate]
    stockitem.reset_index(inplace=True) # 去除以前FILTER掉的行，重新建立index
    stockitem.drop("index", axis = 1, inplace=True)
    stockitem.reset_index(inplace=True) # index改为column
        
    if (validStock(stockitem)):        
        frame = [df, getStockFull(stockitem)]      # @UndefinedVariable
        df = pd.concat(frame, axis = 0) 
    endtime = datetime.datetime.now()
    print (endtime.strftime("%Y-%m-%d %H:%M:%S") + ":  " + "s" + filename[3:9] + "  " + str(curfile) + "/" + str(length) + "-- Time passed " + str((endtime - starttime).total_seconds()))
    if curfile % 100 == 0:
        print ("Data Collection")
        gc.collect()
        df.to_csv(filedir + "stock_full_py_" + str(curfile) + ".csv", index = False)
        df = pd.DataFrame()


if (df.shape[0] > 0):
    df.to_csv(filedir + "stock_full_py_last.csv", index = False)
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
df.to_csv(filedir + "stock_full_py.csv", index = False)     
df.to_csv(filedir + "stock_full_db_"+str(database)+".txt", index = False, sep = '\t', header = 0)     
print("completed!!!")
print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))





    
    
    

