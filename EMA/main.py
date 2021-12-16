from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time




list_of_cryptos = []
cryptos_to_buy = []
my_columns = ['Time', 'Price']

unit = str(input('Enter time unit (minute,hour,day) \n'))


wrx_call = requests.get('https://api.wazirx.com/api/v2/tickers').json()
##print(wrx_call['btcinr']['last'])
##print(len(wrx_call))
for coin in wrx_call:
  for data in coin:
    if (float(wrx_call[coin]['last'])!=0 and wrx_call[coin]['quote_unit'] == "inr"):
      list_of_cryptos.append(wrx_call[coin]['base_unit'].upper())

list_of_cryptos = set(list_of_cryptos)






for crypto in (list_of_cryptos):  
  df = pd.DataFrame(columns = my_columns)
##  print('Starting' , crypto)
  cc_call = requests.get(f'https://min-api.cryptocompare.com/data/v2/histo{unit}?fsym={crypto}&tsym=INR&limit=153&toTs=-1').json()

  if(cc_call['Response'] == 'Success'):
    for data in cc_call['Data']['Data']:
      df = df.append(
        pd.Series([
          datetime.fromtimestamp(int(data['time'])).strftime('%d-%b-%Y %I:%M:%S'),
          data['close']
          ],index = my_columns),
        ignore_index = True
        )

    df.Time = pd.to_datetime(df.Time)
    ##df = df.set_index('Time')
    df['MA 9'] = df.Price.rolling(9).mean()
    df['MA 21'] = df.Price.rolling(21).mean()
    df['MA 55'] = df.Price.rolling(55).mean()
    df.dropna(0, inplace = True)
    i = len(df.index) - 1
    value = 0
    flag = False
    while(df.iloc[i]['MA 9'] > df.iloc[i]['MA 21'] and df.iloc[i]['MA 9'] > df.iloc[i]['MA 55']):
      flag = True
      value = max(df.iloc[i]['MA 9'], value)
      i = i-1
##    if(value == df.iloc[-1]['MA 9']):
##      cryptos_to_buy.append(crypto)
    if(i > (len(df.index) - 5) and flag and value == df.iloc[-1]['MA 9']):
      cryptos_to_buy.append(crypto)
    del df
    print(crypto, 'Done')

  else:
    print(crypto,'Not found')




print(cryptos_to_buy)
