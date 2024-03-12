'''
*Version: 2.0 Published: 2021/03/09* Source: [NASA POWER](https://power.larc.nasa.gov/)
POWER API Multi-Point Download
This is an overview of the process to request data from multiple data points from the POWER API.
'''

import os, json, requests
import pandas as pd
import datetime
import time

def download_all_INMET_stations():

    Station_catalog=pd.read_csv(r"C:\Users\rickg\Desktop\Solar Radiation Project\Data\00-CatalogoEstaçõesAutomáticas.csv",delimiter=";").iloc[:,0:5]
    num_stations=len(Station_catalog)
    counter=1;

    for index, row in Station_catalog.iterrows():
        Start_Time = time.time()
        
        print("Processing station - "+row['CD_ESTACAO']+" ("+str(counter)+" of "+str(num_stations)+" stations).")
        counter+=1
        
        latitude=float(row['VL_LATITUDE'].replace(",","."))
        longitude=float(row['VL_LONGITUDE'].replace(",","."))
        station_name=row['CD_ESTACAO']+" ("+row['DC_NOME']+"_"+row['SG_ESTADO']+").csv"
        output = r"C:\Users\rickg\Desktop\Solar Radiation Project\Data\\"+station_name
        
        #base_url = r"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2MDEW,T2MWET,TS,T2M_RANGE,T2M_MAX,T2M_MIN&community=RE&longitude={longitude}&latitude={latitude}&start=20150101&end=20150305&format=JSON"
        
        
        base_url = r"https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=ALLSKY_SFC_SW_DWN,ALLSKY_KT,CLOUD_AMT,T2M,RH2M,PS,WS10M&community=RE&longitude={longitude}&latitude={latitude}&format=JSON&start=1981&end=2022&format=JSON"
        api_request_url = base_url.format(longitude=longitude, latitude=latitude)

        response = requests.get(url=api_request_url, verify=True, timeout=30.00).json()
        #geometry=response.get("geometry")
        
        header=response.get("header")
        start=header.get("start")
        end=header.get("end")
        
        parameters=response.get("parameters")
        properties=response.get("properties")  
        values=properties.get("parameter")      
        
        header_text=header.get("title")+"\n"
        header_text+="Latitude: "+str(latitude) +"   "+"Longitude: "+str(longitude)+"\n"
        header_text+= "Station ID: "+row['CD_ESTACAO']+" ("+row['DC_NOME']+" "+row['SG_ESTADO'] +")\n"
        
        variable_legend="Legend:\n"
        
        station_data=pd.DataFrame()
        for key in parameters:
            parameters.get(key)
            longname=parameters.get(key).get("longname")
            units=parameters.get(key).get("units")
            variable_legend+=longname+ " - ("+units+")\n"
            
            current_variable=values.get(key)
            
            current_variable=pd.json_normalize(current_variable).transpose().rename(columns={0:key})        
            station_data=pd.concat([station_data,current_variable],axis=1)
            
        header_text+=variable_legend+'\n'
        
        index_value=station_data.index.astype("str")
        
        date_index=[]
        
        yearly_avg=pd.DataFrame()
        
        for value in index_value: 
            year=int(value[0:4])
            month=int(value[4::])
            if(month!=13):
                date=datetime.datetime(year,month,1)
                date_index.append(date)
            else:
                yearly_avg_row=station_data.iloc[station_data.index==value]
                yearly_avg_row.index=[year]
                station_data=station_data.drop(value)
                yearly_avg=pd.concat([yearly_avg,yearly_avg_row])
    
        station_data=station_data.reset_index()
        station_data.index=date_index
        station_data=station_data.drop('index',axis=1)
        
        station_data=station_data.reset_index()
        station_data=station_data.rename(columns={'index':'Date'})
        
        with open(output, 'w') as fp:
            fp.write(header_text)
            
        station_data.to_csv(output,mode='a',index=False)
        
        yearly_output=r'C:\Users\rickg\Desktop\Solar Radiation Project\Data\Yearly Average\\'+station_name
        
        with open(yearly_output, 'w') as fp:
            fp.write(header_text)
        
        yearly_avg=yearly_avg.reset_index()
        yearly_avg=yearly_avg.rename(columns={'index':'Year'})
        yearly_avg.to_csv(yearly_output,mode='a',index=False)

        del(station_data)
        del(current_variable)
        
        print ("Station "+row['CD_ESTACAO']+" finished processing ("+str(round((time.time() - Start_Time), 3))+" s)")
            
        #break;

def download_01_degree_grid():
    grid_catalog=pd.read_csv(r"C:\Users\rickg\Desktop\Solar Radiation Project\Maps\Grid (01 degree).csv")
    grid_catalog=grid_catalog.iloc[:,0:2].rename(columns={'X':'Longitude','Y':'Latitude'})
    num_stations=len(grid_catalog)
    counter=1;

    print('Downloading data for 01 degree grid.')

    for index, row in grid_catalog.iterrows():
        #Start_Time = time.time()
        
        #print("Processing station - "+row['CD_ESTACAO']+" ("+str(counter)+" of "+str(num_stations)+" stations).")
        print("Processing point - "+str(counter)+" of "+str(num_stations)+" points.")
        
        counter+=1
        
        latitude=float(row['Latitude'])
        longitude=float(row['Longitude'])
        
        station_name='('+str(latitude)+';'+str(longitude)+').csv'
        
        output = r"C:\Users\rickg\Desktop\Solar Radiation Project\Heatmaps\01 degree grid\\"+station_name
        
        #base_url = r"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2MDEW,T2MWET,TS,T2M_RANGE,T2M_MAX,T2M_MIN&community=RE&longitude={longitude}&latitude={latitude}&start=20150101&end=20150305&format=JSON"
        
        
        base_url = r"https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude={longitude}&latitude={latitude}&format=JSON&start=1981&end=2022&format=JSON"
        api_request_url = base_url.format(longitude=longitude, latitude=latitude)

        response = requests.get(url=api_request_url, verify=True, timeout=30.00).json()
        #geometry=response.get("geometry")
        
        header=response.get("header")
        start=header.get("start")
        end=header.get("end")
        
        parameters=response.get("parameters")
        properties=response.get("properties")  
        values=properties.get("parameter")      
        
        #header_text=header.get("title")+"\n"
        #header_text+="Latitude: "+str(latitude) +"   "+"Longitude: "+str(longitude)+"\n"
        #header_text+= "Station ID: "+row['CD_ESTACAO']+" ("+row['DC_NOME']+" "+row['SG_ESTADO'] +")\n"
        
        #variable_legend="Legend:\n"
        
        station_data=pd.DataFrame()
        for key in parameters:
            parameters.get(key)
            #longname=parameters.get(key).get("longname")
            #units=parameters.get(key).get("units")
            #variable_legend+=longname+ " - ("+units+")\n"
            
            current_variable=values.get(key)
            
            current_variable=pd.json_normalize(current_variable).transpose().rename(columns={0:key})        
            station_data=pd.concat([station_data,current_variable],axis=1)
            
        #header_text+=variable_legend+'\n'
        
        index_value=station_data.index.astype("str")
        
        date_index=[]
        
        yearly_avg=pd.DataFrame()
        
        for value in index_value: 
            year=int(value[0:4])
            month=int(value[4::])
            if(month!=13):
                date=datetime.datetime(year,month,1)
                date_index.append(date)
            else:
                yearly_avg_row=station_data.iloc[station_data.index==value]
                yearly_avg_row.index=[year]
                station_data=station_data.drop(value)
                yearly_avg=pd.concat([yearly_avg,yearly_avg_row])
    
        station_data=station_data.reset_index()
        station_data.index=date_index
        station_data=station_data.drop('index',axis=1)
        
        station_data=station_data.reset_index()
        station_data=station_data.rename(columns={'index':'Date'})
        
        '''with open(output, 'w') as fp:
            fp.write(header_text)'''
            
        station_data.to_csv(output,mode='a',index=False)
        
        yearly_output=r'C:\Users\rickg\Desktop\Solar Radiation Project\Heatmaps\01 degree grid\Yearly Average\\'+station_name
        
        '''with open(yearly_output, 'w') as fp:
            fp.write(header_text)'''
        
        yearly_avg=yearly_avg.reset_index()
        yearly_avg=yearly_avg.rename(columns={'index':'Year'})
        yearly_avg.to_csv(yearly_output,mode='a',index=False)

        del(station_data)
        del(current_variable)
        
        #print ("Station "+row['CD_ESTACAO']+" finished processing ("+str(round((time.time() - Start_Time), 3))+" s)")
            
        #break;


download_01_degree_grid()



#print('teste')







  
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        