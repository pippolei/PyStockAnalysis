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




sys.path.append("C:/git/PyStockAnalysis/mystock/")
from lib.stockdatalib import *


filedir = "C:/StockAnalysis/py/" 

os.chdir(filedir)
sys.path.append(filedir)

stockfull = pd.read_csv("stock_full.csv", sep = ",", index_col=False)
stockfull_py = pd.read_csv("stock_full_py.csv", sep = ",", index_col=False)


diffvalues = []
g_stockitem = stockfull.groupby("code", axis = 0, as_index = False)
g_stockitem_py = stockfull_py.groupby("code", axis = 0, as_index = False)


codediff = "codelist: "

#code = 's600166'
#data_py, data, diff = getDiffValue(code) 
#diffvalues.append(diff)    
code = 's002450'
data, data_py, codediff, diff = getDiffValue(code,g_stockitem,g_stockitem_py) # @UndefinedVariable
c = data_py.iloc[:,1:] - data.iloc[:,1:]
diff = sum(c.iloc[130:,:].sum()) 

codelist = []
for code, group in g_stockitem:
    data, data_py, codediff, diff = getDiffValue(code,g_stockitem,g_stockitem_py) # @UndefinedVariable
    diffvalues.append(diff)
    codelist.append(code)

t = np.abs(diffvalues)
print("Max values:" + str(t.max()))
print("Diff lines:" + codelist[(t.argmax())])
pass











    
    
