# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:11:51 2023

@author: rickg
"""
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import math
#from statsmodels.tsa.seasonal import seasonal_decompose
#from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
#from pmdarima import auto_arima
#from statsmodels.tsa.arima.model import ARIMA
#from sklearn.metrics import mean_squared_error

#import sklearn.metrics as metrics

from statsmodels.tsa.holtwinters import ExponentialSmoothing


def holt_winters(df):
    model=ExponentialSmoothing(endog=df,trend=None,seasonal='add',seasonal_periods=12).fit()
    predicted_results = model.forecast(steps=12)

    predicted_results=predicted_results.to_frame()
    #predicted_results=predicted_results.reset_index()
    #predicted_results=predicted_results.drop('index',axis='columns')
    predicted_results=predicted_results.rename(columns={0:'HoltWinters'})
    
    return predicted_results


