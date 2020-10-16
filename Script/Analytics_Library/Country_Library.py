import pandas as pd
import datetime
import matplotlib as mlp
import matplotlib.pyplot as plot
import numpy as np
import os
import geopandas as gpd
import imageio
import time


###################################################################    GeoJSON   ################################################################



################################################################### Creation of GIF ###########################################################




#################################################### Creation of Plot ########################################################################

















######################################################### All Analysis #####################################################################

def GetDFDataFromCountryCSV(Country):

    PathToInputData=os.path.join("Script","Data","Data_IN","Youtube_CSV__And_JSON",Country+"videos.csv")
    if Country=="RUS" or Country=="KOR" or Country=="MEX":
        df=pd.read_csv(PathToInputData,engine="python")
    elif Country=="JPN":
        PathToInputData=os.path.join("Script","Data","Data_IN","Youtube_CSV__And_JSON",Country+"videos - Copie.csv")
        df=pd.read_csv(PathToInputData,engine="python", error_bad_lines=False, delimiter=";")
    else:
        df=pd.read_csv(PathToInputData)
    
    return df

#################################################### Time Analysis #################################################################

def CountryGraphInFunctionOfTime(IntervalMinute,Country,ActivatePloting,LocalToUTCTime,FindText):
    """ Plot the bar graph of all the interval and the value inside them in this case the number of video trending for the time of publication """

    #get and read the csv of with youtube value
    df=GetDFDataFromCountryCSV(Country)

    df=FilterByStringInTheTitle(df,FindText)
    df = df.drop_duplicates(subset = 'video_id', keep = 'first')
    
    #all the headers of all the columns of every file
    # Df_Header=[video_id,trending_date,title,channel_title,category_id,publish_time,tags,views,likes,dislikes,comment_count,thumbnail_link,comments_disabled,ratings_disabled,video_error_or_removed,description]
    df=df.drop(columns=['channel_title','category_id','tags','thumbnail_link','comments_disabled','ratings_disabled','video_error_or_removed','description'])
    
    #get the plublish time and put in the column publish time
    df['publish_time'] = pd.to_datetime(df['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')

    df.set_index(df['publish_time'],inplace=True)
    
    #Converting LOcal time to UTC time if LocalToUTCTime==True
    df=ConvertLocalTimeToUTC(df,Country,LocalToUTCTime)

    #Create a dataframe with the number of video published in the time interval (created with IntervalMinute) from 0h to 24h  
    df_NumberHours=NumberOfVideoFilterByPublishTime(df,Country,IntervalMinute,ActivatePloting)
    
    # df_VideoCountForDayOfTheWeek=NumberOfVideoFilterByWeekDay(df,Country,ActivatePloting)

    Abbreviation=False
    ListOfDateAndTime=["date","h",]#,"W","WeekDay"]#,"m"]
    df_NumberOfVideoFilterByPublishTimeOrDate=NumberOfVideoFilterByPublishTimeOrDate(df,Country,ListOfDateAndTime,Abbreviation,ActivatePloting)
    print("Groupby")
    print(df_NumberOfVideoFilterByPublishTimeOrDate)
    # df_VideoCountForMonthOfTheYear=NumberOfVideoFilterByMonth(df)

    # df_VideoCountForYear=NumberOfVideoFilterByYear(df)

    # df_VideoCountForYearAndMonth=NumberOfVideoFilterByYearAndMonth(df,"")
    # #Get all time data in function of the day of the week if DayOfTheWeek=="All" skip this to have all day of the dataframe
    # df["weekday_publish_date"] = df["publish_date"].dt.day_name()
    # df=GetDFFromWeekDay(df,DayOfTheWeek)


    #if ActivatePloting== true plot the graph else no graph

    print("Resample")
    Resample=NumberOfVideoWithOrWithoutFilter(df,Country,"Hour",FindText,ActivatePloting)
    print(Resample)
    ListOfDateAndTime=["Y"]#,"W","WeekDay"]#,"m"]
    df_NumberOfVideoFilterByPublishTimeOrDate=NumberOfVideoFilterByPublishTimeOrDate(df,Country,ListOfDateAndTime,Abbreviation,ActivatePloting)
    
    NumberOfVideoWithOrWithoutFilter(df,Country,"Year",FindText,ActivatePloting)

    NumberOfVideoWithOrWithoutFilter(df,Country,"Month",FindText,ActivatePloting)

    NumberOfVideoWithOrWithoutFilter(df,Country,"Week",FindText,ActivatePloting)

    NumberOfVideoWithOrWithoutFilter(df,Country,"Day",FindText,ActivatePloting)

        

    return df_NumberHours

def FilterByStringInTheTitle(df,FindText):
    #it is here until their is a datetime filter
    if FindText!="":
        df.loc[:,"result"]=df.title.apply(lambda x: 1 if x.find(FindText)!=-1 else 0)#.copy()
        filt=(df.title.str.find(FindText)!=-1)
        df=df.loc[filt]#.copy()
        # filt=(df.index.year==2017) | (df.index.year==2018)
        # df=df[filt].copy()
    return df

def NumberOfVideoFilterByPublishTime(df,Country,IntervalMinute,ActivatePloting):


    df.set_index( df['publish_time'], inplace=True)
    
    
    
    HoursForLabels=pd.date_range('00:00:00', '23:59:59',freq=str(IntervalMinute)+'T').strftime('%H:%M:%S').tolist()

    NumberOfVideoTrendingByCountry="Number Of Video "+Country
    df_NumberHours=pd.DataFrame(0,index=HoursForLabels,columns=[NumberOfVideoTrendingByCountry])
    

    #if it doesn't work put this 
    # df_NumberHours=pd.DataFrame(0,index=HoursForLabels,columns=["Label",NumberOfVideoTrendingByCountry])
    # df_NumberHours["Label"]=HoursForLabels


    start = time.time()
    for index in range(len(HoursForLabels)):
        if index<(len(HoursForLabels)-1):
            df_NumberHours.loc[HoursForLabels[index],NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[index],end_time=HoursForLabels[index+1],include_end=False).count()
        else:
            df_NumberHours.loc[HoursForLabels[index],NumberOfVideoTrendingByCountry]=df["views"].between_time(start_time=HoursForLabels[index],end_time="23:59:59",include_start=True,include_end=True).count()
    end = time.time()
    # print(df_NumberHours.tail(10))

    print("Temps pour categoriser at " +str(IntervalMinute)+" is "+str(end - start))

    if ActivatePloting==True:
        Title="Number of Video Trending in " +Country +" by publication time "+"("+LocalToUTCTime+")"
        XLabel="Time"
        YLabel="Number of Video Trending"
        PlotGraph(df_NumberHours,Title,XLabel,YLabel)


    return df_NumberHours

def NumberOfVideoFilterByPublishTimeOrDate(df,Country,ListOfDateAndTime,Abbreviation,ActivatePloting):
    
    
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
    
    DicoDayOfWeek={
        "00":('Mon','Monday'), "01":('Tue','Tuesday'), "02":('Wed','Wednesday'), "03":('Thu','Thursday'),
        "04":('Fri','Friday'), "05":('Sat','Saturday'), "06":('Sun','Sunday')
        }

    DicoMonthOfTheYear = {
                "01":("Jan", "January"),"02":("Feb","February"),"03":("Mar","March"),"04":("Apr","April"),"05":("May","May"),
                "06":("Jun","June"),"07":("Jul","July"),"08":("Aug","August"),"09":("Sep","September"),"10":("Oct","October"),
                "11":("Nov","November"),"12":("Dec","December")
                }
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

        #Create the name of columns
        NumberOfVideoTrendingByCountry="Number Of Video "+Country

        #Go from pd series to dataframe with another index
        df=df.to_frame(name = NumberOfVideoTrendingByCountry).reset_index()

        #Check if Weekday was ask by the user if it is true then change number into week day name the df.index.weekday_name function is not utilised 
        # here because it messed up the order of the week after grouby function and it is a pain to put the order back
        if "WeekDay" in ListOfDateAndTime:
            if Abbreviation==True:
                df['WeekDay'] = df['WeekDay'].map(lambda x : DicoDayOfWeek[x][0],DicoDayOfWeek)
            else:
                df['WeekDay'] = df['WeekDay'].map(lambda x : DicoDayOfWeek[x][1],DicoDayOfWeek)
        if "M" in ListOfDateAndTime:
            if Abbreviation==True:
                df['M'] = df['M'].map(lambda x : DicoMonthOfTheYear[x][0],DicoMonthOfTheYear)
            elif Abbreviation==False:
                df['M'] = df['M'].map(lambda x : DicoMonthOfTheYear[x][1],DicoMonthOfTheYear)

        #create the columns time in function of the date and time in listoftime
        if len(ListOfDate)>0 and len(ListOfTime)>0:
            df['Time'] = df[ListOfDate].astype(str).agg('-'.join, axis=1)+" "+df[ListOfTime].astype(str).agg(':'.join, axis=1)
        elif len(ListOfDate)>0 and len(ListOfTime)==0:
            df['Time'] = df[ListOfDate].astype(str).agg('-'.join, axis=1)
        elif len(ListOfDate)==0 and len(ListOfTime)>0:
            df['Time'] = df[ListOfTime].astype(str).agg(':'.join, axis=1)
        
        #Put the column Time in index
        df=df.set_index('Time')

        #drop every columns of ListOfDateAndTime to have a nice dataframe with just the number of videos trending and the time index
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

        #Create the name of columns
        NumberOfVideoTrendingByCountry="Number Of Video "+Country

        #Create a dataframe with the grouby serie
        df=df.to_frame(name = NumberOfVideoTrendingByCountry)

        #Check if Weekday was ask by the user if it is true then change number into week day name the df.index.weekday_name function is not utilised 
        # here because it messed up the order of the week after grouby function and it is a pain to put the order back
        if "WeekDay" in ListOfDateAndTime:
            if Abbreviation==True:
                df.index = df.index.map(lambda x : DicoDayOfWeek[x][0],DicoDayOfWeek)
            else:
                df.index = df.index.map(lambda x : DicoDayOfWeek[x][1],DicoDayOfWeek)
        elif "M" in ListOfDateAndTime:
            if Abbreviation==True:
                df.index = df.index.map(lambda x : DicoMonthOfTheYear[x][0],DicoMonthOfTheYear)
            elif Abbreviation==False:
                df.index = df.index.map(lambda x : DicoMonthOfTheYear[x][1],DicoMonthOfTheYear)

        # Rename the dataframe index in Time
        df.index=df.index.rename('Time')

    if ActivatePloting==True:
        Title="Number of Video grouped by " +" ".join(ListOfDateAndTime)+" of publication time"+" for "+ Country
        if len(ListOfDateAndTime)>1:
            XLabel="Time ("+"-".join(ListOfDate)+" "+":".join(ListOfTime)+")"
        else:
            XLabel="Time ("+"-".join(ListOfDateAndTime)+")"
        YLabel="Number of Video Trending"
        PlotGraph(df,Title,XLabel,YLabel)

    
    return df

def ConvertLocalTimeToUTC(df,Country,LocalToUTCTime):
    
    DicoCountryLocalTime={
        "USA":'US/Central',"MEX":'America/Mexico_City',"FRA":'Europe/Paris',"DEU":'Europe/Berlin',"GBR":'Europe/London',
        "IND":'Asia/Kolkata',"CAN":'America/Winnipeg',"KOR":'Asia/Seoul',"RUS":'Asia/Krasnoyarsk',"JPN":'Asia/Tokyo',
        }
    if LocalToUTCTime=="Local":
        df.index=df.index.tz_localize('utc').tz_convert(DicoCountryLocalTime[Country])

    return df


def NumberOfVideoWithOrWithoutFilter(df,Country,TimeDelta,FindText,ActivatePloting):
    
    DicoResampleAndGraph={
        "Year":("Y","%y"),"Month":("M","%y/%m"),"Week":("W","%V"),"Day":("D","%y/%m/%d"),"Hour":("H","%y/%m/%d %H"),
        "Minute":("T","%y/%m/%d %H:%m"),"Second":("S","%y/%m/%d %H:%m:%s")
        }
    filt=(df.index.year==2017) | (df.index.year==2018)
    df=df[filt].copy()
    
    
    if FindText!="":
        df.loc[:,"result"]=df.title.apply(lambda x: 1 if x.find(FindText)!=-1 else 0)#.copy()
        df_FiltResult=df["result"].resample(DicoResampleAndGraph[TimeDelta][0]).sum()#.copy()
    else:
        df_FiltResult=df["views"].resample(DicoResampleAndGraph[TimeDelta][0]).count()
    df_FiltResult.index=df_FiltResult.index.strftime(DicoResampleAndGraph[TimeDelta][1])#-%d
    print(df_FiltResult)
    if ActivatePloting==True:
        Title="Number of Video by " +TimeDelta+" for "+ Country
        XLabel=TimeDelta+" of the Year"
        YLabel="Number of Video Trending"
        PlotGraph(df_FiltResult,Title,XLabel,YLabel)
   
    return df_FiltResult




def PlotGraph(df,Title,XLabel,YLabel):

    NumberOfVideoTrendingByCountry="Number Of Video "+Country
    # Create the bar graph with in x axis Label ("HH:MM") and NumberOfVideoTrendingByCountry in y axis

    if isinstance(df, pd.Series):
        df.plot(y=0, kind='bar')
    else:
        df.plot(y=NumberOfVideoTrendingByCountry, kind='bar')
    

    #title of the plot
    plot.title(Title)

    #title of the x axis of the plot
    plot.xlabel(XLabel)

    #title of y axis of the plot
    plot.ylabel(YLabel)

    #show the graph
    plot.show()



##################################################### Year and Month analysis ##############################################################
# def NumberOfVideoFilterByYearAndMonth(df,sub):
#     NumberOfVideoTrendingByCountry="Number Of Video "+Country
#     YearsAndMonths=[]
#     Months=["January","February","March","April","May","June","July","August","October","November","December"]
    
#     for Year in range(min(df.publish_time.dt.year),max(df.publish_time.dt.year)+1):
#         for month in Months:
#             YearsAndMonths.append(str(Year)+" "+ month)
#     df_VideoCountForYearAndMonth=pd.DataFrame(0,index=YearsAndMonths,columns=[NumberOfVideoTrendingByCountry])
#     # sub="" 
#     for YearAndMonth in YearsAndMonths:
#         YearMonth=YearAndMonth.split()
#         # filtervalue=(df.publish_time.dt.year==2017) & (df.publish_time.dt.month_name()=="November")
#         filtervalue=(df.publish_time.dt.year==int(YearMonth[0])) & (df.publish_time.dt.month_name()==YearMonth[1])& (df.title.str.find(sub)!=-1)
#         df_VideoCountForYearAndMonth.loc[YearAndMonth,NumberOfVideoTrendingByCountry]=max(df[filtervalue].count())
#     print(df_VideoCountForYearAndMonth)

#     return df_VideoCountForYearAndMonth

# def PlotNumberOfVideoTrendingInFunctionOfYearAndMonth(Country,df_VideoCountForYearAndMonth):

#     NumberOfVideoTrendingByCountry="Number Of Video "+Country
#     # Create the bar graph with in x axis Label ("HH:MM") and NumberOfVideoTrendingByCountry in y axis
#     df_VideoCountForYearAndMonth.plot(y=NumberOfVideoTrendingByCountry, kind='bar')
    

#     #title of the plot
#     plot.title("Number of Video Trending in " +Country +" by Year and month")

#     #title of the x axis of the plot
#     plot.xlabel('Years and months')

#     #title of y axis of the plot
#     plot.ylabel('Number of Video Trending')

#     #show the graph
#     plot.show()



##################################################### Year analysis ########################################################################
# def NumberOfVideoFilterByYear(df):
#     NumberOfVideoTrendingByCountry="Number Of Video "+Country
#     Years=[]
#     for Year in range(min(df.publish_time.dt.year),max(df.publish_time.dt.year)+1):
#         Years.append(Year)
#     df_VideoCountForYear=pd.DataFrame(0,index=Years,columns=[NumberOfVideoTrendingByCountry])

#     for Year in Years:
#         filtervalue=(df.publish_time.dt.year==Year)
#         df_VideoCountForYear.loc[Year,NumberOfVideoTrendingByCountry]=max(df[filtervalue].count())
#     print(df_VideoCountForYear)

#     return df_VideoCountForYear

# def PlotNumberOfVideoTrendingInFunctionOfYear(Country,df_VideoCountForYear):

#     NumberOfVideoTrendingByCountry="Number Of Video "+Country
#     # Create the bar graph with in x axis Label ("HH:MM") and NumberOfVideoTrendingByCountry in y axis
#     df_VideoCountForYear.plot(y=NumberOfVideoTrendingByCountry, kind='bar')
    

#     #title of the plot
#     plot.title("Number of Video Trending in " +Country +" by Year")

#     #title of the x axis of the plot
#     plot.xlabel('Years')

#     #title of y axis of the plot
#     plot.ylabel('Number of Video Trending')

#     #show the graph
#     plot.show()

# ##################################################### Months analysis ######################################################################

# def NumberOfVideoFilterByMonth(df):

#     NumberOfVideoTrendingByCountry="Number Of Video "+Country
#     Months=["January","February","March","April","May","June","July","August","October","November","December"]
#     df_VideoCountForMonthOfTheYear=pd.DataFrame(0,index=Months,columns=[NumberOfVideoTrendingByCountry])
    
#     for Month in Months:
#         filtervalue=(df.publish_time.dt.month_name()==Month)
#         df_VideoCountForMonthOfTheYear.loc[Month,NumberOfVideoTrendingByCountry]=max(df[filtervalue].count())
#     print(df_VideoCountForMonthOfTheYear)

#     return df_VideoCountForMonthOfTheYear

# def PlotNumberOfVideoTrendingInFunctionOfMonth(Country,df_VideoCountForMonthOfTheYear):

#     NumberOfVideoTrendingByCountry="Number Of Video "+Country
#     # Create the bar graph with in x axis Label ("HH:MM") and NumberOfVideoTrendingByCountry in y axis
#     df_VideoCountForMonthOfTheYear.plot(y=NumberOfVideoTrendingByCountry, kind='bar')
    

#     #title of the plot
#     plot.title("Number of Video Trending in " +Country +" by Month")

#     #title of the x axis of the plot
#     plot.xlabel('Month of The Year')

#     #title of y axis of the plot
#     plot.ylabel('Number of Video Trending')

#     #show the graph
#     plot.show()
# ######################################################## WeekDay analysis ################################################################

# def NumberOfVideoFilterByWeekDay(df,Country,ActivatePloting):

#     NumberOfVideoTrendingByCountry="Number Of Video "+Country
#     WeekDays=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
#     df_VideoCountForDayOfTheWeek=pd.DataFrame(0,index=WeekDays,columns=[NumberOfVideoTrendingByCountry])
#     for WeekDay in WeekDays:
#         df_VideoCountForDayOfTheWeek.loc[WeekDay,NumberOfVideoTrendingByCountry]=max(df[df.publish_time.dt.day_name()==WeekDay].count())
#     print(df_VideoCountForDayOfTheWeek)

#     if ActivatePloting==True:
#         Title="Number of Video Trending in " +Country +" by Week Day"
#         XLabel="Day of The Week"
#         YLabel="Number of Video Trending"
#         PlotGraph(df_VideoCountForDayOfTheWeek,Title,XLabel,YLabel)

#     return df_VideoCountForDayOfTheWeek



IntervalMinute=30
Country="FRA"
ActivatePloting=True
LocalToUTCTime="Local"
FindText=" Trump "
CountryGraphInFunctionOfTime(IntervalMinute,Country,ActivatePloting,LocalToUTCTime,FindText)

