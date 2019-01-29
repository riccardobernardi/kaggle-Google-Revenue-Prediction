import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def norm(df):
    return (df-df.min())/(df.max()-df.min())

def lin(dev,val,test):
    scaler = MinMaxScaler()
    dev = scaler.fit_transform(dev)
    test = scaler.fit_transform(test)

    lr = LinearRegression().fit(np.array(norm(dev)), np.array(val))
    predictions = lr.predict(np.array(test))
    predictions[predictions<0] = 0
    
    return predictions
