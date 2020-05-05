import os
import matplotlib
import numpy as np
import pandas as pd

import tushare as ts
pro = ts.pro_api("28cacf3fd08f2da30fadedec0e2e550c2a7ed2d907d3b79547d0e293");
os.chdir("C:/Users/i038196")
np.set_printoptions(threshold=np.inf)
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)

stocks = pd.read_csv("stock.txt", sep = '\t')
codes = stocks.apply(lambda x: x[0][2:], axis=1)

def print_index():
    sh = ts.get_realtime_quotes('sh').iloc[0]
    sh['amount'] = int(int(sh['amount']) / 100000000)
    pre_close = float(sh['pre_close'])
    print(sh['price'], int(10000 * (float(sh['price']) / pre_close - 1)) / 100, sh['amount'])

def get_real_time():
    df = ts.get_realtime_quotes(codes)
    pre_close = pd.to_numeric(df['pre_close'])
    price = pd.to_numeric(df['price'])
    df['rize'] = (price / pre_close - 1) * 100
    print(df[['code', 'price', 'rize','high','low', 'bid', 'ask']])
    
get_real_time()