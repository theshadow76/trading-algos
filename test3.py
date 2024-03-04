import pandas as pd
import json
from ExpertOptionAPI2.expert import EoApi as ExpertAPI
from PatternPy.tradingpatterns.tradingpatterns import *
import time
from rsi import Stock

expert = ExpertAPI(token="76782ad35d33d99cb0ed7bc948919dd8", server_region="wss://fr24g1eu.expertoption.com/ws/v34?app_os=win&app_source=web&app_type=web&app_version=15.4.3&app_build_number=7043&app_brand=expertoption&app_device_info=")

expert.connect()

max_attempts = 50000
attempts = 0

data_str = expert.GetCandlesHistory()
data_str_formated = str(data_str).replace("'", '"')
print(f"The data is: {data_str_formated}")
data = json.loads(data_str_formated)


ohlc_data = []
for candle in data['message']['candles'][0]['periods'][0][1]:
    ohlc_data.append(candle)  # Extract OHLC from each period

df = pd.DataFrame(ohlc_data, columns=['Open', 'High', 'Low', 'Close'])
stock = Stock(ticker="EURUSD", data=df)

rsi = stock.RSI(prices=df)

print(rsi)
