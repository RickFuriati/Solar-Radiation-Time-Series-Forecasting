from typing import List

import os

def color_ramp_items(

    colormap: str, minimum: float, maximum: float, nclass: int

) -> List[QgsColorRampShader.ColorRampItem]:

    delta = maximum - minimum

    fractional_steps = [i / nclass for i in range(nclass + 1)]

    ramp = QgsStyle().defaultStyle().colorRamp(colormap)

    colors = [ramp.color(f) for f in fractional_steps]

    steps = [minimum + f * delta for f in fractional_steps]

    return [

        QgsColorRampShader.ColorRampItem(step, color, str(step))

        for step, color in zip(steps, colors)

    ]

def pseudocolor_styling(layer, colormap: str, nclass: int) -> None:
    provider = layer.dataProvider()

    extent = layer.extent()

    stats = provider.bandStatistics(1, QgsRasterBandStats.All,extent, 0)


    #stats = layer.dataProvider().bandStatistics(1, QgsRasterBandStats.All)

    minimum = stats.minimumValue
    maximum = stats.maximumValue

    #minimum = 2
    #maximum = 10



    ramp_items = color_ramp_items(colormap, minimum, maximum, nclass)

    shader_function = QgsColorRampShader()

    shader_function.setClassificationMode(2)

    shader_function.setColorRampItemList(ramp_items)

    shader_function.setColorRampType(QgsColorRampShader.Interpolated )

    raster_shader = QgsRasterShader()

    

    raster_shader.setRasterShaderFunction(shader_function)



    #renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, raster_shader)
    

    renderer=QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 



                                                    layer.type(),  



                                                    raster_shader)

    
    layer.setRenderer(renderer)

    layer.triggerRepaint()




#list_of_folders=os.listdir(os.pardir()+'\Maps\Rasters')
    


'''
path=r'C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'


list_of_folders=os.listdir(path)


for folder_name in list_of_folders:

   # print(folder_name)

    #os.makedirs('C:/Users/rickg/Desktop/Time-series/1.0/Maps/Rasters/'+folder_name+'/StateLimit',exist_ok=True)
    #os.makedirs('C:/Users/rickg/Desktop/Time-series/1.0/Maps/Rasters/'+folder_name+'/Images',exist_ok=True)


    os.makedirs(r'C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'+folder_name+'/StateLimit/',exist_ok=True)
    os.makedirs(r'C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'+folder_name+'/Images/',exist_ok=True)
    
    list_of_files=os.listdir(path+'/'+folder_name)

    for file_name in list_of_files:

        #print(file_name)

        
        if(file_name.endswith('.tif')==True):
        
            #print(file_name)

            
            
           #output_path='C:/Users/rickg/Desktop/Time-series/1.0/Maps/Rasters/'+folder_name+'/StateLimit/'+file_name
            output_path='C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'+folder_name+'/StateLimit/'+file_name

            mask="C:/Users/rickg/Desktop/Solar Radiation Project/Maps/BR_Pais_2021/BR_Pais_2021.shp"
            #mask="C:/Users/rickg/Desktop/Solar Radiation Project/Maps/bra_adm_ibge_2020_shp/bra_admbnda_adm1_ibge_2020.shp"
            #mask='C:/Users/rickg/Documents/Cold Storage/Time-series/1.0/Maps/MG_limite_estadual/MG_limite_estadual.shp'

            processing.run("gdal:cliprasterbymasklayer", {'INPUT':'C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'+folder_name+'/'+file_name,
                                                          'MASK':mask,'SOURCE_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),'TARGET_EXTENT':'-73.9904679169921877,-33.7507685263671959 ,-28.8491679169921866,5.2711314736328063 [EPSG:4326]',

            'NODATA':0,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,'KEEP_RESOLUTION':True,'SET_RESOLUTION':True,'X_RESOLUTION':0.05,'Y_RESOLUTION':0.05,'MULTITHREADING':True,

            'OPTIONS':'','DATA_TYPE':0,'EXTRA':'',

            'OUTPUT':output_path})

            
            

            layer=iface.addRasterLayer(output_path,file_name.removesuffix('.tif'))
            #layer = QgsProject.instance().mapLayersByName("saidaTeste")[0]
            pseudocolor_styling(layer, colormap="Turbo", nclass=255)

            img=QImage(QSize(1800,1000),QImage.Format_ARGB32_Premultiplied)

            color=QColor(255,255,255,255)
            img.fill(color.rgba())



            


            p=QPainter()
            p.begin(img)
            p.setRenderHint(QPainter.Antialiasing)

            ms=QgsMapSettings()
            ms.setBackgroundColor(color)

            layer1=QgsProject.instance().mapLayersByName(file_name.removesuffix('.tif'))[0]
            layer2=QgsProject.instance().mapLayersByName('BR_Pais_2021')[0]

            ms.setLayers([layer2,layer1])

            rect=QgsRectangle(ms.fullExtent())
            rect.scale(1.1)
            ms.setExtent(rect)

            ms.setOutputSize(img.size())

            render=QgsMapRendererCustomPainterJob(ms,p)
            render.start()
            render.waitForFinished()
            p.end()

            Image_path='C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'+folder_name+'/Images/'+file_name.removesuffix('.tif')+'.png'

            img.save(Image_path)
            QgsProject.instance().removeMapLayer(layer1.id())

            break
        break
'''


def create_maps():


    #list_of_folders=os.listdir(os.pardir()+'\Maps\Rasters')

    path=r'C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'

    list_of_folders=os.listdir(path)



    #list_of_folders.remove('Teste')
    #list_of_folders.remove('SARIMA')

    #list_of_folders.remove('LSTM')

    #list_of_folders.remove('HoltWinters')

    #list_of_folders.remove('Actual')
    for folder_name in list_of_folders:

        #print(folder_name)

        os.makedirs(r'C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'+folder_name+'/StateLimit/',exist_ok=True)
        os.makedirs(r'C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'+folder_name+'/Images/',exist_ok=True)
        
        list_of_files=os.listdir(path+'\\'+folder_name)

        
        #list_of_files=list_of_files[260:286]
        #list_of_files=list_of_files[339:340]
        #list_of_files=['2020_Average.tif']

        for file_name in list_of_files:

            if(file_name.endswith('.tif')==True):

                mask="C:/Users/rickg/Desktop/Solar Radiation Project/Maps/BR_Pais_2021/BR_Pais_2021.shp"

                #print(file_name)
                output_path='C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'+folder_name+'/StateLimit/'+file_name

                processing.run("gdal:cliprasterbymasklayer", {'INPUT':'C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'+folder_name+'/'+file_name,
                                                          'MASK':mask,'SOURCE_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),'TARGET_EXTENT':'-73.9904679169921877,-33.7507685263671959 ,-28.8491679169921866,5.2711314736328063 [EPSG:4326]',

                'NODATA':0,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,'KEEP_RESOLUTION':True,'SET_RESOLUTION':True,'X_RESOLUTION':0.05,'Y_RESOLUTION':0.05,'MULTITHREADING':True,

                'OPTIONS':'','DATA_TYPE':0,'EXTRA':'',

                'OUTPUT':output_path})

                layer=iface.addRasterLayer(output_path,file_name.removesuffix('.tif'))
                #layer = QgsProject.instance().mapLayersByName("saidaTeste")[0]
                pseudocolor_styling(layer, colormap="Turbo", nclass=255)

                img=QImage(QSize(800,800),QImage.Format_ARGB32_Premultiplied)
            
                color=QColor(255,255,255,255)
                img.fill(color.rgba())

                provider = layer.dataProvider()
                extent = layer.extent()
                stats = provider.bandStatistics(1, QgsRasterBandStats.All,extent, 0)
                minimum = stats.minimumValue
                maximum = stats.maximumValue
                

                project=QgsProject.instance()
                manager=project.layoutManager()
                
                
                layout_list=manager.printLayouts()
                layout= layout_list[0]



                max_label = QgsLayoutItemLabel(layout)  
                str_max=f'{maximum:.1f}'
                max_label.setText(str_max)
                max_label.setFont(QFont("Arial", 12))
                layout.addLayoutItem(max_label)
                max_label.attemptMove(QgsLayoutPoint(245,56))

                

                min_label = QgsLayoutItemLabel(layout)  
                str_min=f'{minimum:.1f}'
                min_label.setText(str_min)
                min_label.setFont(QFont("Arial", 12))
                layout.addLayoutItem(min_label)
                min_label.attemptMove(QgsLayoutPoint(245,139))

                units_label= QgsLayoutItemLabel(layout) 
                str_units='kWh/m\u00b2/day'

                units_label.setText(str_units)

                units_label.setFont(QFont("Arial", 12))

                layout.addLayoutItem(units_label)

                units_label.attemptMove(QgsLayoutPoint(245,47))
                
                
                
                month_number=(file_name[5:7])

                if month_number=='01':
                    month_name='Jan'
                elif month_number=='02':
                    month_name='Feb'
                elif month_number=='03':
                    month_name='Mar'
                elif month_number=='04':
                    month_name='Apr'
                elif month_number=='05':
                    month_name='May'
                elif month_number=='06':
                    month_name='Jun'
                elif month_number=='07':
                    month_name='Jul'
                elif month_number=='08':
                    month_name='Aug'
                elif month_number=='09':
                    month_name='Sep'
                elif month_number=='10':
                    month_name='Oct'
                elif month_number=='11':
                    month_name='Nov'
                elif month_number=='12':
                    month_name='Dec'
                else:
                    month_name=' '

             

                
                date_label = QgsLayoutItemLabel(layout)  
                str_date=month_name
                




                #date_label.setText(str_date)
                #date_label.setFont(QFont("Arial", 20))
                #layout.addLayoutItem(date_label)
                #date_label.attemptMove(QgsLayoutPoint(70,160))
    

                str_date=''
                
                map=QgsLayoutItemMap(layout)
                map.setRect(20,20,20,20)

                ms=QgsMapSettings()
                ms.setBackgroundColor(color)
                layer1=project.mapLayersByName(file_name.removesuffix('.tif'))[0]
                layer2=project.mapLayersByName('BR_Pais_2021')[0]
                ms.setLayers([layer2,layer1])
                rect=QgsRectangle(ms.fullExtent())
                rect.scale(1.1)
                ms.setExtent(rect)
                layout.addLayoutItem(map)
                
                manager.addLayout(layout)
                

                layer_list =names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
                

                for layer_name in layer_list:

                    while layer_list.count(layer_name)>1:

                        QgsProject.instance().removeMapLayer(layer_name)
                
            
                legend=QgsLayoutItemLegend(layout)
                
                layerTree=iface.layerTreeCanvasBridge().rootGroup()
                layerTree.insertChildNode(1,QgsLayerTreeLayer(layer1))
                layerTree.insertChildNode(0,QgsLayerTreeLayer(layer2))
        

                legend.model().setRootGroup(layerTree)

                layout.addLayoutItem(map)
            
                legend.setAutoUpdateModel(True)

                exporter=QgsLayoutExporter(layout)
               
                Image_path='C:/Users/rickg/Desktop/Solar Radiation Project/Maps/Rasters/'+folder_name+'/Images/'+file_name.removesuffix('.tif')+'.png'

                exporter.exportToImage(Image_path,QgsLayoutExporter.ImageExportSettings())

                
                layout.removeLayoutItem(max_label)
                layout.removeLayoutItem(date_label)
                layout.removeLayoutItem(min_label)
                QgsProject.instance().removeMapLayer(layer1.id())

                legend.model().rootGroup().removeLayer(project.mapLayersByName('BR_Pais_2021')[0])
                

                legend.setAutoUpdateModel(False)
                legend.adjustBoxSize()
                layout.refresh()
            
            break
        break
                
def create_maps_01_degree_grid():
    #list_of_folders=os.listdir(os.pardir()+'\Maps\Rasters')

    path=r'C:/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/'

    list_of_folders=os.listdir(path)

    #list_of_folders.remove('Teste')
    #list_of_folders.remove('SARIMA')

    #list_of_folders.remove('LSTM')

    #list_of_folders.remove('HoltWinters')

    #list_of_folders.remove('Actual')

    #list_of_folders=['SARIMA']
    for folder_name in list_of_folders:

        #print(folder_name)

        os.makedirs(r'C:/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/'+folder_name+'/StateLimit/',exist_ok=True)
        os.makedirs(r'C:/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/'+folder_name+'/Images/',exist_ok=True)
        
        list_of_files=os.listdir(path+folder_name)

        
        #list_of_files=list_of_files[260:286]
        #list_of_files=list_of_files[339:340]
        #list_of_files=['2020_Average.tif']

        for file_name in list_of_files:

            if(file_name.endswith('.tif')==True):

                mask="C:/Users/rickg/Desktop/Solar Radiation Project/Maps/BR_Pais_2021/BR_Pais_2021.shp"

                #print(file_name)
                output_path='C:/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/'+folder_name+'/StateLimit/'+file_name

                processing.run("gdal:cliprasterbymasklayer", {'INPUT':'C:/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/'+folder_name+'/'+file_name,
                                                          'MASK':mask,'SOURCE_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),'TARGET_EXTENT':'-73.9904679169921877,-33.7507685263671959 ,-28.8491679169921866,5.2711314736328063 [EPSG:4326]',

                'NODATA':0,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,'KEEP_RESOLUTION':True,'SET_RESOLUTION':True,'X_RESOLUTION':0.05,'Y_RESOLUTION':0.05,'MULTITHREADING':True,

                'OPTIONS':'','DATA_TYPE':0,'EXTRA':'',

                'OUTPUT':output_path})

                layer=iface.addRasterLayer(output_path,file_name.removesuffix('.tif'))
                #layer = QgsProject.instance().mapLayersByName("saidaTeste")[0]
                pseudocolor_styling(layer, colormap="Turbo", nclass=255)

                img=QImage(QSize(800,800),QImage.Format_ARGB32_Premultiplied)
            
                color=QColor(255,255,255,255)
                img.fill(color.rgba())

                provider = layer.dataProvider()
                extent = layer.extent()
                stats = provider.bandStatistics(1, QgsRasterBandStats.All,extent, 0)
                #minimum = stats.minimumValue
                #maximum = stats.maximumValue

                minimum=2
                maximum=10
                

                project=QgsProject.instance()
                manager=project.layoutManager()
                
                
                layout_list=manager.printLayouts()
                layout= layout_list[0]

                max_label = QgsLayoutItemLabel(layout)  
                str_max=f'{maximum:.1f}'


                max_label.setText(str_max)
                max_label.setFont(QFont("Arial", 12))
                layout.addLayoutItem(max_label)
                max_label.attemptMove(QgsLayoutPoint(245,56))


                min_label = QgsLayoutItemLabel(layout)  
                str_min=f'{minimum:.1f}'
                min_label.setText(str_min)
                min_label.setFont(QFont("Arial", 12))
                layout.addLayoutItem(min_label)
                min_label.attemptMove(QgsLayoutPoint(245,139))

                units_label= QgsLayoutItemLabel(layout) 
                str_units='kWh/m\u00b2/day'

                units_label.setText(str_units)

                units_label.setFont(QFont("Arial", 12))

                layout.addLayoutItem(units_label)

                units_label.attemptMove(QgsLayoutPoint(245,47))
                
            
                month_number=(file_name[5:7])

                if month_number=='01':
                    month_name='Jan'
                elif month_number=='02':
                    month_name='Feb'
                elif month_number=='03':
                    month_name='Mar'
                elif month_number=='04':
                    month_name='Apr'
                elif month_number=='05':
                    month_name='May'
                elif month_number=='06':
                    month_name='Jun'
                elif month_number=='07':
                    month_name='Jul'
                elif month_number=='08':
                    month_name='Aug'
                elif month_number=='09':
                    month_name='Sep'
                elif month_number=='10':
                    month_name='Oct'
                elif month_number=='11':
                    month_name='Nov'
                elif month_number=='12':
                    month_name='Dec'
                else:
                    month_name=' '

             

                
                date_label = QgsLayoutItemLabel(layout)  
                str_date=month_name
                




                #date_label.setText(str_date)
                #date_label.setFont(QFont("Arial", 20))
                #layout.addLayoutItem(date_label)
                #date_label.attemptMove(QgsLayoutPoint(70,160))
    

                str_date=''
                
                map=QgsLayoutItemMap(layout)
                map.setRect(20,20,20,20)

                ms=QgsMapSettings()
                ms.setBackgroundColor(color)
                layer1=project.mapLayersByName(file_name.removesuffix('.tif'))[0]
                layer2=project.mapLayersByName('BR_Pais_2021')[0]
                ms.setLayers([layer2,layer1])
                rect=QgsRectangle(ms.fullExtent())
                rect.scale(1.1)
                ms.setExtent(rect)
                layout.addLayoutItem(map)
                
                manager.addLayout(layout)
                

                layer_list =names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
                

                for layer_name in layer_list:

                    while layer_list.count(layer_name)>1:

                        QgsProject.instance().removeMapLayer(layer_name)
                
            
                legend=QgsLayoutItemLegend(layout)
                
                layerTree=iface.layerTreeCanvasBridge().rootGroup()
                layerTree.insertChildNode(1,QgsLayerTreeLayer(layer1))
                layerTree.insertChildNode(0,QgsLayerTreeLayer(layer2))
        

                legend.model().setRootGroup(layerTree)

                layout.addLayoutItem(map)
            
                legend.setAutoUpdateModel(True)

                exporter=QgsLayoutExporter(layout)
               
                Image_path='C:/Users/rickg/Desktop/Solar Radiation Project/Heatmaps/Rasters/'+folder_name+'/Images/'+file_name.removesuffix('.tif')+'.png'

                exporter.exportToImage(Image_path,QgsLayoutExporter.ImageExportSettings())

                layout.removeLayoutItem(max_label)
                layout.removeLayoutItem(date_label)
                layout.removeLayoutItem(min_label)
                QgsProject.instance().removeMapLayer(layer1)

                legend.model().rootGroup().removeLayer(project.mapLayersByName('BR_Pais_2021')[0])
                
                legend.setAutoUpdateModel(False)
                legend.adjustBoxSize()
                layout.refresh()
            
              
#create_maps()

create_maps_01_degree_grid()




























