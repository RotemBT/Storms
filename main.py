from AcquisitionHelper import *

df = pd.read_csv('storms.csv')


print(df)
df.to_csv('stormsDate.csv', index=False)
