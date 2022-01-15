import pandas as pd

from AcquisitionHelper import *


start = time.time()

scrapData()
df = getDataFrame(stormsName, yearOfStorm, oceans, dates, hours, windPower, airPressure,
                  stormType, latCorr, longCorr)

sendToCSV(df, 'demo.csv')

print(f'The time to scrap from Wunderground is : {time.time() - start}')


"""# concat csv files
listOfFiles = ['atlantic_ocean.csv', 'central_pacific.csv', 'east_pacific.csv',
               'indian_ocean.csv', 'Southern_Hemisphere.csv', 'western_pacific.csv']
mergeCSV =pd.concat([pd.read_csv(f) for f in listOfFiles])
print(mergeCSV)
mergeCSV.to_csv('storms.csv', index=False)"""
"""df = pd.read_csv('western_pacific.csv')
df[['Month', 'Day','year']] = df.date.str.split("/", expand=True)
df.drop(['date'], axis = 1, inplace = True)

print(df)"""
