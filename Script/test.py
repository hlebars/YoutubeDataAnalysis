import pandas as pd
import datetime
import numpy as np
import os
import re
# Hours=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
# Hours=pd.date_range('17:30:00', '21:00:00',freq='15T').strftime('%H:%M').tolist()
# pd.to_datetime(Hours,format='%H:%M')
# print(Hours)
Hours=pd.date_range('00:00:00', '23:59:00',freq=str(30)+'T').time
IntervalMinute=30
HoursForLabels=pd.date_range('00:00:00', '23:59:00',freq=str(IntervalMinute)+'T').strftime('%H:%M').tolist()
    
df_NumberHours=pd.DataFrame(0,index=Hours,columns=["Number","Label"])
df_NumberHours["Label"]=HoursForLabels

print(df_NumberHours["Label"].head(3))

Country="MX"
PathToInputData=os.path.join("Script","Data","Data_IN","Youtube_CSV__And_JSON",Country+"videos.csv")

    

try:
    df=pd.read_csv(PathToInputData,delimiter=",") 
except Exception  as a:
    ErrorLine=str(a)
    ListOfNumberInTheError=map(int, re.findall(r'\d+', ErrorLine))
    print(str(a))


    a_file = open(PathToInputData, "r",encoding='utf-8')
    

    lines = a_file.readlines()
    a_file.close()

    del lines[ListOfNumberInTheError[2]]
    


    new_file = open("sample.txt", "w+")
    

    for line in lines:
        new_file.write(line)

    new_file.close()

df_NumberHours.index = df_NumberHours.index.strftime('%H:%M')
df_NumberHours.index=datetime.time(df_NumberHours.index.hour,df_NumberHours.index.minute)
# print(datetime.time(hour=,minute=-30,second=40))
print(df_NumberHours.tail(5))
#40562 via fonction via tableau 40723 
#il faut que les valeur centrer entre 16:30 avec 15 min a gauche 15 min a droite soit increment/2 


print(df_NumberHours["Number Of Video"].sum())
#et si les minutes sont egales a zero alors il faut retirer une heure
# 
# df_NumberHours.plot(x="Label",y=NumberOfVideoTrendingByCountry, kind='bar')

#         #title of the plot
#         plot.title("Number of Video Trending in " +Country +" by publication time")

#         #title of the x axis of the plot
#         plot.xlabel('Time')

#         #title of y axis of the plot
#         plot.ylabel('Number of Video Trending')

#         #show the graph
#         plot.show()