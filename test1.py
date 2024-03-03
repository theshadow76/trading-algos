from PatternPy.tradingpatterns.tradingpatterns import *
import yfinance as yf
import pandas as pd

ticker = "AAPL"       # Replace with your desired stock ticker
start_date = "2023-08-01"
end_date = "2024-03-06" 
# Fetch data using Yahoo Finance
data = yf.download(ticker, start=start_date, end=end_date)

df = pd.DataFrame(data)
head_and_shoulder = detect_head_shoulder(df)

head_and_shoulder_data = head_and_shoulder['head_shoulder_pattern']

head_and_shoulder_data_formated = head_and_shoulder_data.dropna()
print(head_and_shoulder_data_formated)