import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

# Fetch Historical Stock Data
# For this example, we'll use Yahoo Finance to fetch historical data for a particular stock (e.g., Apple, symbol 'AAPL').
stock_symbol = 'AAPL'
start_date = '2020-01-01'
end_date = '2021-01-01'
df = pdr.get_data_yahoo(stock_symbol, start=start_date, end=end_date)

# Calculate Moving Averages
# We'll use a short-term (e.g., 40 days) and a long-term (e.g., 100 days) moving average.
short_window = 40
long_window = 100
df['Short_MA'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
df['Long_MA'] = df['Close'].rolling(window=long_window, min_periods=1).mean()

# Generate Trading Signals
# We'll create a signal when the short MA crosses the long MA.
df['Signal'] = 0
df['Signal'][short_window:] = np.where(df['Short_MA'][short_window:] > df['Long_MA'][short_window:], 1, 0)
df['Position'] = df['Signal'].diff()

# Plotting the Strategy
# Visualize the stock price, MAs, and buy/sell signals.
plt.figure(figsize=(12,6))
plt.plot(df['Close'], label=stock_symbol, alpha=0.5)
plt.plot(df['Short_MA'], label='Short MA', alpha=0.5)
plt.plot(df['Long_MA'], label='Long MA', alpha=0.5)
plt.scatter(df.loc[df['Position'] == 1].index, df.loc[df['Position'] == 1]['Short_MA'], label='Buy Signal', marker='^', color='green')
plt.scatter(df.loc[df['Position'] == -1].index, df.loc[df['Position'] == -1]['Short_MA'], label='Sell Signal', marker='v', color='red')
plt.title('Stock Price with Trading Signals')
plt.legend()
plt.show()
