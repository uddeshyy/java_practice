import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
import xlsxwriter


my_columns = ['Time', 'Price']

df = pd.DataFrame(columns = my_columns)

cc_call = requests.get(f'https://min-api.cryptocompare.com/data/v2/histohour?fsym=STX&tsym=INR&limit=153&toTs=-1').json()

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
df['MA 9'] = df.Price.rolling(9).mean()
df['MA 21'] = df.Price.rolling(21).mean()
df['MA 55'] = df.Price.rolling(55).mean()
df.dropna(0, inplace = True)
df.reset_index(drop = True, inplace = True)
df = df[50:]
i = len(df.index) - 1
value = 0
while(df.iloc[i]['MA 9'] > df.iloc[i]['MA 21'] and df.iloc[i]['MA 9'] > df.iloc[i]['MA 55']):
  value = max(df.iloc[i]['MA 9'], value)
  i = i-1

print(i)
print(df.iloc[i])
print(df)
df.plot()
plt.show()
