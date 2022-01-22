import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, f1_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame(pd.read_csv('addingBeaufort.csv'))
scaler = MinMaxScaler(feature_range=(0, 1))
std = StandardScaler()
X = df.loc[:, ~df.columns.isin(
    ['storm_name', 'time', 'wind_power', 'storm_type', 'Ocean','ocean_code'
     ,'curr_date','beaufort_scale'])]
y = df['wind_power']
print(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, shuffle=False)
model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)
print(r2_score(y_test, y_pred))
print(model.predict([[1951, 980, 20, 105, 10, 3]]))
"""
lat = float(input("Please enter Lat value: "))
long = float(input("Please enter Long value: "))
date_entry = float(input('Enter a date in Month format'))
year, month, day = map(int, date_entry.split('-'))
date = float(datetime.date(year, month, day).strftime('%Y%m%d'))

while (-90 <= lat <= 90 and -180 <= long <= 180):
    userInput = [lat, long, date_entry]
    # userInput=scaler.fit_transform(userInput)
    print(
        'Prediction of wind power is : {:.1f} mph'.format(round(float(model.predict([[lat, long, date_entry]])[0]))))
    lat = float(input("Please enter Lat value: "))
    long = float(input("Please enter Long value: "))
    date_entry = float(input('Enter a date in Month format'))

print('Input is out of range!')
"""
"""
bins = [0, 1, 3, 7, 12, 18, 24, 31, 38, 46, 54, 63, 72, 250]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# https://en.wikipedia.org/wiki/Beaufort_scale
df['beaufort_scale'] = pd.cut(df['wind_power'], bins, labels=labels)
df['Ocean'] = df['Ocean'].astype('category')
df['ocean_code'] = df['Ocean'].cat.codes
df['curr_date'] = df.apply(
    lambda row: datetime.datetime.strptime(f"{int(row.year)}-{int(row.Month)}-{int(row.Day)}", '%Y-%m-%d'), axis=1)
df["curr_date"] = df["curr_date"].dt.strftime('%Y%m%d').astype(float)
df.drop('Unnamed: 0', 1,inplace=True)
df.to_csv('addingBeaufort.csv', index=False)"""
