from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import numpy as np

def disc2txt(file):
    HtmlFile = open(file, 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    soup = BeautifulSoup(source_code, 'html.parser')
    times = soup.select(".chatlog__timestamp")
    real_time = []
    for time in times:
        fix_time = re.findall("(?<=\>)(.*?)(?=\<)", str(time))[0]
        real_time.append(fix_time)
    signals = []
    for string in soup.strings:
        if "New Buy signal" in string:
            signals.append(string)
    signal_dict = {}
    for signal in signals:
        print(signal)
        split_up = signal.split('\n')
        for i in range(len(split_up)):
            if "New Buy" in split_up[i]:
                Target = np.nan
                master_index = i
                company = split_up[i + 1].strip()
                Option_date = split_up[i + 2]
                Option_date = Option_date.strip()
                Option_price = split_up[i + 3]

                Call_Put = split_up[i + 4].strip()[0]
                for j in range(len(split_up)):
                    if 'target' in split_up[j].lower():
                        Target = split_up[j]
                        Target = re.findall("\d+", Target)
                        Target = float('.'.join(Target))
                        break
                print(Target)
                if np.isnan(Target):
                    print('Going to Back up')
                    Target = float(split_up[i+5])
                print(Target)
                signal_dict[company] = {'Expire_date': Option_date, "Option_price": int(Option_price[1:]),
                                        "Call_Put": Call_Put, 'Target': Target}
    All_signals = pd.DataFrame(signal_dict)
    All_signals = All_signals.T
    All_signals = All_signals.reset_index()
    All_signals.rename(columns={'index': "Company"}, inplace=True)
    All_signals["Start Date"] = pd.to_datetime(real_time, format="%d-%b-%y %I:%M %p")

    for i in range(len(All_signals)):
        All_signals.iloc[i, 5] = All_signals.iloc[i, 5].replace(hour = All_signals.iloc[i, 5].hour + 1)
    print(All_signals)
    return All_signals

disc2txt('Nexus Trading Room - swing-trade-signals🚨 [575108339139215375] (2019-10-01 to 2019-12-26).html')