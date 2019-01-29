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
import pandas
from pandas.plotting import scatter_matrix
from pandas.io.json import json_normalize

#seaborn
import seaborn as sns

import generic as gn

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

#plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
from plotly import tools

#pickle
import pickle

import ast
import string

plotly.tools.set_credentials_file(username='bernifix', api_key='14saznMjRbcxdhF8SwQ8')

def flatten(twoDim):
    support = []
    for new_feats in twoDim:
        for feat in new_feats:
            support += [feat]
    return support

def into_dataframe(col_names, matr):
    new_data = pd.DataFrame()
    for i, name in enumerate(col_names):
        new_data[name] = pd.Series(matr[:, i])

    return new_data

def drop_cols(df, not_drop):
    return df[not_drop]

def encode_cats(train, test, cats):
    t = gn.toolbar(11)

    t.prin()
    # creo encoder
    oh_enc = OneHotEncoder(sparse=False)

    t.prin()
    # encodo e prendo i nomi vecchi
    new_cols_train = oh_enc.fit_transform(array(train[cats]))
    feat_train = oh_enc.categories_

    t.prin()
    # anche per il test
    new_cols_test = oh_enc.fit_transform(array(test[cats]))
    feat_test = oh_enc.categories_

    t.prin()
    # i nomi vecchi sono una matr n*n, la rendo n*1
    feat_train = flatten(feat_train)

    # anche per il test
    feat_test = flatten(feat_test)

    t.prin()
    # trasformo le nuove colonne in un dataframe
    new_train = into_dataframe(feat_train, new_cols_train)

    t.prin()
    # anche per il test
    new_test = into_dataframe(feat_test, new_cols_test)

    t.prin()
    # cerco le colonne uguali nei dataframes
    commons = gn.common_feats(new_train, new_test)

    t.prin()
    new_train = drop_cols(new_train, commons)
    new_test = drop_cols(new_test, commons)

    t.prin()
    for col in cats:
        train = train.drop(col, axis=1)
        test = test.drop(col, axis=1)

    t.prin()
    cats = commons

    t.prin()
    train = train.merge(new_train, right_index=True, left_index=True)
    test = test.merge(new_test, right_index=True, left_index=True)

    t.prin()
    return train, test, cats

# In[70]:


def reset_index(df, groupper):
    df[groupper] = df.index
    df = df.set_index(array([x for x in range(df.shape[0])]))

    return df


def group_me(df,groupper,cats,nums,mode):
    t = gn.toolbar(6)

    t.prin()
    # raggruppo per il valore groupper

    # raccolgo con la media per i numeri
    t.prin()
    df_num = pd.DataFrame()
    
    train=0
    
    try:
        if "totals.totalTransactionRevenue" in df.columns:
            train=1
    except:
        pass
    
    if train==1:
        #siamo nel train
        #print(set(nums).difference(set(nums).intersection(set(df.columns))))
        df_num[nums] = df.groupby(groupper)[nums].mean()
    else:
        #siamo nel test
        nn = list(set(nums).difference(set(["totals.totalTransactionRevenue"])))
        df_num[nn] = df.groupby(groupper)[nn].mean()
        

    # raggruppo per la mediana per le categorie
    t.prin()
    df_cat = pd.DataFrame()
    groupped = df.groupby(groupper)
    
    if mode == "mode":
        for col in cats:
            df_cat[col] = groupped[col].agg(lambda x: stats.mode(x)[0][0])
    if mode == "mean":
        df_cat[cats] = df.groupby(groupper)[cats].mean()
    if mode == "median":
        df_cat[cats] = df.groupby(groupper)[cats].median()
    if mode == "mode_approx":
        my_group = df.groupby(groupper)[cats]
        df_cat[cats] = -(2*my_group.mean() - 3*my_group.median())
        

    t.prin()
    # unisco i due nuovi dataframes
    df = df_num.merge(df_cat, right_index=True, left_index=True)

    t.prin()
    # df[groupper]=df.index
    # df = df.set_index(array([x for x in range(df.shape[0])]))
    df = reset_index(df, groupper)

    t.prin()
    return df