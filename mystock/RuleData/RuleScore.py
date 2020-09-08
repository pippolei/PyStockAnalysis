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

stockfull = pd.read_csv("rule_full.csv", sep = ",", index_col=False)
selected_rule = stockfull[stockfull['rulename'] == 'Buy6Rize']
selected_rule.drop(["type","id","rulename"], axis = 1, inplace = True)

selected_rule["sequence"] = selected_rule["grade"].groupby(selected_rule["date"]).rank(ascending=0, method="first")
check_data = selected_rule[["date","grade","sequence","kpis", "num_kpis","dapan"]]

check_data.to_csv(filedir + "rule_score_py.csv", index = False)

selected = selected_rule[selected_rule["sequence"] <= 2]
unselected = selected_rule[selected_rule["sequence"] > 2]