#coding=gbk
import os,sys
sys.path.append("C:/Users/Administrator/git/PyStockAnalysis")
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib
import datetime, time
import seaborn as sns
from mystock.lib.mylib import *
from mystock.lib.modellib import * 
import math
from dateutil.relativedelta import relativedelta
from sklearn.model_selection import GridSearchCV


sns.set(color_codes = True)

os.chdir(rootDir)
sys.path.append(rootDir)
pd.set_option('display.max_columns', None)

rulefull = pd.read_csv("rule_full.csv")
#rulefull.drop(["id",'type'], axis = 1, inplace = True)

rulefull["rize"] = (rulefull["next4"] / rulefull["price"]) - 1
analysis = rulefull[["rulename","rize"]]
fig, ax = plt.subplots(figsize=(8,6))

bp = analysis.groupby('rulename').plot(kind='kde', ax=ax)

print("done")
 