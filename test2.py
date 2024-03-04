import pandas as pd
import json
from ExpertOptionAPI2.expert import EoApi as ExpertAPI
from PatternPy.tradingpatterns.tradingpatterns import *
import time

expert = ExpertAPI(token="76782ad35d33d99cb0ed7bc948919dd8", server_region="wss://fr24g1eu.expertoption.com/ws/v34?app_os=win&app_source=web&app_type=web&app_version=15.4.3&app_build_number=7043&app_brand=expertoption&app_device_info=")

expert.connect()

max_attempts = 50000
attempts = 0

while True:
    data_str = expert.GetCandlesHistory()
    data_str_formated = str(data_str).replace("'", '"')
    print(f"The data is: {data_str_formated}")
    data = json.loads(data_str_formated)


    ohlc_data = []
    for candle in data['message']['candles'][0]['periods'][0][1]:
        ohlc_data.append(candle)  # Extract OHLC from each period

    df = pd.DataFrame(ohlc_data, columns=['Open', 'High', 'Low', 'Close'])

    head_and_shoulder = detect_head_shoulder(df)

    head_and_shoulder_data = head_and_shoulder['head_shoulder_pattern']

    head_and_shoulder_data_latest = head_and_shoulder_data.tail(3)
    for result in head_and_shoulder_data_latest:
        if result == "Inverse Head and Shoulder":
            expert.Buy(amount=1000, type="put", assetid="245")
            print("Putting...")
        elif result == "Head and Shoulder":
            expert.Buy(amount=1000, type="call", assetid="245", exptime=60)
            print("Calling...")
        else:
            print("Nothing")
        attempts = attempts + 1
        if attempts == max_attempts:
            break
        print(f"The message was: {result}")
    time.sleep(30)