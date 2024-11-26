from backtesting import Backtest, Strategy
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
import time

# Binance API connection settings
import encrypt_key
import original_key
simple_en_decrypt = original_key.simple_en_decrypt(encrypt_key.encrypt_key)
binance_access = simple_en_decrypt.decrypt(original_key.access)
binance_secret = simple_en_decrypt.decrypt(original_key.secret)

binance = ccxt.binance({
    'apiKey': binance_access,
    'secret': binance_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

# Constants
DAYS = 1000               # Data collection period
INTERVAL = '4h'           # Data interval
PERIOD1 = 4               # First Supertrend period
MULTIPLIER1 = 2.4         # First Supertrend multiplier
PERIOD2 = 4               # Second Supertrend period
MULTIPLIER2 = 4.8         # Second Supertrend multiplier
SYMBOL = 'BTC/USDT'       # Trading symbol
INITIAL_CASH = 1000000    # Initial capital for backtesting
COMMISSION = 0.002        # Trading commission

def get_binance_data(symbol, days, interval=INTERVAL, chunk_size=DAYS):
    df = pd.DataFrame()
    end_date = datetime.now() - timedelta(minutes=5)
    start_date = end_date - timedelta(days=chunk_size)
    since = int(start_date.timestamp() * 1000)
    
    while True:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe=interval, since=since, limit=1000)
        temp_df = pd.DataFrame(ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        temp_df['datetime'] = pd.to_datetime(temp_df['datetime'], unit='ms')
        df = pd.concat([df, temp_df], ignore_index=True)
        since = int(temp_df['datetime'].iloc[-1].timestamp() * 1000)
        
        time.sleep(0.05)  # Minimize delay
        
        # Exit condition
        if temp_df['datetime'].iloc[-1] >= end_date or len(df) >= (days * 6):
            break

    df.set_index('datetime', inplace=True)
    df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
    
    return df

# SuperTrend calculation function
def calculate_supertrend(df, period, multiplier):
    hl2 = (df['High'] + df['Low']) / 2  # Change column name to uppercase
    atr = df['High'].rolling(window=period).max() - df['Low'].rolling(window=period).min()
    up_trend = hl2 - multiplier * atr
    down_trend = hl2 + multiplier * atr
    trend = np.where(df['Close'] > down_trend.shift(), 1, -1)
    st_line = np.where(trend == 1, up_trend, down_trend)
    return st_line, trend

# SuperTrend strategy
class SuperTrendCloudStrategy(Strategy):
    def init(self):
        # First SuperTrend indicator
        self.st_line1, self.trend1 = calculate_supertrend(self.data.df, PERIOD1, MULTIPLIER1)
        # Second SuperTrend indicator
        self.st_line2, self.trend2 = calculate_supertrend(self.data.df, PERIOD2, MULTIPLIER2)
        self.supertrend1 = self.I(lambda: self.st_line1)
        self.supertrend2 = self.I(lambda: self.st_line2)
        
    def next(self):
        # Long entry condition
        if (self.data.Close[-1] > self.supertrend1[-1] and self.data.Close[-2] < self.supertrend1[-2]) or \
           (self.data.Close[-1] > self.supertrend2[-1] and self.data.Close[-2] < self.supertrend2[-2]):
            self.buy()
        
        # Short entry condition
        elif (self.data.Close[-1] < self.supertrend1[-1] and self.data.Close[-2] > self.supertrend1[-2]) or \
             (self.data.Close[-1] < self.supertrend2[-1] and self.data.Close[-2] > self.supertrend2[-2]):
            self.sell()
        
        # Exit position on cloud condition
        cloud = (self.data.Close[-1] < self.supertrend1[-1] and self.data.Close[-2] > self.supertrend2[-2]) or \
                (self.data.Close[-1] > self.supertrend1[-1] and self.data.Close[-2] < self.supertrend2[-2])
        if cloud:
            self.position.close()

# Run backtesting
btc_data = get_binance_data(SYMBOL, DAYS)
bt = Backtest(btc_data, SuperTrendCloudStrategy, cash=INITIAL_CASH, commission=COMMISSION)
output = bt.run()
print(output)
bt.plot()
