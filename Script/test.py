import pandas as pd
import datetime
import numpy as np
import os
import re
import matplotlib.pyplot as plot

import pytz
# @timeit (repeat=3,number=10)
def testtemps():
    print(pytz.country_timezones('JP'))
    # Hours=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    # Hours=pd.date_range('17:30:00', '21:00:00',freq='15T').strftime('%H:%M').tolist()
    # pd.to_datetime(Hours,format='%H:%M')
    # print(Hours)
    Hours=pd.date_range('00:00:00', '23:59:00',freq=str(30)+'T').time

        
    df_NumberHours=pd.DataFrame(0,index=Hours,columns=["Number","Label"])
    # df_NumberHours["Label"]=HoursForLabels

    # print(df_NumberHours["Label"].head(3))

    Country="FRA"
    PathToInputData=os.path.join("Script","Data","Data_IN","Youtube_CSV__And_JSON",Country+"videos.csv")

        


    df=pd.read_csv(PathToInputData)#,engine="python") 

    #'video_id','title',

    df=df.drop(columns=['channel_title','category_id','tags','thumbnail_link','comments_disabled','ratings_disabled','video_error_or_removed','description'])

    #get the plublish time and put in the column publish time
    df['publish_time'] = pd.to_datetime(df['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
    # print(df['publish_time'])



    # ["JPN",
    LocalTime=False

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

            

    # filtertime=(df[df.index.time > datetime.time(12),] & df[df.index.time < datetime.time(13)])

   #Converting LOcal time to UTC time if LocalToUTCTime==True
    # df=ConvertLocalTimeToUTC(df,Country,LocalToUTCTime)
    print(df["video_id"].nunique())
    df = df.drop_duplicates(subset = 'video_id', keep = 'first')
    print(df)
    df.set_index( df['publish_time'], inplace=True)
    # df_FiltResult=
    
    # df=df.groupby([df.index.day_name()],)["views"].count()#,df.index.hour

    # df.plot(kind="bar")
    # plot.show()


    # filt=(df.title.str.find(sub)!=-1)
    # filt=None
    # df_FiltResult=df["title"].resample("D")
    #juste le filtre 
    # df_FiltResultsample=df["title"][filt].resample("M").count()
    # totalite de la periode 
    
    # sub=""
    #fictionnary of group by possibilities
    DicoGroubyPossibility={
        "Y":df.index.year,
        "M":df.index.month,
        "W":df.index.week,
        "D":df.index.day,
        "h":df.index.hour,
        "m":df.index.minute,
        "s":df.index.second,
        "time":df.index.time,
        "date":df.index.date,
        "WeekDay":df.index.weekday,
        }
    ListOfDateAndTime=["WeekDay"]#,"h"]#,"M","D"]

    #test if the list contain more than one parameter for grouby if it is true then it will group by by the composant o the list
    if len(ListOfDateAndTime)>1:

        
        
        
        #Create empty list for date and time classification
        ListOfDate=[]
        ListOfTime=[]

        #Classify Date and time in the corresponding list in fucntion of it is in upper case or not upper=date  low=time
        for i in ListOfDateAndTime:
            if i.isupper() or i=="date" or i=="WeekDay":
                ListOfDate.append(i)
            else:
                ListOfTime.append(i)

            #get the list of all indexes  
            SegmentOfDateOrTime=DicoGroubyPossibility[i].astype(str).tolist()

            # and add a zero in front of the index string to have 00 h and not 0h or days etc 
            for DateOrTime in range(len(SegmentOfDateOrTime)):
                if len(SegmentOfDateOrTime[DateOrTime])==1:
                    SegmentOfDateOrTime[DateOrTime]=str(0)+SegmentOfDateOrTime[DateOrTime]
            
            #Place it back in the columns of the date or time correspondant like Y(Year) or h(hour) to get a series grouby with different name
            df.loc[:,i]=SegmentOfDateOrTime


        #grouby in function of the entry in the list of date and time   
        df=df.groupby(ListOfDateAndTime)["views"].count()

        #Go from pd series to dataframe with another index
        df=df.to_frame(name = 'Number Of Video Trending').reset_index()
        
        if "WeekDay" in ListOfDateAndTime:
            dayOfWeek={"00":'Monday', "01":'Tuesday', "02":'Wednesday', "03":'Thursday', "04":'Friday', "05":'Saturday', "06":'Sunday'}
            df['WeekDay'] = df['WeekDay'].map(dayOfWeek)

        #create the columns time in function of the date and time in listoftime
        if len(ListOfDate)>0 and len(ListOfTime)>0:
            df['Time'] = df[ListOfDate].astype(str).agg('-'.join, axis=1)+" "+df[ListOfTime].astype(str).agg(':'.join, axis=1)
        elif len(ListOfDate)>0 and len(ListOfTime)==0:
            df['Time'] = df[ListOfDate].astype(str).agg('-'.join, axis=1)
        elif len(ListOfDate)==0 and len(ListOfTime)>0:
            df['Time'] = df[ListOfTime].astype(str).agg(':'.join, axis=1)
        
        #Put the column Time in index
        df.set_index( df['Time'], inplace=True)

        #add the column Time to ListOfDateAndTime before dropping every columns of ListOfDateAndTime to have a nice dataframe with just the number
        #of videos trending and the time index
        ListOfDateAndTime.append('Time')
        df=df.drop(ListOfDateAndTime,axis=1)

    else:
        #if their is only one thing in the list


        #get the list of all indexes  
        SegmentOfDateOrTime=DicoGroubyPossibility[ListOfDateAndTime[0]].astype(str).tolist()

        # and add a zero in front of the index string to have 00 h and not 0h or days etc 
        for DateOrTime in range(len(SegmentOfDateOrTime)):
            if len(SegmentOfDateOrTime[DateOrTime])==1:
                SegmentOfDateOrTime[DateOrTime]=str(0)+SegmentOfDateOrTime[DateOrTime]

        #grouby in function of the entry in the list of index  
        df=df.groupby(SegmentOfDateOrTime)["views"].count()

        #Create a dataframe with the grouby serie
        df=df.to_frame(name = 'Number Of Video Trending')#.reset_index()

        # Rename the dataframe index in Time
        df.index=df.index.rename('Time')

    
    
    # df1.columns=ListOfDateAndTime.split("_")
    # df1=df1.to_frame(name = 'count').reset_index()
    
    # df=df.loc[:,ListOfTime].join()
 




    # df=df.resample("60T").views.count()#, df.index.minute df.index.hour
    # df=df.groupby(pd.Grouper(key='publish_time',freq='30T')).views.count()#, df.index.minute df.index.hour
    # df=df.groupby([df.index.second]).views.count()#df.index.hour,
    # df=df.groupby([df.index.hour,df.index.minute,df.index.second]).views.count()
    # df=df.groupby([df.index.year,df.index.month,df.index.day,df.index.hour,df.index.minute,df.index.second]).views.count()
    # print(df)
    df.plot(kind="bar")

    plot.show()
    
    # df_FiltResult=df["views"].resample("H").count()
    # print(df_FiltResult)
    FindText=" !"
    filtre="Minute"
    NumberOfVideoTrendingByCountry="Number Of Video "+Country
    DicoResampleAndGraph={"Year":("Y","%y"),"Month":("M","%y/%m"),"Day":("D","%y/%m/%d"),"Hour":("H","%y/%m/%d %H"),"Minute":("m","%y/%m/%d %H:%m")}
    # filt=(df.index.year==2017) | (df.index.year==2018)
    filt=(df.index.month==12) | (df.index.day==25)
    df=df[filt]
    if FindText!="":
        df["result"]=df["title"].apply(lambda x: 1 if x.find(FindText)!=-1 else 0)
        df_FiltResult=df["result"].resample(DicoResampleAndGraph[filtre][0]).sum()
        
    else:
        df_FiltResult=df["views"].resample(DicoResampleAndGraph[filtre][0]).count()
    df_FiltResult.columns=["Label",NumberOfVideoTrendingByCountry]
    df_FiltResult.index=df_FiltResult.index.strftime(DicoResampleAndGraph[filtre][1])#-%d

    # df_FiltResult.index=df_FiltResult.index.strftime("%V")#-%d
    # print(df_FiltResult.index)
    # filt=(df.title.str.find(sub)!=-1)
    # df_FiltResult=df["title"][filt].resample("W").count()
    # df_FiltResult=df["title"].resample("W").count()
    # df_FiltResult.index=df_FiltResult.index.strftime("%V")#-%d
    print(df_FiltResult)
    
       # if df
    # df_FiltResult.loc["value"]=df["title"][filt].count()
    # df.index=pd.to_datetime(df.index,format='%Y-%m-%d')
    # df_FiltResultsample.plot(y=0,kind="bar")
    df_FiltResult.plot(y=0,kind="bar")
    plot.show()
    NumberOfVideoTrendingByCountry="Number Of Video "+Country
    Months=["January","February","March","April","May","June","July","August","October","November","December"]
    Years=[]
    for Year in range(min(df.publish_time.dt.year),max(df.publish_time.dt.year)+1):
        Years.append(Year)
    df_VideoCountForDayOfTheWeek=pd.DataFrame(0,index=Years,columns=[NumberOfVideoTrendingByCountry])
    print(min(df.publish_time.dt.year))
    print(max(df.publish_time.dt.year))
    sub=" Noël "
    for Year in Years:
        filtervalue=(df.publish_time.dt.year==Year) & (df.title.str.find(sub)!=-1)
        df_VideoCountForDayOfTheWeek.loc[Year,NumberOfVideoTrendingByCountry]=max(df[filtervalue].count())
    print(df_VideoCountForDayOfTheWeek)
    WeekDays=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    df_VideoCountForDayOfTheWeek=pd.DataFrame(0,index=WeekDays,columns=["Number Of Videos"])
    for WeekDay in WeekDays:
        df_VideoCountForDayOfTheWeek.loc[WeekDay,"Number Of Videos"]=max(df[df.publish_time.dt.day_name()==WeekDay].count())
    print(df_VideoCountForDayOfTheWeek)

    df_VideoCountForDayOfTheWeek.plot(y="Number Of Videos",kind="bar")
    plot.show()
    #insert publish date in the corresponding columns
    df.insert(5, 'publish_date', df['publish_time'].dt.date)

    # convert them into datetime time 
    df['publish_time'] = df['publish_time'].dt.time

    #convert the trending date string into a datetime format
    df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m')

    #Put the trending date in the same format before soustracting them to 
    # get the time before trending
    df["trending_date"]=df["trending_date"].values.astype('datetime64[D]')
    df["publish_date"]=df["publish_date"].values.astype('datetime64[D]')



    # functionning from 1 s tp 24h 
    IntervalMinute=1/60

    if IntervalMinute==1/60:

        
        counttotal=0
        countindex=0
        
        HoursForLabels=pd.date_range('00:00:00', '23:59:59',freq=str(IntervalMinute)+'T').strftime('%H:%M:%S').tolist()

        NumberOfVideoTrendingByCountry="Number Of Video "+Country
        df_NumberHours=pd.DataFrame(0,index=HoursForLabels,columns=["Label",NumberOfVideoTrendingByCountry])
        df_NumberHours["Label"]=HoursForLabels



        for index in range(len(HoursForLabels)):
            if index<(len(HoursForLabels)-1):
                df_NumberHours.loc[HoursForLabels[index],NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[index],end_time=HoursForLabels[index+1],include_end=False).count()
            else:
                df_NumberHours.loc[HoursForLabels[index],NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[index],end_time="23:59:59",include_start=True,include_end=True).count()

    else:
        #insert publish date in the corresponding columns
        df.insert(5, 'publish_date', df['publish_time'].dt.date)

        # convert them into datetime time 
        df['publish_time'] = df['publish_time'].dt.time

        #convert the trending date string into a datetime format
        df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m')

        #Put the trending date in the same format before soustracting them to 
        # get the time before trending
        df["trending_date"]=df["trending_date"].values.astype('datetime64[D]')
        df["publish_date"]=df["publish_date"].values.astype('datetime64[D]')


        #Get all time data in function of the day of the week if DayOfTheWeek=="All" skip this to have all day of the dataframe
        df["weekday_publish_date"] = df["publish_date"].dt.day_name()
        # df=GetDFFromWeekDay(df,DayOfTheWeek)
        



        # get the time before trending
        df["Time_Before_Trending"]=df["trending_date"].sub(df["publish_date"],axis=0)



        # count the number of video publish in the same time 
        df_NumberHours=df['publish_time'].value_counts()
        df_NumberHours.sort_values(0,ascending=True)
        # df_NumberHours.index=sorted(df_NumberHours.index,key=)
        df_NumberHours=df_NumberHours.sort_index()
        HoursForLabels=pd.date_range('00:00:00', '23:59:59',freq=str(IntervalMinute)+'T').strftime('%H:%M:%S').tolist()
        for time in HoursForLabels:
            if time not in df_NumberHours.index:
                df_NumberHours.set_value(time,0)
        df_NumberHours.index=df_NumberHours.index.time
        #Supres the last row of the df for interval and video publish in the interval 
        # because it is 23:59:59 but is empty cause every thing goes to 00:00:00
        df_NumberHours.drop(df_NumberHours.tail(1).index,inplace=True)

    # print(df_NumberHours)
    # print(len(df))
    # print(df_NumberHours[NumberOfVideoTrendingByCountry].sum())


    # df_NumberHours.plot(y=NumberOfVideoTrendingByCountry,kind="bar")
    # plot.show()

    ##############################################################################################################################
    # x=2
    # print(df)
    # print(df["views"].between_time(start_time="00:00:00",end_time="23:59:59").count())
    # print(df["views"].count())
    # print(len(df["views"]))

    # df_NumberHours.loc["23:59",["Label",NumberOfVideoTrendingByCountry]] = "23:59",0
    # print(df_NumberHours)
    # for index in range(len(HoursForLabels)+1):
    #     if index<(len(HoursForLabels)-1):
    #         # if HoursForLabels[index]=="23:30":
    #         #     x=1
    #         df_NumberHours.loc[HoursForLabels[index],NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[index],end_time=HoursForLabels[index+1],include_end=False).count()
    #     elif index==(len(HoursForLabels)-1):
    #         df_NumberHours.loc[HoursForLabels[-1],NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[index-1],end_time=HoursForLabels[-1],include_end=False).count()
    #     else:
    #         df_NumberHours.loc["23:59",NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[-1],end_time="23:59:59",include_start=True,include_end=True).count()


    # df_NumberHours.set_index("Label",inplace=True)


    # for index in range(len(HoursForLabels)):
    #     if index<(len(HoursForLabels)-1):
    #         df_NumberHours.loc[HoursForLabels[index],NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[index],end_time=HoursForLabels[index+1],include_end=False).count()
    #     elif index==len(HoursForLabels)-1:
    #         df_NumberHours.loc[HoursForLabels[-1],NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[-1],end_time="23:59:59",include_end=True).count()
            # df_NumberHours.loc["23:59",NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[-1],end_time="23:59:59",include_start=True,include_end=True).count()
        # elif index==len(HoursForLabels):
            
        # print(df_NumberHours[NumberOfVideoTrendingByCountry].sum())

    #0 a 03 






def anepasutiliser():
        
    print(df_NumberHours[NumberOfVideoTrendingByCountry].sum())

    print(df_NumberHours)




    df_NumberHours=pd.DataFrame(0,index=HoursForLabels,columns=["Label",NumberOfVideoTrendingByCountry])
    df.insert(5, 'publish_date', df['publish_time'].dt.date)

    #convert them into datetime time 
    # df['publish_time'] = df['publish_time'].dt.time
    # df['publish_time'] =df['publish_time'] .astype('datetime64[D]')
    df['publish_time'] = pd.DatetimeIndex(df['publish_time'])
    df['publish_time']=df['publish_time'].dt.time
    print(df['publish_time'])
    # count the number of video publish in the same time 
    df["Count"]=df['publish_time'].value_counts()
    df.sort_values('Count',ascending=True)
    print(df)
    pd.to_timedelta(df['publish_time'])

    df.set_index(pd.to_datetime(df['publish_time'],"hh:mm:ss"), inplace=True)

    print(df.index.time)


    # df.set_index(pd.DatetimeIndex(df['publish_time']), inplace=True)


    print(df.index)






    print(df['views'].resample('T').sum())




    df['publish_time'] = df['publish_time']



    #convert the trending date string into a datetime format
    df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m')



    #Put the trending date in the same format before soustracting them to 
    # get the time before trending
    df["trending_date"]=df["trending_date"].values.astype('datetime64[D]')
    df["publish_date"]=df["publish_date"].values.astype('datetime64[D]')


    df["weekday_publish_date"] = df["publish_date"].dt.day_name()
    # df=df[df.weekday_publish_date==DayOfTheWeek]



    print(df)

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

testtemps()



def NumberOfVideoFilterByPublishTime(df,Country,IntervalMinute):

    if IntervalMinute!=1/60:
        df.set_index( df['publish_time'], inplace=True)
        counttotal=0
        countindex=0
        IntervalMinute=1/60
        HoursForLabels=pd.date_range('00:00:00', '23:59:59',freq=str(IntervalMinute)+'T').strftime('%H:%M:%S').tolist()

        NumberOfVideoTrendingByCountry="Number Of Video "+Country
        df_NumberHours=pd.DataFrame(0,index=HoursForLabels,columns=["Label",NumberOfVideoTrendingByCountry])
        df_NumberHours["Label"]=HoursForLabels



        for index in range(len(HoursForLabels)):
            if index<(len(HoursForLabels)-1):
                df_NumberHours.loc[HoursForLabels[index],NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[index],end_time=HoursForLabels[index+1],include_end=False).count()
            else:
                df_NumberHours.loc[HoursForLabels[index],NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[index],end_time="23:59:59",include_start=True,include_end=True).count()
    else:


        #insert publish date in the corresponding columns
        df.insert(5, 'publish_date', df['publish_time'].dt.date)

        # convert them into datetime time 
        df['publish_time'] = df['publish_time'].dt.time

        #convert the trending date string into a datetime format
        df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m')

        #Put the trending date in the same format before soustracting them to 
        # get the time before trending
        df["trending_date"]=df["trending_date"].values.astype('datetime64[D]')
        df["publish_date"]=df["publish_date"].values.astype('datetime64[D]')


        #Get all time data in function of the day of the week if DayOfTheWeek=="All" skip this to have all day of the dataframe
        df["weekday_publish_date"] = df["publish_date"].dt.day_name()
        df=GetDFFromWeekDay(df,DayOfTheWeek)
        



        # get the time before trending
        df["Time_Before_Trending"]=df["trending_date"].sub(df["publish_date"],axis=0)



        # count the number of video publish in the same time 
        df_NumberHours=df['publish_time'].value_counts()
        # df_NumberHours.sort_values(0,ascending=True)


        
        #Supres the last row of the df for interval and video publish in the interval 
        # because it is 23:59:59 but is empty cause every thing goes to 00:00:00
        df_NumberHours.drop(df_NumberHours.tail(1).index,inplace=True)
    

    return df_NumberHours