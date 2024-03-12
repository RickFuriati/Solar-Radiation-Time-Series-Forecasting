import os
os.chdir('/mnt/c/Users/rickg/Desktop/Solar Radiation Project/')
import pandas as pd
import numpy as np
import datetime
import sklearn.metrics as metrics
import warnings

import seaborn as sns

warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt

def calculate_metrics(actual_values,predicted_values):
    MAE=metrics.mean_absolute_error(actual_values,predicted_values)
    MSE=metrics.mean_squared_error(actual_values,predicted_values)
    RMSE=np.sqrt(MSE)
    R2=metrics.r2_score(actual_values,predicted_values)

    MAE=round(MAE,6)
    MSE=round(MSE,6)
    RMSE=round(RMSE,6)
    R2=round(R2,6)

    return MAE,MSE,RMSE,R2


def group_stations_latitude():
    station_catalog=pd.read_csv(r"/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Data/00-CatalogoEstaçõesAutomáticas.csv",delimiter=";").iloc[:,0:5]
    
    grouped_stations=pd.DataFrame(columns=['ID','Latitude','Group'])
    count_per_group=[0,0,0,0,0,0,0,0]

    for index, row_catalog in station_catalog.iterrows():

        
        latitude=float(row_catalog['VL_LATITUDE'].replace(",","."))
        station=row_catalog['CD_ESTACAO']
        
        
        if latitude <= 5 and latitude > 0:
            row=pd.DataFrame({'ID':[station],'Latitude':[latitude],'Group':['(5,0)']})
            grouped_stations=pd.concat([grouped_stations,row],axis=0)
            count_per_group[0]+=1
            
        elif latitude <= 0 and latitude > -5:
            row=pd.DataFrame({'ID':[station],'Latitude':[latitude],'Group':['(0,-5)']})
            grouped_stations=pd.concat([grouped_stations,row],axis=0)
            count_per_group[1]+=1

        elif latitude <= -5 and latitude > -10:
            row=pd.DataFrame({'ID':[station],'Latitude':[latitude],'Group':['(-5,-10)']})
            grouped_stations=pd.concat([grouped_stations,row],axis=0)
            count_per_group[2]+=1

        elif latitude <= -10 and latitude > -15:
            row=pd.DataFrame({'ID':[station],'Latitude':[latitude],'Group':['(-10,-15)']})
            grouped_stations=pd.concat([grouped_stations,row],axis=0)
            count_per_group[3]+=1

        elif latitude <= -15 and latitude > -20:
            row=pd.DataFrame({'ID':[station],'Latitude':[latitude],'Group':['(-15,-20)']})
            grouped_stations=pd.concat([grouped_stations,row],axis=0)
            count_per_group[4]+=1

        elif latitude <= -20 and latitude > -25:
            row=pd.DataFrame({'ID':[station],'Latitude':[latitude],'Group':['(-20,-25)']})
            grouped_stations=pd.concat([grouped_stations,row],axis=0)
            count_per_group[5]+=1

        elif latitude <= -25 and latitude > -30:
            row=pd.DataFrame({'ID':[station],'Latitude':[latitude],'Group':['(-25,-30)']})
            grouped_stations=pd.concat([grouped_stations,row],axis=0)
            count_per_group[6]+=1

        elif latitude <= -30 and latitude > -35:
            row=pd.DataFrame({'ID':[station],'Latitude':[latitude],'Group':['(-30,-35)']})
            grouped_stations=pd.concat([grouped_stations,row],axis=0)
            count_per_group[7]+=1
            
    
    fig = plt.figure(figsize = (10, 5))
    plt.bar(coordinates, count_per_group, color ='maroon', width = 0.4)
    
    for index, value in enumerate(count_per_group):
        plt.text(index-0.1, value+2,str(value))
 
    
    plt.xlabel("Latitude Paralels")
    plt.ylabel("Number of Stations")
    plt.title("Stations Distribution in Brazil")
    plt.show()
    plt.savefig(log_path+'Distribution.png', format="png")


    
    log_path=r'/mnt/C/Users/rickg/Desktop/Solar Radiation Project/Log files'

    grouped_stations.to_csv(log_path+'/grouped_stations.csv',index=False)
    

prediction_folders=os.listdir(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Predictions')

prediction_folders=['ALLSKY_SFC_SW_DWN']

models=['SARIMA','HoltWinters','LSTM']



'''stations_average=pd.DataFrame()


for folder_name in prediction_folders:
    
    list_of_files=os.listdir(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Predictions/'+folder_name)
    
    list_of_files.remove('F501 (BELO HORIZONTE - CERCADINHO_MG).csv')
    
    global_metrics=pd.DataFrame(columns=['Model','Date','MAE','MSE','RMSE','R2'])
    
    for i in range(0,12):
        month_dataframe=pd.DataFrame()
        
        for file_name in list_of_files:
            station_data=pd.read_csv(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Predictions/'+folder_name+'/'+file_name)
            #station_data=station_data.drop('Date',axis=1)
            month_dataframe=pd.concat([month_dataframe,station_data.iloc[[i]]])

        for model in models:
            MAE,MSE,RMSE,R2=calculate_metrics(month_dataframe[folder_name],month_dataframe[model])
            row=pd.DataFrame({'Model':[model],'Date':[month_dataframe.iloc[0]['Date']],'MAE':[MAE],'MSE':[MSE],'RMSE':[RMSE],'R2':[R2]})
            global_metrics=pd.concat([global_metrics,row],axis=0)
       
Sarima_metrics=global_metrics[global_metrics['Model']=='SARIMA']
Sarima_metrics.rename(columns={'MAE':'MAE_SARIMA','MSE':'MSE_SARIMA','RMSE':'RMSE_SARIMA','R2':'R2_SARIMA'},inplace=True)


HoltWinters_metrics=global_metrics[global_metrics['Model']=='HoltWinters']
HoltWinters_metrics.rename(columns={'MAE':'MAE_HoltWinters','MSE':'MSE_HoltWinters','RMSE':'RMSE_HoltWinters','R2':'R2_HoltWinters'},inplace=True)

LSTM_metrics=global_metrics[global_metrics['Model']=='LSTM']
LSTM_metrics.rename(columns={'MAE':'MAE_LSTM','MSE':'MSE_LSTM','RMSE':'RMSE_LSTM','R2':'R2_LSTM'},inplace=True)

global_MAE=pd.concat([Sarima_metrics['Date'],
                      Sarima_metrics['MAE_SARIMA'],
                      HoltWinters_metrics['MAE_HoltWinters'],
                      LSTM_metrics['MAE_LSTM']],axis=1).set_index('Date')


figure = plt.figure(dpi=200,figsize=(10,5)) 
plt.title('Monthly MAE by Model')
plt.xlabel('Date')
plt.ylabel('MAE')
plt.plot(global_MAE['MAE_SARIMA'],color='green',label='SARIMA')
plt.plot(global_MAE['MAE_HoltWinters'],color='blue',label='HoltWinters')
plt.plot(global_MAE['MAE_LSTM'],color='orange',label='LSTM')
plt.legend()
plt.show()'''


station_catalog=pd.read_csv(r"/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Data/00-CatalogoEstaçõesAutomáticas.csv",delimiter=";").iloc[:,0:5]

all_stations_metrics=pd.DataFrame(columns=['Station','Latitude','Longitude','Model','MAE','MSE','RMSE','R2'])

for folder_name in prediction_folders:
    
    list_of_files=os.listdir(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Predictions/'+folder_name)
    
    list_of_files.remove('F501 (BELO HORIZONTE - CERCADINHO_MG).csv')
    list_of_files.remove('(5.68,-60.33).csv')
    list_of_files.remove('(-7.23,-33.32).csv')
    list_of_files.remove('(-7.26,-74.32).csv')

    station_groups=pd.read_csv(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Log files/grouped_stations.csv')
    groups=station_groups['Group'].unique()

    complete_metrics=pd.DataFrame(columns=['Group','Model','Date','MAE','MSE','RMSE','R2'])

    for group in groups:
        
        current_group=station_groups[station_groups['Group']==group]['ID'].to_list()

        current_group_file_names=[file_name for file_name in list_of_files if (file_name[:4] in current_group)]

        global_metrics=pd.DataFrame(columns=['Group','Model','Date','MAE','MSE','RMSE','R2'])

        for i in range(0,12):
            month_dataframe=pd.DataFrame()

            for file_name in current_group_file_names:
                station_data=pd.read_csv(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Predictions/'+folder_name+'/'+file_name)
                month_dataframe=pd.concat([month_dataframe,station_data.iloc[[i]]])

            for model in models:
                MAE,MSE,RMSE,R2=calculate_metrics(month_dataframe[folder_name],month_dataframe[model])
                row=pd.DataFrame({'Group':group,'Model':[model],'Date':[month_dataframe.iloc[0]['Date']],'MAE':[MAE],'MSE':[MSE],'RMSE':[RMSE],'R2':[R2]})
                global_metrics=pd.concat([global_metrics,row],axis=0)
        
        SARIMA_metrics=global_metrics[global_metrics['Model']=='SARIMA']
        HoltWinters_metrics=global_metrics[global_metrics['Model']=='HoltWinters']
        LSTM_metrics=global_metrics[global_metrics['Model']=='LSTM']   

        complete_metrics=pd.concat([complete_metrics,SARIMA_metrics,HoltWinters_metrics,LSTM_metrics],axis=0)
    

    
x = [1,2,3,4,5,6,7,8,9,10,11,12]

columns_dict={0:'(5,0)',1:'(0,-5)',2:'(-5,-10)',3:'(-10,-15)',4:'(-15,-20)',5:'(-20,-25)',6:'(-25,-30)',7:'(-30,-35)'}
rows_dict={'2022-01-01':'Jan','2022-02-01':'Feb','2022-03-01':'Mar','2022-04-01':'Apr','2022-05-01':'May','2022-06-01':'Jun','2022-07-01':'Jul','2022-08-01':'Aug','2022-09-01':'Sep','2022-10-01':'Oct','2022-11-01':'Nov','2022-12-01':'Dec'}

log_path=r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Log files/'
metrics_path=r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Metrics/ALLSKY_SFC_SW_DWN/'


for model in models:
    current_model_metrics=complete_metrics[complete_metrics['Model']==model]  
    current_model_metrics=current_model_metrics[['Group','Date','MAE','MSE']].sort_values('Group')
    current_model_metrics=current_model_metrics.replace({'(5,0)':0,
                                        '(0,-5)':1,
                                        '(-5,-10)':2,
                                        '(-10,-15)':3,
                                        '(-15,-20)':4,
                                        '(-20,-25)':5,
                                        '(-25,-30)':6,
                                        '(-30,-35)':7,
                                        })
    
    current_model_MAE=current_model_metrics.pivot_table(index='Date',columns='Group',values='MAE')
    current_model_MSE=current_model_metrics.pivot_table(index='Date',columns='Group',values='MSE')

    for column in current_model_MAE.columns:
            fig, ax = plt.subplots(figsize = (12, 8))
            
            bars_MAE=ax.bar(x, current_model_MAE[column].values ,width=0.7, edgecolor="white", linewidth=1,color='#7eb54e',label='MAE')
            bars_MSE=ax.bar(x, current_model_MSE[column].values ,width=0.7, edgecolor="white", linewidth=1,color='Gray',label='MSE')
            
    
            for bar in bars_MAE:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height + 0.02, '{:.2f}'.format(height),
                        ha='center', va='bottom')
                
            for bar in bars_MSE:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height + 0.02, '{:.2f}'.format(height),
                        ha='center', va='bottom')
    
            ax.set(xlim=(0, 13), xticks=x, xticklabels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                ylim=(0, 1.3))
    
            ax.set_xlabel('Month')
            ax.set_ylabel('Error')
    
            plt.title(columns_dict[column]+' '+model)
            plt.legend()
            #plt.show()
    
            plt.savefig(metrics_path+model+'/group '+columns_dict[column]+'.png', format="png")
            plt.close('all')
            
    current_model_MAE=current_model_MAE.rename(columns=columns_dict,index=rows_dict).transpose()
    current_model_MAE=current_model_MAE.astype(float)   

    fig, ax = plt.subplots(figsize=(16,9))  
    error_map=sns.heatmap(current_model_MAE,annot=True, fmt=".2f",ax=ax, cmap='coolwarm', linewidths=0.5)
    ax.set_title('MAE Metrics - '+model)
    fig.savefig(metrics_path+model+'/MAE.png', format="png")
    
    current_model_MSE=current_model_MSE.rename(columns=columns_dict,index=rows_dict).transpose()
    current_model_MSE=current_model_MSE.astype(float)  

    fig, ax = plt.subplots(figsize=(16,9))  
    error_map=sns.heatmap(current_model_MSE,annot=True, fmt=".2f",ax=ax, cmap='coolwarm', linewidths=0.5)
    ax.set_title('MSE metrics - '+model)
    fig.savefig(metrics_path+model+'/MSE.png', format="png")

    plt.close('all')

            







            

current_model_MAE=current_model_MAE.rename(columns=columns_dict,index=rows_dict).transpose()
current_model_MAE=current_model_MAE.astype(float)

#current_model_MAE=current_model_MAE.set_index('Group')

fig, ax = plt.subplots(figsize=(16,9))  
#ax = plt.axes()
error_map=sns.heatmap(current_model_MAE,annot=True, fmt="d",ax=ax, cmap='coolwarm', linewidths=0.5)
ax.set_title('MAE metrics')

#fig=error_map.get_figure()
fig.savefig(log_path+'Metrics/'+model+'/MAE.png', format="png")




'''Plot Modelo Individual
SARIMA_metrics=complete_metrics[complete_metrics['Model']=='SARIMA']

SARIMA_metrics=SARIMA_metrics[['Group','Date','MAE','MSE']].sort_values('Group')

SARIMA_metrics=SARIMA_metrics.replace({'(5,0)':0,
                                       '(0,-5)':1,
                                       '(-5,-10)':2,
                                       '(-10,-15)':3,
                                       '(-15,-20)':4,
                                       '(-20,-25)':5,
                                       '(-25,-30)':6,
                                       '(-30,-35)':7,
                                       })

SARIMA_metrics=SARIMA_metrics.replace({'2022-01-01':0,
                                       '2022-02-01':1,
                                       '2022-03-01':2,
                                       '2022-04-01':3,
                                       '2022-05-01':4,
                                       '2022-06-01':5,
                                       '2022-07-01':6,
                                       '2022-08-01':7,
                                       '2022-09-01':8,
                                       '2022-10-01':9,
                                       '2022-11-01':10,
                                       '2022-12-01':11,
                                       })



SARIMA_MAE=SARIMA_metrics.pivot_table(index='Date',columns='Group',values='MAE')
SARIMA_MSE=SARIMA_metrics.pivot_table(index='Date',columns='Group',values='MSE')





x = [1,2,3,4,5,6,7,8,9,10,11,12]

columns_dict={0:'(5,0)',1:'(0,-5)',2:'(-5,-10)',3:'(-10,-15)',4:'(-15,-20)',5:'(-20,-25)',6:'(-25,-30)',7:'(-30,-35)'}

log_path=r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Log files/'



for column in SARIMA_MAE.columns:

    fig, ax = plt.subplots(figsize = (10, 8))
    
    bars_MAE=ax.bar(x, SARIMA_MAE[column].values ,width=0.7, edgecolor="white", linewidth=1,color='#7eb54e',label='MAE')
    bars_MSE=ax.bar(x, SARIMA_MSE[column].values ,width=0.7, edgecolor="white", linewidth=1,color='Gray',label='MSE')
    

    for bar in bars_MAE:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.02, '{:.2f}'.format(height),
                ha='center', va='bottom')
        
    for bar in bars_MSE:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.02, '{:.2f}'.format(height),
                ha='center', va='bottom')

    ax.set(xlim=(0, 13), xticks=x, xticklabels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        ylim=(0, 1.3))

    ax.set_xlabel('Month')
    ax.set_ylabel('Error')

    plt.title(columns_dict[column])
    plt.legend()
    #plt.show()

    plt.savefig(log_path+'Sarima group '+columns_dict[column]+'.png', format="png")
    
    plt.close('all')

    
    



teste=SARIMA_metrics.iloc[:,0]

fig, ax = plt.subplots()

bars=ax.bar(x, teste.values ,width=1, edgecolor="white", linewidth=1)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.02, '{:.2f}'.format(height),
            ha='center', va='bottom')

ax.set(xlim=(0, 13), xticks=x, xticklabels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
       ylim=(0, 1))

ax.set_xlabel('Month')
ax.set_ylabel('Error')

plt.title('Monthly MAE by Latitude Group')

plt.show()

'''

'''Grafico 3D
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Criar um DataFrame de exemplo com 12 linhas e 8 colunas
#data = np.random.rand(12, 8)  # Use seus dados reais aqui
#df = pd.DataFrame(data)

# Criar uma figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Definir posições das barras
xpos, ypos = np.meshgrid(np.arange(SARIMA_metrics.shape[1]), np.arange(SARIMA_metrics.shape[0]))
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = 0

# Definir as alturas das barras
dz = SARIMA_metrics.values.ravel()

# Criar o gráfico de barras em 3D
ax.bar3d(xpos, ypos, zpos, 1, 1, dz, shade=True)

# Definir rótulos dos eixos
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Exibir o gráfico
plt.show()
'''

'''Testes


from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot( projection='3d')

x3=SARIMA_metrics.index
y3=SARIMA_metrics.columns.values
z3= np.zeros(len(x3))

dx = np.full(len(x3),0.5)
dy = np.full(len(x3),0.5)


dz = SARIMA_metrics.values

ax1.bar3d(x3, y3, z3, dx, dy, dz)


ax1.set_xlabel('Longitude')
ax1.set_ylabel('Lagitude')
ax1.set_zlabel('MAE')

plt.show()

january=station_data.iloc[[0]]
july=station_data.iloc[[6]]


MAE_january=metrics.mean_absolute_error(january[folder_name],january['SARIMA'])
MAE_july=metrics.mean_absolute_error(july[folder_name],july['SARIMA'])

coordinates=['(5,0)','(0,-5)','(-5,-10)','(-10,-15)','(-15,-20)','(-20,-25)','(-25,-30)','(-30,-35)']
'''

 

    
