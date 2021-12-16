import requests 
import pandas as pd
from datetime import datetime
import mplfinance as mpl

fsym = str(input('Enter from symbol : ')).upper()
tsym = str(input('Enter to symbol : ')).upper()

print(fsym,tsym)
my_columns = ['time','open', 'close', 'high', 'low', 'volume']
api_call = requests.get(f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={fsym}&tsym={tsym}&limit=150&toTs=-1').json()
df = pd.DataFrame(columns = my_columns)

if(api_call['Response'] != 'Success'):
    print('Crypto Error')

for row in api_call['Data']['Data']:
    df = df.append(
        pd.Series([
            datetime.fromtimestamp(int(row['time'])).strftime('%d-%b-%Y %I:%M:%S'),
            float(row['open']),
            float(row['close']),
            float(row['high']),
            float(row['low']),
            float(row['volumefrom'])
            ],index=my_columns),
        ignore_index=True)

df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace = True)

len(df)

def support(df, pv_point, start, end):
    for i in range(pv_point-start +1 , pv_point+1):
        if(df.low[i] > df.low[i-1]):
            return False
    for i in range(pv_point+1, pv_point+end - 1 ):
        if(df.low[i] < df.low[i-1]):
            return False
    return True

def resistance(df, pv_point, start, end):
    for i in range(pv_point-start+1, pv_point+1):
        if(df.high[i] < df.high[i-1]):
            return False
    for i in range(pv_point+1, pv_point+end-1):
        if(df.high[i] > df.high[i-1]):
            return False
    return True

sup_points = []
res_points = []

start = int(input('Start interval: '))
end = int(input('End interval: '))

for i in range(start, len(df)-1):
    if support(df,i,start,end):
        sup_points.append(df.low[i])
    if resistance(df,i,start,end):
        res_points.append(df.high[i])

colors = []
for i in range(len(res_points)):colors.append('b')
for i in range(len(sup_points)):colors.append('y')
pv_lines = dict(hlines = res_points + sup_points, colors = colors, linewidths = (0.5))
mpl.plot(df, type='candle', style = 'charles', hlines = pv_lines)
