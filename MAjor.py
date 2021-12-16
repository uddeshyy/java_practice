from datetime import datetime
import requests
import pandas as pd
from pushbullet import Pushbullet
##import matplotlib.pyplot as plt
##from datetime import datetime
##import time


list_of_cryptos = []
cryptos_to_buy = []
my_columns = ['Time', 'Price']
key = 'o.UwBSW2wXpg6KbhO3UA73o33QWQkcrjED'



def calculate_EMA(df):
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
  if(i > (len(df.index) - 5) and flag and value == df.iloc[-1]['MA 9']):
    return True
  return False


def calculate_MACD(df):
  df = df[54:]
  df.reset_index(drop = True, inplace = True)
  ma_12 = df.Price.ewm(span = 12, adjust = False).mean()
  ma_26 = df.Price.ewm(span = 26, adjust = False).mean()
  df['Main'] = ma_12 - ma_26
  df['Trend'] = df['Main'].ewm(span = 9, adjust = False).mean()
  df.drop(['Price'], axis=1, inplace=True)
  i = len(df.index) - 1
  value = df.iloc[i]['Main']
  flag = False
  while(df.iloc[i]['Main'] > df.iloc[i]['Trend']):
    flag = True
    value = max(df.iloc[i]['Main'], value)
    i = i-1
  if(value == df.iloc[-1]['Main'] and flag):
    return True
  return False






unit = str(input('Enter time unit (minute,hour,day) \n'))


wrx_call = requests.get('https://api.wazirx.com/api/v2/tickers').json()
for coin in wrx_call:
  for data in coin:
    if (float(wrx_call[coin]['last'])!=0 and wrx_call[coin]['quote_unit'] == "inr"):
      list_of_cryptos.append(wrx_call[coin]['base_unit'].upper())

list_of_cryptos = set(list_of_cryptos)

EMA_list = []
MACD_list = []



for crypto in (list_of_cryptos):
  df = pd.DataFrame(columns = my_columns)
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
    if(calculate_EMA(df)):
      EMA_list.append(crypto)

    if(calculate_MACD(df)):
      MACD_list.append(crypto)

    print(crypto, 'Done')
  else:
    print(crypto, 'Not Found')


intersection = set(EMA_list) & set(MACD_list)
text = 'EMA Prediction:  ' + str(EMA_list) + '\nMACD Prediction:  ' + str(MACD_list) +  '\nIntersection(Strong Signal):' + str(intersection)
print('EMA Prediction: ' ,EMA_list)
print('MACD Prediction: ' , MACD_list)
print('Intersection(Strong Signal): ', intersection)

pb = Pushbullet(key)
ps = pb.push_note(str(datetime.today().strftime('%d-%b-%Y'))+" Report",text)





