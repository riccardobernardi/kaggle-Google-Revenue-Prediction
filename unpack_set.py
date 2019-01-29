#mathplotlib
import matplotlib.pyplot as plt
from matplotlib import pylab
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#math
import math

#numpy
from numpy import arange,array,ones
import numpy as np

#scipy
from scipy import stats
import scipy

#csv
import csv, json

#pandas
import pandas as pd
from pandas.plotting import scatter_matrix
from pandas.io.json import json_normalize

#seaborn
import seaborn as sns

#options
get_ipython().run_line_magic('matplotlib', 'notebook')
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import warnings
warnings.simplefilter("ignore")

#lgb
import lightgbm as lgb

#sklearn
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn import metrics
from sklearn.preprocessing import OneHotEncoder

#os
import os
import datetime
import sys, time

# trasforma liste di dizionari in un solo dizionario
def unpack(col):
    mod = []
    for row in col:
        try:
            mod += eval(row)
        except:
            mod += row

    return pd.Series(mod)


def correction_nan(x):
    if type(x) == type(0.0):
        return {}
    else:
        return x


def mappa(fun, ite):
    return [fun(x) for x in ite]


# è una sola la colonna che ricevo e la trasformo in un dict
def from_dict_to_frame(df, col):
    # return pd.DataFrame(df[col])

    df[col] = mappa(correction_nan, df[col])

    new = []
    for c in df[col]:
        new += [c]
    new2 = pd.DataFrame.from_records(new)
    # corretto new2 -> print(type(new2))

    return new2


# trasforma n colonne con un dict all interno in un dizionario che le comprende
def unfold(df, cols,target):
    for col in cols:
        if col not in target:
            df = df.merge(from_dict_to_frame(df, col), right_index=True, left_index=True)
            df = df.drop(col, axis=1)

    return df


# trasforma jsons in colonne
def load_jsons_as_cols(df, JSON_COLUMNS):
    for column in JSON_COLUMNS:
        column_as_df = json_normalize(df[column])
        column_as_df.columns = [f"{column}.{subcolumn}" for subcolumn in column_as_df.columns]
        df = df.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)

    return df


def find_dicts(df,target):
    dicts_to_dump = []
    for x in range(len(df.columns)):
        try:
            if (type(df.iloc[0, x]) == type({})) & (df.columns[x] not in target):
                dicts_to_dump += [df.columns[x]]
        except:
            try:
                if (type(eval(df.iloc[0, x])) == type({})) & (df.columns[x] not in target):
                    dicts_to_dump += [df.columns[x]]
            except:
                pass
    return dicts_to_dump


def find_lists(df,target):
    lists_to_dump = []
    for x in range(len(df.columns)):
        try:
            if (type(eval(df.iloc[0, x])) == type([])) & (df.columns[x] not in target):
                lists_to_dump += [df.columns[x]]
        except:
            try:
                if (type(df.iloc[0, x]) == type([])) & (df.columns[x] not in target):
                    lists_to_dump += [df.columns[x]]
            except:
                pass

    return lists_to_dump


def drop_const(df,target):
    for col in df.columns:
        if (df[col].astype(str).nunique(dropna=False) == 1) & (col not in target):
            df = df.drop(col, axis=1)

    return df


def drop_uniques(df,target):
    for col in df.columns:
        if (df[col].astype(str).nunique(dropna=False) == df.shape[0]) & (col not in target):
            df = df.drop(col, axis=1)

    return df

def load_df(csv_path,n_rows,target):
    JSON_COLUMNS = ["device", "geoNetwork", "totals", "trafficSource"]

    df = pd.DataFrame()

    if n_rows == -1:
        df = pd.read_csv(csv_path,
                         converters={column: json.loads for column in JSON_COLUMNS}
                         , dtype={"fullVisitorId": "str"}
                         )
    else:
        df = pd.read_csv(csv_path,
                         converters={column: json.loads for column in JSON_COLUMNS}
                         ,nrows = n_rows, dtype={"fullVisitorId": "str"}
                        )
    
    df = load_jsons_as_cols(df,JSON_COLUMNS)
    
    #while ((len(find_dicts(df,target)) > 0) | (len(find_lists(df,target)) > 0)):

    if len(find_lists(df,target)) > 0:
        for col in find_lists(df,target):
            df[col] = unpack(df[col])
            
    while len(find_dicts(df,target)) > 0:
        df = unfold(df, find_dicts(df,target),target)
        
    '''summa=0
    new_col = []
    #ciclo le colonne che ho scoperto contenere liste
    for col in find_lists(df,target):
        #ciclo le righe che contenti liste
        for row in df[col]:
            #ciclo la lista contenete dizionari
            if len(row)>0:
                #print(row[:3],len(row))
                for d in row:
                    try:
                        summa += float(d['productPrice'])
                    except:
                        pass
                new_col += [summa]
                summa = 0
    df["transactionRevenue"] = pd.Series(new_col)'''
    
    df = drop_const(df,target)

    df = drop_uniques(df,target)
    
    print(f"Loaded {os.path.basename(csv_path)}. Shape: {df.shape}")
    
    return df