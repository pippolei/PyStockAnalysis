#coding=gbk
import os
import matplotlib
import numpy as np
import pandas as pd
import talib
import datetime, time
from lib import mylib
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import math
from dateutil.relativedelta import relativedelta
from sklearn.model_selection import GridSearchCV

def GetRuleData():
    ruleitem_raw = pd.read_csv("rule_full.csv", sep = ",", index_col=False)
    ruleitem = ruleitem_raw[ruleitem_raw["type"]==1]
    ori_column = ruleitem.columns
    savevalue = ruleitem.iloc[:1,:]
    rize = ruleitem["next2"] / ruleitem["price"] - 1
    ruleitem["rize"] = rize.apply(lambda x: 1.0 if x > 0.0 else 0.0)

    label_encode, rulename_encode = mylib.Oneencode(ruleitem["rulename"])
    rule_kpis = mylib.col_split_explode(ruleitem["kpis"],'#')
    rule_kpis = mylib.change_type(rule_kpis, 'float')
    rule_dapan = mylib.col_split_explode(ruleitem["dapan"],'#')
    rule_dapan = mylib.change_type(rule_dapan, 'float')
    rule_num_kpis = mylib.col_split_explode(ruleitem["num_kpis"],'#')
    rule_num_kpis = mylib.change_type(rule_num_kpis, 'float')
    #rule_num_kpis2 = mylib.binary_splite(rule_num_kpis, 0)
    frame = [ruleitem, rulename_encode, rule_dapan, rule_kpis,rule_num_kpis]
    ruleitem = pd.concat(frame, axis = 1)
    colname = ruleitem.columns[22:]
    return ruleitem, ori_column, colname


def GetModel(ruleitem, date_train, date_test, date_vali, date_to, colname):
    #按照时间分train, test, validate数据
    intdate_train = (date_train.year) * 10000 + date_train.month * 100 + 1
    intdate_test = (date_test.year) * 10000 + date_test.month * 100 + 1
    intdate_vali = (date_vali.year) * 10000 + date_vali.month * 100 + 1  
    intdate_to = (date_to.year) * 10000 + date_to.month * 100 + 1 
    print("From:" + str(intdate_train) + " / To:" + str(intdate_vali)) 
    traindata = ruleitem[(ruleitem["date"] >= intdate_train) & (ruleitem["date"] < intdate_test)]
    testdata = ruleitem[(ruleitem["date"] >= intdate_test) & (ruleitem["date"] < intdate_vali)]
    validata = ruleitem[(ruleitem["date"] >= intdate_vali) & (ruleitem["date"] < intdate_to)]
    validata_y = validata["rize"] 
    validata = validata.drop("rize", axis = 1)     
    train_x = traindata.drop("rize", axis = 1)
    train_y = traindata["rize"]           
    test_x1 = testdata.drop("rize", axis = 1)
    if(test_x1.shape[0] == 0):
         return None, None
    test_y = testdata["rize"]    
    train_x = train_x[colname]
    test_x = test_x1[colname]
    eval_set = [(test_x, test_y)]

    other_params = {'learning_rate': 0.1, 'n_estimators': 100, 'max_depth': 3, 'min_child_weight': 5, 'seed': 0,
                'subsample': 0.8, 'colsample_bytree': 1, 'objective': 'binary:logistic', 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}
    model = XGBClassifier(**other_params)
    model.fit(train_x, train_y, early_stopping_rounds=10, eval_metric="error", eval_set=eval_set, verbose=True)
    y_pred = model.predict(test_x)
    accuracy = accuracy_score(test_y, y_pred)
    print("Test Accuracy" + str(accuracy))
    y_pred = model.predict(validata[colname])
    accuracy = accuracy_score(validata_y, y_pred)
    print("Vali Accuracy" + str(accuracy) + "/n")
    print("*******************************************************************")
    return model, validata, validata_y    
