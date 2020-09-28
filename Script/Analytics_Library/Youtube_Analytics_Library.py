import pandas as pd
import datetime
import matplotlib as mlp
import matplotlib.pyplot as plot
import numpy as np
import os

def CreateAndOrPlotTimeVsNumberOfVideoDF(ListOfCountry,IntervalMinute,ActivatePloting,ForceRenderingData):

    PathToDataOUT=os.path.join("Script","Data","Data_OUT","")
    NameOfTheFile="TrendingVideoVSTimeForEveryCountry_"+str(IntervalMinute)+"_min"
    PathToTheOUTDataFile=os.path.join(PathToDataOUT,NameOfTheFile+".csv")

    # If the file doesn't exist it will create it
    if os.path.isfile(PathToTheOUTDataFile)==False or ForceRenderingData==True:

        for Country in ListOfCountry:
            
            
            
            #If it is at the beginning of the list of country create an empty DF and then initilized it with the first country data 
            if Country==ListOfCountry[0]:
                DF_NumberOfVideoTrendingInFunctionOfTimeByCountry=pd.DataFrame()
                DF_NumberOfVideoTrendingInFunctionOfTimeByCountry=PlotBarGraphInFunctionOfTime(IntervalMinute,Country,ActivatePloting)

            # for every other country it will then merge data that have been generated from the csv in the df created with the first country 
            else:
                Df_NewCountryValue=PlotBarGraphInFunctionOfTime(IntervalMinute,Country,ActivatePloting)
                DF_NumberOfVideoTrendingInFunctionOfTimeByCountry=pd.merge(DF_NumberOfVideoTrendingInFunctionOfTimeByCountry,Df_NewCountryValue, on='Label')
                

        

        

    else:
        #If the file PathToTheOUTDataFile exist then load the data andd plot them to a graph
        DF_NumberOfVideoTrendingInFunctionOfTimeByCountry=pd.read_csv(PathToTheOUTDataFile)

        for Country in ListOfCountry:
            NumberOfVideoTrendingByCountry="Number Of Video "+Country

            #get the colunmns name compare it to NumberOfVideoTrendingByCountry if it doesnt match with the list
            #then PlotBarGraphInFunctionOfTime(Df_TimeAndNumberOfPublication,IntervalMinute,Country,ActivatePloting) return the 
            #dataframe and append it to DF_NumberOfVideoTrendingInFunctionOfTimeByCountry and then plot it et save it
            
            DF_NumberOfVideoTrendingInFunctionOfTimeByCountry=AppendNewCountryToTheDFofTheResultData(Country,IntervalMinute,NumberOfVideoTrendingByCountry,DF_NumberOfVideoTrendingInFunctionOfTimeByCountry)
            
            PlotNumberOfVideoTrendingInFunctionOfTime(Country,NumberOfVideoTrendingByCountry,DF_NumberOfVideoTrendingInFunctionOfTimeByCountry)
      
    DF_NumberOfVideoTrendingInFunctionOfTimeByCountry.to_csv(PathToTheOUTDataFile)

    return DF_NumberOfVideoTrendingInFunctionOfTimeByCountry





def PlotBarGraphInFunctionOfTime(IntervalMinute,Country,ActivatePloting):
    """ Plot the bar graph of all the interval and the value inside them in this case the number of video trending for the time of publication """

    #get and read the csv of with youtube value
    df=GetDFDataFromCountryCSV(Country)
    
    #all the headers of all the columns of every file
    # Df_Header=[video_id,trending_date,title,channel_title,category_id,publish_time,tags,views,likes,dislikes,comment_count,thumbnail_link,comments_disabled,ratings_disabled,video_error_or_removed,description]
    df=df.drop(columns=['video_id','title','channel_title','category_id','tags','thumbnail_link','comments_disabled','ratings_disabled','video_error_or_removed','description'])
    
    #get the plublish time and put in the column publish time
    df['publish_time'] = pd.to_datetime(df['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
    
    df.insert(5, 'publish_date', df['publish_time'].dt.date)

    #convert them into datetime time 
    df['publish_time'] = df['publish_time'].dt.time
    


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


    #Create all the time interval for time data to be put in for TimeOfPublication of the dataframe
    Hours=pd.date_range('00:00:00', '23:59:00',freq=str(IntervalMinute)+'T').time

    #Create all the time interval for time data to be put in for Label of the graph because second are not necessary
    HoursForLabels=pd.date_range('00:00:00', '23:59:00',freq=str(IntervalMinute)+'T').strftime('%H:%M').tolist()

    #Create and initialise the dataframe with TimeOfPublication datetime.time value to be use 
    # to class the publish time data in the for loop
    NumberOfVideoTrendingByCountry="Number Of Video "+Country
    df_NumberHours=pd.DataFrame(0,index=Hours,columns=["Label",NumberOfVideoTrendingByCountry])

    #Put the list of label in the column Label
    df_NumberHours["Label"]=HoursForLabels

    #initialise 23:59:59 to get the value of midnight and to put them into the 00:00:00 label
    df_NumberHours.loc[datetime.time(23,59,59)] = 0

    # Get the time value of the dataframe containing all the time data in TimeOfPublication 
    # with the number of the video trending by time of publication
    for TimeOfPublication in Df_TimeAndNumberOfPublication.index:

        #Get the center Time value that have been generated by the interval in minute by the user
        for Time in df_NumberHours.index:
            
            #For 0 hour
            if Time.hour==0:
                #For 0 hour 0 minute
                if Time.minute==0:

                    #if the time value from the dataframe with the number of all the publication date 
                    # and the number of video publish is between inferior 00+interval/2
                    if TimeOfPublication<=datetime.time(hour=Time.hour,minute=int(0+(IntervalMinute/2)),second=0) :
                        df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry]=int(df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry])+int(Df_TimeAndNumberOfPublication[TimeOfPublication])

                else:
                    # For 0 hour 30 min and so on 
                    if TimeOfPublication>datetime.time(hour=Time.hour,minute=int(Time.minute-(IntervalMinute/2)),second=0) and TimeOfPublication<=datetime.time(hour=Time.hour,minute=Time.minute+int((IntervalMinute/2)),second=0):
                        df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry]=int(df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry])+int(Df_TimeAndNumberOfPublication[TimeOfPublication])

            # For 23 hours            
            elif Time.hour==23:
                
                #for the interval value 23:59:59 initialize before
                if Time.minute==59:
                    
                    #For 23 hour 59 minute because midnight not possible so all the data 
                    # from the last interval get to the 00:00:00 interval because it is midnight
                    
                    #if the time value from the dataframe with the number of all the publication date 
                    # and the number of video publish is between superior 60-interval/2

                    if TimeOfPublication>datetime.time(hour=Time.hour,minute=int(60-(IntervalMinute/2)),second=0) :
                        #Put the number of the last interval in the first interval for midnight publication
                        df_NumberHours.loc[Hours[0],NumberOfVideoTrendingByCountry]=int(df_NumberHours.loc[Hours[0],NumberOfVideoTrendingByCountry])+int(Df_TimeAndNumberOfPublication[TimeOfPublication])

                elif Time.minute==0:
                    # for 23 hour 0 minute interval
                    if TimeOfPublication>datetime.time(hour=Time.hour-1,minute=int(60-(IntervalMinute/2)),second=0) and TimeOfPublication<=datetime.time(hour=Time.hour,minute=00+int((IntervalMinute/2)),second=0):
                        df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry]=int(df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry])+int(Df_TimeAndNumberOfPublication[TimeOfPublication])
                else:
                    # for 23 hour 30 minute and every other minute interval without 00 minute
                    if TimeOfPublication>datetime.time(hour=Time.hour,minute=int(Time.minute-(IntervalMinute/2)),second=0) and TimeOfPublication<=datetime.time(hour=Time.hour,minute=Time.minute+int((IntervalMinute/2)),second=0):
                        df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry]=int(df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry])+int(Df_TimeAndNumberOfPublication[TimeOfPublication])

            else: 
                #For other than 0 or 23 hours
                if Time.minute==0:
                    # for n hour 0 minute
                    if TimeOfPublication>datetime.time(hour=Time.hour-1,minute=int(60-(IntervalMinute/2)),second=0) and TimeOfPublication<=datetime.time(hour=Time.hour,minute=00+int((IntervalMinute/2)),second=0):
                        df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry]=int(df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry])+int(Df_TimeAndNumberOfPublication[TimeOfPublication])
                else:
                    # for n hour 30 minute every other interval without 00 minute 
                    if TimeOfPublication>datetime.time(hour=Time.hour,minute=int(Time.minute-(IntervalMinute/2)),second=0) and TimeOfPublication<=datetime.time(hour=Time.hour,minute=Time.minute+int((IntervalMinute/2)),second=0):
                        df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry]=int(df_NumberHours.loc[Time,NumberOfVideoTrendingByCountry])+int(Df_TimeAndNumberOfPublication[TimeOfPublication])

    #Supres the last row of the df for interval and video publish in the interval 
    # because it is 23:59:59 but is empty cause every thing goes to 00:00:00
    df_NumberHours.drop(df_NumberHours.tail(1).index,inplace=True)
    
    #if ActivatePloting== true plot the graph else no graph
    if ActivatePloting==True:
        #Put the time center value of interval generated in the beginning of this function to be shown 
        # without second value because it is more beautiful on the bar graph

        PlotNumberOfVideoTrendingInFunctionOfTime(Country,NumberOfVideoTrendingByCountry,df_NumberHours)

    return df_NumberHours

def GetDFDataFromCountryCSV(Country):

    PathToInputData=os.path.join("Script","Data","Data_IN","Youtube_CSV__And_JSON",Country+"videos.csv")
    if Country=="RU" or Country=="KR" or Country=="MX":
        df=pd.read_csv(PathToInputData,engine="python")
    elif Country=="JP":
        PathToInputData=os.path.join("Script","Data","Data_IN","Youtube_CSV__And_JSON",Country+"videos - Copie.csv")
        df=pd.read_csv(PathToInputData,engine="python", error_bad_lines=False, delimiter=";")
    else:
        df=pd.read_csv(PathToInputData)

    return df


def AppendNewCountryToTheDFofTheResultData(Country,IntervalMinute,NumberOfVideoTrendingByCountry,DF_NumberOfVideoTrendingInFunctionOfTimeByCountry):
    if NumberOfVideoTrendingByCountry not in sorted(DF_NumberOfVideoTrendingInFunctionOfTimeByCountry):
        #Desactivate Plotting because it will be shown after adding it to the DF_NumberOfVideoTrendingInFunctionOfTimeByCountry 
        ActivatePloting=False
        Df_NewCountryValue=PlotBarGraphInFunctionOfTime(IntervalMinute,Country,ActivatePloting)
        DF_NumberOfVideoTrendingInFunctionOfTimeByCountry=pd.merge(DF_NumberOfVideoTrendingInFunctionOfTimeByCountry,Df_NewCountryValue, on='Label')

    return DF_NumberOfVideoTrendingInFunctionOfTimeByCountry

def PlotNumberOfVideoTrendingInFunctionOfTime(Country,NumberOfVideoTrendingByCountry,DF_NumberOfVideoTrendingInFunctionOfTimeByCountry):

    # Create the bar graph with in x axis Label ("HH:MM") and NumberOfVideoTrendingByCountry in y axis
    DF_NumberOfVideoTrendingInFunctionOfTimeByCountry.plot(x="Label",y=NumberOfVideoTrendingByCountry, kind='bar')
    

    #title of the plot
    plot.title("Number of Video Trending in " +Country +" by publication time")

    #title of the x axis of the plot
    plot.xlabel('Time')

    #title of y axis of the plot
    plot.ylabel('Number of Video Trending')

    #show the graph
    plot.show()

            