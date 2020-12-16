import pandas as pd
import datetime
import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
import os
import geopandas as gpd
import imageio
import time
import math
import itertools
from matplotlib._layoutbox import plot_children


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
    """ Plot the bar graph of all the interval and the value inside them in this case the number of videos trending for the time of publication """

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

    BeginingDateOrTime=""
    EndDateOrTime=""

    # BeginingDateOrTime="2018-04"
    # EndDateOrTime="2018-05"
    df=FilterByDateTimePeriod(df,BeginingDateOrTime,EndDateOrTime)

    print(df)
    
    #Converting LOcal time to UTC time if LocalToUTCTime==True
    df=ConvertLocalTimeToUTC(df,Country,LocalToUTCTime)

    #Create a dataframe with the number of video published in the time interval (created with IntervalMinute) from 0h to 24h  
    df_NumberHours=NumberOfVideoFilterByPublishTime(df,Country,IntervalMinute,ActivatePloting)
    
    # df_VideoCountForDayOfTheWeek=NumberOfVideoFilterByWeekDay(df,Country,ActivatePloting)

    Abbreviation=False
    ListOfDateAndTime=["WeekDay","h"]#,"W","WeekDay"]#,"m"]
    df_NumberOfVideoFilterByPublishTimeOrDate=NumberOfVideoFilterByPublishTimeOrDate(df,Country,ListOfDateAndTime,Abbreviation,ActivatePloting)
    print("Groupby")
    print(df_NumberOfVideoFilterByPublishTimeOrDate)



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

def FilterByDateTimePeriod(df,BeginingDateOrTime,EndDateOrTime):
    #it is here until their is a datetime filter

    if BeginingDateOrTime!="" and EndDateOrTime!="":
        df=df.loc[BeginingDateOrTime:EndDateOrTime]
    elif BeginingDateOrTime=="" and EndDateOrTime!="":
        df=df.loc[::EndDateOrTime]
    elif BeginingDateOrTime!="" and EndDateOrTime=="":
        df=df.loc[BeginingDateOrTime::]
    # if FindText!="":
    #     df.loc[:,"result"]=df.title.apply(lambda x: 1 if x.find(FindText)!=-1 else 0)#.copy()
    #     filt=(df.title.str.find(FindText)!=-1)
    #     df=df.loc[filt]#.copy()
    #     # filt=(df.index.year==2017) | (df.index.year==2018)
    #     # df=df[filt].copy()
    return df

def NumberOfVideoFilterByPublishTime(df,Country,IntervalMinute,ActivatePloting):


    df.set_index( df['publish_time'], inplace=True)
    
    
    
    HoursForLabels=pd.date_range('00:00:00', '23:59:59',freq=str(IntervalMinute)+'T').strftime('%H:%M:%S').tolist()

    NumberOfVideoTrendingByCountry="Number Of Videos "+Country
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
        Title="Number of Videos Trending in " +Country +" by publication time "+"("+LocalToUTCTime+")"
        XLabel="Time"
        YLabel="Number of Videos Trending"
        PlotGraph(df_NumberHours,Title,XLabel,YLabel)


    return df_NumberHours


def GroupByDateAndTime(df,ListOfDateAndTime,Abbreviation):


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
    df_grp=df.groupby(ListOfDateAndTime)#["views"].count()

    #count the number of row in view columns
    SerieAfterGrpBy=df_grp["views"].count()

    #check the level of indexing in the series after grouby to modify the day or month number by their name after grouping and before plotting
    nblevels = SerieAfterGrpBy.index.nlevels 

    #Check if Weekday or M was ask by the user in ListOfDateAndTime if it is true then change number into week day, or month name the df.index.weekday_name function is not utilised 
    #here because it messed up the order of the week after grouby function and it is a pain to put the order back so we replace the number by the name after grouby function
    if nblevels!=1:

        #if their is more than one level of indexing in the series modify the corresponding index level by the month name or weekday name
        for ColumnsName in ListOfDateAndTime:

            ListMultiIndexName=SerieAfterGrpBy.index.names

            if ColumnsName in ListMultiIndexName:
                level_index=ListMultiIndexName.index(ColumnsName)
                
                if Abbreviation==True:
                    if ColumnsName=="WeekDay":
                        SerieAfterGrpBy.index = SerieAfterGrpBy.index.set_levels(SerieAfterGrpBy.index.levels[level_index].map(lambda x : DicoDayOfWeek[x][0],DicoDayOfWeek), level=level_index)
                    elif ColumnsName=="M":
                        SerieAfterGrpBy.index = SerieAfterGrpBy.index.set_levels(SerieAfterGrpBy.index.levels[level_index].map(lambda x : DicoMonthOfTheYear[x][0],DicoDayOfWeek), level=level_index)
                elif Abbreviation==False:
                    if ColumnsName=="WeekDay":
                        SerieAfterGrpBy.index = SerieAfterGrpBy.index.set_levels(SerieAfterGrpBy.index.levels[level_index].map(lambda x : DicoDayOfWeek[x][1],DicoDayOfWeek), level=level_index)
                    elif ColumnsName=="M":
                        SerieAfterGrpBy.index = SerieAfterGrpBy.index.set_levels(SerieAfterGrpBy.index.levels[level_index].map(lambda x : DicoMonthOfTheYear[x][1],DicoDayOfWeek), level=level_index)
    else:
        #if their is no more than one level of indexing in the series modify the index with the month name or weekday name
        IndexName=ListOfDateAndTime[0]
        if Abbreviation==True:
            if IndexName=="WeekDay":
                SerieAfterGrpBy.index = SerieAfterGrpBy.index.map(lambda x : DicoDayOfWeek[x][0],DicoDayOfWeek)
            elif IndexName=="M":
                SerieAfterGrpBy.index = SerieAfterGrpBy.index.map(lambda x : DicoMonthOfTheYear[x][0],DicoMonthOfTheYear)
        elif Abbreviation==False:
            if IndexName=="WeekDay":
                SerieAfterGrpBy.index = SerieAfterGrpBy.index.map(lambda x : DicoDayOfWeek[x][1],DicoDayOfWeek)
            elif IndexName=="M":
                SerieAfterGrpBy.index = SerieAfterGrpBy.index.map(lambda x : DicoMonthOfTheYear[x][1],DicoMonthOfTheYear)

    return SerieAfterGrpBy,ListOfDate,ListOfTime

def GroupPlottingInOnePlot(SerieAfterGrpBy,Country,ListOfDateAndTime,ListOfDate,ListOfTime,Abbreviation,ActivatePloting):


    #Create the name of columns
    NumberOfVideoTrendingByCountry="Number Of Videos "+Country

    #Go from pd series to dataframe with another index
    df=SerieAfterGrpBy.to_frame(name = NumberOfVideoTrendingByCountry).reset_index()

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

    #Plot the graph if ActivatePloting==True 
    if ActivatePloting==True:
        Title="Number of Videos grouped by " +" ".join(ListOfDateAndTime)+" of publication time"+" for "+ Country
        if len(ListOfDateAndTime)>1:
            XLabel="Time ("+"-".join(ListOfDate)+" "+":".join(ListOfTime)+")"
        else:
            XLabel="Time ("+"-".join(ListOfDateAndTime)+")"
        YLabel="Number of Videos Trending"
        PlotGraph(df,Title,XLabel,YLabel)

    return df

def NumberOfVideoFilterByPublishTimeOrDate(df,Country,ListOfDateAndTime,Abbreviation,ActivatePloting):

    SerieAfterGrpBy,ListOfDate,ListOfTime = GroupByDateAndTime(df,ListOfDateAndTime,Abbreviation)

    df=GroupPlottingInOnePlot(SerieAfterGrpBy,Country,ListOfDateAndTime,ListOfDate,ListOfTime,Abbreviation,ActivatePloting)
    print("all in one plot")
    print(df)

    if len(ListOfDateAndTime)>1:
        print("eclated plot")
        df_eclated=EclatedSubPlot(SerieAfterGrpBy,ActivatePloting,ListOfDateAndTime,Abbreviation)
        print(df_eclated)
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
        Title="Number of Videos by " +TimeDelta+" for "+ Country
        XLabel=TimeDelta+" of the Year"
        YLabel="Number of Videos Trending"
        PlotGraph(df_FiltResult,Title,XLabel,YLabel)
   
    return df_FiltResult

def EclatedSubPlot(SerieAfterGrpBy,ActivatePlotting,ListOfDateAndTime,Abbreviation):
    
    df_unstack=SerieAfterGrpBy.unstack(level=0)
    # NBcolumns=math.ceil(len(df_unstack.columns)/4)
    # if NBcolumns=<1:
    #     row=math.ceil(len(df_unstack.columns))
    # else:
    ActivatePlotting=True
    if ActivatePlotting==True:

        DicoConfigRowColumsSubPlot={"Y":(4,3),"M":(-1,4),"W":(13,4),"D":(8,4),"WeekDay":(4,2),"h":(6,4),"m":(10,6),"s":(10,6)}
        # fig=df_unstack.plot(subplots=True, layout=DicoConfigRowColumsSubPlot[ListOfDateAndTime[0]],kind="bar",sharex=True,sharey=True,legend=False,)#.flatten()#.map(set_xlabel=("toto"))#**kwargs)
        # fig=df_unstack.plot(subplots=True,kind="bar",sharex=True,sharey=True,legend=False)
        if "m" is ListOfDateAndTime[0] or "s" is ListOfDateAndTime[0]:
            ncol = 6  # how many plots per row
        elif "Y" is ListOfDateAndTime[0]:
            ncol=2
        else:
            ncol = 4
        if len(df_unstack.columns)<ncol:
            ncol=(len(df_unstack.columns))
        nrow = math.ceil(len(df_unstack.columns) / ncol)  # how many rows of plots
        
        
       # make a list of all dataframes 
        df_list = df_unstack.columns
        fig, axes = plt.subplots( nrow, ncol,sharex=True,sharey=True,figsize=(10,5),)
        # figsize=(12,7)

          # change the figure size as needed
        # plot counter
        # axes.add_suplots
        # map(lambda x: df_unstack[df_list].plot(ax=x,kind="bar",title=df_list),axes.flatten())
        DicoConfigRowColumsSubPlot={"Y":"Year","M":"Month","W":"Week","D":"Day","WeekDay":"Weekday","h":"Hour","m":"Minute","s":"Second"}
        CommonXLabel="Time ("+','.join(list(map(lambda x: DicoConfigRowColumsSubPlot[x],ListOfDateAndTime[1:])))+")"
        count=0
        minx0=miny0=99
        for r in range(nrow):
            for c in range(ncol):

                if len(axes.shape)!=1 and count<=len(df_list)-1:
                    df_unstack[df_list[count]].plot(ax=axes[r,c],kind="bar",title=df_list[count],)
                    axes[r,c].set_xlabel(CommonXLabel,color="w")
                    axes[r,c].set_ylabel(CommonXLabel,color="w")
                    
                    
                    
                    # axes[r,c]
                    # miny = min(miny, a.get_ylim()[0])
                    # print(minx0,miny0)
                    # if len(axes[r,c].xaxis.get_ticklabels())!=0 and c!=0:
                    #     label = axes[-1,c].xaxis.get_ticklabels()[-1]
                    #     # for label in labels:
                    #     # box=label.get_tightbbox()
                    #     totot=axes[-1,c].xaxis.get_tightbbox()
                    #     print(totot)
                    #     box=label.get_window_extent()
                    #     # Nminx0,Nminy0=fig.transFigure.inverted().transform((axes[r,c].yaxis.majorTicks[0].get_clip_box().x0,axes[r,c].yaxis.majorTicks[0].get_clip_box().y0))
                    #     Nminx0,Nminy0=fig.transFigure.inverted().transform((box.x0,box.y0))
                    #     minx0=min(minx0,Nminx0)
                    #     miny0=min(miny0,Nminy0)
                    #     print(minx0,miny0)
                    # minx0=min(minx0,axes[r,c].get_position().x0)
                    # axes[r,c].yaxis.majorTicks[0].get_clip_box().x0
                    # miny0=min(miny0,axes[r,c].xaxis.majorTicks[0].get_clip_box().y0)
                    # print(axes[r,c].xaxis.label.getposition())
                    XListTickLabels=axes[-1,0].xaxis.get_ticklabels()
                    YListTickLabels=axes[-1,0].yaxis.get_ticklabels()
                elif len(axes.shape)==1:
                    df_unstack[df_list[count]].plot(ax=axes[c],kind="bar",title=df_list[count],)
                    axes[c].set_xlabel(CommonXLabel,color="w")
                    XListTickLabels=axes[0].xaxis.get_ticklabels()
                    YListTickLabels=axes[0].yaxis.get_ticklabels()

                else:
                    fig.delaxes(axes[r,c])
                count=count+1
        # get_tick_bboxes _get_tick_boxes_siblings _get_ticks_position
        fig.canvas.draw()
        # minx0=min(minx0,axes[r,c].yaxis.get_label().get_position()[0])
        # miny0=min(miny0,axes[r,c].xaxis.get_label().get_position()[1])
        # print(minx0,miny0)
        # axes[-1, 0].set_xlabel('.', color=(0, 0, 0, 0))
        # axes[-1, 0].set_ylabel('.', color=(0, 0, 0, 0))
        
        # axes[r,c].xaxis.majorTicks[0].get_clip_box()
        # fig.transFigure.inverted().transform((axes[r,c].xaxis.get_clip_box().x0,axes[r,c].xaxis.get_clip_box().y0))
        
        

        Nminx0,Nminy0=fig.transFigure.inverted().transform((minx0,miny0))
        print(Nminx0,Nminy0)
        # fig.text(0.5, (axes[-1,0].get_position().y0)*(1/3), CommonXLabel, ha='center', fontsize=14,color='b')
        # fig.text((axes[-1,0].get_position().x0)*(2/3), 0.5, 'Number of Video Trending', va='center', ha='center', rotation='vertical', fontsize=14, color='b')
        # label = axes[-1,0].xaxis.get_ticklabels()[-1]
        # label.set_bbox(dict(facecolor='none', edgecolor='red'))
        # labely = axes[-1,0].yaxis.get_ticklabels()[-1]
        # labely.set_bbox(dict(facecolor='none', edgecolor='blue'))
        # plt.rcParams['axes.labelsize']
        # fig.text(0.5, axes[-1,-1].get_position().y0, CommonXLabel, ha='center', fontsize=14,color='b')
        # fig.text(axes[0,0].get_position().x0, 0.5, 'Number of Video Trending', va='center', ha='center', rotation='vertical', fontsize=14, color='b')


        

            # Ybbox=axes[-1,0].yaxis.get_ticklabels()[-1].get_window_extent()
            # Xbbox=axes[-1,0].xaxis.get_ticklabels()[-1].get_window_extent()
        
        # Yx0,Yy0=fig.transFigure.inverted().transform((Ybbox.x0,Ybbox.y0))
        # Yx1,Yy1=fig.transFigure.inverted().transform((Ybbox.x1,Ybbox.y1))

        # Xx0,Xy0=fig.transFigure.inverted().transform((Xbbox.x0,Xbbox.y0))
        # Xx1,Xy1=fig.transFigure.inverted().transform((Xbbox.x1,Xbbox.y1))

        
        # 0.021875
        # fig.text(0.5, Xy0*3/4, ' Xy0 Time', ha='center')
        # # fig.text(0.5, Xy1, ' Xy1 Time', ha='center')

        # fig.text(Yx0*2/3, 0.5, 'Yx0 Number of Video Trending', va='center', rotation='vertical')
        # # fig.text(Yx1, 0.5, 'Yx1 Number of Video Trending', va='center', rotation='vertical')

        # fig.text(0.5, 0.11993634, ' x1 Time', ha='center')
        # fig.text(0.11579557, 0.5, 'x1 Number of Video Trending', va='center', rotation='vertical')
        # fig.subplots_adjust()
        # fig.title("toto")
        # plt.figure(figsize=(10, 5))
        
        # if len(ListOfDateAndTime)==2:
        #             TitleOfTheEclatedFigure='Number of Video Trending by '+DicoConfigRowColumsSubPlot[ListOfDateAndTime[0]]+' in function of '+DicoConfigRowColumsSubPlot[ListOfDateAndTime[1]]
        #             CommonXLabel="Time ("+DicoConfigRowColumsSubPlot[ListOfDateAndTime[1]]+")"
        # else:
        #     for i in range(len(ListOfDateAndTime)):
        #         if i==0:
        #             TitleOfTheEclatedFigure='Number of Video Trending by '+DicoConfigRowColumsSubPlot[ListOfDateAndTime[i]]+' in function of '

                    
        #         elif len(ListOfDateAndTime)>2:
        #             TitleOfTheEclatedFigure=TitleOfTheEclatedFigure+" and " + DicoConfigRowColumsSubPlot[ListOfDateAndTime[i]]
        #             CommonXLabel="Time ("+','.join(list(map(lambda x: DicoConfigRowColumsSubPlot[x],ListOfDateAndTime[1:])))+")"

        
        # plt.title(TitleOfTheEclatedFigure, )
        # fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        # plt.subplots_adjust(top=0.9, bottom=None, ) \n\n\n

        # miny = maxy = 0
        # minx = maxx = 0
        # for i, a in enumerate(itertools.chain(*axes)):
        #     # a.plot([0,4**i], [0,4**i])
        #     # a.set_title(i)
        #     miny = min(miny, a.get_ylim()[0])
        #     maxy = max(maxy, a.get_ylim()[1])
        #     minx = min(minx, a.get_xlim()[0])
        #     maxx = max(maxx, a.get_xlim()[1])
        #     ticksy = [(tick - miny)/(maxy - miny) for tick in a.get_yticks()]
        #     ticksx = [(tick - minx)/(maxx - minx) for tick in a.get_xticks()]
        #     print(ticksy,ticksx)


        
        # # add a big axes, hide frame
        # # set ylim to match the largest range of any subplot
        # ax_invis = fig.add_subplot(111, frameon=False)
        # xlbl=ax_invis.set_xlabel("common X",fontsize=16)
        # xlb2=ax_invis.set_ylabel("common Y", fontsize=16)
        # ax_invis.xaxis.set_label_coords(0.5, 0)
        # ax_invis.set_position([0,0,1,1])
        # print(ax_invis.get_position())
        # ax_invis.set_ylim([miny, maxy])
        # ax_invis.set_xlim([minx, maxx])

        # # hide tick and tick label of the big axis
        # plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        
        # print(xlbl.set_position(),xlb2.get_position())

        # # shrink plot to prevent clipping
        # plt.subplots_adjust(left=0.15)
        # plt.show()

        # if "m" is ListOfDateAndTime[0] or "s" is ListOfDateAndTime[0]:
        #     plt.subplots_adjust(hspace=1)
        # else:
        #     plt.subplots_adjust(bottom=0.2,hspace=0.3)

        # axes[r-1,c].title.get_tightbbox( fig.canvas.get_renderer())
        # bboxTitle=axes[-1,c].title.get_window_extent()
        # tbbox=fig.transFigure.inverted().transform(bbox)
        UpperAxeBbox=axes[-2,c].get_position()



        # Y1BBoxTitleLastRowAxes=axes[r,0].get_tightbbox(fig.canvas.get_renderer()).y1
        # X1BBoxTitleLastRowAxes=axes[r,0].get_tightbbox(fig.canvas.get_renderer()).x1
        # X0BBoxBeforeLastRowAxes=axes[r-1,0].get_tightbbox(fig.canvas.get_renderer()).x0
        # Y0BBoxBeforeLastRowAxes=axes[r-1,0].get_tightbbox(fig.canvas.get_renderer()).y0
        # TX0BBoxLastRowAxes,TY0BBoxBeforeLastRowAxes=fig.transFigure.inverted().transform((X0BBoxBeforeLastRowAxes,Y0BBoxBeforeLastRowAxes))
        # TX1BBoxTitleLastRowAxes,TY1BBoxBeforeLastRowAxes=fig.transFigure.inverted().transform((X1BBoxTitleLastRowAxes,Y1BBoxTitleLastRowAxes))

        # Y1BBoxTitleLastRowAxes=axes[r,0].title.get_tightbbox(fig.canvas.get_renderer()).y1
        # X1BBoxTitleLastRowAxes=axes[r,0].title.get_tightbbox(fig.canvas.get_renderer()).x1

        # X0BBoxBeforeLastRowAxes=axes[r-1,0].get_position().x0
        Y0BBoxBeforeLastRowAxes=axes[r-1,0].get_position().y0
        Y1BBoxTitleLastRowAxes=axes[r,0].title.get_tightbbox(fig.canvas.get_renderer()).y1
        X1BBoxTitleLastRowAxes=axes[r,0].title.get_tightbbox(fig.canvas.get_renderer()).x1
        TX1BBoxTitleLastRowAxes,TY1BBoxTitleLastRowAxes=fig.transFigure.inverted().transform((X1BBoxTitleLastRowAxes,Y1BBoxTitleLastRowAxes))
        DiffBetweenAxeTitleAndSuperiorAxes=Y0BBoxBeforeLastRowAxes-TY1BBoxTitleLastRowAxes





        Xy0=Yx0=99
        for i,YLabel in enumerate(YListTickLabels):
            
            Ybbox=YLabel.get_window_extent()
            NYx0,Yy0=fig.transFigure.inverted().transform((Ybbox.x0,Ybbox.y0))
            # if NYx0<Yx0 and i!=0:
            #     YLabel.set_bbox(dict(facecolor='none', edgecolor='red'))
            #     OldYlabel.set_bbox(dict(facecolor='none', edgecolor='none'))
            #     OldYlabel=YLabel
            # elif i==0:
            #     OldYlabel=YLabel
            Yx0=min(Yx0,NYx0)


        for i,XLabel in enumerate(XListTickLabels):
            
            Xbbox=XLabel.get_window_extent()
            Xx0,NXy0=fig.transFigure.inverted().transform((Xbbox.x0,Xbbox.y0))

            # if NXy0<Xy0 and i!=0:
            #     XLabel.set_bbox(dict(facecolor='none', edgecolor='red'))
            #     OldXlabel.set_bbox(dict(facecolor='none', edgecolor='none'))
            #     OldXlabel=XLabel
            # elif i==0:
            #     OldXlabel=XLabel
            Xy0=min(Xy0,NXy0)
        # plt.subplots_adjust()
        


        MinTickLabel=99
        BottomMargin=LeftMargin=hspaceMargin=DiffBetweenTickLabelAndXTitle=DiffBetweenTitleAndAxes=0
        MinimumSpaceBetwweenTickLabelAndXTitle=0.05
        while Yx0<0 or DiffBetweenTickLabelAndXTitle<0.02 or DiffBetweenAxeTitleAndSuperiorAxes<=0.01:# or TY1BBoxBeforeLastRowAxes>Y0BBoxBeforeLastRowAxes or DiffBetweenTickLabelAndXTitle<=MinimumSpaceBetwweenTickLabelAndXTitle or DiffBetweenAxeTitleAndSuperiorAxes<=0.02:
# Xy0<0.01
            
            
            for i,XLabel in enumerate(XListTickLabels):
            
                Xbbox=XLabel.get_window_extent()
                Xx0,NXy0=fig.transFigure.inverted().transform((Xbbox.x0,Xbbox.y0))
                
                if Xy0>0:
                    Xy0=min(Xy0,NXy0)
                else:
                    Xy0=max(Xy0,NXy0)

            DiffBetweenTickLabelAndXTitle=Xy0-MinimumSpaceBetwweenTickLabelAndXTitle
            Xy0=99

            
            for i,YLabel in enumerate(YListTickLabels):
    
                Ybbox=YLabel.get_window_extent()
                NYx0,Yy0=fig.transFigure.inverted().transform((Ybbox.x0,Ybbox.y0))
    
                if Yx0>0:
                    Yx0=min(Yx0,NYx0)
                else:
                    Yx0=max(Yx0,NYx0)


            
            Y0BBoxBeforeLastRowAxes=axes[r-1,0].get_position().y0
            Y1BBoxTitleLastRowAxes=axes[r,0].title.get_tightbbox(fig.canvas.get_renderer()).y1
            X1BBoxTitleLastRowAxes=axes[r,0].title.get_tightbbox(fig.canvas.get_renderer()).x1
            TX1BBoxTitleLastRowAxes,TY1BBoxTitleLastRowAxes=fig.transFigure.inverted().transform((X1BBoxTitleLastRowAxes,Y1BBoxTitleLastRowAxes))
            DiffBetweenAxeTitleAndSuperiorAxes=Y0BBoxBeforeLastRowAxes-TY1BBoxTitleLastRowAxes

            # Xy0-MinimumSpaceBetwweenTickLabelAndXTitle>0:

            if DiffBetweenTickLabelAndXTitle<0.02:
                BottomMargin=BottomMargin+0.05

            elif BottomMargin==0:
                BottomMargin=0.1

            # if Xy0<0.01 or DiffBetweenTickLabelAndXTitle<=MinimumSpaceBetwweenTickLabelAndXTitle:
            #     BottomMargin=BottomMargin+0.05
            # elif BottomMargin==0:
            #     BottomMargin=0.1
                # NewPositionXlabel=Xy0-MinimumSpaceBetwweenTickLabelAndXTitle

            if Yx0<0:
                LeftMargin=LeftMargin+0.1
            elif LeftMargin==0:
                LeftMargin=0.125

            if DiffBetweenAxeTitleAndSuperiorAxes<=0.02:#TY1BBoxTitleLastRowAxes>Y0BBoxBeforeLastRowAxes or 
                hspaceMargin=hspaceMargin+0.1
            elif hspaceMargin==0:
                hspaceMargin=0.2

            plt.subplots_adjust(bottom=BottomMargin,left=LeftMargin,hspace=hspaceMargin,top=None)
                  
        # if BottomMargin==0 and LeftMargin==0:

        #     if "m" is ListOfDateAndTime[0] or "s" is ListOfDateAndTime[0]:
        #         plt.subplots_adjust(hspace=2)
        #     else:
        #         plt.subplots_adjust(hspace=0.5)







        # MinTickLabel=99
        # BottomMargin=LeftMargin=hspaceMargin=DiffBetweenTickLabelAndXTitle=0
        # while Xy0<0.01 or Yx0<0 or TY1BBoxBeforeLastRowAxes>Y0BBoxBeforeLastRowAxes or DiffBetweenTickLabelAndXTitle<=0.05:

            
        #     if Xy0<0.01 or DiffBetweenTickLabelAndXTitle<=0.05:
        #         for i,XLabel in enumerate(XListTickLabels):
                
        #             Xbbox=XLabel.get_window_extent()
        #             Xx0,NXy0=fig.transFigure.inverted().transform((Xbbox.x0,Xbbox.y0))

        #             if Xy0>0:
        #                 MinTickLabel=min(MinTickLabel,NXy0)
        #             else:
        #                 Xy0=max(Xy0,NXy0)
        #                 DiffBetweenTickLabelAndXTitle=0
                        
        #         DiffBetweenTickLabelAndXTitle=max(DiffBetweenTickLabelAndXTitle,MinTickLabel-Xy0)
        #         MinTickLabel=99
        #         if Xy0<0.01 or DiffBetweenTickLabelAndXTitle<=0.05:
        #             BottomMargin=BottomMargin+0.1
        #     elif BottomMargin==0:
        #         BottomMargin=0.1

        #     if Yx0<0:
        #         for i,YLabel in enumerate(YListTickLabels):
        
        #             Ybbox=YLabel.get_window_extent()
        #             NYx0,Yy0=fig.transFigure.inverted().transform((Ybbox.x0,Ybbox.y0))
        #             # if NYx0<Yx0 and i!=0:
        #             #     YLabel.set_bbox(dict(facecolor='none', edgecolor='red'))
        #             #     OldYlabel.set_bbox(dict(facecolor='none', edgecolor='none'))
        #             #     OldYlabel=YLabel
        #             # elif i==0:
        #             #     OldYlabel=YLabel
        #             if Yx0>0:
        #                 Yx0=min(Yx0,NYx0)
        #             else:
        #                 Yx0=max(Yx0,NYx0)
        #         LeftMargin=LeftMargin+0.1
        #     else:
        #         LeftMargin=0.125

        #     if TY1BBoxBeforeLastRowAxes>Y0BBoxBeforeLastRowAxes:

        #         Y0BBoxBeforeLastRowAxes=axes[r-1,0].get_position().y0
        #         Y1BBoxTitleLastRowAxes=axes[r,0].title.get_tightbbox(fig.canvas.get_renderer()).y1
        #         X1BBoxTitleLastRowAxes=axes[r,0].title.get_tightbbox(fig.canvas.get_renderer()).x1
        #         TX1BBoxTitleLastRowAxes,TY1BBoxBeforeLastRowAxes=fig.transFigure.inverted().transform((X1BBoxTitleLastRowAxes,Y1BBoxTitleLastRowAxes))
        #         hspaceMargin=hspaceMargin+0.1
        #         # hspaceMargin=0.2
        #     else:
        #         hspaceMargin=0.2
        #     # else:


            
        #     # if Xy0<0 or Yx0<0:
        #     plt.subplots_adjust(bottom=BottomMargin,left=LeftMargin,hspace=hspaceMargin,top=None)
                  
        # if BottomMargin==0 and LeftMargin==0:

        #     if "m" is ListOfDateAndTime[0] or "s" is ListOfDateAndTime[0]:
        #         plt.subplots_adjust(hspace=2)
        #     else:
        #         plt.subplots_adjust(hspace=0.5)


        # BottomMargin=0
        # while Xy0<0 :

        #     plt.subplots_adjust(bottom=BottomMargin,hspace=0.3)
    
        #     for i,XLabel in enumerate(axes[-1,0].xaxis.get_ticklabels()):
            
        #         Xbbox=XLabel.get_window_extent()
        #         Xx0,NXy0=fig.transFigure.inverted().transform((Xbbox.x0,Xbbox.y0))

        #         # if NXy0<Xy0 and i!=0:
        #         #     XLabel.set_bbox(dict(facecolor='none', edgecolor='red'))
        #         #     OldXlabel.set_bbox(dict(facecolor='none', edgecolor='none'))
        #         #     OldXlabel=XLabel
        #         # elif i==0:
        #         #     OldXlabel=XLabel
        #         if Xy0>0:
        #             Xy0=min(Xy0,NXy0)
        #         else:
        #             Xy0=max(Xy0,NXy0)
        #     BottomMargin=BottomMargin+0.1

        # plt.subplots_adjust(hspace=2,top=None)
        # Y1BBoxTitleLastRowAxes=axes[r,0].title.get_tightbbox(fig.canvas.get_renderer()).y1
        # X1BBoxTitleLastRowAxes=axes[r,0].title.get_tightbbox(fig.canvas.get_renderer()).x1

        # X0BBoxBeforeLastRowAxes=axes[r-1,0].get_position().x0
        # Y0BBoxBeforeLastRowAxes=axes[r-1,0].get_position().y0

        # X0BBoxBeforeLastRowAxes=axes[r-1,0].xaxis.get_tightbbox(fig.canvas.get_renderer()).x0
        # Y0BBoxBeforeLastRowAxes=axes[r-1,0].xaxis.get_tightbbox(fig.canvas.get_renderer()).y0



        # TX0BBoxLastRowAxes,TY0BBoxBeforeLastRowAxes=fig.transFigure.inverted().transform((X0BBoxBeforeLastRowAxes,Y0BBoxBeforeLastRowAxes))
        # TX1BBoxTitleLastRowAxes,TY1BBoxBeforeLastRowAxes=fig.transFigure.inverted().transform((X1BBoxTitleLastRowAxes,Y1BBoxTitleLastRowAxes))

        # fig.text(TX1BBoxTitleLastRowAxes,TY1BBoxBeforeLastRowAxes, "Y1BBoxTitleLastRowAxes", ha='center', fontsize=14,)
        # fig.text(TX0BBoxLastRowAxes, TY0BBoxBeforeLastRowAxes, 'Y0BBoxBeforeLastRowAxes', va='center', ha='center', fontsize=14, )

        # fig.text(TX1BBoxTitleLastRowAxes,TY1BBoxBeforeLastRowAxes, "Y1BBoxTitleLastRowAxes", ha='center', fontsize=14,)
        # fig.text(X0BBoxBeforeLastRowAxes, Y0BBoxBeforeLastRowAxes, 'Y0BBoxBeforeLastRowAxes', va='center', ha='center', fontsize=14, )



        # X,Y Axis label
        CommonXLabel="Time ("+','.join(list(map(lambda x: DicoConfigRowColumsSubPlot[x],ListOfDateAndTime[1:])))+")"
        # if Xy0>0:
            
            
        #     fig.text(0.5, NewPositionXlabel*1/2, CommonXLabel, ha='center', fontsize=14,)
        # else:   
        fig.text(0.5, DiffBetweenTickLabelAndXTitle, CommonXLabel, ha='center', fontsize=14,)
        fig.text(Yx0*5/6, 0.5, 'Number of Videos Trending', va='center', ha='center', rotation='vertical', fontsize=14, )

        TitleOfTheEclatedFigure='Number of Videos Trending by '+DicoConfigRowColumsSubPlot[ListOfDateAndTime[0]]+' in function of '+' and '.join(list(map(lambda x: DicoConfigRowColumsSubPlot[x],ListOfDateAndTime[1:])))
        # fig.add_subplot(111, frame_on=False,)
        # plt.tick_params(labelcolor="none", bottom=False, left=False)
        # plt.xlabel(CommonXLabel,fontsize=14,)
        # plt.ylabel("\nNumber of Video Trending",fontsize=14,)
        fig.suptitle(TitleOfTheEclatedFigure, fontsize=16,)
        
        # plt.tight_layout()
        
        # plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)

        # plt.xlabel(CommonXLabel,fontsize=14,)
        # plot_children(fig, fig._layoutbox, printit=False)
        plt.show()
        
        

        for Row in range(DicoConfigRowColumsSubPlot[ListOfDateAndTime[0]][0]):

            FigRow=fig[Row].flatten()

            if DicoConfigRowColumsSubPlot[ListOfDateAndTime[0]][0]%2!=0 and Row%3==1 and Row!=DicoConfigRowColumsSubPlot[ListOfDateAndTime[0]][0]:
                FigRow[0].set_ylabel("Nb. Video Trending")
            elif DicoConfigRowColumsSubPlot[ListOfDateAndTime[0]][0]%2==0 and Row%2==1 and Row!=DicoConfigRowColumsSubPlot[ListOfDateAndTime[0]][0]:
                FigRow[0].set_ylabel("Nb. Video Trending")  
            elif DicoConfigRowColumsSubPlot[ListOfDateAndTime[0]][0]==4:
                FigRow[0].set_ylabel("Nb. Video Trending")
            
            for Column in range(len(FigRow)):
                    FigRow[Column].set_xlabel("Time")

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.5)
        plt.show()

    return df_unstack


def PlotGraph(df,Title,XLabel,YLabel):

    NumberOfVideoTrendingByCountry="Number Of Videos "+Country
    # Create the bar graph with in x axis Label ("HH:MM") and NumberOfVideoTrendingByCountry in y axis

    if isinstance(df, pd.Series):
        df.plot(y=0, kind='bar')
    else:
        df.plot(y=NumberOfVideoTrendingByCountry, kind='bar')
    

    #title of the plot
    plt.title(Title)

    #title of the x axis of the plot
    plt.xlabel(XLabel)

    #title of y axis of the plot
    plt.ylabel(YLabel)

    #show the graph
    plt.show()


IntervalMinute=30
Country="FRA"
ActivatePloting=False
LocalToUTCTime="Local"
FindText=""
CountryGraphInFunctionOfTime(IntervalMinute,Country,ActivatePloting,LocalToUTCTime,FindText)

