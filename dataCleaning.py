import cmath
import math

import pandas as pd


def removeDuplicatives(df):
    return df.drop_duplicates().copy()


df = pd.read_csv('stormsDate.csv')
indexNames = df[(df['storm_type'] == 'Unknown')].index

print(indexNames)
print(df.iloc[indexNames])
print(df.duplicated().sum())
print(removeDuplicatives(df))
print(df.dropna(thresh=len(df.columns)-2))
def squareEqution(a,b,c):
    # https://sciencing.com/convert-wind-speed-pressure-5814125.html
    # convertor -https://www.metric-conversions.org/speed/miles-per-hour-to-meters-per-second.htm
    try:
        d = (b**2) -(4*a*c)
        sol1 = (-b-math.sqrt(d))/(2*a)
        sol2 = (-b+math.sqrt(d))/(2*a)
        print("Solution are {0} and {1}".format(sol1,sol2))
    except:
        return None
squareEqution(-0.00259,-0.31451,1020-1008)