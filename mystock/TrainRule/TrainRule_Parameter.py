#coding=gbk
import os
import matplotlib
import matplotlib.pyplot as plt
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
from sklearn.model_selection import GridSearchCV
os.chdir("C:/mystock/py")
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
date_train = datetime.date(curyear, curmonth, 1) 
date_to = datetime.date(maxyear, maxmonth, 1) 

intdate_train = (date_train.year) * 10000 + date_train.month * 100 + 1
intdate_to = (date_to.year) * 10000 + date_to.month * 100 + 1 

print("From:" + str(intdate_train) + " / To:" + str(intdate_to)) 
traindata = ruleitem[(ruleitem["date"] >= intdate_train) & (ruleitem["date"] < intdate_to)]
train_x = traindata.drop("rize", axis = 1)
train_y = traindata["rize"]          
train_x = train_x[colname]


cv_params = {
    'n_estimators': (100,150,200),
    'max_depth':range(3,10,2),
    'min_child_weight':range(1,6,2)
}
other_params = {'learning_rate': 0.1, 'n_estimators': 100, 'max_depth': 5, 'min_child_weight': 1, 'seed': 0,
                'subsample': 0.8, 'colsample_bytree': 0.8, 'objective': 'binary:logistic', 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}
model = XGBClassifier(**other_params)
optimized_GBM = GridSearchCV(estimator=model, param_grid=cv_params, scoring='accuracy', cv=5, verbose=1, n_jobs=4)
optimized_GBM.fit(train_x, train_y)
evalute_result = optimized_GBM.cv_results_
print('每轮迭代运行结果:{0}'.format(evalute_result))
print('参数的最佳取值：{0}'.format(optimized_GBM.best_params_))
print('最佳模型得分:{0}'.format(optimized_GBM.best_score_))


print("done")
 