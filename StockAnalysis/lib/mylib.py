#coding=gbk
import os
import matplotlib
import numpy as np
import pandas as pd
import talib
import datetime
from sklearn.preprocessing import OneHotEncoder 
from sklearn.preprocessing import LabelEncoder

def GetShiftColumn(datacolumn, day):
    name = datacolumn.name + "_shift" + str(day)
    newcolumn = datacolumn.shift(day)
    newcolumn.name = name
    return newcolumn
    
    

def Oneencode(DataVector):
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(DataVector)
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    onehot_encoded = pd.DataFrame(onehot_encoded, columns = ["Encode %d" %(i+1) for i in range(onehot_encoded.shape[1])])
    return (label_encoder, onehot_encoded)


def Reverse_encode(label_encoder, onehot_encoded):
    maxcols = pd.DataFrame(onehot_encoded).apply(lambda x: np.argmax(x), axis = 1)
    return label_encoder.inverse_transform(maxcols)
     

def col_split_explode(datacolumn, splitter):
    ret = datacolumn.apply(lambda x: split_to_column(x, splitter))
    ret.columns = [datacolumn.name + "_"+str(i+1) for i in range(ret.columns.shape[0])]
    return ret

def split_to_column(datavalue, splitter):
    wordlist = datavalue.split(splitter)
    return pd.Series(i for i in wordlist)

#将所有列和bench做比较， 大于则为1， 小于则为0
def binary_splite(dataframe, bench):
    colnames = dataframe.columns
    ret = pd.DataFrame()
    for onename in colnames:
        ret[onename] = dataframe[onename] > bench
    return ret   
    
def change_type(dataframe, to_type):
    colnames = dataframe.columns
    for onename in colnames:
        dataframe[onename] = dataframe[onename].astype(to_type)
    return dataframe