# coding=gbk
import os
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib
import sys
import math
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None 


os.chdir("C:/StockAnalysis/py")
stockfull = pd.read_csv("stock_full.csv", sep = ",", index_col=False)
stockfull_py = pd.read_csv("stock_full_py.csv", sep = ",", index_col=False)

sys.path.append("C:/git/PyAnalysis")
import lib.stockdatalib as datalib

diffvalues = []
g_stockitem = stockfull.groupby("code", axis = 0, as_index = False)
g_stockitem_py = stockfull_py.groupby("code", axis = 0, as_index = False)

codediff = "codelist: "

#code = 's600166'
#data_py, data, diff = getDiffValue(code) 
#diffvalues.append(diff)    
code = 's600895'
data, data_py, codediff, diff = datalib.getDiffValue(code,g_stockitem,g_stockitem_py) 
c = data_py.iloc[:,1:] - data.iloc[:,1:]
diff = sum(c.iloc[130:,:].sum()) 
for code, group in g_stockitem:
    data, data_py, codediff, diff = datalib.getDiffValue(code,g_stockitem,g_stockitem_py) 
    diffvalues.append(diff)

print("Max values:" + str(max(np.abs(diffvalues))))
print("Diff lines:" + codediff)
pass











    
    
