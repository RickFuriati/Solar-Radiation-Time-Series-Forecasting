import pandas as pd
import geopandas
from shapely.geometry import Point
from osgeo import gdal
import os

import warnings



warnings.filterwarnings("ignore")

os.chdir('/mnt/c/Users/rickg/Desktop/Solar Radiation Project/')

def grid_INMET_stations():

    data_path=r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Data/00-CatalogoEstaçõesAutomáticas.csv'

    station_index=pd.read_csv(data_path,delimiter=';')

    predictions_path=r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Predictions/ALLSKY_SFC_SW_DWN/'

    list_of_files=os.listdir(predictions_path)

    grid=pd.DataFrame(columns=['ID','Latitude','Longitude','SARIMA','HoltWinters','LSTM','Actual','Date']).set_index('Date')

        
    station_reference_data=pd.read_csv(predictions_path+list_of_files[0])

    for i in range(0,len(station_reference_data)):
            
            mean_grid=pd.DataFrame()
            grid=pd.DataFrame()
            
            for file_name in list_of_files:
                
                if file_name[0]!='(':

                    station_name=file_name[0:4]
            
                else:
                    station_name=file_name.removesuffix('.csv')
            
                
                station_data=pd.read_csv(predictions_path+file_name)
                

                station_data=station_data.iloc[[i]]
                

                latitude=station_index[station_index['CD_ESTACAO']==station_name]['VL_LATITUDE'].values
                latitude=float(latitude[0].replace(',','.'))
                
                longitude=station_index[station_index['CD_ESTACAO']==station_name]['VL_LONGITUDE'].values
                longitude=float(longitude[0].replace(',','.'))
                
                row=pd.DataFrame({'ID':station_name,'Latitude':latitude,'Longitude':longitude,'Date':station_data['Date'],
                                'SARIMA':station_data['SARIMA'],'HoltWinters':station_data['HoltWinters'],
                                'LSTM':station_data['LSTM'],'Actual':station_data['ALLSKY_SFC_SW_DWN']})
                
                #grid=grid.append(row,ignore_index=True)
                grid=pd.concat([grid,row],axis=0,ignore_index=True)

                


            #mean_grid.to_csv(os.getcwd()+'\Maps\Rasters\Actual\\'+station_name+'.csv')
            grid['coordinates']=grid[['Longitude','Latitude']].values.tolist()
            grid['coordinates']=grid['coordinates'].apply(Point)
        

            start=0
            end=11
            for i in range(0,len(grid)):
                if(i%11==0):
                    sarima_mean=grid['SARIMA'].iloc[start:end].mean()
                    holtWinters_mean=grid['HoltWinters'].iloc[start:end].mean()
                    lstm_mean=grid['LSTM'].iloc[start:end].mean()
                    actual_mean=grid['Actual'].iloc[start:end].mean()
                    start=end;
                    end=end+11;

                    mean_row=pd.DataFrame({'ID':station_name,'Latitude':latitude,'Longitude':longitude,'Date':station_data['Date'],
                                'SARIMA':sarima_mean,'HoltWinters':holtWinters_mean,
                                'LSTM':lstm_mean,'Actual':actual_mean})
                
                    
                    #mean_grid=mean_grid.append(mean_row,ignore_index=True)
                    mean_grid=pd.concat([mean_grid,mean_row],axis=0,ignore_index=True)

            spacial_grid=geopandas.GeoDataFrame(grid,geometry='coordinates')
            spacial_grid.to_file(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Shapefile/spacial_grid.shp')

            mean_grid['coordinates']=mean_grid[['Longitude','Latitude']].values.tolist()
            mean_grid['coordinates']=mean_grid['coordinates'].apply(Point)

            mean_spacial_grid=geopandas.GeoDataFrame(grid,geometry='coordinates')
        
            mean_spacial_grid.to_file( r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Shapefile/mean_spacial_grid.shp')
            
            Date=grid['Date'].iloc[0]
            #print(Date)
            
            
            paramters='invdist:power=6:smoothing=1:radius1=100:radius2=100'
    
            
            idw_actual=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/Actual/'+Date+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Shapefile/spacial_grid.shp',zfield='Actual',algorithm=paramters)
            idw_actual=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/Actual/'+Date[0:4]+'_Average'+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Shapefile/mean_spacial_grid.shp',zfield='Actual',algorithm=paramters)

            idw_actual=None
            

            idw_sarima=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/SARIMA/'+Date+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Shapefile/spacial_grid.shp',zfield='SARIMA',algorithm=paramters)
            idw_sarima=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/SARIMA/'+Date[0:4]+'_Average'+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Shapefile/mean_spacial_grid.shp',zfield='SARIMA',algorithm=paramters)

            idw_sarima=None
            
            idw_holtWinters=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/HoltWinters/'+Date+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Shapefile/spacial_grid.shp',zfield='HoltWinter',algorithm=paramters)
            idw_holtWinters=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/HoltWinters/'+Date[0:4]+'_Average'+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Shapefile/mean_spacial_grid.shp',zfield='HoltWinter',algorithm=paramters)

            idw_holtWinters=None
            
            idw_lstm=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/LSTM/'+Date+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Shapefile/spacial_grid.shp',zfield='LSTM',algorithm=paramters)
            idw_lstm=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/LSTM/'+Date[0:4]+'_Average'+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Shapefile/mean_spacial_grid.shp',zfield='LSTM',algorithm=paramters)

            idw_lstm=None
            
def grid_01_degree():
    #data_path=r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Data/00-CatalogoEstaçõesAutomáticas.csv'

    station_index=pd.read_csv(r"/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Maps/Grid (01 degree) - Useful.csv")
    station_index=station_index.set_index('id')
    station_index=station_index.iloc[:,0:2].rename(columns={'X':'Longitude','Y':'Latitude'})
    station_index['Name']='('+station_index['Latitude'].astype(str)+';'+station_index['Longitude'].astype(str)+')'

    station_index=station_index.set_index('Name')


    #station_index=pd.read_csv(data_path,delimiter=';')

    predictions_path=r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/01 degree predictions/ALLSKY_SFC_SW_DWN/'

    list_of_files=os.listdir(predictions_path)

    grid=pd.DataFrame(columns=['ID','Latitude','Longitude','SARIMA','HoltWinters','LSTM','Actual','Date']).set_index('Date')

        
    station_reference_data=pd.read_csv(predictions_path+list_of_files[0])

    for i in range(0,len(station_reference_data)):
            
            mean_grid=pd.DataFrame()
            grid=pd.DataFrame()
            
            for file_name in list_of_files:
                
                station_name=file_name.removesuffix('.csv')
            
                station_data=pd.read_csv(predictions_path+file_name)
                

                station_data=station_data.iloc[[i]]
                
                latitude=station_index[station_index.index==station_name]['Latitude'].values
                longitude=station_index[station_index.index==station_name]['Longitude'].values

                #latitude=station_index[station_index['CD_ESTACAO']==station_name]['VL_LATITUDE'].values
                #latitude=float(latitude[0].replace(',','.'))
                
                #longitude=station_index[station_index['CD_ESTACAO']==station_name]['VL_LONGITUDE'].values
                #longitude=float(longitude[0].replace(',','.'))
                
                row=pd.DataFrame({'ID':station_name,'Latitude':latitude,'Longitude':longitude,'Date':station_data['Date'],
                                'SARIMA':station_data['SARIMA'],'HoltWinters':station_data['HoltWinters'],
                                'LSTM':station_data['LSTM'],'Actual':station_data['ALLSKY_SFC_SW_DWN']})
                
                #grid=grid.append(row,ignore_index=True)
                grid=pd.concat([grid,row],axis=0,ignore_index=True)

                


            #mean_grid.to_csv(os.getcwd()+'\Maps\Rasters\Actual\\'+station_name+'.csv')
            grid['coordinates']=grid[['Longitude','Latitude']].values.tolist()
            grid['coordinates']=grid['coordinates'].apply(Point)
        

            start=0
            end=11
            for i in range(0,len(grid)):
                if(i%11==0):
                    sarima_mean=grid['SARIMA'].iloc[start:end].mean()
                    holtWinters_mean=grid['HoltWinters'].iloc[start:end].mean()
                    lstm_mean=grid['LSTM'].iloc[start:end].mean()
                    actual_mean=grid['Actual'].iloc[start:end].mean()
                    start=end;
                    end=end+11;

                    mean_row=pd.DataFrame({'ID':station_name,'Latitude':latitude,'Longitude':longitude,'Date':station_data['Date'],
                                'SARIMA':sarima_mean,'HoltWinters':holtWinters_mean,
                                'LSTM':lstm_mean,'Actual':actual_mean})
                
                    
                    #mean_grid=mean_grid.append(mean_row,ignore_index=True)
                    mean_grid=pd.concat([mean_grid,mean_row],axis=0,ignore_index=True)

            spacial_grid=geopandas.GeoDataFrame(grid,geometry='coordinates')
            spacial_grid.to_file(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/spacial_grid.shp')

            mean_grid['coordinates']=mean_grid[['Longitude','Latitude']].values.tolist()
            mean_grid['coordinates']=mean_grid['coordinates'].apply(Point)

            mean_spacial_grid=geopandas.GeoDataFrame(grid,geometry='coordinates')
        
            mean_spacial_grid.to_file( r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/mean_spacial_grid.shp')
            
            Date=grid['Date'].iloc[0]
            #print(Date)
            
            
            paramters='invdist:power=5:smoothing=1:radius1=555000:radius2=555000'
            #paramters='linear:radius=555000'
            
            idw_actual=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/Actual/'+Date+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/spacial_grid.shp',zfield='Actual',algorithm=paramters)
            idw_actual=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/Actual/'+Date[0:4]+'_Average'+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/mean_spacial_grid.shp',zfield='Actual',algorithm=paramters)

            idw_actual=None
            

            idw_sarima=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/SARIMA/'+Date+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/spacial_grid.shp',zfield='SARIMA',algorithm=paramters)
            idw_sarima=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/SARIMA/'+Date[0:4]+'_Average'+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/mean_spacial_grid.shp',zfield='SARIMA',algorithm=paramters)

            idw_sarima=None
            
            idw_holtWinters=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/HoltWinters/'+Date+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/spacial_grid.shp',zfield='HoltWinter',algorithm=paramters)
            idw_holtWinters=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/HoltWinters/'+Date[0:4]+'_Average'+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/mean_spacial_grid.shp',zfield='HoltWinter',algorithm=paramters)

            idw_holtWinters=None
            
            idw_lstm=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/LSTM/'+Date+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/spacial_grid.shp',zfield='LSTM',algorithm=paramters)
            idw_lstm=gdal.Grid(r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/LSTM/'+Date[0:4]+'_Average'+'.tif',r'/mnt/c/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/mean_spacial_grid.shp',zfield='LSTM',algorithm=paramters)

            idw_lstm=None

grid_01_degree()