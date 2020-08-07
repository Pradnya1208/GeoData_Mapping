import requests
import csv
import json
import pandas as pd
from pandas import DataFrame as df
JSON_URL = 'https://api.covid19india.org/v5/min/timeseries-MH.min.json'

dist_name  = []
colNames = ['Districts,']
covidData =[]
covidRec = []
covidDeath = []
dateCol =[]
keys = [] 
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
        covidRec.append('\n')
        covidData.append(dist + ",")
        covidRec.append(dist + ",")
        covidDeath.append('\n')
        covidDeath.append(dist + ",")
        
        covid = df(req.json()['MH']['districts'][dist])
        
        
        for dates in covid.index:
            i+=1          
            if dates not in dateCol:
                dateCol.append(dates)
               
            if i != dateCol.index(dates)+1:
         
                #print(str(i) + ":" + str(dateCol.index(dates)+1))
                i = dateCol.index(dates)+1
                for x in range (dateCol.index(dates)):    
                    covidData.append("0,")
                    covidRec.append("0,")
                    covidDeath.append("0,")
                
        # in case of fixed Dates
        #if  len(covid.index) != len(colNames)-1:
            #nullVal = (len(colNames)-1) - len(covid.index)
            #print(nullVal)
            #for x in range (nullVal):    
             #   covidData.append("0,")
         
                
        for conf in covid.dates:
            for t in conf.keys():
                if 'total' in t:
                    if 'confirmed' in (conf['total'].keys()):
                        covidData.append(str(conf['total']['confirmed']) + ",")
                    if not 'confirmed' in (conf['total'].keys()):
                        covidData.append("0,")
                        
                    if 'recovered' in (conf['total'].keys()):
                        covidRec.append(str(conf['total']['recovered']) + ",")
                    if not 'recovered' in (conf['total'].keys()):
                        covidRec.append("0,")
                        
                    if 'deceased' in (conf['total'].keys()):
                        covidDeath.append(str(conf['total']['deceased']) + ",")
                    if not 'deceased' in (conf['total'].keys()):
                        covidDeath.append("0,")
                        
# TODO: Delta and no of tests
                                
                      

for elem in dateCol:
    colNames.append(elem + ",")
    
with open('Maharashtra_total_confirmed_cases.csv', 'w') as f:
    f.writelines(colNames)
    f.writelines(covidData)
    
with open('Maharashtra_total_recovered_cases.csv', 'w') as f:
    f.writelines(colNames)
    f.writelines(covidRec)

with open('Maharashtra_total_Death_toll.csv', 'w') as f:
    f.writelines(colNames)
    f.writelines(covidDeath)


    


