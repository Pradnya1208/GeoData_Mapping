import requests
import csv
import json
import pandas as pd
from pandas import DataFrame as df

JSON_URL = 'https://api.covid19india.org/v5/min/timeseries.min.json'

state_name  = []
dtcolNames =[]
covidData =[]
covidRec = []
covidDeath = []
dateCol =[]

req = requests.get(JSON_URL)


stateNames = df(req.json())
statesData = stateNames.T

# TODO : compare with QGIS names
# (Statecode)TT for India
for st in statesData.index:
     state_name.append(st)


# # In case of fixed Dates
date_ = df(req.json()['TT'])
for dt in date_.index:
    dtcolNames.append(dt + ",")
    


for state in state_name:   
    
    if not 'Unknown' in state:
        i=0
        covidData.append('\n')
        covidRec.append('\n')
        covidData.append(state + ",")
        covidRec.append(state + ",")
        covidDeath.append('\n')
        covidDeath.append(state + ",")
        covid = df(req.json()[state])     
                
        for conf, dt in zip(covid.dates, covid.index):
            dt = dt + ","
            i+=1
            index = dtcolNames.index(dt) + 1
            if i!= index:
                print("State:" +  state + ":" + dt + ": Ind:" + str(index) + ": i :" + str(i))
                for n in range(index-1):
                    covidData.append("0,")
                    covidRec.append("0,")
                    covidDeath.append("0,")
                i = index
            # TODO : Data cleaning for Missing values                
                
            
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
              
     # TODO :check last date value of state and Compare it with ideal last value               
# TODO: Delta and no of tests
                                

    
with open('Indian_States_total_confirmed_cases.csv', 'w') as f:
    f.writelines("State Code,")
    f.writelines(dtcolNames)
    f.writelines(covidData)
    
with open('Indian_States_total_recovered_cases.csv', 'w') as f:
    f.writelines("State Code,")
    f.writelines(dtcolNames)
    f.writelines(covidRec)

with open('Indian_States_total_Death_toll.csv', 'w') as f:
    f.writelines("State Code,")
    f.writelines(dtcolNames)
    f.writelines(covidDeath)


    


