import yfinance as yf
from yahoo_fin import stock_info as si
tick = yf.Ticker("TSLA")
from yahoo_fin import options
import pandas as pd


account = open('account_sid.txt','r').readlines()[0]
print(account)
company = 'HP'
Exp_date = "01/17/20"
strike = 42.5
data = options.get_calls(company, Exp_date)
current_opt_price = (data[data['Strike'] == strike]['Bid'].values[0] + data[data['Strike'] == strike]['Ask'].values[0])/2
print(current_opt_price)

