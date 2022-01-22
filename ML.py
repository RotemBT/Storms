import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler, StandardScaler, normalize
from sklearn.model_selection import train_test_split

df = pd.read_csv('addingBeaufort.csv')
bins = [0, 1, 3, 7, 12, 18, 24, 31, 38, 46, 54, 63, 72, 250]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# https://en.wikipedia.org/wiki/Beaufort_scale
df['beaufort_scale'] = pd.cut(df['wind_power'], bins, labels=labels)
df['Ocean'] = df['Ocean'].astype('category')
df['ocean_code'] = df['Ocean'].cat.codes
print(df['beaufort_scale'].max())
print(df['beaufort_scale'].min())
X = df[df.columns[
    (df.columns != 'Ocean') & (df.columns != 'storm_name') & (df.columns != 'time') & (df.columns != 'storm_type')]]
y = df['wind_power']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)
model = sklearn.linear_model.LinearRegression().fit(X_train, y_train)
