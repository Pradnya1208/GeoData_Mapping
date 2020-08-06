import requests
import csv
import json
import pandas as pd
from pandas import DataFrame as df
JSON_URL = 'https://api.covid19india.org/v5/min/timeseries-MH.min.json'

dist_name  = []
colNames = ['Districts,']
covidData =[]
dateCol =[] 
#df = pd.read_json(JSON_URL)
req = requests.get(JSON_URL)


distNames = df(req.json()['MH']['districts'])
distNames = distNames.T


for dis in distNames.index:
    dist_name.append(dis)


# In case of fixed Dates
#dates = df(req.json()['MH']['districts'][dist_name[0]])
#for dt in dates.index:
#    colNames.append(dt + ",")
    


for dist  in dist_name:   
    
    if not 'Unknown' in dist:
        i=0
        covidData.append('\n')
        covidData.append(dist + ",")
        covid = df(req.json()['MH']['districts'][dist])
        
        
        for dates in covid.index:
            i+=1          
            if dates not in dateCol:
                dateCol.append(dates)
               
            if i != dateCol.index(dates)+1:
         
                print(str(i) + ":" + str(dateCol.index(dates)+1))
                i = dateCol.index(dates)+1
                for x in range (dateCol.index(dates)):    
                    covidData.append("0,")
                
        # in case of fixed Dates
        #if  len(covid.index) != len(colNames)-1:
            #nullVal = (len(colNames)-1) - len(covid.index)
            #print(nullVal)
            #for x in range (nullVal):    
             #   covidData.append("0,")
         
                
        for conf in covid.dates:
            covidData.append(str(conf['total']['confirmed']) + ",")
            #print(dist  + " : " + str(d['total']['confirmed']))
                      

for elem in dateCol:
    colNames.append(elem + ",")
    
with open('Maharashtra_total_confirmed_cases.csv', 'w') as f:
    f.writelines(colNames)
    f.writelines(covidData)



    


