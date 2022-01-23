import math
import time
import numpy as np
import pandas as pd

df = pd.read_csv('stormsDate.csv')


def windSpeedToPressure(windSpeedInMPH):
    windSpeedInMS = windSpeedInMPH * 0.44704
    return round(1014.9 - 0.361451 * windSpeedInMS - 0.00259 * windSpeedInMS ** 2)


def pressureToWindSpeed(pressure):
    # Only in Pacific Ocean
    # https://sciencing.com/convert-wind-speed-pressure-5814125.html
    # convertor -https://www.metric-conversions.org/speed/miles-per-hour-to-meters-per-second.htm
    a = -0.00259
    b = -0.361451
    c = 1014.9 - pressure
    try:
        d = (b ** 2) - (4 * a * c)
        sol1 = (-b - math.sqrt(d)) / (2 * a)
        sol2 = (-b + math.sqrt(d)) / (2 * a)
        return round(max(sol1, sol2))
    except:
        return None


def manipulatePacific(df):
    dataframe = df.copy()
    for ind, row in dataframe.iterrows():
        if math.isnan(row['air_pressure']) and row['wind_power'] > 0:
            dataframe.loc[ind, 'air_pressure'] = float(windSpeedToPressure(row['wind_power']))
        elif row['air_pressure'] is not None and row['wind_power'] <= 0.0:
            dataframe.loc[ind, 'wind_power'] = pressureToWindSpeed(row['air_pressure'])
    return dataframe


def fillMissingWindOrPressure(df, columnName, compareTo):
    missingValues = df[np.logical_or(df[columnName] == 0.0, df[columnName].isnull())].index
    for ind in missingValues:
        row = df.loc[ind].copy()
        columnValues = df[np.logical_and(row['Ocean'] == df['Ocean'],
                                         row[compareTo] == df[compareTo])][columnName]
        df.loc[ind, columnName] = columnValues[columnValues != 0].median()


start = time.time()

# remove storms without lan and long coordinate.
df.dropna(subset=['lat', 'long'], axis=0, inplace=True)
# fill air_pressure column
fillMissingWindOrPressure(df, 'air_pressure', 'wind_power')
# fill wind_power column
fillMissingWindOrPressure(df, 'wind_power', 'air_pressure')
# remove storms with wrong wind_power calculation.
df.drop(df[df['wind_power'] <= 0].index, inplace=True)
# remove last missing values
df.dropna(axis=0, inplace=True)
# drop duplicates
df.drop_duplicates()
print(df)
df.to_csv('rotem1.csv', index=False)
# take 14 min
print(f'The time is {time.time() - start}')
