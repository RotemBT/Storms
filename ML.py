import pandas as pd
from sklearn import metrics
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score

df = pd.read_csv('addingBeaufort.csv')
bins = [0, 1, 3, 7, 12, 18, 24, 31, 38, 46, 54, 63, 72, 250]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# https://en.wikipedia.org/wiki/Beaufort_scale
df['beaufort_scale'] = pd.cut(df['wind_power'], bins, labels=labels)
df['Ocean'] = df['Ocean'].astype('category')
df['ocean_code'] = df['Ocean'].cat.codes

X = df.loc[:, ~df.columns.isin(
    ['storm_name', 'time', 'wind_power', 'storm_type', 'Ocean', 'ocean_code', 'beaufort_scale'])]
y = df['wind_power']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, shuffle=False)
model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)
print(r2_score(y_test, y_pred))
lat = float(input("Please enter Latitude value: "))
long = float(input("Please enter Longitude value: "))
pressure = float(input("Please enter air pressure value: "))
year, month, day = map(int, input('Enter a date in date format: year month day').split(' '))

while (-90 <= lat <= 90 and -180 <= long <= 180):
    print(
        '\nPrediction of wind power is : {:.1f} mph\n'.format(
            round(float(model.predict([[year, pressure, lat, long, month, day]])[0]))))
    lat = float(input("Please enter Latitude value: "))
    long = float(input("Please enter Longitude value: "))
    pressure = float(input("Please enter air pressure value: "))
    year, month, day = map(int, input('Enter a date in date format: year month day').split(' '))

print('Input is out of range!')


def getWindFromLinearModel(df, lat, long, pressure, year, month, day):
    X = df.loc[:, ~df.columns.isin(
        ['storm_name', 'time', 'wind_power', 'storm_type', 'Ocean', 'ocean_code', 'beaufort'])]
    y = df['wind_power']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, shuffle=False)
    model = LinearRegression().fit(X_train, y_train)
    lat = lat
    long = long
    pressure = pressure
    year, month, day = year, month, day
    return round(float(model.predict([[year, pressure, lat, long, month, day]])[0]))


# Logistic Regression by beaufort split (windy ,low, med, high)
dfBeaufortScaleLessThan5 = df[df['beaufort_scale'] < 5].reset_index(drop=True)
dfBeaufortScaleBetween5To8 = df[(df['beaufort_scale'] >= 5) & (df['beaufort_scale'] <= 8)].reset_index(drop=True)
dfBeaufortScaleBetween9To11 = df[(df['beaufort_scale'] >= 9) & (df['beaufort_scale'] <= 11)].reset_index(drop=True)
dfBeaufortScaleHigherThan12 = df[(df['beaufort_scale'] >= 12)].reset_index(drop=True)
dfBeaufortScaleHigherThan12['beaufort'] = 3
dfBeaufortScaleBetween9To11['beaufort'] = 2
dfBeaufortScaleBetween5To8['beaufort'] = 1
dfBeaufortScaleLessThan5['beaufort'] = 0
df = pd.concat(
    [dfBeaufortScaleHigherThan12, dfBeaufortScaleBetween9To11, dfBeaufortScaleBetween5To8, dfBeaufortScaleLessThan5],
    ignore_index=True).drop(['beaufort_scale'], axis=1)
X = df.loc[:, ~df.columns.isin(
    ['storm_name', 'time', 'storm_type', 'Ocean', 'ocean_code', 'beaufort'])]
y = df['beaufort']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)
scaler = MinMaxScaler(feature_range=(0, 1))
X_train_scaled = scaler.fit_transform(X_train)
model = LogisticRegression().fit(X_train_scaled, y_train)

scaler.fit(X_test)
latitude = float(input("Please enter Latitude value: "))
longitude = float(input("Please enter Longitude value: "))
airPressure = float(input("Please enter air pressure value: "))
y, m, d = map(int, input('Enter a date in date format: year month day').split(' '))
wind = getWindFromLinearModel(df, latitude, longitude, airPressure, y, m, d)
cords = scaler.transform([[y, wind, airPressure, latitude, longitude, m, d]])
predicted_values = model.predict_proba(cords)[0]
y_predict = model.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_predict))
print("Precision:", metrics.precision_score(y_test, y_predict, average='macro'))
print("Recall:", metrics.recall_score(y_test, y_predict, average='macro'))
while (-90 <= latitude <= 90 and -180 <= longitude <= 180):
    windyP, lowP, medP, highP = predicted_values[0] * 100, predicted_values[1] * 100, predicted_values[2] * 100, \
                                predicted_values[3] * 100
    print(
        'Coordinates ({}, {}):\nA windy storm probability: {:.2f}%\nTropical Depression probability: {:.2f}%\n'
        'Tropical Storm probability: {:.2f}%\nA deadly storm probability: {:.2f}%\n'.format(
            latitude, longitude, windyP, lowP, medP, highP))
    latitude = float(input("Please enter Latitude value: "))
    longitude = float(input("Please enter Longitude value: "))
    airPressure = float(input("Please enter air pressure value: "))
    y, month, day = map(int, input('Enter a date in date format: year month day').split(' '))
    wind = getWindFromLinearModel(df, latitude, longitude, airPressure, y, m, d)
    cords = scaler.transform([[y, wind, airPressure, latitude, longitude, m, d]])
    predicted_values = model.predict_proba(cords)[0]
print('Input is out of range!')
