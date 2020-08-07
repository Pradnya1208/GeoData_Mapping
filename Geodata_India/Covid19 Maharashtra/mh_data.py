import requests
import csv
import json
import pandas as pd
from pandas import DataFrame as df

JSON_URL = 'https://api.covid19india.org/v5/min/timeseries-MH.min.json'
JSON_INDIA = 'https://api.covid19india.org/v5/min/timeseries.min.json'

dist_name  = []
covidData =[]
covidRec = []
covidDeath = []

dtcolNames =[]

req = requests.get(JSON_URL)
req_India = requests.get(JSON_INDIA)

# TODO List for State codes and iterate on it in single class

distNames = df(req.json()['MH']['districts'])
distNames = distNames.T

for dis in distNames.index:
    dist_name.append(dis)

date_ = df(req_India.json()['TT'])
for dt in date_.index:
    dtcolNames.append(dt + ",")



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
        
                
        for conf, dt in zip(covid.dates, covid.index):
            dt = dt + ","
            i+=1
            index = dtcolNames.index(dt) + 1
            if i!= index:
                #print("city:" +  dist + ":" + dt + ": Ind:" + str(index) + ": i :" + str(i))
                for n in range(index-1):
                    covidData.append("0,")
                    covidRec.append("0,")
                    covidDeath.append("0,")
                i = index
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
                                
   
with open('Maharashtra_total_confirmed_cases.csv', 'w') as f:
    f.writelines("Cities,")
    f.writelines(dtcolNames)
    f.writelines(covidData)
    
with open('Maharashtra_total_recovered_cases.csv', 'w') as f:
    f.writelines("Cities,")
    f.writelines(dtcolNames)
    f.writelines(covidRec)

with open('Maharashtra_total_Death_toll.csv', 'w') as f:
    f.writelines("Cities,")
    f.writelines(dtcolNames)
    f.writelines(covidDeath)


    


