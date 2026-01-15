import pandas as pd
import numpy as np

def calculate_technical_indicators(df):
    """
    Adds technical indicators to the dataframe.
    """
    print("Calculating Technical Indicators...")
    
    # Ensure data is sorted by time
    df = df.sort_values('Datetime').reset_index(drop=True)
    
    # 1. Returns (Percentage change from previous candle)
    df['returns'] = df['Close'].pct_change()
    
    # 2. EMA (Exponential Moving Average) - Trend
    # Short term trend (9 candles) vs Long term trend (21 candles)
    df['ema_9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['ema_21'] = df['Close'].ewm(span=21, adjust=False).mean()
    
    # 3. Volatility (Standard Deviation of returns)
    df['volatility'] = df['returns'].rolling(window=20).std()
    
    # 4. RSI (Relative Strength Index) - Momentum
    # Complex math simplified: Are we winning more than losing?
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # Drop rows with NaN (the first few rows won't have calculated values)
    df.dropna(inplace=True)
    
    print(f"✅ Indicators Added. Columns: {list(df.columns)}")
    return df

if __name__ == "__main__":
    # Test the function
    try:
        data = pd.read_csv("data/nifty_final_clean.csv")
        data_with_features = calculate_technical_indicators(data)
        data_with_features.to_csv("data/nifty_features.csv", index=False)
        print("Test Run Successful: Saved to data/nifty_features.csv")
    except FileNotFoundError:
        print("❌ Error: Run src/data_utils.py first!")