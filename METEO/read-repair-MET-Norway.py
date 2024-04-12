import requests
import json
import datetime
import random
import numpy as np
import pandas as pd
import seaborn as sb

import matplotlib.pyplot as plt

plt.style.use('ggplot')


#firstDate = '2023-07-19T21:00:00'
firstDate = '2024-03-31T15:00:00'
lastDate = '2024-04-05T15:00:00'
timeHelper = (datetime.datetime.strptime(lastDate, '%Y-%m-%dT%H:%M:%S') - datetime.datetime.strptime(firstDate, '%Y-%m-%dT%H:%M:%S'))

filesNo = 1 + (timeHelper.days*24 + timeHelper.seconds//3600) // 6

print(f"You have {filesNo} MET-Norway files")

############################################################################ read first file to build df structure
f = open(f'/home/lali/TITAN-ROG-sync/python/METEO/bkp/MET-Norway-{firstDate}.json',)
data = json.load(f)
f.close()

nowTime = datetime.datetime.strptime(data['RO']['now'], '%Y-%m-%dT%H:%M:%S')
nowTemp = data['RO']['temp']

allData = pd.DataFrame(columns = ['Date', 'Real'])
for i in range(len(data['METNO'])):
    prognosisTime = datetime.datetime.strptime(data['METNO'][i]['now'], '%Y-%m-%dT%H:%M:%S')
    prognosisTemp = data['METNO'][i]['temp']
    deltaTime = prognosisTime - nowTime
    diferenta = deltaTime.days*24 + deltaTime.seconds//3600
    allData[diferenta] = []

newRowDict = {'Date':firstDate}
newRowDF = pd.DataFrame([newRowDict])
allData = pd.concat([allData, newRowDF])
for i in range(filesNo + len(data['METNO'])):
    intermDate = datetime.datetime.strptime(firstDate, '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=6*(i+1))
    newRowDict = {'Date':intermDate.isoformat()}
    newRowDF = pd.DataFrame([newRowDict])
    #newRowDF.reset_index(drop=True, inplace=True)
    #allData.reset_index(drop=True, inplace=True)
    allData = pd.concat([allData, newRowDF])
    allData.reset_index(drop=True, inplace=True)

allData = allData.set_index('Date')
#print(allData)
##################################################################### df ready

for i in range(filesNo):
#for i in range(2):
    fileTime = (datetime.datetime.strptime(firstDate, '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=6*i)).isoformat()
    f = open(f'/home/lali/TITAN-ROG-sync/python/METEO/bkp/MET-Norway-{fileTime}.json',)
    print(f"reading {fileTime}")
    data = json.load(f)
    f.close()
    allData.at[fileTime, 'Real'] = data['RO']['temp']
    nowTime = datetime.datetime.strptime(data['RO']['now'], '%Y-%m-%dT%H:%M:%S')
    for i in range(len(data['METNO'])):
        prognosisTime = datetime.datetime.strptime(data['METNO'][i]['now'], '%Y-%m-%dT%H:%M:%S')
        prognosisTemp = data['METNO'][i]['temp']
        deltaTime = prognosisTime - nowTime
        diferenta = deltaTime.days*24 + deltaTime.seconds//3600
        allData.at[data['METNO'][i]['now'], diferenta] = prognosisTemp
    lastPrognosisTime = prognosisTime
    if ( (len(data['METNO']) < 15) ):
        for j in range(len(data['METNO'])+1, 39):
            prognosisTime = lastPrognosisTime + datetime.timedelta(hours=((j-len(data['METNO']))*6))
            prognosisTemp = 50
            deltaTime = prognosisTime - nowTime
            diferenta = deltaTime.days*24 + deltaTime.seconds//3600
            allData.at[prognosisTime.strftime("%Y-%m-%dT%H:%M:%S"), diferenta] = prognosisTemp

nowTime = datetime.datetime.strptime(firstDate, '%Y-%m-%dT%H:%M:%S')
for i in range(57):
    diferenta = 0
    theTemp = allData.at[nowTime.strftime("%Y-%m-%dT%H:%M:%S"), diferenta]
    for j in range(37):
        diferenta = diferenta + 6
        myTemp = allData.at[nowTime.strftime("%Y-%m-%dT%H:%M:%S"), diferenta]
        theRandom = (random.random() - 0.5) / 1.0
        if (myTemp > 45):
            allData.at[nowTime.strftime("%Y-%m-%dT%H:%M:%S"), diferenta] = theTemp + theRandom
        else:
            theTemp = myTemp
    nowTime = nowTime + datetime.timedelta(hours=6)

allDataDiff = allData.copy()
for index, row in allDataDiff.iterrows():
    for i in np.arange(0, 230, 6):
        allDataDiff.at[index, i] = allDataDiff.at[index, i] - allDataDiff.at[index, 'Real']

for i in range(filesNo):
#for i in range(2):
    fileTime = (datetime.datetime.strptime(firstDate, '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=6*i)).isoformat()
    
    fileName = f'/home/lali/TITAN-ROG-sync/python/METEO/repair/MET-Norway-{fileTime}.json'
    
    currentTime = datetime.datetime.strptime(firstDate, '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=6*(i))
    currentTemp = allData.at[currentTime.strftime("%Y-%m-%dT%H:%M:%S"), 'Real']

    myDict = {}
    myDict["RO"] = {"now": f"{currentTime.isoformat()}", "temp": float(currentTemp)}
    myDict["METNO"] = []
    for j in range(38):
        prognosisTime = currentTime + datetime.timedelta(hours=6*j)
        deltaTime = prognosisTime - currentTime
        diferenta = deltaTime.days*24 + deltaTime.seconds//3600
        prognosisTemp = round(allData.at[prognosisTime.strftime("%Y-%m-%dT%H:%M:%S"), diferenta], 1)
        myDict["METNO"].append({"now": f"{prognosisTime.isoformat()}", "temp": prognosisTemp})

    with open(fileName, "w") as outfile:
        outfile.write(json.dumps(myDict, indent=4)) 







print(allDataDiff)

#allData.to_csv('/home/lali/TITAN-ROG-sync/python/METEO/MET-Norway.csv')
#allDataDiff.to_csv('/home/lali/TITAN-ROG-sync/python/METEO/MET-Norway-diff.csv')

if (False):
    if (False): #True pentru diferenta
        allDataDiffPlot = allDataDiff.replace(np.nan,0)
        del allDataDiffPlot['Real']
        ax = sb.heatmap(allDataDiffPlot, annot = False, linewidths = 0, cmap="vlag", vmin=-15, vmax=15)
    else:
        allDataPlot = allData.replace(np.nan,0)
        ax = sb.heatmap(allDataPlot, annot = False, linewidths = 0, cmap="vlag")
    plt.show()