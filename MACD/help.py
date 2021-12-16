import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

my_columns = ['Time', 'Price']


df = pd.DataFrame(columns = my_columns)

cc_call = requests.get(f'https://min-api.cryptocompare.com/data/v2/histoday?fsym=HOT&tsym=INR&limit=100&toTs=-1').json()

if(cc_call['Response'] == 'Success'):
  for data in cc_call['Data']['Data']:
    df = df.append(
      pd.Series([
        datetime.fromtimestamp(int(data['time'])).strftime('%d-%b-%Y %I:%M:%S'),
        data['close']
        ],index = my_columns),
      ignore_index = True
      )

##df.Time = pd.to_datetime(df.Time)
##df = df.set_index('Time')
df.reset_index(drop = True, inplace = True)
print(len(df.index))
ma_12 = df.Price.ewm(span = 12, adjust = False).mean()
ma_26 = df.Price.ewm(span = 26, adjust = False).mean()
df['Main'] = ma_12 - ma_26
df['Trend'] = df['Main'].ewm(span = 9, adjust = False).mean()
df.drop(['Price'], axis=1, inplace=True)
##df.dropna(0, inplace = True)
##df.reset_index(drop = True, inplace = True)
i = len(df.index) - 1
value = df.iloc[i]['Main']
while(df.iloc[i]['Main'] > df.iloc[i]['Trend']):
  value = max(df.iloc[i]['Main'], value)
  i = i-1

print(value == df.iloc[-1]['Main'])
print(i)
print(df)
df.plot()
plt.show()
