#coding=gbk
import os
import matplotlib
import numpy as np
import pandas as pd
import talib
import datetime, time
from lib import mylib
from lib import modellib
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import math
from dateutil.relativedelta import relativedelta



os.chdir("C:/StockAnalysis/py")
pd.set_option('display.max_columns', None)


ruleitem, ori_column, colname = modellib.GetRuleData()
savevalue = ruleitem.iloc[:1,:][ori_column]

intdate_max = ruleitem["date"].max()
maxyear = math.floor(intdate_max / 10000)
maxmonth = math.floor(intdate_max / 100) - 100 * maxyear
date_end = datetime.date(maxyear, maxmonth, 1)

intdate_min = ruleitem["date"].min()
curyear = math.floor(intdate_min / 10000)
curmonth = math.floor(intdate_min / 100) - 100 * curyear
#初始化将trains数据往前移一个月， 这在下面的循环里第一次加回一个月
date_train = datetime.date(curyear, curmonth, 1) + relativedelta(months=-1) 
date_test = date_train + relativedelta(months=+15) 
date_vali = date_train + relativedelta(months=+18) 
date_to = date_train + relativedelta(months=+19) 

while True:    
    date_train = date_train + relativedelta(months=1)
    date_test = date_test + relativedelta(months=1) 
    date_vali = date_vali + relativedelta(months=1) 
    date_to = date_to + relativedelta(months=1) 
    #(date_train,date_test,date_vali,date_to)
    if date_vali > date_end: break
    model, validata, valiresult = modellib.GetModel(ruleitem,date_train,date_test,date_vali,date_to,colname)
    if (model is None):
        continue
    prediction = model.predict_proba(validata[colname])
    y_pred = pd.DataFrame(prediction).iloc[:,1]
    validata.reset_index(inplace=True)
    validata["pregrade"] = y_pred
    validata["grade"] = y_pred
    select = y_pred > 0.50
    export = validata.loc[select.to_numpy(),ori_column]
    
    frame = [savevalue, export]
    savevalue = pd.concat(frame, axis = 0)
    


savevalue['type'] = '2'
savevalue.iloc[1:,:].to_csv("c:/StockAnalysis/log/ml_rule.txt", index = False, sep = '\t', header = False)
print("done")
 