
import os
os.chdir('/mnt/c/Users/rickg/Desktop/Solar Radiation Project/')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import pandas as pd
import numpy as np
import datetime
import sklearn.metrics as metrics
import warnings
warnings.filterwarnings("ignore")

from Algorithms import SARIMA
from Algorithms import HoltWinters
from Algorithms import LSTM_model
   

def calculate_metrics(actual_values,predicted_values):
    MAE=metrics.mean_absolute_error(actual_values,predicted_values)
    MSE=metrics.mean_squared_error(actual_values,predicted_values)
    RMSE=np.sqrt(MSE)

    MAE=round(MAE,6)
    MSE=round(MSE,6)
    RMSE=round(RMSE,6)
    return MAE,MSE,RMSE



def window_specific_year(year, training_size,station_data):    
    training_size_months=training_size*12

    #station_data=station_data[['ALLSKY_SFC_SW_DWN','CLOUD_AMT','PS','RH2M','T2M','WS10M']]
    
    start_position=len(station_data)-training_size_months-12
        
    window_data=station_data[start_position:len(station_data)]
    train_set=window_data[0:training_size_months]
    test_set=window_data[training_size_months:len(window_data)]
    
    #return window_data.to_frame(), train_set.to_frame(), test_set.to_frame()
    return window_data, train_set, test_set

def predictions_INMET_stations():  

    data_path=r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Data'

    list_of_files= os.listdir(data_path)

    list_of_files.remove('00-CatalogoEstaçõesAutomáticas.csv')
    list_of_files.remove('Yearly Average')

    list_of_files=['A521 (BELO HORIZONTE (PAMPULHA)_MG).csv']
    #list_of_files=list_of_files[0:3]
    #list_of_files=['(5.68,-60.33).csv','(-7.23,-33.32).csv','(-7.26,-74.32).csv']

    params=['ALLSKY_SFC_SW_DWN','CLOUD_AMT','PS','RH2M','T2M','WS10M']

    remaining_stations=len(list_of_files)
        
    counter=0
    
    for file_name in list_of_files:
        
        log_file=open(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Log files/Predictions log.txt','r')
        
        log_data=log_file.read()
        log_data=log_data.split('\n')
        
        log_file.close()
        
        remaining_stations=len(list_of_files)
        
        
        if(file_name in log_data):
            
            print("Station "+file_name.removesuffix(".csv")+" was alredy processed!")
            remaining_stations-=1

        else:
            
            year=2022
            window_size=5
        
            counter+=1
            print("Station "+file_name.removesuffix(".csv")+" is beeing processed! ("+str(counter)+" of "+ str(remaining_stations)+' stations)')
            remaining_stations-=1

            station_data=pd.read_csv(data_path+'/'+file_name, sep=',', encoding='latin1',skiprows=12).set_index('Date')
            window_data, train_set, test_set=window_specific_year(year, window_size, station_data)
            
            for parameter in params: 
                
                #print(parameter)
                
                window=window_data[parameter].to_frame()
                train=train_set[parameter].to_frame()
                test=test_set[parameter].to_frame()
                
                sarima_predictions=SARIMA.sarima(window,train,test,1)
                sarima_predictions.index=test.index
                
                HoltWinters_predictions=HoltWinters.holt_winters(train)
                HoltWinters_predictions.index=test.index
                
                LSTM_predictions=LSTM_model.lstm(train,test,12)
                station_results=pd.concat([test, sarima_predictions, HoltWinters_predictions, LSTM_predictions], axis=1)
                station_results.to_csv(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Predictions/'+parameter+'/'+file_name)
                del(station_results)
            
        with open(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Log files/Predictions log.txt', 'a') as f:
                f.write(file_name+'\n')

            #parameter_info="Training size: "+str(window_size) +" years of data (predicting for "+str(year)+")"
        
def predictions_01_degree_grid():

    data_path=r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/01 degree grid/'

    #list_of_files= os.listdir(data_path)

    useful_grid=pd.read_csv(r"/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Grid (01 degree) - Useful.csv")
    useful_grid=useful_grid.set_index('id')
    useful_grid=useful_grid.iloc[:,0:2].rename(columns={'X':'Longitude','Y':'Latitude'})

    useful_grid['Name']='('+useful_grid['Latitude'].astype(str)+';'+useful_grid['Longitude'].astype(str)+').csv'

    list_of_files=useful_grid['Name'].tolist()


    #list_of_files.remove('Yearly Average')
    
    params=['ALLSKY_SFC_SW_DWN']

    remaining_stations=len(list_of_files)
        
    counter=0
    year=2022
    window_size=5

    for file_name in list_of_files:

        counter+=1
        
        print("Processing point "+str(counter)+" - " +file_name.removesuffix(".csv")+"  "+str(counter)+" of "+ str(remaining_stations)+' stations.')

        station_data=pd.read_csv(data_path+file_name, sep=',', encoding='latin1').set_index('Date')
        window_data, train_set, test_set=window_specific_year(year, window_size, station_data)
        
        for parameter in params: 
            
            #print(parameter)
            
            window=window_data[parameter].to_frame()
            train=train_set[parameter].to_frame()
            test=test_set[parameter].to_frame()
            
            sarima_predictions=SARIMA.sarima(window,train,test,1)
            sarima_predictions.index=test.index
            
            HoltWinters_predictions=HoltWinters.holt_winters(train)
            HoltWinters_predictions.index=test.index
            
            LSTM_predictions=LSTM_model.lstm(train,test,12)
            station_results=pd.concat([test, sarima_predictions, HoltWinters_predictions, LSTM_predictions], axis=1)
            
            station_results.to_csv(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/01 degree predictions/'+parameter+'/'+file_name)
            
            del(station_results)
        

#print("main!!!!!!!!!!")

predictions_01_degree_grid()






''' Metrics Experimentation
prediction_folders=os.listdir(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Predictions')

models=['SARIMA','HoltWinters','LSTM']



stations_average=pd.DataFrame()

for folder_name in prediction_folders:
    
    list_of_files=os.listdir(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Predictions/'+folder_name)
    
    list_of_files.remove('F501 (BELO HORIZONTE - CERCADINHO_MG).csv')
    
    
    
    metrics_all_stations=pd.DataFrame(columns=['Model','MAE','MSE','RMSE'])
    row=pd.DataFrame({'Model':'SARIMA','MAE':[0],'MSE':[0],'RMSE':[0]})
    metrics_all_stations=pd.concat([metrics_all_stations,row],axis=1)
    
    for file_name in list_of_files:
        
        station_data=pd.read_csv(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Predictions/'+folder_name+'/'+file_name)
        station_data=station_data.drop('Date',axis=1)
        
        if file_name=='A521 (BELO HORIZONTE (PAMPULHA)_MG).csv':
            belo_horizonte=station_data
        
        
        metrics_current_station=pd.DataFrame(columns=['Model','MAE','MSE','RMSE'])
        
        for model in models:
            
            MAE,MSE,RMSE=calculate_metrics(station_data[folder_name],station_data[model])
            row=pd.DataFrame({'Model':[model],'MAE':[MAE],'MSE':[MSE],'RMSE':[RMSE]})
            metrics_current_station=pd.concat([metrics_current_station,row],axis=0)
            
            
        metrics_current_station=metrics_current_station.drop('Model',axis=1)
        
        metrics_current_station=metrics_current_station.drop('Model',axis=1)
        
        metrics_all_stations=pd.DataFrame()
        metrics_all_stations=metrics_all_stations.add(metrics_current_station,axis=1)
    
    metrics_all_stations=metrics_all_stations.set_index('Model')
    metrics_all_stations=metrics_all_stations.div(len(list_of_files))
    
    metrics_BH=pd.DataFrame(columns=['Model','MAE','MSE','RMSE'])
    
    for model in models:
        MAE,MSE,RMSE=calculate_metrics(belo_horizonte[folder_name],belo_horizonte[model])
        row=pd.DataFrame({'Model':[model],'MAE':[MAE],'MSE':[MSE],'RMSE':[RMSE]})
        metrics_BH=pd.concat([metrics_BH,row],axis=0,ignore_index=True)
    
    metrics_all_stations.to_csv(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Metrics/'+folder_name+'/All_stations.csv')
    metrics_BH.to_csv(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Metrics/'+folder_name+'/Belo_Horizonte.csv')
'''
        
