import pandas as pd
import os
import datetime
import matplotlib as mlp
import matplotlib.pyplot as plot
import numpy as np
from Analytics_Library import Youtube_Analytics_Library as YAL
# import geopandas as gpd

#arriver a un graph monde du nombre de video en fonction du temps de publication 
# puis par jour et par heure de publication puis par type de video et par temps 
# et jour et optionnelement temps par rapport au jour de l'année

#Creer un elif si pays dans la liste n'existe pas alors loader le csv correspondant au temps et et faire un rendering des données de ce pays et les append au dataframe des autres pays
# PathToInputData=os.path.join("Script","Data","Data_IN","GeoJSON","countries-hires","countries-hires.JSON")
# earthquake = gpd.read_file(PathToInputData)
# print(earthquake.head())


# Script\Data\Data_IN\GeoJSON\ref-countries-2020-60m.geojson\CNTR_RG_60M_2020_3857.geojson
#Script\Data\Data_IN\GeoJSON\ref-countries-2020-60m.geojson\CNTR_RG_60M_2020_4326.geojson
#,"KR" "JP" ,"MX" ,"RU" 
ListOfCountry=["JP","RU","KR","MX","CA","DE","FR","GB","IN","US"]
IntervalMinute=30
ActivatePloting=True
ForceRenderingData=True

YAL.CreateAndOrPlotTimeVsNumberOfVideoDF(ListOfCountry,IntervalMinute,ActivatePloting,ForceRenderingData)