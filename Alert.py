import pandas as pd
from yahoo_fin import options
from yahoo_fin import stock_info as si
import time
from twilio.rest import Client
from Watchlist import watchlist

account_sid = open('account_sid.txt','r').readlines()[0]
auth = open('auth.txt','r').readlines()[0]
comp_number = open('comp_number.txt','r').readlines()[0]
my_number = open('my_number.txt','r')
client = Client(account_sid, auth)
wlist = watchlist()

while True:
    for i in range(len(wlist)):

        company = wlist.iloc[i,0]
        CallPut = wlist.iloc[i,1]
        Exp_date = wlist.iloc[i,2]
        Target = wlist.iloc[i,3]
        Paid = wlist.iloc[i,4]
        strike = wlist.iloc[i,5]
        if CallPut == "Call":
            data = pd.DataFrame(options.get_calls(company, Exp_date))
            current_opt_price = (data[data['Strike'] == strike]['Bid'].values[0] + data[data['Strike'] == strike]['Ask'].values[0])/2
        else:
            data = pd.DataFrame(options.get_puts(company, Exp_date))
            current_opt_price = round((data[data['Strike'] == strike]['Bid'] + data[data['Strike'] == strike]['Ask']) / 2,2)

        stoploss = 0.85

        if current_opt_price < stoploss * Paid:
            client.messages.create(body = "Stop loss has been hit for " + company + ", Sell now to avoid heavier losses.",
                                   from_ = comp_number,
                                   to = my_number)

            wlist = wlist.drop(wlist.index[i])
            break
        current_stock_price = round(si.get_live_price(company), 2)
        print(current_stock_price)
        if CallPut == "Call" and current_stock_price >= Target:
            client.messages.create(body="Target has been hit for " + company + ", Sell now.",
                                   from_=comp_number,
                                   to=my_number)

            wlist = wlist.drop(wlist.index[i])
            break
        if CallPut == "Put" and current_stock_price <= Target:
            client.messages.create(body="Target has been hit for " + company + ", Sell now.",
                                   from_=comp_number,
                                   to=my_number)

            wlist = wlist.drop(wlist.index[i])
            break
    wlist.to_csv('watching.csv')
    time.sleep(10)