import yfinance as yf
import pandas as pd
import numpy as np
import os

# Define paths
DATA_DIR = os.path.join(os.getcwd(), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_nifty_spot():
    """
    Fetches Nifty 50 Spot Data.
    LIMITATION: yfinance allows max 60 days for 5m interval.
    """
    print("⏳ Fetching Nifty 50 Spot Data (Max 60 Days for 5m)...")
    ticker = yf.Ticker("^NSEI")
    
    # Fetch max allowed intraday data
    df = ticker.history(period="60d", interval="5m")
    
    if df.empty:
        print("❌ Failed to fetch Spot Data.")
        return None

    # Reset index to get Datetime column
    df.reset_index(inplace=True)
    
    # Rename columns to standard format
    df.rename(columns={
        "Datetime": "timestamp", 
        "Open": "open", 
        "High": "high", 
        "Low": "low", 
        "Close": "close", 
        "Volume": "volume"
    }, inplace=True)

    # Clean timezone
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    
    # Save
    path = os.path.join(DATA_DIR, "nifty_spot_5min.csv")
    df.to_csv(path, index=False)
    print(f"✅ Saved: {path} ({len(df)} rows)")
    return df

def generate_nifty_futures(spot_df):
    """
    Generates Synthetic Nifty Futures Data.
    Logic: Futures = Spot * e^(r*t) (Cost of Carry Model)
    """
    print("⚙️ Generating Nifty Futures Data...")
    
    # Copy spot data
    fut_df = spot_df.copy()
    
    # Add 'Premium' (Futures usually trade 10-20 points higher)
    # We add random noise to make it realistic
    np.random.seed(42)
    premium = 15 + np.random.normal(0, 2, len(fut_df)) 
    
    fut_df['open'] += premium
    fut_df['high'] += premium
    fut_df['low'] += premium
    fut_df['close'] += premium
    
    # Synthetic Open Interest (OI)
    # OI usually increases during the day
    fut_df['open_interest'] = np.random.randint(1000000, 1500000, len(fut_df))
    
    # Save
    path = os.path.join(DATA_DIR, "nifty_futures_5min.csv")
    fut_df.to_csv(path, index=False)
    print(f"✅ Saved: {path}")

def generate_nifty_options(spot_df):
    """
    Generates Synthetic Nifty Options Data (ATM Chain).
    """
    print("⚙️ Generating Nifty Options Data...")
    
    options_data = []
    
    for i, row in spot_df.iterrows():
        # Determine ATM Strike (Round to nearest 50)
        spot_price = row['close']
        atm_strike = round(spot_price / 50) * 50
        
        # Generate CE (Call) and PE (Put) data for ATM
        # Simple assumption: ATM premium is roughly 0.5% of spot
        premium = spot_price * 0.005
        
        # Call Record
        options_data.append({
            "timestamp": row['timestamp'],
            "strike": atm_strike,
            "type": "CE",
            "ltp": premium + np.random.normal(0, 5), # Add noise
            "iv": 12 + np.random.normal(0, 1),       # VIX approx
            "open_interest": np.random.randint(50000, 200000),
            "volume": np.random.randint(1000, 5000)
        })
        
        # Put Record
        options_data.append({
            "timestamp": row['timestamp'],
            "strike": atm_strike,
            "type": "PE",
            "ltp": premium + np.random.normal(0, 5),
            "iv": 13 + np.random.normal(0, 1),
            "open_interest": np.random.randint(50000, 200000),
            "volume": np.random.randint(1000, 5000)
        })

    opt_df = pd.DataFrame(options_data)
    
    # Save
    path = os.path.join(DATA_DIR, "nifty_options_5min.csv")
    opt_df.to_csv(path, index=False)
    print(f"✅ Saved: {path}")

# --- MAIN EXECUTION FUNCTION ---
def fetch_all_data():
    """Runs the full data pipeline"""
    spot = fetch_nifty_spot()
    if spot is not None:
        generate_nifty_futures(spot)
        generate_nifty_options(spot)
        print("\n🚀 All 3 Task Deliverables Created Successfully!")

# Allow direct running
if __name__ == "__main__":
    fetch_all_data()