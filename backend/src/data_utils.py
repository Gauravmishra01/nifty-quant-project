import yfinance as yf
import pandas as pd
import os
import numpy as np

def fetch_nifty_spot():
    print("⬇️ Downloading Nifty 50 Data (1 Year Demo)...")
    
    # 1. Fetch Data
    try:
        # Using period='1y' and interval='1d' for the demo
        df = yf.download('^NSEI', period='1y', interval='1d', progress=False)
    except Exception as e:
        print(f"❌ Download Failed: {e}")
        return None
    
    if df.empty:
        print("❌ Error: No data fetched.")
        return None
        
    # 2. Flatten MultiIndex columns if they exist (Fix for yfinance updates)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    # 3. Reset Index FIRST to bring the Date/Datetime into the columns
    df.reset_index(inplace=True)

    # 4. RENAME rigorously (Handle 'Date', 'Datetime', 'date', etc.)
    # This fixes the error you are seeing!
    df.rename(columns={
        'Date': 'timestamp',      # Daily data format
        'Datetime': 'timestamp',  # Intraday data format
        'index': 'timestamp'      # Generic fallback
    }, inplace=True)

    # 5. Clean up column names to be lowercase (Close -> close)
    df.columns = [c.lower() for c in df.columns]
    
    # Verify timestamp exists
    if 'timestamp' not in df.columns:
        print("❌ Critical Error: 'timestamp' column missing after processing.")
        print("Columns found:", df.columns)
        return None

    # 6. Save for debugging
    data_dir = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_dir, exist_ok=True)
    df.to_csv(os.path.join(data_dir, "nifty_spot_5min.csv"), index=False)
    
    print(f"✅ Downloaded {len(df)} rows (1 Year Daily Data).")
    return df

# --- SYNTHETIC OPTIONS GENERATOR ---
def generate_synthetic_options(spot_df):
    print("⚡ Generating Synthetic Options...")
    options_data = []
    
    # Loop through the data to create fake options
    for index, row in spot_df.iterrows():
        spot_price = row['close']
        timestamp = row['timestamp']
        
        # Simple Logic: ATM Strike
        atm_strike = round(spot_price / 50) * 50
        
        # Fake Call/Put Prices
        call_ltp = max(spot_price - atm_strike, 0) + np.random.uniform(50, 100)
        put_ltp = max(atm_strike - spot_price, 0) + np.random.uniform(50, 100)
        
        options_data.append({
            'timestamp': timestamp,
            'strike': atm_strike,
            'type': 'CE',
            'ltp': call_ltp,
            'iv': 15.5,
            'oi': 100000,
            'volume': 5000
        })
        options_data.append({
            'timestamp': timestamp,
            'strike': atm_strike,
            'type': 'PE',
            'ltp': put_ltp,
            'iv': 15.5,
            'oi': 100000,
            'volume': 5000
        })
        
    return pd.DataFrame(options_data)

# --- MASTER LOADER ---
def load_and_merge_data():
    spot = fetch_nifty_spot()
    if spot is None: return None
    
    # Create dummy futures (Just Spot + 0.5% premium)
    futures = spot.copy()
    futures['close'] = futures['close'] * 1.005
    
    # Create dummy options
    options = generate_synthetic_options(spot)
    
    return spot, futures, options