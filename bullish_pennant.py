import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

pole_high = None
pole_start = None

def is_bullish_pennant(prices):
  """
  This function analyzes a price list to identify a Bullish Pennant pattern.

  Args:
      prices: A list of closing prices.

  Returns:
      A tuple containing three booleans:
          - is_pennant: True if a pennant pattern is identified.
          - pennant_start: Index of the starting bar of the pennant.
          - pennant_end: Index of the ending bar of the pennant (before breakout).
  """
  print(f"THe data is: {prices.head()}")
  prices['Close'] = pd.to_numeric(prices['Close']) # Assuming your price column is 'Close'
  # Identify the pole
  pole_high = max(prices.fillna(method='ffill')[:int(len(prices) * 0.3)])  
  pole_start = prices[prices == pole_high].index[0]
  pole_start_ordinal = pd.to_numeric(pole_start).astype(int) 

  print(pole_start)                  # Print the timestamp value
  print(type(pole_start))            # Print its data type


  # Define minimum number of bars for the pennant and breakout
  min_bars_in_pennant = 10
  min_bars_after_pennant = 5

  # Initialize variables for trendline calculations
  highest_high = pole_high
  lowest_low = min(prices[pole_start:])
  pennant_formed = False
  pennant_start = None
  pennant_end = None

  for i in range(pole_start_ordinal + 1, len(prices)):  # Assuming pole_start_ordinal exists
    current_datetime = prices.index[i]  # New line
    current_high = prices.loc[i]  # Accessing a single price
    current_low = min(prices[pole_start : pole_start + pd.Timedelta(i - pole_start, unit='D')])

    # Update highest_high and lowest_low for pennant trendlines
    highest_high = max(highest_high, current_high)
    lowest_low = min(lowest_low, current_low)

    # Check if pennant is forming (converging highs and lows)
    if (current_high < highest_high * 0.9) and (current_low > lowest_low * 1.1):
      if not pennant_formed:
        pennant_start = i
      pennant_formed = True
    else:
      # Potential breakout if pennant formed and enough bars passed
      if pennant_formed and (i - pennant_start >= min_bars_in_pennant) and (len(prices) - i >= min_bars_after_pennant):
        pennant_end = i - 1  # Last bar before breakout
        return True, pennant_start, pennant_end
      else:
        # Reset pennant formation if trend diverges
        pennant_formed = False
        highest_high = current_high
        lowest_low = current_low

  return False, None, None

# Parameters
ticker = "AAPL"       # Replace with your desired stock ticker
start_date = "2023-08-01"
end_date = "2024-03-06" 
# Fetch data using Yahoo Finance
data = yf.download(ticker, start=start_date, end=end_date)
prices = data["Close"]

pole_start_ordinal = pd.to_numeric(pole_start).astype(int)

# Detect Bullish Pennant
is_pennant, pennant_start, pennant_end = is_bullish_pennant(prices)

if is_pennant:
    print("Bullish Pennant Detected!")
    print("  Pole Start: ", prices.index[pole_start].strftime('%Y-%m-%d'))
    print("  Pennant Start: ", prices.index[pennant_start].strftime('%Y-%m-%d'))
    print("  Pennant End: ", prices.index[pennant_end].strftime('%Y-%m-%d'))

    pole_start_ordinal = pd.to_numeric(pole_start).astype(int)

    pennant_start_ordinal = pd.to_numeric(pennant_start).astype(int)
    pennant_end_ordinal = pd.to_numeric(pennant_end).astype(int)

    # Plotting 
    plt.figure(figsize=(10, 5))
    plt.plot(prices)

    # Mark the pole
    plt.plot(pole_start, prices[pole_start], marker='o', color='green')

    # Draw pennant trendlines (approximate, you may want refinements)
    x_values = list(range(pennant_start_ordinal, pennant_end_ordinal + 1))

    upper_trendline = np.polyfit(x_values, prices[pennant_start:pennant_end+1], 1)[0] * x_values + np.polyfit(x_values, prices[pennant_start:pennant_end+1], 1)[1]
    lower_trendline = np.polyfit(x_values, prices[pennant_start:pennant_end+1], deg=1)[0] * x_values + np.polyfit(x_values, prices[pennant_start:pennant_end+1], deg=1)[1]
    plt.plot(x_values, upper_trendline, color='red') 
    plt.plot(x_values, lower_trendline, color='blue') 

    # Mark breakout (assuming breakout is at pennant end)
    plt.plot(pennant_end, prices[pennant_end], marker='*', color='red')

    plt.title(f'Bullish Pennant Pattern in {ticker}')
    plt.show()
else:
    print("No Bullish Pennant Pattern Found.")