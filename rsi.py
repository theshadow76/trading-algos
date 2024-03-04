import datetime
import random
from urllib.request import urlopen
import numpy as np
import pandas_datareader.data as web


class Stock:

    ticker = None
    dates = None
    closes = None
    highs = None
    lows = None
    opens = None
    volumes = None
    rsi = None

    def __init__(self, ticker, data):
        self.ticker = ticker

        """
        Different sources for pulling data can be found here:
        https://readthedocs.org/projects/pandas-datareader/downloads/pdf/latest/
        """
        self.closes = data['Close']
        self.highs = data['High']
        self.lows = data['Low']
        self.opens = data['Open']

        self.rsi = self.RSI(self.closes)

    def RSI(self, prices, n=14):
        deltas = np.diff(prices)
        seed = deltas[:n+1]
        up = seed[seed >= 0].sum()/n
        down = -seed[seed < 0].sum()/n
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:n] = 100. - 100./(1.+rs)

        for i in range(n, len(prices)):
            delta = deltas[i-1]  # The diff is 1 shorter

            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(n-1) + upval)/n
            down = (down*(n-1) + downval)/n

            rs = up/down
            rsi[i] = 100. - 100./(1.+rs)

        return rsi

    def SMA(self, period, values=None):

        values = self.closes if values is None else values

        """
        Simple Moving Average. Periods are the time frame. For example, a period of 50 would be a 50 day
        moving average. Values are usually the stock closes but can be passed any values
        """

        weigths = np.repeat(1.0, period)/period
        smas = np.convolve(values, weigths, 'valid')
        return smas  # as a numpy array

    def EMA(self, period, values=None):

        values = self.closes if values is None else values

        """
        Exponential Moving Average. Periods are the time frame. For example, a period of 50 would be a 50 day
        moving average. Values are usually the stock closes but can be passed any values
        """

        weights = np.exp(np.linspace(-1., 0., period))
        weights /= weights.sum()
        a = np.convolve(values, weights, mode='full')[:len(values)]
        a[:period] = a[period]
        return a

    def MACD(self, x, slow=26, fast=12):
        """
        Compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
        return value is emaslow, emafast, macd which are len(x) arrays
        """

        emaslow = self.EMA(slow, x)
        emafast = self.EMA(fast, x)
        return emaslow, emafast, emafast - emaslow