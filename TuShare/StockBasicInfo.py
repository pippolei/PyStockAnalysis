import os
import matplotlib
import numpy as np
import pandas as pd

import tushare as ts

os.chdir("C:/Users/i038196")
pd.set_option('display.max_columns', None)

basics = ts.get_stock_basics()
colnames = ['pe','outstanding','totals','esp','pb']


stocks = pd.read_csv("stock.txt", sep = '\t')
codes = stocks.apply(lambda x: x[0][2:], axis = 1)

basics.loc[codes,colnames].to_csv("basic.csv")

#comment