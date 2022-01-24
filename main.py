from AcquisitionHelper import *

df = pd.read_csv('storms.csv')
df[['Month', 'Day', 'year']] = df.date.str.split("/", expand=True)
df.drop(['date'], axis=1, inplace=True)

print(df)
df.to_csv('stormsDate.csv', index=False)
