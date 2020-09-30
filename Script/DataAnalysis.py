import pandas as pd
import os
import datetime
import matplotlib as mlp
import matplotlib.pyplot as plot
import numpy as np
from Analytics_Library import Youtube_Analytics_Library as YAL
import geopandas as gpd
import imageio


ListOfCountry=["JPN","RUS","KOR","MEX","CAN","DEU","FRA","GBR","IND","USA"]
ListOfIntervalMinute=[30,20,10,4,2]
ListOfTimeZone=["Local","UTC"]
ActivatePloting=False
ForceRenderingData=False
# LocalToUTCTime="UTC"






def PlotPublicationOfVideoByTimeMAP(ListOfCountry,IntervalMinute,ActivatePloting,ForceRenderingData,LocalToUTCTime):

    PathToDataOUT_JPG=os.path.join("Script","Data","Data_OUT","JPG",LocalToUTCTime,"")
    PathToDataOUT_GIF=os.path.join("Script","Data","Data_OUT","GIF",LocalToUTCTime,"")
    PathToGeoJSONInputData=os.path.join("Script","Data","Data_IN","GeoJSON","ref-countries-2020-60m.geojson","CNTR_RG_60M_2020_3857.geojson")
    world = gpd.read_file(PathToGeoJSONInputData)
    world=world[world.NAME_ENGL!="Antarctica"]

    DataDf=YAL.CreateAndOrPlotTimeVsNumberOfVideoDF(ListOfCountry,IntervalMinute,ActivatePloting,ForceRenderingData,LocalToUTCTime)

    DataDf.set_index("Label",inplace=True)

    MaxValueOfTheTimeEC=max(DataDf.max())
        
    DataDf=DataDf.transpose()

    for i in DataDf.index:
        DataDf.loc[i,"ISO3_CODE"]=i.split()[-1]

    DataWorld=world.merge(DataDf, on="ISO3_CODE")
    
    images = []
    for Time in sorted(DataDf):
        if Time!="Label" and Time!="ISO3_CODE":

            # MaxValueOfTheTime=DataDf[Time].max()
            # DataDf[index]=DataDf[index]/MaxValueOfTheTime


            Title="Number of Video Trending in the world published at: "+LocalToUTCTime+" Time "+Time
            WorldBase=world.plot(color="lightgrey")
            DataWorld.plot(column=Time,ax=WorldBase, legend=True,vmin=0,vmax=MaxValueOfTheTimeEC,cmap='OrRd',legend_kwds={'label': "Number of Video published By Country",'orientation': "horizontal"})
            
            plot.title(Title)
            plot.gca().axes.get_yaxis().set_visible(False)
            plot.gca().axes.get_xaxis().set_visible(False)
            # plot.show()
            
            PathToTheOUTDataFile=os.path.join(PathToDataOUT_JPG,str(Time)+".jpg")

            plot.savefig(PathToTheOUTDataFile)
            plot.close()
            images.append(imageio.imread(PathToTheOUTDataFile))




    if LocalToUTCTime=="Local": 
        PathToTheOUTDataFile=os.path.join(PathToDataOUT_GIF,"Number of Video Trending in the world "+"Local Time "+str(IntervalMinute)+".gif")   
    else:
        PathToTheOUTDataFile=os.path.join(PathToDataOUT_GIF,"Number of Video Trending in the world "+"UTC Time "+str(IntervalMinute)+".gif")   
    imageio.mimsave(PathToTheOUTDataFile, images,duration=0.5)


for IntervalMinute in ListOfIntervalMinute:
    for TimeZone in ListOfTimeZone:
        PlotPublicationOfVideoByTimeMAP(ListOfCountry,IntervalMinute,ActivatePloting,ForceRenderingData,TimeZone)
    print("Interval: "+str(IntervalMinute)+" done !")





#time normalise for every country
# for index in sorted(DataDf):
    
#     MaxValueOfTheTime=DataDf[index].max()
#     DataDf[index]=DataDf[index]/MaxValueOfTheTime

# for i in sorted(DataDf):
#     if i !="Label":
#         DataDf.loc[i,"ISO3_CODE"]=i.split()[-1]



# time normalise to every country 
# for index in sorted(DataDf):
#     if index !="Label":
#         MaxValueOfTheTime=DataDf[index].max()
#         DataDf[index]=DataDf[index]/MaxValueOfTheTime


# print(world[world.iso_a3=="FRA"])

#  ce que l'on veut voir c'est le le nombre de video publie en fonction du temps par pays



# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# print(world.head())

# world.plot()

# plot.show()
# #arriver a un graph monde du nombre de video en fonction du temps de publication 
# puis par jour et par heure de publication puis par type de video et par temps 
# et jour et optionnelement temps par rapport au jour de l'année

#Creer un elif si pays dans la liste n'existe pas alors loader le csv correspondant au temps et et faire un rendering des données de ce pays et les append au dataframe des autres pays
# PathToInputData=os.path.join("Script","Data","Data_IN","GeoJSON","countries-hires","countries-hires.JSON")
# earthquake = gpd.read_file(PathToInputData)
# print(earthquake.head())

#temps utc temps universel ce qui expliue pourquoi toute les couleurs sont en meme temps

# Script\Data\Data_IN\GeoJSON\ref-countries-2020-60m.geojson\CNTR_RG_60M_2020_3857.geojson
#Script\Data\Data_IN\GeoJSON\ref-countries-2020-60m.geojson\CNTR_RG_60M_2020_4326.geojson
#,"KR" "JP" ,"MX" ,"RU" 