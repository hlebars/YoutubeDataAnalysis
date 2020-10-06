import pandas as pd
import os
import datetime
import matplotlib as mlp
import matplotlib.pyplot as plot
import numpy as np
from Analytics_Library import Youtube_Analytics_Library as YAL
import geopandas as gpd
import imageio
import time


def functionatimer():

    ListOfCountry=["JPN","RUS","KOR","MEX","CAN","DEU","FRA","GBR","IND","USA"]
    ListOfIntervalMinute=[30,20,10,4,2]
    ListOfTimeZone=["Local","UTC"]
    ActivatePloting=False
    ForceRenderingData=True
    TotalTimeGIF=10
    WeekDays = ["Monday"]#,"Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    for DayOfTheWeek in WeekDays:
        for IntervalMinute in ListOfIntervalMinute:
            for TimeZone in ListOfTimeZone:
                YAL.PlotPublicationOfVideoByTimeMAP(ListOfCountry,IntervalMinute,ActivatePloting,ForceRenderingData,TimeZone,TotalTimeGIF,DayOfTheWeek)
            print("Interval: "+str(IntervalMinute)+" done !")
        print(DayOfTheWeek+" done !")


start = time.time()

functionatimer()

end = time.time()

print(end - start)















# a retravailler
# def ChooseTypeOfDataToBePlotted(DataToBePLotted,ListOfIntervalMinute,ActivatePloting,ForceRenderingData):

#     ListOfCountry=["JPN","RUS","KOR","MEX","CAN","DEU","FRA","GBR","IND","USA"]
#     ListOfTimeZone=["Local","UTC"]

#     if DataToBePLotted=="WorldEveryTimeZoneEveryInterval":
#         for IntervalMinute in ListOfIntervalMinute:
#             for TimeZone in ListOfTimeZone:
#                 PlotPublicationOfVideoByTimeMAP(ListOfCountry,IntervalMinute,ActivatePloting,ForceRenderingData,TimeZone)
#             print("Interval: "+str(IntervalMinute)+" done !")

#     elif DataToBePLotted=="WorldUTCOneInterval":
#         TimeZone=ListOfTimeZone[1]
#         PlotPublicationOfVideoByTimeMAP(ListOfCountry,ListOfIntervalMinute,ActivatePloting,ForceRenderingData,TimeZone)

#     elif DataToBePLotted=="WorldLocalOneInterval":
#         TimeZone=ListOfTimeZone[0]
#         PlotPublicationOfVideoByTimeMAP(ListOfCountry,ListOfIntervalMinute,ActivatePloting,ForceRenderingData,TimeZone)

#     elif DataToBePLotted=="WorldEveryTimeZoneOneInterval":
#         for TimeZone in ListOfTimeZone:
#                 PlotPublicationOfVideoByTimeMAP(ListOfCountry,ListOfIntervalMinute,ActivatePloting,ForceRenderingData,TimeZone)

#     elif DataToBePLotted=="WorldUTCEveryInterval":
#         TimeZone=ListOfTimeZone[1]
#         for IntervalMinute in ListOfIntervalMinute:
#                 PlotPublicationOfVideoByTimeMAP(ListOfCountry,IntervalMinute,ActivatePloting,ForceRenderingData,TimeZone)

#     elif DataToBePLotted=="WorldLocalEveryInterval":
#         TimeZone=ListOfTimeZone[0]
#         for IntervalMinute in ListOfIntervalMinute:
#                 PlotPublicationOfVideoByTimeMAP(ListOfCountry,IntervalMinute,ActivatePloting,ForceRenderingData,TimeZone)
# ChooseTypeOfDataToBePlotted(ListOfPlottedChoice[0],ListOfIntervalMinute,ActivatePloting,ForceRenderingData)

# Insert the polygon into 'geometry' -column at index 0
# In [22]: newdata.loc[0, 'geometry'] = poly


# world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
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