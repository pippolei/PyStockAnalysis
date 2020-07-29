import os
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib
import sys
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None 


os.chdir("C:/mystock/py")
stockitem = pd.read_csv("stock_item.csv", sep = ",", index_col=False)
stockfull = pd.read_csv("stock_full.csv", sep = ",", index_col=False)

sys.path.append("C:/git/PyAnalysis")
import lib.stockdatalib as datalib

formatedData = stockitem['date'].apply(datalib.formatDate)
stockitem.loc[:,'date'] = formatedData
stockfull.loc[:,'date'] = formatedData
stockitem.index = formatedData
stockfull.index = formatedData

g_stockitem = stockitem.groupby("code", axis = 0, as_index = False)
g_stockfull = stockfull.groupby("code", axis = 0, as_index = False)

diffvalues = []



code = 's600166'
a, b, codediff, diff = datalib.getDiffValue(code,g_stockitem,g_stockfull) 
#diffvalues.append(diff)    
for code, group in g_stockitem:
    a, b, codediff, diff = datalib.getDiffValue(code,g_stockitem,g_stockfull) 
    diffvalues.append(diff)

print("Max values:" + str(max(diffvalues)))
pass











    
    
