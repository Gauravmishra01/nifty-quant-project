import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def calculate_technical_indicators(df):
    """
    Adds technical indicators (RSI, EMA, Bollinger Bands) to the dataframe.
    """
    # Ensure data is sorted
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    # 1. RSI (14)
    rsi_indicator = RSIIndicator(close=df['close'], window=14)
    df['rsi'] = rsi_indicator.rsi()

    # 2. EMA (9 and 21)
    ema_fast = EMAIndicator(close=df['close'], window=9)
    ema_slow = EMAIndicator(close=df['close'], window=21)
    df['ema_9'] = ema_fast.ema_indicator()
    df['ema_21'] = ema_slow.ema_indicator()

    # 3. Bollinger Bands (20, 2)
    bb_indicator = BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb_indicator.bollinger_hband()
    df['bb_lower'] = bb_indicator.bollinger_lband()
    
    # 4. Simple Signal (1 = Buy, 0 = Wait)
    # Buy if Fast EMA > Slow EMA and RSI is not overbought (>70)
    df['signal'] = 0
    condition = (df['ema_9'] > df['ema_21']) & (df['rsi'] < 70)
    df.loc[condition, 'signal'] = 1

    # Fill NaN values (caused by the first 20 rows of calculation)
    df = df.fillna(0)
    
    return df