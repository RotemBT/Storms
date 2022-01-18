import cmath
import math

import numpy as np
import pandas as pd


def removeDuplicatives(df):
    return df.drop_duplicates().copy()


df = pd.read_csv('stormsDate.csv')
indexNames = df[(df['storm_type'] == 'Unknown')].index


def windSpeedToPressure(windSpeedInMPH):
    windSpeedInMS = windSpeedInMPH * 0.44704
    return round(1014.9 - 0.361451 * windSpeedInMS - 0.00259 * windSpeedInMS ** 2)


def pressureToWindSpeed(pressure):
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
    print(dataframe['wind_power'])
    return dataframe


df[df['Ocean'].str.contains('Pacific')] = manipulatePacific(df[df['Ocean'].str.contains('Pacific')])
print(df[df['Ocean'].str.contains('Pacific')]['wind_power'])
