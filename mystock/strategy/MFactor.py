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
import xgboost

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None 


sys.path.append("C:/git/PyStockAnalysis/mystock/")
from lib.stockdatalib import *

importfile_path = "C:/StockAnalysis/hs300"
filedir = "C:/StockAnalysis/py/" 

#待比较的文件列明
stockfull = pd.read_csv(filedir + "stock_full_py.csv", sep = ",", index_col=False)
newdata = stockfull[["END_ABOVE_AVE_10","END_ABOVE_AVE_20","END_ABOVE_AVE_60","A10_ABOVE_20","A10_ABOVE_60",
                     "A20_ABOVE_60","A10V_ABOVE_60V","END_FAR_ABOVE_05","END_FAR_BELOW_05","END_ABOVE_HIGH_60",
                     "END_BELOW_LOW_60","START_RIZE","START_RIZE_BIG","END_RIZE_START","IS_BIG_RIZE","IS_MEDIUM_RIZE",
                     "RIZE1","RIZE2","RIZE3","RIZE4","RIZE5",
                     "end", "DEF_SELL_MEDIUM_price", "DEF_SELL_LONG_price", "DEF_SELL_END_price"
                     ]]

testdata = newdata[["END_ABOVE_AVE_10","DEF_SELL_LONG_price"]]