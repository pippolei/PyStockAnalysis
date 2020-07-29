#coding=gbk
import os
import matplotlib
import numpy as np
import pandas as pd
import talib
import datetime, time
from mystock.lib.mylib import *
from mystock.lib.modelib import * 
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import math
from dateutil.relativedelta import relativedelta
from sklearn.model_selection import GridSearchCV

os.chdir(rootDir)
pd.set_option('display.max_columns', None)

rulefull = pd.read_csv("rule_full.csv")


print("done")
 