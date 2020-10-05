from iexfinance.stocks import Stock, get_historical_intraday
from datetime import datetime
from iexfinance.stocks import get_historical_data
import numpy as np
import yfinance as yf

from disc2txt import disc2txt

data = disc2txt('NTRtest.html')
TF = []
success_times = []
for i in range(len(data)):
    not_reached = False
    print(TF)
    company = data.iloc[i, 0]
    date = data.iloc[i, 5]
    tick = yf.Ticker(company)
    date2 = date.replace(minute = date.minute + 1)
    start_df = tick.history(start =date, end = date2, interval = '1m')
    start_price = start_df['Close'].values[0]

    #while np.isnan(df1.loc[df1.index == date, 'average'].values[0]):
        #if date.minute == 59:
            #date = date.replace(minute=00, hour=date.hour + 1)
       # date = date.replace(minute=date.minute + 1)

    target_price = data.iloc[i, 4]
    end_date = datetime(2019, 12, 13, 16, 0, 0)
    prices = tick.history(start = date, end = end_date,interval = '1d')
    values = prices['High'].values
    big_key = 0
    for j in range(len(values)):
        if values[j] > target_price:
            big_key = j
            break
        if j == len(values)-1:
            TF.append(False)
            success_times.append(np.nan)
            not_reached = True
            break
    if not_reached:
        continue
    print(TF)
    target_date = prices.index[big_key]
    target_date2 = target_date.replace(day = target_date.day + 1)
    target_day = tick.history(start = target_date, end = target_date2, interval = '1m')
    cash = target_day['Close'].values
    for k in range(len(cash)):
        if target_price < cash[k]:
            success_time = target_day.index[k]
            success_times.append(success_time)
            TF.append(True)
            break
data['Hit Target'] = TF
data['Hit Time'] = success_times
print(data)
