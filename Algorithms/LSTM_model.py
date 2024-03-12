# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:16:32 2023

@author: rickg

"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import math
#from statsmodels.tsa.seasonal import seasonal_decompose
#from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.preprocessing import MinMaxScaler
#import keras


#from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import *
from keras.layers import Dense
#from keras.layers import Dropout
#from keras.models import load_model
from keras.preprocessing.sequence import TimeseriesGenerator
#import sklearn.metrics as metrics



def lstm(train,test,WS):
    sc= MinMaxScaler (feature_range =(0,1))

    train_scaled=sc.fit_transform(train.to_numpy())
    test_scaled=sc.fit_transform(test.to_numpy())


    series_generator = TimeseriesGenerator(train_scaled, train_scaled, length=WS,batch_size=1)

    model= Sequential()
    model.add(LSTM(64,activation='relu',input_shape=(WS,1)))
    model.add(Dense(1,'linear'))
    model.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=0.002), metrics=[RootMeanSquaredError()])

    #model.summary()
    
    model.fit(series_generator,epochs=20,verbose=0)

    prediction_batch = train_scaled[-WS:]
    prediction_batch = prediction_batch.reshape((1, WS, 1))

    model.predict(prediction_batch,verbose=0)

    test_predictions = []

    first_eval_batch = train_scaled[-WS:]
    current_batch=first_eval_batch.reshape((1, WS, 1))

    for i in range(len(test)):
        current_pred = model.predict(current_batch,verbose=0)[0]
        test_predictions.append(current_pred)
        current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

    actual_predictions=sc.inverse_transform(test_predictions)
    #actual_predictions=pd.DataFrame(actual_predictions,index=test.index)
    actual_predictions=pd.DataFrame(actual_predictions)
    actual_predictions=actual_predictions.rename(columns={0:'LSTM'})

    actual_predictions.index=test.index


    return actual_predictions

    
    