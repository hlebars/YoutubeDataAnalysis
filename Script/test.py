import pandas as pd
import datetime
import numpy as np
import os
import re

import pytz
print(pytz.country_timezones('JP'))
# Hours=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
# Hours=pd.date_range('17:30:00', '21:00:00',freq='15T').strftime('%H:%M').tolist()
# pd.to_datetime(Hours,format='%H:%M')
# print(Hours)
Hours=pd.date_range('00:00:00', '23:59:00',freq=str(30)+'T').time
IntervalMinute=30
HoursForLabels=pd.date_range('00:00:00', '23:59:00',freq=str(IntervalMinute)+'T').strftime('%H:%M').tolist()
    
df_NumberHours=pd.DataFrame(0,index=Hours,columns=["Number","Label"])
df_NumberHours["Label"]=HoursForLabels

# print(df_NumberHours["Label"].head(3))

Country="MEX"
PathToInputData=os.path.join("Script","Data","Data_IN","Youtube_CSV__And_JSON",Country+"videos.csv")

    


df=pd.read_csv(PathToInputData,engine="python") 



df=df.drop(columns=['video_id','title','channel_title','category_id','tags','thumbnail_link','comments_disabled','ratings_disabled','video_error_or_removed','description'])

#get the plublish time and put in the column publish time
df['publish_time'] = pd.to_datetime(df['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
print(df['publish_time'])


# ["JPN",
LocalTime=True

if LocalTime==True:
    if Country=="USA":
        df['publish_time']=pd.DatetimeIndex(df['publish_time']).tz_localize('utc').tz_convert('US/Central')
    elif Country=="MEX":
        df['publish_time']=pd.DatetimeIndex(df['publish_time']).tz_localize('utc').tz_convert('America/Mexico_City')
    elif Country=="FRA":
        df['publish_time']=pd.DatetimeIndex(df['publish_time']).tz_localize('utc').tz_convert('Europe/Paris')
    elif Country=="DEU":
        df['publish_time']=pd.DatetimeIndex(df['publish_time']).tz_localize('utc').tz_convert('Europe/Berlin')
    elif Country=="GBR":
        df['publish_time']=pd.DatetimeIndex(df['publish_time']).tz_localize('utc').tz_convert('Europe/London')
    elif Country=="IND":
        df['publish_time']=pd.DatetimeIndex(df['publish_time']).tz_localize('utc').tz_convert('Asia/Kolkata')
    elif Country=="CAN":
        df['publish_time']=pd.DatetimeIndex(df['publish_time']).tz_localize('utc').tz_convert('America/Winnipeg')
    elif Country=="KOR":
        df['publish_time']=pd.DatetimeIndex(df['publish_time']).tz_localize('utc').tz_convert('Asia/Seoul')
    elif Country=="RUS":
        df['publish_time']=pd.DatetimeIndex(df['publish_time']).tz_localize('utc').tz_convert('Asia/Krasnoyarsk')
    elif Country=="JPN":
        df['publish_time']=pd.DatetimeIndex(df['publish_time']).tz_localize('utc').tz_convert('Asia/Tokyo')

        

print(df['publish_time'])
df.insert(5, 'publish_date', df['publish_time'].dt.date)

#convert them into datetime time 
df['publish_time'] = df['publish_time'].dt.time
df['publish_time'] = df['publish_time']



#convert the trending date string into a datetime format
df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m')

#Put the trending date in the same format before soustracting them to 
# get the time before trending
df["trending_date"]=df["trending_date"].values.astype('datetime64[D]')
df["publish_date"]=df["publish_date"].values.astype('datetime64[D]')

# get the time before trending
df["Time_Before_Trending"]=df["trending_date"].sub(df["publish_date"],axis=0)



# count the number of video publish in the same time 
Df_TimeAndNumberOfPublication=df['publish_time'].value_counts()
Df_TimeAndNumberOfPublication.sort_values(0,ascending=True)

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