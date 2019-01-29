base_path="/Users/rr/Desktop/UniVe/PRIMO_SEMESTRE/WEB_INTELLIGENCE_anno_2018_2019/datasets/gstore/"
base_path_data="/Users/rr/Desktop/UniVe/PRIMO_SEMESTRE/WEB_INTELLIGENCE_anno_2018_2019/datasets/gstore/data/"
train_file = base_path+"train_v2.csv"
test_file = base_path+"test_v2.csv"
my_submission_file = base_path+"mysub.csv"

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
plotly.tools.set_credentials_file(username='bernifix', api_key='14saznMjRbcxdhF8SwQ8')

#my pythonic modules
from unpack_set import load_df
from generic import drop_uncommons
from generic import find_num_cols
from generic import find_cat_cols
from generic import stringify_cats
from generic import cc
from preprocessing import encode_cats
from preprocessing import group_me
from generic import drop_exceeding