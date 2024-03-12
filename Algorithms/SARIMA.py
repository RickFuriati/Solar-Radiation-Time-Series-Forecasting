# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 17:30:43 2023

@author: rickg
"""
#print("teste")

import os
import warnings
warnings.filterwarnings("ignore")
from statsmodels.tools.sm_exceptions import ValueWarning 
warnings.simplefilter('ignore', ValueWarning)

#from pmdarima import auto_arima
#from statsmodels.tsa.arima.model import ARIMA
#from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX

#import sklearn.metrics as metrics
#import matplotlib.patches as patche



def optimizer(df):
    min=auto_arima(df['value'],m=12,trace=True,d=1).seasonal_order
    p=min[0]
    d=min[1]
    q=min[2]
    m=min[3]
    return p,d,q,m
    

def sarima (df,train,test,parameters):

    if parameters==-1:
        p,d,q,m=optimizer(train)
    else:
        p=2
        d=0
        q=0
        m=12

    #train.index = pd.DatetimeIndex(train.index.values,freq=train.index.inferred_freq)
    Sarima_model = SARIMAX(train, seasonal_order=(p,d,q,m),enforce_stationarity=False,enforce_invertibility=False)
    predictor = Sarima_model.fit(disp=0)
    predicted_results= predictor.predict(start = len(train),end = (len(df)-1),typ='levels')
    
    predicted_results=predicted_results.to_frame()
    #predicted_results=predicted_results.reset_index()
    #predicted_results=predicted_results.drop('index',axis='columns')
    predicted_results=predicted_results.rename(columns={'predicted_mean':'SARIMA'})
    return predicted_results


