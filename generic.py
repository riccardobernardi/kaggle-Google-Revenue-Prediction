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

def common_feats(train, test):
    return list(set(test.columns).intersection(set(train.columns)))


def drop_uncommons(train, test, exceptions):
    commons = common_feats(train, test)

    for col in train.columns:
        if (col not in commons) & (col not in exceptions):
            train = train.drop(col, axis=1)

    for col in test.columns:
        if (col not in commons) & (col not in exceptions):
            test = test.drop(col, axis=1)

    return train, test


class toolbar:

    def __init__(self, length=10):
        self.length = length
        self.steps = 1

    def set_len(self, new):
        self.length = new

    def prin(self):
        if (self.steps <= self.length):
            str1 = "["
            for i in range(self.steps):
                str1 += '*'
            for i in range(self.length - self.steps):
                str1 += ' '
            str1 += "]"
            sys.stdout.write('\r' * self.length + str(str1))

            self.steps += 1

    def update(self):
        if (self.steps < self.length):
            self.steps += 1


#tipi numerici
tipi_num = [np.int64,float,int]

def find_num_cols(df,exceptions,cats,nums):
    vet = []
    for col in df.columns:
        try:
            if (type(eval(df[col][0])) in tipi_num) & (col not in cats) & (col not in nums) & (
                    df[col].nunique() > 10) & (col not in exceptions):
                #print("aggiugngo ai num_cols", col)
                vet += [col]
        except:
            try:
                if (type(df[col][0]) in tipi_num) & (col not in cats) & (col not in nums) & (
                        df[col].nunique() > 10) & (col not in exceptions):
                    #print("aggiugngo ai num_cols", col)
                    vet += [col]
            except:
                pass

    vet += nums
    return vet


def find_cat_cols(df,exceptions,nums):
    return list( (set(df.columns).difference(set(nums))).difference(set(exceptions))   )

class game:

    def __init__(self):
        self.ph = pd.DataFrame([["Florida", 2], ["Florida", 8], ["Arizona", 4]], columns=["a", "b"])

    def view(self):
        self.ph.head()

    def applica(self, fun):
        return fun(self.ph)

    def restore(self):
        self.ph = pd.DataFrame([["Florida", 2], ["Florida", 8], ["Arizona", 4]], columns=["a", "b"])
        return self.ph

    def mean(self):
        return self.ph.groupby("a").mean()

    def get(self):
        return self.ph
        
def stringify_cats(df,cats):
    df[cats] = df[cats].astype(str)
    return df

def drop_exceeding(train,test,max_new_feat,cats,target):
    da_droppare=[]

    for col in cats:
        if (train[col].nunique()>max_new_feat) & (col not in target):
            da_droppare+=[col]
            train=train.drop(col,axis=1)

    for col in da_droppare:
        test=test.drop(col,axis=1)

    new=[]
    for col in cats:
        if col not in da_droppare:
            new += [col]

    cats = new
    
    return train,test,cats

# check_coherence between train_df cat_cols num_cols test_df
def cc(train_df,test_df,cats,nums):
    if len(list(set(cats).intersection(set(nums)))) > 0:
        raise Exception("intersection not empty between cats & nums")

    for col in cats:
        if col not in train_df.columns:
            raise Exception("incohererence between cat_cols and train_df.columns with col {}".format(col))

    for col in nums:
        if col not in train_df.columns:
            raise Exception("incohererence between num_cols and train_df.columns with col {}".format(col))

    for col in cats:
        if col not in test_df.columns:
            raise Exception("incohererence between cat_cols and test_df.columns with col {}".format(col))

    for col in nums:
        if (col not in test_df.columns) & (col != "totals.totalTransactionRevenue"):
            raise Exception("incohererence between num_cols and test_df.columns with col {}".format(col))
            
    if "totals.totalTransactionRevenue" not in nums:
        raise Exception("incohererence: nums is corrupted")

    if "totals.totalTransactionRevenue" not in train_df.columns:
        raise Exception("incohererence: transactionRevenue not in train_df.columns")

    if ("fullVisitorId" not in train_df.columns) | ("fullVisitorId" not in test_df.columns):
        raise Exception("incohererence: fullVisitorId not in train_df.columns or test_df.columns")
        
    if len(list(set(cats).intersection(set(nums)))):
        raise Exception("intersection not-empty")
        
    for col in train_df.columns:
        if type(col)!=type(""):
            raise Exception("uncorrect type in cols names of train")
            
    for col in test_df.columns:
        if type(col)!=type(""):
            raise Exception("uncorrect type in cols names of test")
            
    if "totals.totalTransactionRevenue" in test_df.columns:
        raise Exception("target dont have to stay in test dataset")
        
        
        
def norm(l):
    return (l-min(l))/(max(l) - min(l))
